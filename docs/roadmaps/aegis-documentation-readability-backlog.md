# Documentation readability and component guide backlog

## Start here — current reading

As of `410b90aa` on 2026-09-30 Coordinated Universal Time (UTC), this remains
the active repository-wide documentation acceptance backlog. The latest count
is in the paragraph for main after #561 (`410b90aa`): 653 tracked Markdown
files, 584 accepted reader pages, one generated report, 55 classified
synthetic fixtures and thirteen known pending pages; the paragraphs between are
dated history, oldest first, and no dated snapshot is rewritten. The
**skill-eval round recorded below** supersedes those totals without rewriting
the history: it adds three new pending pages, giving **656** tracked Markdown
files and **16** pending, with the accepted, generated and
synthetic-fixture counts unchanged. (A later merge, PR #577, adds one further
tracked page — `docs/evidence/session-continuation-2026-09-30.md` — so the tip
count is now **657**; that page joins the pending set, and this sentence is left
as the dated snapshot it is.)

### Owner decision on the count's authority — appended 2026-10-07

**Scope: this note records where the owner's 2026-10-07 decision is recorded
and what it changes now: nothing in this ledger's records or readings.** It
adds no page and no table row, confers nothing, changes no counting rule in
force today, and rewrites no dated text.

**The decision.** The acceptance index will become the official readability
pending count once its tool is repaired and passes an independent review. A
later pull request makes that switch; until it merges, this ledger's records
and the readings below remain current. Recorded as
[AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#aegis-apr-113-readability-pending-count-authority-option-1)
to AEGIS-APR-115 and decision D73 of the
[recorded decisions](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions).

**What it answers:** the "Held for the owner" question in the current-count
reconciliation that directly follows this note;
"Both deserve an owner ruling before the convention is relied on again" in the
[first ledger-keeper recording](#first-ledger-keeper-recording--owner-ratified-role-2026-10-02),
since future records go into one fixed-format table in this ledger, whose
columns D73 sets as an audit condition (page, full commit and blob ID, a blob
ID being the Git object ID of the file's exact content), added by the repair
pull request and not by this note; and the precedence and counting rules the
[keeper consistency note](#consistency-note--the-ledger-keeper-entry-2026-10-02-local--recorded-2026-10-03-utc)
calls "still separately unresolved".

**What changes only at the switch:** the index reads only the keeper's table; a
page with no recorded acceptance counts as pending, replacing this ledger's
current default for unlisted pages in the official count; a page whose recorded
acceptance commit no longer exists anywhere counts as pending until it is
re-reviewed; and this ledger stops stating its own count and cites the index.

**What does not change:** the keeper's role under AEGIS-APR-101, and the
[targeted-edit rule](#remaining-page-review-in-larger-batches), cited here and
not restated. The "Owed, not done here" harvester repair becomes D73's
structured-table repair, so the four prose blind spots are not repaired in the
parser.

**Self-cost.** This note adds 45 lines and deletes 0 (git diff --numstat
against the base commit) on an already-pending ledger. It confers nothing, and
the ledger stays pending its independent full-page re-read. Like the 2026-10-03
and 2026-10-07 notes, it moves the index's recorded rule line ranges and the
`tracker_line` labels in `stated-acceptances.json` further down; neither is
validated, and only the owed rebuild repairs them.

### Current-count reconciliation — appended 2026-10-07, measured at 03c93c77

**Scope: this note re-measures the readability position at commit
`03c93c77a05e89d082f93c91b23dffabb332373c` and points to the current reading.**
It adds no page, confers or records no acceptance, changes no counting rule,
approves nothing about the acceptance index's precedence, and rewrites no dated
text. Terms used here: a **pull request (PR)** is a proposed change reviewed
before it merges; a **commit SHA** is the 40-character Git object ID of one
commit, and a short form is its leading characters; the **acceptance index** is
`tools/readability_acceptance/acceptance-index.json`, a per-page record of the
revision at which each page last received a full-page acceptance, harvested by
`tools/readability_acceptance/build_index.py` from this ledger and the
documentation evidence records; `check_index.py`, in the same folder, is the
read-only script that applies this ledger's more-than-10-lines-or-new-section
rule to that index; a **bound** is a provable minimum or maximum, not an exact
count; the **ledger keeper** is the recording-only role the owner ratified; and
[AEGIS-APR-101](../approvals/APPROVAL_REGISTER.md#aegis-apr-101-ledger-keeper-role-and-two-historical-recording-acts)
is the owner approval register entry that ratified that role and expressly did
not approve the index's precedence or any changed counting rule.

**Dated, not current:** the opening paragraph's counts above (653 tracked, 584
accepted, thirteen then 16 pending, 656, tip 657); older readings below it such
as 17 and 18 known pending; the floor of 35 in
[Correction to the pending floor — 2026-10-02](#correction-to-the-pending-floor--2026-10-02),
measured at `d6e48418`; and the 674 tracked files, 608 reader pages, 218 and
"at most 390" of the
[premises correction](#premises-correction--appended-2026-10-03-measured-at-c3527560),
measured at `c3527560`.

**Inventory at `03c93c77`.** Method as in the 2026-10-03 note (paths from
`git ls-tree -r --name-only 03c93c77` ending `.md`, one per path): 675 tracked
Markdown files; 65 classified fixtures (the 66 under `scripts/` less
`scripts/tests/fixtures/README.md`); one generated report; so
`675 − 1 − 65 = 609` reader pages. One page was added since `c3527560`,
`.coord/proc08-sweep-2026-10-03.md` (PR #656); none was deleted or renamed.

**What the acceptance tool reports, on its own basis.** Command, with `--ref`
pinned to the full commit SHA:

```text
python3 -I -B tools/readability_acceptance/check_index.py --json --ref 03c93c77a05e89d082f93c91b23dffabb332373c
```

Its summary: `reader_pages_in_index` 602, `recorded_pages_compared` 436,
`provably_pending` 212, `no_recorded_acceptance` 159,
`recorded_acceptance_within_10_lines` 224, `cannot_decide` 7, and
`exact_pending_count` "NOT DERIVABLE from this procedure". The 212-page pending
set is identical at `d6e48418`, `c3527560` and `03c93c77`: the index's
acceptance rows are frozen at `d6e48418`, and no indexed page crossed the rule's
threshold in its terms since. The 7 undecidable rows name two acceptance
revisions, `65bacc7d6b85` and `d3dcb62a335d`, that no remote-tracking ref
contains. **212 is the tool's count on its own basis — not a floor or ceiling on
this ledger's records.**

**The 2026-10-03 note's `unsure`, answered: yes, the tool over-counts relative
to this ledger's records.** For each page below this ledger records a later
full-page acceptance at revision R; `git diff --numstat <R> 03c93c77 -- <path>`
prints nothing, so no line and no heading changed since; yet the tool lists the
page as pending.

| Page | Recorded acceptance revision (R) | Review recorded for |
| --- | --- | --- |
| `.claude/skills/iac-reviewer/SKILL.md` | `f5a6dabb7c8b` | PR #521 |
| `.claude/skills/llm-output-safety-reviewer/SKILL.md` | `af328b512417` | PR #424 |
| `.claude/skills/multi-tenant-data-architect/SKILL.md` | `a56c60d8ad54` | PR #410 |
| `.claude/skills/source-of-truth-reconciler/SKILL.md` | `620b24595255` | PR #456 |
| `tools/behavioral_eval_runner/README.md` | `acdcdad4563b` | PR #475 |
| `docs/evidence/setup/issue-101-package-4a-host-feasibility.md` | `e6fc8d24ad78` | PR #625 review, recorded by the ledger keeper in PR #635; `e6fc8d24` is not an ancestor of the default branch and is reachable only through `origin/docs/readability-batch-b` |

The over-count is **at least 6** pages; its full size is **not derivable**
without repairing the harvester and rebuilding the index. So the 2026-10-03
note's 218 and "at most 390" are tool-basis figures, **not** a floor or ceiling
on this ledger's records.

**What this ledger's records support at `03c93c77`: at least 40 pending.** This
is the 2026-10-02 named set carried forward, 35 − 2 + 7 = 40. The 35 names were
read from the three page lists in `verify_ground_truth.py` (19, 5 and 11, union
35), the tool's encoding of the 2026-10-02 derivation. The two setup evidence
pages leave the set because the keeper's first recording gives each a later
recorded full-page acceptance at `e6fc8d24`, with no line changed since. The seven are reader pages
added after `d6e48418`; they start pending under the new-page rule and none has
a recorded full-page acceptance. **This is not a re-run of the 2026-10-02
audit.** `git diff --numstat d6e48418 03c93c77 -- '*.md'` lists 44 Markdown paths
changed or added — 34 reader pages and 10 classified fixtures; apart from the
two setup pages and the seven new pages, those reader pages were not re-measured
against their last recorded acceptance. For example, `docs/README.md` shows 83
added and 60 deleted lines (143 changed) since `d6e48418`, and the keeper
section below already records 141 for it with no acceptance conferred, so a
re-run could only raise the floor. One carried page,
`.claude/skills/cloud-security-baseline-reviewer/SKILL.md`, rests on the
2026-10-02 determination because its drift cannot be re-measured in a fresh
clone.

Under this ledger's accepted-unless-listed default, 609 reader pages less at
least 40 pending leaves **at most 569** counted accepted, so the 584 in the
opening paragraph cannot be current. The floor of 40 and the tool's 212 are
**different bases and are not nested**: 10 of the 33 carried pages are outside
the tool's 212 (9 have no recorded index revision, 1 is undecidable). Do not
add, subtract or merge the two figures. **The exact pending count is not
derivable; this note asserts no exact count.**

**Held for the owner:** whether this ledger's floor should follow the index's
decision procedure once the harvester is repaired. AEGIS-APR-101's Scope
FORBIDDEN reads: *"No approval of the charter's proposed canonical index, its
precedence, or changed counting rules."*

**Owed, not done here** (each writes under `tools/` and needs its own plan and
review): the `build_index.py` re-run the 2026-10-03 note already names; and a
harvester repair for four blind spots — a statement wrapped across lines, a page
and its verdict in different table cells, short page names without the .md
suffix and `../`-relative links, and keeper rows that carry no verdict word —
with the six pages above as its regression cases.

**Self-cost.** This note adds 120 lines and deletes 0 (`git diff --numstat
03c93c77`) on an already-pending ledger; it confers no acceptance, and the
ledger stays pending its independent full-page re-read. Like the 2026-10-03
note, it moves the index's recorded rule line ranges and the `tracker_line`
labels in `stated-acceptances.json` further down; neither is validated, and only
the owed rebuild repairs them.

### Premises correction — appended 2026-10-03, measured at c3527560

**Scope: this note repairs three premises of this ledger and nothing else.** It
adds no page, confers no acceptance, changes no label, re-prioritises nothing,
and rewrites no dated snapshot above or below it. Under this ledger's own rule —
dated text is corrected forward by a dated note, never rewritten — the sentences
corrected here keep their original words and are quoted verbatim.

**(1) The ancestry sentence is wrong: the canonical acceptance index exists.**
[First ledger-keeper recording](#first-ledger-keeper-recording--owner-ratified-role-2026-10-02)
records that *"the process's canonical per-path acceptance index (section (c) of
the conversion note) does not exist on main, so these rows are recorded in this
ledger as dated prose instead of as index rows."* **The index does exist on
main.** It is
[`tools/readability_acceptance/acceptance-index.json`](../../tools/readability_acceptance/acceptance-index.json),
a tracked file (350,376 bytes) with schema `aegis.documentation-acceptance-index/1`,
built by `tools/readability_acceptance/build_index.py` and checked by
`check_index.py` and `verify_ground_truth.py`. Its own `rule_text_file` field
names **this ledger**, and its `rules` map gives line ranges in it
(`reader_page_default` 103–104, `acceptance_criteria` 2376–2397,
`full_page_acceptance_event` 2478–2482) — so the index derives its rule text
from this page. Those ranges are the index's recorded references at its
`source_revision` `d6e48418`. **At this head every one of them is wrong**, and
this note is the cause: it inserts lines at line 19, above every recorded range —
the lowest recorded start is line 22 — so each range moves down. **Measured by
comparing the lines at each recorded range between `c3527560` and this head: 0 of
the 11 ranges still resolves to the text its key names.** `targeted_edit_scope`,
recorded as 22–26, no longer begins at line 22 at all. Making them correct again
means rebuilding the index, which is part of the owed `build_index.py` re-run
recorded below; **this note does not edit committed consumers**, so those anchors
stay wrong until that re-run. The direction of derivation the
ledger recorded is therefore the
reverse of the truth: **the ledger is the index's rule source.**

**What that does not establish, and what this note does not decide.** Those
anchors show that the index **exists** and that the dependence runs ledger →
index. They do **not** show that the index is where acceptance rows should be
*recorded*, or which artifact takes precedence — and that question is **open**,
as two tracked sources state. `docs/approvals/APPROVAL_REGISTER.md:3150`, the
**`AEGIS-APR-101`** entry's **Scope FORBIDDEN**, reads: *"No approval of the
charter's proposed canonical index, its precedence, or changed counting rules."*
This ledger itself says the same, at line 3230 of this head, under
[First ledger-keeper recording](#first-ledger-keeper-recording--owner-ratified-role-2026-10-02):
*"**Still separately unresolved, and still undecided.** The charter's proposed
canonical index — its ownership, path, precedence and changed counting rules — is
**not** approved by this entry."* So the acceptance rows stay recorded here as
dated prose, and whether they should ever move to index rows is a question for
the owner — **not** something this note settles. Measured:
`git ls-files --error-unmatch tools/readability_acceptance/acceptance-index.json`
→ the path, exit 0.

**(2) The stale denominator, replaced with measured figures.** Counts below are
records emitted by `git ls-tree -r --name-only <ref>`, filtered to paths ending
`.md`, counted one per emitted path, newline-based; no file blob was split on
newlines and `Measure-Object -Line` is not used. Measured **2026-10-03** at
`c3527560fb7ef06043f56a0cb9bbbabf604e84f0` (tree
`58fda42bd77bb75418c06ac55ce29681462f0b0a`), which is `origin/main`:

| Figure | Recorded in this ledger | Measured 2026-10-03 at `c3527560` |
| --- | ---: | ---: |
| tracked Markdown files | 658 at `d6e48418`; 659 at PR #635 | **674** |
| Markdown paths under `scripts/` | 56 | **66** |
| classified synthetic fixtures (that count less the fixture index) | 55 | **65** |
| generated reports | 1 | **1** |
| reader pages (total less generated and fixtures) | 602 | **608** |

The arithmetic closes: `674 − 1 − 65 = 608`, and `1 + 65 + 608 = 674`. The
fixture rule is this ledger's own, unchanged: every Markdown path under
`scripts/` except the reader-facing `scripts/tests/fixtures/README.md`; measured,
all 66 are under `scripts/tests/fixtures/**` or
`scripts/acceptance/scenario-a-fixture/**`. The one generated report remains
[the skill-contract audit baseline](../audits/skill-contract-audit-baseline.md).

**What moved since the ledger's own newest reading.** Command:
`git diff --name-status --diff-filter=A d6e48418 c3527560 -- "*.md"` → **16
added, 0 deleted** (`--diff-filter=D` prints nothing). Ten are
`scripts/tests/fixtures/markdown-links/**` Markdown-link fixtures, so they are
classified fixtures; the other six are reader pages:

- [the delivery workflow](../delivery-workflow.md)
- [the acceptance conversion process](../evidence/documentation/acceptance-conversion-process-2026-10-02.md)
- [process issues and prevention](../evidence/documentation/process-issues-and-prevention-2026-10-02.md)
- [stale checkout instruction divergence](../evidence/documentation/stale-checkout-instruction-divergence-2026-10-02.md)
- [coordinator figures](aegis-coordinator-figures.md)
- [the readability acceptance index README](../../tools/readability_acceptance/README.md)

Cross-checks: `658 + 16 = 674`; `55 + 10 = 65`; `602 + 6 = 608`.

**(3) What this does to the remaining-work totals — the floor rises from 35 to
at least 218.** Repairing (1) is what makes this measurable: while this ledger
believed the index absent, it recorded the exact count as *"not derivable from a
command"*. The index's own read-only decision procedure can now be run against a
named revision. Command, run 2026-10-03 against the revision below, with `--ref`
**pinned explicitly** rather than left to its default: `origin/main` moves, and a
bound is only meaningful against a named revision. (`origin/main` **was** this
revision when the command was run.)

```text
python -P -B tools/readability_acceptance/check_index.py --json `
    --ref c3527560fb7ef06043f56a0cb9bbbabf604e84f0
```

Its `summary` at that ref reports `compared_ref`
`c3527560fb7ef06043f56a0cb9bbbabf604e84f0`, `reader_pages_in_index` **602**,
`recorded_pages_compared` **436**, `provably_pending` **212**,
`no_recorded_acceptance` 159, `recorded_acceptance_within_10_lines` 224,
`cannot_decide` 7, and `exact_pending_count` **"NOT DERIVABLE from this
procedure"**. Its own bound string reads *"at least 212 pages are provably
pending by the tracker's own >10-lines-or-new-section rule"*.

**The recorded floor of 35 was the narrower figure** — the pages the tracker's
2026-10-01 audit could name. The tool's 212 is larger, and the containment of the
ten-page table is spot-verified: nine of the ten pages in the ten-page table under
**Correction: one base SHA in the table above is not an ancestor of `origin/main`
— 2026-10-02** (below) appear in the tool's provably-pending list, and the tenth,
`.claude/skills/cloud-security-baseline-reviewer/SKILL.md`, is the page this
ledger already records as undecidable because its acceptance revision
`65bacc7d6b85` is contained by no remote-tracking ref — the same page the tool
reports under `cannot_decide`.

**But that bound is the TOOL'S, on the tool's frozen basis — not this ledger's
floor, and this note does not adopt it as one.** `check_index.py` reads
acceptance rows **frozen at the index's `source_revision` `d6e48418`**; a page
whose acceptance was recorded *after* that revision is still counted pending by
it, so **212 is not guaranteed to be a floor.** Whether the tool over-counts for
that reason, and by how much, is **`unsure` here** — the same question the
independent reviewer marked `unsure` rather than implying it had been checked.
Every figure in this paragraph is quoted from the tool and attributed to it.

**Two adjustments on the tool's figure, carrying the same attribution and the
same reservation.** Six reader pages have been added since `d6e48418`; they are
absent from the index and start pending under this ledger's new-page rule, so
**the tool's bound rises to at least `212 + 6 = 218`** on the same frozen basis.
And the ceiling this ledger records — *"at most 567 are counted accepted or
unknown with no per-page recorded full-page re-read that a command can bind"* —
was `602 − 35` on the old inputs; on these inputs it is `608 − 218 = ` **at most
390**, again attributed to the tool.

The exact pending count is still **not derivable**, and the index says so in the
same words this ledger uses. What changed is the provenance of the bound: one of
35 carried in prose is superseded by one of 218 **produced by a named tool against
a named revision** — attributed there, with the tool's frozen basis and this
note's `unsure` recorded beside it rather than absorbed. For completeness, the
index's companion verifier
`verify_ground_truth.py` exits **1** at this ref on one pre-existing mismatch —
`.claude/skills/cloud-security-baseline-reviewer/SKILL.md`, the same
unreachable-acceptance page — which this ledger already records above and which
this note neither creates nor fixes.

**Owed follow-up, and why it is not done here.** The index exists but is built
at `source_revision d6e48418`, and carries the same stale basis this note
replaces: its `counts` read `tracked_markdown 658, generated_reports 1,
fixtures 55, reader_pages 602` — matching this ledger's figures at that revision
exactly, and stale by the same 16 files. `check_index.py` can still be pointed
at the current ref, which is what produces the bound in (3), but its per-page
coverage stops at the index's `source_revision`: the six reader pages added since
are simply absent from it. Re-running
`tools/readability_acceptance/build_index.py` at the current revision would
refresh that coverage, re-base the counts, and let prose recording give way to
index rows for the rows this ledger still stores as dated prose. It writes under
`tools/`, outside this note's one-file scope, and needs its own review: **named
as owed, not done here.**

**This note is not an acceptance.** It is an edit to a page that is already
pending, so it confers no acceptance and, being longer than 10 changed lines,
leaves this ledger owing its own independent full-page re-read against
[Acceptance for each page](#acceptance-for-each-page) by a reader who did not
write it.

**This round's determination: no acceptance was conferred, and two erroneous
ones were corrected.** The round was
instructed to "record the accepted transitions" for the pages below. Under the
[targeted-edit rule](#remaining-page-review-in-larger-batches), the 10-line
exemption keeps acceptance only for a page that is **already accepted**; it
gives a currently **pending** page nothing, because that page already owes a
full re-read against every criterion in [Acceptance for each
page](#acceptance-for-each-page). Each page below is therefore recorded as
still pending (or moved back to pending), not accepted. Changed-line counts
are added plus deleted lines from `git diff --numstat`.

- [approval register](../approvals/APPROVAL_REGISTER.md): 525 net since its
  last full-page acceptance at `a890669` (PR #533). Its review on #533
  **accepted** it on `a890669` ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/533#issuecomment-5882995051)),
  but PR #525 then made it pending again, and the #550 round recorded it as
  pending with 519 net. PR #554 changed it by 4+2=6 lines; its independent
  review certified append-only immutability and the corrected reading aid (98
  entries byte-identical, normalized SHA-256
  `c80d02f5987747728a1eb28573e822250e80973d6c577039ad8bf67d2c52591a`), not the
  whole page. **That range hash is since superseded** — PR #569 and PR #571
  appended inside the certified range, so it no longer reproduces; the register
  carries the re-verification convention under `AEGIS-APR-086`.
  **Moves to pending.** The #554 paragraph below recorded this page
  as accepted on the strength of a **targeted** review. That was wrong: under
  [Targeted edits to accepted
  pages](#remaining-page-review-in-larger-batches), a targeted review cannot
  confer full-page acceptance on a page that is already pending, and this page
  was pending. `git diff --numstat a890669 410b90aa -- docs/approvals/APPROVAL_REGISTER.md`
  is still `523 2`.
- [backlog forecast](aegis-backlog-forecast.md): 88 net since its last
  acceptance at `826f40b` (PR #497, 2026-09-28), which was a full-page
  corrected-candidate acceptance. PR #555 changed it by 86+2=88 lines and added
  a catch-up section. #555's retrospective review, posted 2026-09-30 after the
  merge, records an independent **ACCEPT** bound to `c199e57`, the merged head,
  and independently reproduced the bounded-window count of 62. That review
  satisfies the rule for a small edit — but 88 lines is
  not small. The exemption's **second sentence** applies instead: "A larger
  change, meaning more than 10 changed lines on that page or any new section,
  returns the page to **pending** until an independent reader re-reads the whole
  page." The page has had no full-page re-read since `826f40b`, so it **moves to
  pending**.
- [BER backlog](behavioral-eval-runner-backlog.md): 151 net since `032e030`.
  PR #557 changed it by 1+1=2 lines. #557's retrospective review records an
  independent **SHIP** bound to `665b2829`, the merged head. The edit is within
  10 lines, but the exemption is a *retention* rule for accepted pages and this
  page is pending, so it has no acceptance to retain. **Stays pending.**
- [step-0 reconciliation log](../reconciliation/step-0-reconciliation-v4.md):
  343 net since `97c8682`. PR #558 changed it by 7+2=9 lines. #558's
  retrospective review records an independent **ACCEPT** bound to its merged
  head. As with the BER backlog, the edit is within 10 lines and the review is
  real, but the page is pending, so the exemption gives it nothing. **Stays
  pending.**
- [AEGIS-060+ register](../audits/aegis-060-plus-register.md): 25 net since
  `04af9d9`. PR #559 changed it by 2+1=3 lines and added one severity gloss.
  #559's retrospective review records an independent **SHIP** bound to its
  merged head. **Stays pending**, for the same reason: the exemption retains, it
  does not confer.
- [skills catalog](../skills-catalog.md): 108 net since `2e15b23`. PR #560
  changed it by 6+4=10 lines, sitting exactly on the boundary. #560's
  retrospective review records an independent **SHIP** bound to `1b9e7049`, the
  merged head, and verified the roster exhaustively in both directions
  (195/196/0/0, 7/7 subagents); it also named an honest limitation, that it did
  not read all 1,492 lines at `1b9e7049` for prose-level readability (1,495
  lines after #572). The page was pending and
  owed a full read, so the exemption cannot confer acceptance. **Stays
  pending.**
- `.claude/skills/scoped-approval-register/SKILL.md`: 10 net since its last
  change at `61f2a464`. PR #561 is the only one of these merges whose reviews
  were posted at review time rather than retrospectively: an independent quality
  **SHIP** at the current head `41c7a649` and a security **SHIP** on the earlier
  head, each covering the eval cases and the added guidance rather than the
  whole page. This ledger records no status for the page and the page is not in
  its pending set, so this round changes no classification for it. The named
  follow-up is to record its status and give it the full-page re-read the rule
  requires.

  **Correction (appended 2026-09-30, verified against `origin/main` at `5c806348`).** Two
  items this paragraph leaves open are settled here. **The figure:** "10 net since
  `61f2a464`" was the state at `41c7a649`; PR #585 has since changed the page by 4+1=5 more
  lines, so `git diff --numstat 61f2a464 origin/main --
  .claude/skills/scoped-approval-register/SKILL.md` now reads `14 1`. The owed follow-up is
  now recorded: the page's status is **no recorded full-page acceptance**. Both reviews named
  above were targeted — the eval cases and the added guidance — so neither read the
  whole page, and under the rule above a targeted review confers nothing. Whether the page
  belongs in the pending set is deliberately not asserted here: this ledger's totals count a
  tracked reader page as accepted unless it is pending, and changing that bucket would restate
  dated totals that still owe their own full-page re-read. The independent full-page re-read
  the rule requires remains **owed and not performed**.

Two pages therefore change classification, both away from acceptance: the
forecast returns to pending under the "larger change" sentence, and the
register returns to pending while additionally correcting an erroneous
acceptance recorded by the #554 round. Eleven pages were already pending and
stay pending even though four of them — the BER backlog, the step-0 log, the
AEGIS-060+ register and the skills catalog — now have a recorded independent
review. Accepted falls 586 → 584 and pending rises 11 → 13. This round changes
this ledger by more than 10 lines, so the ledger itself returns to **pending**
and needs its own
independent full-page re-read against [Acceptance for each
page](#acceptance-for-each-page).

The register's move matters beyond its own row: it corrects a prior round of
this ledger that recorded a targeted review as a full-page acceptance. That is
the same class of error this round was briefed to avoid, and it was introduced
by an earlier merged PR, not by the pages it recorded.

Two authorities outside this ledger confirm the determination rather than
weakening it. [CONTRIBUTING](../../CONTRIBUTING.md), in **Write documentation
for a new reader** rule 6, states that the pull request must "name the pages
reviewed and any pages still waiting for the repository-wide readability
sweep" and "Ask an independent reviewer to describe the component's purpose
and normal use from the documentation alone, then correct any gap they find":
PRs #555, #557, #558, #559 and #560 each now carry an independent review, so
they satisfy that contributor-facing instruction for their changed lines.
What they do not supply is a full-page re-read of a page that was already
pending, which is why their pages stay pending. And the 10-line rule carries
no decision number: it rests on dated owner decisions (2026-09-27, refined
2026-09-28 and 2026-09-29), recorded here and in the [open-decisions
index](aegis-open-decisions-2026-09-23.md); the step-0 reconciliation record
names this backlog nowhere and its highest decision is D71, so there is no
D-number to cite for it. Because no decision entry adjudicates the rule, this
round had to settle the register's status from the rule text plus the ledger's
own dated history, which is exactly where the earlier erroneous acceptance
came from.

**Current-truth restatement, appended 2026-10-01 — re-derived at `origin/main` `f38dcc25`.**
Nothing above is rewritten or reordered. This note records only what changed since the last
reading and re-derives, from the repository, every figure it can. Where a figure cannot be
derived from a command it is left as read or reported as a proven bound, never replaced by an
invented number.

*Superseded reading.* The last reading is the **Re-check and restamp, 2026-09-30** above, which
re-derived its figures at `origin/main` `5c806348`: "`git ls-tree -r --name-only origin/main`
filtered to `*.md` returns **657** tracked Markdown files". That revision is fourteen commits
behind the `f38dcc25` this note was asked to re-derive against — `git log --oneline
5c806348..f38dcc25` lists fourteen — and sixteen behind `origin/main` at the time of writing,
`29817f50` (PR #597), where `git log --oneline 5c806348..refs/remotes/origin/main` lists sixteen,
and seventeen behind `origin/main` as this revision was prepared, `253aa338` (PR #602). The
ledger itself is unchanged between those revisions: `git diff --stat 29817f50
refs/remotes/origin/main -- docs/roadmaps/aegis-documentation-readability-backlog.md` prints
nothing, so this note reads the same ledger text at each.

*What changed since `5c806348`.* Two facts settle the inventory, and they are checked per commit
rather than inferred from the pull-request list. **First, exactly one commit in the range added a
tracked Markdown file.** Running `git show --name-status <commit>` for every commit in
`git log --format='%h' 5c806348..f38dcc25` yields a single `A` entry across all fourteen:
commit `1955c222` adds the
[2026-09-30 evening session continuation](../evidence/session-continuation-2026-09-30-evening.md).
Its full line is `git log --diff-filter=A --format='%h %s' refs/remotes/origin/main --
docs/evidence/session-continuation-2026-09-30-evening.md` →
`1955c222 docs(evidence): record the 2026-09-30 evening session state for continuation (#586)`.
**Second, no commit in the range deleted one:** `git diff --name-status --diff-filter=D 5c806348
refs/remotes/origin/main` prints nothing, as does the same command over `410b90aa`.

The eight merges this correction was asked to account for — **#589**, **#590**, **#591**,
**#595**, **#596**, **#598**, **#599** and **#600** — are all in that range and are all
modification-only: `git show --name-status` lists only `M` (modified) entries for each and no `A`
tracked Markdown path. So are the range's other six merges (#586, #587, #588, #592, #593, #594),
with the single exception of #586's added page above. The eight named merges therefore move no
inventory figure at all. Nor does the later **#601** (`ed5f8ae6`), whose only Markdown entries are
seven modifications under `.claude/skills/`, nor **#597**, which amends `AGENTS.md` only, nor
**#602** (`253aa338`), which again modifies seven skill files and adds none. So at `f38dcc25`, at
`29817f50` and at `253aa338` alike, the file count is **658**.

*Tracked Markdown files: **658**.* Command: `git ls-tree -r --name-only
refs/remotes/origin/main | Select-String '\.md$'` → **658**. The same command returns **657** at
`5c806348` and **653** at `410b90aa`, and `653 + 5 = 658`, where the five additions are exactly
the Markdown paths in `git diff --name-status --diff-filter=A 410b90aa refs/remotes/origin/main`:
the [procedure](../skill-eval-behavioral-test-procedure.md), the
[authorization request](skill-eval-harness-authorization-request.md), the
[run record](../evidence/skill-eval-run-2026-09-30.md), the
[session continuation](../evidence/session-continuation-2026-09-30.md) and the
[evening session continuation](../evidence/session-continuation-2026-09-30-evening.md).

*Pending pages: **not derivable** from a command. The newest figure the ledger states is **16**,
and the lowest figure its own newest reading can support at `f38dcc25` is **17**.* This ledger has
no single command that yields its pending set, and the pages that would move the figure are
precisely the pages that remain unread. What can be stated is bounded rather than guessed:

- The pending set was **13** at `410b90aa`, the last reading that stated it with a closed
  arithmetic: `584 + 1 + 55 + 13 = 653`.
- Five pages were added between `410b90aa` and `f38dcc25`. Under the targeted-edit rule above,
  each starts pending, because that rule *retains* an acceptance and *confers* none.
- Three of the five are recorded pending in this ledger: the
  [procedure](../skill-eval-behavioral-test-procedure.md) and the
  [authorization request](skill-eval-harness-authorization-request.md) ("the pending set from 13
  to **15**") and the [run record](../evidence/skill-eval-run-2026-09-30.md) ("from 15 to
  **16**"). Those three are therefore already inside the recorded 16.
- The other two are not. The [session continuation](../evidence/session-continuation-2026-09-30.md)
  does move the tip count: the current-reading note reads "(A later merge, PR #577, adds one
  further tracked page … so the tip count is now **657**; that page joins the pending set …)".
  What it does not do is move the pending figure in the arithmetic, which the skill-eval round
  sections below still close at `584 + 1 + 55 + 16 = 656`, without counting it. The
  [evening session continuation](../evidence/session-continuation-2026-09-30-evening.md) carries
  no review result at all. The ledger *before* this note never named it, so no acceptance of it
  and no review of it could have been recorded:
  `git show refs/remotes/origin/main:docs/roadmaps/aegis-documentation-readability-backlog.md |
  Select-String -SimpleMatch 'session-continuation-2026-09-30-evening'` returns **0** lines. On
  this branch the same filter returns **5** lines, and all five are added by this note — the two
  cross-references above and this sentence — not by an earlier reading. The rule above therefore
  leaves a new page pending.
- That is the gap, and it is a text gap rather than a review gap. The section's `16` is the
  pre-#577 snapshot at the skill-eval-round revision, and the restamp above — which is the
  ledger's newest reading — confirms at `5c806348` both that the file count is `657` and that
  PR #577's page "already joins the pending set", then declines to restate the pending figure.
  So the ledger's newest *stated* pending count is 16 while its own newest *confirmed* facts imply
  17 at `5c806348`.
- At `f38dcc25` the provable floor is therefore `17 + 0 = **17**`: the evening session
  continuation is a further new page that the rule leaves pending, but this ledger records no
  reading of it, and a page that has never been reviewed cannot be shown to have joined a set
  that has never been recomputed. **The exact current pending count is not derivable from a
  command, and this note does not assert one.** Naming the gap is the honest output; the restamp
  above already records the owed full-page re-read that would settle the set itself, and it
  remains owed.

*Accepted readers and classified fixtures: left as read, with one check.* The accepted figure
(584) counts pages a reviewer has read whole; no command reproduces it, and this note performs no
review, so it is not re-derived. The classified synthetic-fixture figure (55) has a path-based
check that reproduces it: `git ls-tree -r --name-only refs/remotes/origin/main -- scripts`
filtered to `*.md` returns **56**, and removing the one reader-facing
`scripts/tests/fixtures/README.md` that this ledger's own fixture rule excepts leaves **55**,
matching the recorded figure. That the remaining 55 files are each genuinely
classification-only test input is not re-verified here. The generated-report count stays **1**. The
generator this ledger names is `scripts/audit-skill-contracts.py`, whose `--markdown` option writes
the [baseline report](../audits/skill-contract-audit-baseline.md); that report is judged on its
output format rather than by a full-page re-read.

*Unchanged.* None of the eight merges named above adds a Markdown page, changes a grant, or
touches a protected path, so the eight move no classification by their own content. This
restatement confers no acceptance. Itself an edit to a page that is already pending, it leaves
this ledger **pending** its own independent full-page re-read against [Acceptance for each
page](#acceptance-for-each-page).

### Acceptance audit of the 2026-10-01 provenance relabels — 2026-10-01

**Determination: nine accepted skill pages have silently lost their full-page
acceptance and are recorded here as pending.** The [targeted-edit
rule](#remaining-page-review-in-larger-batches) keeps an acceptance only for a
change of at most 10 net lines on the page that adds no section, measured from
that page's accepted version to now. Four merges relabelled provenance and
expanded shorthand across skill pages only — **#601** (`ed5f8ae6`), **#602**
(`253aa338`), **#604** (`c03f77f9`) and **#607** (`cc697914`) — and **#486**
(`8459ac73`) contributed two more lines to one of the nine. Each added no `##`
section to any page, so only the line limb is in play. A single merge alone
took each page past the threshold: decomposing every page into the commits it
received since acceptance returns one commit whose own change is already over
10 lines — 31, 26, 18, 15, 14, 14, 12, 12 and 11 — so no cumulation is needed
and none is claimed. `iso-27001-isms-architect` is the only page with a second
contributor, the two #486 lines inside its 17, and it too crosses on its
relabel commit alone. No commit after `cc697914` touches any of them, so each
page's accepted version still stands:

| Page | Accepted at | Net changed lines | `--numstat` |
| --- | --- | ---: | --- |
| `performance-test-harness/SKILL.md` | `8c6750a` (batch 3, #473) | 31 | `21 10` |
| `iso-42001-aims-architect/SKILL.md` | `2a86058` (batch 7, #470) | 26 | `17 9` |
| `qa-strategy-architect/SKILL.md` | `54034fa` (batch 9, #468) | 18 | `12 6` |
| `iso-27001-isms-architect/SKILL.md` | `14ecd0c` (batch 5, #474) | 17 | `11 6` |
| `merge-is-deploy-governance/SKILL.md` | `2a86058` (batch 7, #470) | 14 | `10 4` |
| `authority-invalidation-architect/SKILL.md` | `8c6750a` (batch 3, #473) | 14 | `9 5` |
| `adr-sequencer/SKILL.md` | `2a86058` (batch 7, #470) | 12 | `8 4` |
| `risk-tiered-validation-selector/SKILL.md` | `5e0e9ad7` (#224 batch) | 12 | `10 2` |
| `resilience-architecture-reviewer/SKILL.md` | `d75cd58` (#522) | 11 | `8 3` |

Each row is `git diff --numstat <accepted-at> refs/remotes/origin/main --
.claude/skills/<name>/SKILL.md`, added plus deleted. Each row uses the latest
revision at which that page is recorded accepted, so every figure is a **lower
bound**: an earlier acceptance can only enlarge the count. The deleted line is
load-bearing on five rows — `merge-is-deploy-governance`, `authority-
invalidation-architect`, `adr-sequencer`, `risk-tiered-validation-selector` and
`resilience-architecture-reviewer` would not reach 10 on added lines alone, and
the first and fourth sit at exactly 10 added. The rule names added plus deleted,
so the sum is the measure and the choice is not arbitrary.

Each page is recorded as accepted at the revision cited: seven in the
"(102 of the 103)" list above; `risk-tiered-validation-selector` through the
#224 acceptance batch (`5e0e9ad7`), which the ledger counts as gaining twenty
pages without naming each; and `resilience-architecture-reviewer` in its own
#522 row. No later reading restated any of the nine. The totals therefore
overstate accepted readers by nine: at most **575** against the recorded 584.
The dated arithmetic `584 + 1 + 55 + 16 = 656` is left exactly as the snapshot
it is and is **not** rewritten. The pending set rises from the provable floor
the 2026-10-01 restatement establishes — 17, not the earlier recorded 16 — to
at least **26**. The exact pending count stays not derivable from a command,
for the reason recorded above.

Each of the nine needs one independent full-page re-read against [Acceptance
for each page](#acceptance-for-each-page). The relabels that pushed them over
were reader-only: they changed no rule, heading, frontmatter `description:` or
line-count limit. This note is itself an edit to a page that is already
pending, so it confers no acceptance and leaves this ledger **pending** its own
independent full-page re-read.

### Ledger update for the skill-eval rounds — 2026-09-30

This round adds Markdown and changes no skill, no eval file and no script. The
[skill-eval behavioral test procedure](../skill-eval-behavioral-test-procedure.md)
merged in PR #564 (198 added lines, merge commit `6a37c8d8`), and the
[skill-eval harness authorization request](skill-eval-harness-authorization-request.md)
is registered here.

The procedure page is a **new tracked page and is pending**. It has had no
independent full-page re-read against [Acceptance for each
page](#acceptance-for-each-page), and the [targeted-edit
rule](#remaining-page-review-in-larger-batches) *retains* an acceptance rather
than conferring one, so a new page starts pending and stays pending until
someone reads it whole. Its independent review on PR #564 returned
SHIP-WITH-NITS against a factual-accuracy standard and found no blocker, but it
reviewed the page's claims, not its readability against this list, so it does
not confer acceptance. A later PR (#566, merge commit `3d3a0868`) corrected one
false sentence in the pending
[delivery control-plane guide](../../tools/aegis_delivery_control/README.md);
that page also **stays pending**.

**This PR adds the second new page**, the
[skill-eval harness authorization request](skill-eval-harness-authorization-request.md)
registered above, and it is pending on the same reasoning. **A ledger that
counts a new page must count its own**, so the round's own page is included in
the totals below — an earlier draft of this section omitted it and stated 654,
which was wrong.

The inventory therefore moves from 653 to **655** tracked Markdown files, and
the pending set from 13 to **15**. Accepted readers stay **584**, the generated
report stays **1**, and the classified synthetic fixtures stay **55**. The
arithmetic closes: 584 + 1 + 55 + 15 = 655, which is `git ls-tree -r
--name-only` filtered to `.md` at this PR's head.

This round changes this ledger by more than 10 lines, so the ledger itself
**stays pending** and still owes its own independent full-page re-read. No
grant and no gate changed: the procedure page starts nothing, the request page
authorizes nothing, and neither touches a protected path.

### Ledger update for the skill-eval run record — 2026-09-30

A later PR this round adds one more page, the
[skill-eval run record](../evidence/skill-eval-run-2026-09-30.md), which
records three executed eval cases, their independent grading, and two findings
plus one **withdrawn** non-finding. It is **pending**: no independent full-page
re-read, and the targeted-edit rule retains rather than confers, so a new page
starts pending.

It exists because an independent reviewer of #567 twice found that the run's
findings had **no committed artifact** — first as an unsupported claim, then as
*"still attestation-only"* — until this page committed them, which is why the
page is not optional.

The inventory therefore moves from 655 to **656** tracked Markdown files, and
the pending set from 15 to **16**. Accepted readers stay **584**, the generated
report stays **1**, and the classified synthetic fixtures stay **55**. The
arithmetic closes: 584 + 1 + 55 + 16 = 656.

**Re-check and restamp, 2026-09-30.** The tip figures above were re-derived at `origin/main`
`5c806348`: `git ls-tree -r --name-only origin/main` filtered to `*.md` returns **657**
tracked Markdown files, matching the PR #577 annotation above exactly, and no page has been
added since. PR #577's added page is already recorded in the current-reading note at the top of
this ledger and already joins the pending set, so it needs no further edit. What does stay open is
recorded here rather than fixed: **this ledger is itself still pending and still owes its
own independent full-page re-read.** That is an owed independent review, not a text fix, so
it is deliberately left undone rather than faked; this restamp confers no acceptance.

The two component guides,
root guide and documentation index have received bounded readability work;
the [delivery batches](#documentation-batches) identify what was checked.
The **491-file inventory and the ordered "start with" steps below are the
original launch plan**, retained to show how this work began. Do not restart
those delivered batches from that plan.

The merged #360 tree (`4227b71`) had **604 tracked Markdown files: 560
accepted reader pages and 44 classified synthetic fixtures**, with zero known
pending pages; the skill-contract follow-up below brings it to 605.
Merged PR #335 added the [Stage 4B synthetic case fixture draft](aegis-setup-package-4b-synthetic-case-fixtures.md)
without a ledger entry; a forecast checkpoint reconciliation found the gap,
and PR #354 recorded the page as pending. Despite its name, that page is not
one of the 44 classified fixtures: those are test-input files under
`scripts/`, while this page is a reader-facing offline planning draft for
issue #101 Stage 4B. It proposes invented inputs and expected outcomes for
eight cases, all **NOT RUN**, and is not host proof. A first independent
full-page review returned FIX-FIRST; after its nine minimal edits, a separate
corrected-candidate review **accepted** the
[Stage 4B synthetic case fixture draft](aegis-setup-package-4b-synthetic-case-fixtures.md)
against [Acceptance for each page](#acceptance-for-each-page). Acceptance
changes no claim, grant or host status. No other Markdown file was added,
removed or renamed between #333 and #356.

The 2026-09-26 skill-contract follow-up adds one reader page, the
[dated candidate disposition record](../evidence/skill-contract-dispositions-2026-09-26/candidate-dispositions.md),
to the 604-page #360 tree (`4227b71`). It reviews nine audit candidates and
changes no skill. After a FIX-FIRST review and its minimal edits, a separate
independent corrected-candidate review **accepted** it against
[Acceptance for each page](#acceptance-for-each-page). The tree now has **605
tracked Markdown files: 561 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages.

The governance change recording the owner's 2026-09-26 decisions — the #331
correction and #333 option A (Behavioral Eval Runner (BER) decision
BER-DEC-014 and approval-register entries AEGIS-APR-046 and AEGIS-APR-047),
and the standing merge conditions, eval-maintenance ruling and package-2
consumption (AEGIS-APR-048 through AEGIS-APR-052) — changed seven existing
reader pages and added no Markdown file: the approval register, BER backlog,
guard decision packet, merge policy, offline CI guide, forecast and this
ledger. Independent full-page reviews corrected and accepted all seven
against [Acceptance for each page](#acceptance-for-each-page) after minimal
edits to owner-confirmation wording, pinned grant conditions, status-code and
priority-level explanations, links, the forecast's material-decision section
and this ledger's placement. Acceptance changes no grant, gate or host
status. The tree remains **605 Markdown files: 561 accepted reader pages and
44 classified synthetic fixtures**, with zero known pending pages.

The 2026-09-26 feature-flag skill follow-up adds one reader page, the
[feature-flag system skill proposal](feature-flag-architect-skill-proposal.md),
to the 605-page #370 tree (`eadf1fd`). It records the owner-accepted scope for
a new `feature-flag-architect` skill and a provisional 3–5.75 active-hour
estimate; it builds no skill and grants no authority beyond the standing
delivery approvals. A first independent full-page review returned FIX-FIRST;
its minimal edits corrected the highest decision number seen on `main` (D63,
not D60) and defined `project-orchestrator` stages and the Use When and Stop
Conditions sections at first use, and a corrected-candidate review accepted
it. Fixes for eight Codex review findings on PR #378 and the owner's
2026-09-26 decisions (Stage 9 route added, D64 row, the
`caching-strategy-designer` seam kept, hub ROUTE-002 findings (the
skill-contract audit rule that flags a skill handing work to a neighbour that
never hands back) kept as census data) then changed the page materially. An independent re-review of the
revised page returned FIX-FIRST; its one minimal edit aligned the merge step
with AEGIS-APR-050 (Codex confirmed unavailable) and defined Codex, P1/P2
and `gate-guard` at first use. A separate independent corrected-candidate
review **accepted** it against
[Acceptance for each page](#acceptance-for-each-page). The candidate tree has
**606 tracked Markdown files: 562 accepted reader pages and 44 classified
synthetic fixtures**, with zero known pending pages.

The governance change recording delivery of the BER-DEC-014 correction in
merged PR #374 (`7390ae0`) and the consumption of its one-package grant
(AEGIS-APR-053, consuming AEGIS-APR-046), plus the owner's protected-path grant
and one-time guard exception for merged PR #373 and their consumption
(AEGIS-APR-054 through AEGIS-APR-056), changes three existing reader pages and
adds no Markdown file: the approval register, BER backlog and this ledger. A
first independent read-only full-page review returned FIX-FIRST. Its minimal
edits attributed the pinned eval ids and expanded Pacific Daylight Time (PDT)
in AEGIS-APR-054, corrected the timing sentence in AEGIS-APR-055, disclosed the
corrected `gate-guard` log citation in AEGIS-APR-053, split the BER backlog's
start-here paragraph, stated that planned `UNRUN` attempts can still count
under `NOT_SELECTED`, named the automated Codex review and APR-050 at first
use, pinned the WP-2B-3 record's effective governance merge `2aed8dd` and
receipt-correction wording, and tightened this paragraph's follow-up wording.
A separate independent corrected-candidate review **accepted** all three pages
against [Acceptance for each page](#acceptance-for-each-page). Acceptance
changes no grant, gate or host status. With the feature-flag proposal page
above, merged in PR #378 (`a2d2b83`), the tree stands at **606 tracked
Markdown files: 562 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages.

The catch-up forecast checkpoint after #370 changes three existing reader
pages and this ledger, and adds no Markdown file: the [backlog forecast](aegis-backlog-forecast.md),
the [execution measurements](aegis-execution-metrics.md) and the
[open-decisions index](aegis-open-decisions-2026-09-23.md). #352 had also
changed the forecast and measurement pages without a recorded full-page
review; the AEGIS-APR-046 to AEGIS-APR-052 governance change above later accepted the forecast but not the
measurement page. A first independent full-page review returned FIX-FIRST;
its minimal edits removed a stale owner-read horizon for S5 (the owner-choice
batch of six skills classified UNSURE), aligned the
feature-flag skill's status (scope accepted, skill in progress, routing not
started) across all three pages, reconciled the owner-choice batch counts and
dated the open-PR list. After those edits all three pages are **re-accepted
after a separate corrected-candidate review** against
[Acceptance for each page](#acceptance-for-each-page); no measurement,
estimate, grant or gate changed. The tree on main after #370 had **605
tracked Markdown files: 561 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages; #364 added the only new page and
this checkpoint adds none.

That record covered only three pages, but the checkpoint also changed this
ledger, whose own revision had no recorded review. An automated Codex review
of that candidate also found a delivered estimate still counted as remaining
work, a resolved row in the open owner queue, a missing open owner decision
and mismatched owner-choice counts. The follow-up revision changes all four
pages again to fix those findings and record merges and owner decisions made
later on 2026-09-26. A first independent full-page review of
the follow-up returned FIX-FIRST: PR #382, described as open, had merged.
Its minimal edits recorded that merge on the three roadmap pages and removed
#382 from the open owner queue. A separate corrected-candidate review
asked for one more wording edit, so 22 skills reads only as the original
audit count, and then **accepted all four pages, including this ledger**,
against [Acceptance for each page](#acceptance-for-each-page). No estimate,
grant or gate changed.

On 2026-09-27 UTC, #378 merged the feature-flag proposal page described
above, then #375, #376 and #377 merged, and later #371 (one skill's seam, no new page), #381 (the APR-046 consumption record, three changed existing pages), #383 (the `feature-flag-architect` skill) and #384 (the `project-orchestrator` flag routes, one changed skill page, no new page). A reconciliation revision recorded
those merges as after-reading notes on the three roadmap pages, including
that all 23 owner-choice skills are now delivered, and updated this ledger's
current count; it reassesses no estimate. Main after #381 had **606 tracked
Markdown files: 562 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages; #371, #381 and this checkpoint add none. #383 added two skill reader pages, `.claude/skills/feature-flag-architect/SKILL.md` and its `references/flag-system-sheet.md`, after a skill-quality review but with no recorded full-page review against [Acceptance for each page](#acceptance-for-each-page), so both are **pending**; the named follow-up is one independent full-page review of both. Main after #383 (`6844ab9`) has **608 tracked Markdown files: 562 accepted reader pages, 44 classified synthetic fixtures and two known pending pages**; #384 (`0f46808`) adds no Markdown file, so main after #384 still has 608. A first independent full-page review of this reconciliation returned FIX-FIRST; its minimal edits recorded #383 and its two pending skill pages, the D64 row and the fifth one-way ROUTE-002 finding as census data, and made an unclear governance reference explicit. A separate corrected-candidate review returned FIX-FIRST only because #384 merged during review; after its minimal edits recorded that merge on all four pages, it **accepted all four pages, including this ledger**, against [Acceptance for each page](#acceptance-for-each-page). No estimate, grant or gate changed.

PR #387 (`dcccb10`), merged on 2026-09-27 UTC, applied the minimal edits from
a first independent full-page review of #383's two skill pages,
`.claude/skills/feature-flag-architect/SKILL.md` and its
`references/flag-system-sheet.md`; that review had returned FIX-FIRST for
terms not defined at first use. A separate corrected-candidate review then
returned FIX-FIRST for one sentence: the sheet said it served Workflow steps
2–9, but its sections serve steps 2, 4 and 6–9. #387's final commit
(`037f883`) made that correction. A final independent read-only check of both
pages on main after #387, by a reviewer who wrote neither the pages nor the
edits, checked every criterion in [Acceptance for each
page](#acceptance-for-each-page) and **accepted both pages** with no further
edits: terms are defined at first use, the sheet's step list matches its
section headings, every named skill and evaluation case exists, and both
relative links resolve. Main after #387 and #379 (`7947b5e`) has **608 tracked
Markdown files: 564 accepted reader pages and 44 classified synthetic
fixtures**, with zero known pending pages; #387 and this update add no
Markdown file. No skill behavior, grant or gate changed. PR #386 (`39f2a28`)
merged after #379; it changed one existing reader page, the [project
history](../HISTORY.md), and adds no Markdown file, so main after #386 still
has 608 tracked Markdown files; an independent full-page review accepted it
before merge. An independent full-page review then **accepted this ledger
change**, including this paragraph and its batch row, against [Acceptance for
each page](#acceptance-for-each-page).

PRs #388 (`a3ae6cf`), #390 (`fcd525b`), #394 (`29c484f`), #395 (`741b29a`)
and #396 (`cd7af02`), merged on 2026-09-27 UTC after #386, made targeted
corrections to 37 already-accepted reader pages: ten skill reference sheets,
one `SKILL.md` body passage, the README, the skills catalog and 24 `SKILL.md`
frontmatter descriptions (23 ROUTE-002 target skills and one source skill).
Their changed passages were reviewed before merge as targeted corrections,
not full-page reviews. Under the owner's 2026-09-27
[targeted-edit rule](#remaining-page-review-in-larger-batches), each of
those edits changed at most 10 lines on its page (added plus deleted lines
from `git diff --numstat`; the largest was 10, the README in #390) and added
no section, so the pages kept their earlier full-page acceptance. Later
merges, recorded in the next paragraph, returned the README, the skills
catalog and `.claude/skills/human-approval-boundary/SKILL.md` to pending.
#391 (`7108d64`) changed evaluation JSON (JavaScript Object Notation) files
only. None adds a Markdown file, so
main after #396 had **608 tracked Markdown files: 564 accepted reader pages
and 44 classified synthetic fixtures**, with zero known pending pages. No
grant or gate changed.

PRs #385 (`867cb82`), #389 (`0fb9c06`), #392 (`e56d863`), #393 (`9b8f5b2`),
#399 (`c5ff91d`), #400 (`e00df2d`) and #402 (`8bd1d58`), merged on
2026-09-27 UTC after #396, then #398 (`6c5313a`), #401 (`56ea7e4`) and #407
(`1ec01bf`), changed 11 already-accepted reader pages and added one. None
recorded a full-page review. The [targeted-edit
rule](#remaining-page-review-in-larger-batches) was applied to each page,
counting added plus deleted lines from `git diff --numstat` between each
merge's first parent and the merge, and adding together every edit a page
received since its last full-page acceptance, including the edits in the
previous paragraph. No edit added a heading to an existing page.

- **Keep full-page acceptance (four pages):**
  `.claude/skills/api-event-architect/SKILL.md` (#396 and #385, 7 lines),
  `.claude/skills/file-upload-storage-architect/SKILL.md` (#385, 10),
  `.claude/skills/cloud-architecture-decider/references/decision-inputs.md`
  (#393, 4) and
  `.claude/skills/risk-tiered-validation-selector/references/classifier-rules.md`
  (#402, 2).
- **Pending until an independent full-page re-read (eight pages):**
  [README](../../README.md) (#390, #389, #392 and #393, 111 lines; #392 alone
  changed 98), [skills catalog](../skills-catalog.md) (#390, #389 and #393,
  16), [skill generation standard](../skill-generation-standard.md) (#402,
  15), `.claude/skills/cloud-architecture-decider/SKILL.md` (#393, 198),
  `.claude/skills/multi-tenant-data-architect/SKILL.md` (#385, 22),
  `.claude/skills/ci-pipeline-architect/SKILL.md` (#385, 13),
  `.claude/skills/human-approval-boundary/SKILL.md` (#394 and #385, 11) and
  the new
  `.claude/skills/cloud-architecture-decider/references/managed-platform-tier.md`
  (added by #393 with no full-page review).

#399, #400, #398, #401 and #407 changed evaluation JSON only. #393 is the
only merge that adds a Markdown file, so main after #407 (`1ec01bf`) had
**609 tracked Markdown files: 557 accepted reader pages, 44 classified
synthetic fixtures and eight known pending pages**. The named follow-up is
one independent full-page re-read of each pending page against [Acceptance
for each page](#acceptance-for-each-page). No grant or gate changed.

PRs #404 (`b08103e`), #405 (`f2d57b5`) and #406 (`6488eaa`), merged on
2026-09-27 UTC after #407, changed 30 existing reader pages and added none.
#404 updated the agent instruction file map, #405 re-anchored the artificial intelligence (AI) security
pack to the 2026 OWASP (Open Worldwide Application Security Project) Top 10
for large language model (LLM) applications, and #406 corrected a README
option and aligned the cloud decider's category names. None recorded a
full-page review. The [targeted-edit
rule](#remaining-page-review-in-larger-batches) was applied as in the
previous paragraph: added plus deleted lines from `git diff --numstat`
between each merge's first parent and the merge, added together for every
edit a page received since its last full-page acceptance. By owner decision
(2026-09-27), a renamed existing heading is not a new section; #405
renamed or renumbered existing headings on three pages and added no section.

- **Keep full-page acceptance (18 pages):** in `.claude/skills/`,
  `agent-tool-safety-guard/SKILL.md` (10) and its
  `references/tool-permission-matrix.md` (2),
  `ai-cost-guardrail-designer/SKILL.md` (10) and its
  `references/cost-guardrail-patterns.md` (4),
  `ai-misinformation-guard/references/grounding-controls.md` (2),
  `llm-output-safety-reviewer/SKILL.md` (#396 and #405, 8) and its
  `references/output-sink-catalog.md` (8),
  `memory-context-poisoning-reviewer/SKILL.md` (6) and its
  `references/memory-poisoning-controls.md` (4),
  `model-poisoning-reviewer/references/poisoning-controls.md` (10),
  `prompt-injection-defender/references/injection-defense-patterns.md` (3),
  `rag-security-architect/references/rag-retrieval-authz.md` (6, one renamed
  heading), `sensitive-disclosure-guard/references/disclosure-controls.md`
  (2), `skill-quality-reviewer/SKILL.md` (6) and its
  `references/quality-review-checklist.md` (4),
  `supply-chain-security-reviewer/references/supply-chain-checklist.md` (#388
  and #405, 9, one renamed heading), and
  `system-prompt-leakage-reviewer/SKILL.md` (8) and its
  `references/prompt-leakage-checks.md` (9). Counts are #405 alone unless
  another PR is named.
- **Newly pending until an independent full-page re-read (nine pages):** in
  `.claude/skills/`,
  `agent-instruction-consolidator/references/instruction-file-map.md` (#404,
  19), `ai-misinformation-guard/SKILL.md` (#395 and #405, 12),
  `ai-threat-modeler/SKILL.md` (#405, 21) and its
  `references/llm-top10-threat-catalog.md` (#405, 115; its renumbered
  headings add no section), `model-poisoning-reviewer/SKILL.md` (#394 and
  #405, 15), `rag-security-architect/SKILL.md` (#405, 14),
  `supply-chain-security-reviewer/SKILL.md` (#388 and #405, 18) and
  `cloud-architecture-decider/references/decision-inputs.md` (#393 and #406,
  12, which moves from the previous paragraph's keep list to pending); and
  `docs/reconciliation/step-0-reconciliation-v4.md` (#405, 14).
- **Already pending, with updated totals:** the [README](../../README.md)
  (165 lines after #405 added 32 and #406 added 22), the [skills
  catalog](../skills-catalog.md) (66 after #405 added 50) and
  `.claude/skills/cloud-architecture-decider/SKILL.md` (204 after #406 added
  6).

Main after #406 (`6488eaa`) therefore had **609 tracked Markdown files: 548
accepted reader pages, 44 classified synthetic fixtures and 17 known pending
pages**. No grant or gate changed.

PR #408 (`0533764`), merged on 2026-09-27 UTC after #406, changed two reader
pages and added none. The [skill generation
standard](../skill-generation-standard.md), pending since #402, now codifies
the owner's 2026-09-27 one-missing-fact-per-turn loop in §4, defines
`when_to_use` in §2, dates the D49 measurement and aligns the §6 census
wording with `census.py`. A first independent full-page review returned
FIX-FIRST (three edits plus the optional D49 date); a separate independent
corrected-candidate review **accepted** it against [Acceptance for each
page](#acceptance-for-each-page). `.claude/skills/_template/SKILL.md` changed
its Workflow missing-fact sentence to match standard §4; the same
corrected-candidate review re-read the whole page and **accepted** it, so the
template, already accepted, stays accepted. Main after #408 (`0533764`) has
**609 tracked Markdown files: 549 accepted reader pages, 44 classified
synthetic fixtures and 16 known pending pages**: the README, the skills
catalog, `.claude/skills/cloud-architecture-decider/SKILL.md` and its
`references/decision-inputs.md` and `references/managed-platform-tier.md`,
`.claude/skills/multi-tenant-data-architect/SKILL.md`,
`.claude/skills/ci-pipeline-architect/SKILL.md`,
`.claude/skills/human-approval-boundary/SKILL.md`, and the other eight pages
newly pending after #404–#406. The named follow-up is one independent
full-page re-read of each pending page against [Acceptance for each
page](#acceptance-for-each-page). No grant or gate changed.

PRs #409 (`4416c6d`), #411 (`7693c26`) and #397 (`4a68ace`) merged on
2026-09-27 UTC after #408, in that order. The [targeted-edit
rule](#remaining-page-review-in-larger-batches) was applied as above, adding
together each page's `git diff --numstat` lines since its last full-page
acceptance.

- **#409** extended the skill for LLM08 (the eighth risk in that OWASP list)
  to the full OWASP Hidden Context Exposure scope and renamed it from
  `system-prompt-leakage-reviewer` to `hidden-context-exposure-reviewer`
  (decision D66). It deleted the old
  skill's two accepted pages and added
  `.claude/skills/hidden-context-exposure-reviewer/SKILL.md` and its
  `references/hidden-context-checks.md`. Its independent review was a skill
  review whose REVISE verdict asked for two edits, not a full-page review,
  so both new pages are **pending**.
  `.claude/skills/agent-tool-safety-guard/SKILL.md` becomes **pending** (17
  lines: 10 in #405 and 7 in #409). In `.claude/skills/`,
  `prompt-injection-defender/SKILL.md` (8),
  `sensitive-disclosure-guard/SKILL.md` (6) and
  `ai-evaluation-harness/references/eval-harness-design.md` (5) **keep
  acceptance**. The README (167), the skills catalog (77),
  `ai-threat-modeler/SKILL.md` (25), its
  `references/llm-top10-threat-catalog.md` (121) and the step-0
  reconciliation record (56) were already pending. Main after #409 had **609
  tracked Markdown files: 546 accepted reader pages, 44 classified synthetic
  fixtures and 19 known pending pages**.
- **#411** applied the minimal edits from full-page re-reads of the skills
  catalog and `.claude/skills/cloud-architecture-decider/SKILL.md`. The first
  review returned FIX-FIRST; a separate independent corrected-candidate
  review **accepted** both pages on #411's branch head (`4e643c6`).
  `cloud-architecture-decider/SKILL.md` on main matches that head, so it is
  **accepted**. That head did not contain #409, which merged first and
  changed the catalog by 11 lines (7 added, 4 deleted), so under the rule
  the catalog on main stays **pending** (11 lines since its accepted
  candidate). Main after #411 had **609 tracked Markdown files: 547
  accepted reader pages, 44 classified synthetic fixtures and 18 known
  pending pages**.
- **#397** recorded the ROUTE-002 census dispositions. It added the
  [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md),
  which is **pending** until a full-page re-read, and a JSON data file.
  The [AEGIS-060+ register](../audits/aegis-060-plus-register.md) (proposed
  corpus-audit findings numbered AEGIS-060 and later), previously counted as
  accepted, becomes **pending** (21 lines). The step-0 reconciliation
  record's D64 amendment added 8 lines; the record was already pending (64
  lines after #405, #409 and #397).

Main after #397 (`4a68ace`) therefore had **610 tracked Markdown files: 546
accepted reader pages, 44 classified synthetic fixtures and 20 known pending
pages**. The pending pages are the README, the skills catalog and, in
`.claude/skills/`,
`cloud-architecture-decider/references/decision-inputs.md` and
`references/managed-platform-tier.md`, `multi-tenant-data-architect/SKILL.md`,
`ci-pipeline-architect/SKILL.md`, `human-approval-boundary/SKILL.md`,
`agent-instruction-consolidator/references/instruction-file-map.md`,
`ai-misinformation-guard/SKILL.md`, `ai-threat-modeler/SKILL.md` and its
`references/llm-top10-threat-catalog.md`, `model-poisoning-reviewer/SKILL.md`,
`rag-security-architect/SKILL.md`, `supply-chain-security-reviewer/SKILL.md`,
`agent-tool-safety-guard/SKILL.md`, and
`hidden-context-exposure-reviewer/SKILL.md` and its
`references/hidden-context-checks.md`; and the step-0 reconciliation record,
the ROUTE-002 dispositions record and the AEGIS-060+ register. The named
follow-up is one independent full-page re-read of each pending page against
[Acceptance for each page](#acceptance-for-each-page). No grant or gate
changed.

PRs #410 (`b553d91`), #412 (`2219ac8`) and #414 (`3a1e9da`), then #419
(`9033e7c`), #417 (`dcec7f2`) and #418 (`02f054c`), then #413 (`fa1e344`),
#415 (`f4defa2`) and #416 (`da2636d`) merged on 2026-09-27 UTC after #397,
in that order; #403 (`f42e3f0`), which recorded #409, #411 and #397, merged
between #418 and #413. None adds, removes or renames a Markdown file. Five of
them applied the minimal edits from full-page re-reads of pending pages; a
page counts as accepted only when a separate independent corrected-candidate
review accepted it and the page on main matches the reviewed candidate. The
[targeted-edit rule](#remaining-page-review-in-larger-batches) was applied to
every other changed page as above, adding together each page's
`git diff --numstat` lines since its last full-page acceptance.

- **Accepted after full-page re-reads (16 pages).** #410:
  `.claude/skills/multi-tenant-data-architect/SKILL.md`,
  `ci-pipeline-architect/SKILL.md`, `human-approval-boundary/SKILL.md` and
  `cloud-architecture-decider/references/managed-platform-tier.md`, accepted
  on #410's branch head (`a56c60d`). #412: the [README](../../README.md),
  accepted on `ecbd860`. #414:
  `agent-instruction-consolidator/references/instruction-file-map.md` and
  `cloud-architecture-decider/references/decision-inputs.md`, accepted on
  `bd3219f`. #413: the [skills catalog](../skills-catalog.md), accepted on
  `2ceea06` after an independent full-page re-read. #415:
  `ai-threat-modeler/SKILL.md` and its
  `references/llm-top10-threat-catalog.md`, `rag-security-architect/SKILL.md`,
  `ai-misinformation-guard/SKILL.md`, `model-poisoning-reviewer/SKILL.md` and
  `supply-chain-security-reviewer/SKILL.md`, accepted on `79cee79`. #416: the
  [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md)
  and the [AEGIS-060+ register](../audits/aegis-060-plus-register.md),
  accepted on `a548dcb`. Each page on main after its merge is identical to
  the reviewed head. `human-approval-boundary/SKILL.md` then gained 4 lines
  in #419 and **keeps acceptance** (4 since #410).
- **Still pending:** `docs/reconciliation/step-0-reconciliation-v4.md`. #414
  added a "How to read this log" paragraph, updated the banner date and added
  a historical-edition note (19 lines), but its review covered only those
  passages, not the whole page (83 lines since its last acceptance).
- **Hand-back bullets, #417–#419 (27 `SKILL.md` pages, 3–7 lines each).**
  #419 and #417 each added a Use When bullet mirroring the description's
  hand-back clause from #394–#396; #418 made Use When mirror neighbours
  already named in six descriptions (for `code-simplifier`, by editing an
  existing bullet); independent reviews returned SHIP (approve to merge), not
  full-page reviews. In `.claude/skills/`, 25 pages **keep acceptance**:
  `admin-console-architect` (#395 and #419, 5), `adr-writer` (#396 and #417,
  5), `ai-closeout-reporter` (#418, 7), `architecture-designer` (#395 and
  #419, 6), `audit-log-architect` (#396 and #417, 5),
  `authorization-matrix-designer` (#418, 3), `change-classification-gate`
  (#394 and #419, 5), `code-reviewer` (#394 and #419, 6), `code-simplifier`
  (#418, 3), `human-agent-trust-reviewer` (#418, 4), `human-approval-boundary`
  (above), `plan-entitlement-architect` (#395 and #419, 7),
  `product-spec-writer` (#394 and #419, 6),
  `profiling-methodology-designer` (#418, 3),
  `requirements-gathering-facilitator` (#394 and #419, 5),
  `rls-policy-auditor` (#395, #413 and #417, 7),
  `roadmap-under-uncertainty-planner` (#418, 4), `rollback-runbook-author`
  (#396 and #417, 5), `screenshot-evidence-planner` (#394 and #419, 5),
  `security-pr-reviewer` (#395, #413 and #417, 8),
  `source-of-truth-reconciler` (#394 and #419, 5),
  `static-analysis-reviewer` (#395, #413 and #417, 8),
  `streaming-event-architect` (#396 and #417, 5), `tech-spec-writer` (#396
  and #417, 5) and `tenant-modeler` (#395 and #417, 6). Two become
  **pending**: `api-event-architect/SKILL.md` (12 lines: 5 in #385, 2 in
  #396 and 5 in #417) and `llm-output-safety-reviewer/SKILL.md` (11 lines: 2
  in #396, 6 in #405 and 3 in #417).
- **Master-prompt citation fix, #413.** It pointed the "master-prompt §6"
  citations at the historical master prompt that has numbered sections. Besides
  the catalog above, it changed seven pages in `.claude/skills/`, which all
  **keep acceptance**: `multi-tenant-security-tester/SKILL.md` (2),
  `rls-policy-auditor/SKILL.md` and `security-pr-reviewer/SKILL.md` and
  `static-analysis-reviewer/SKILL.md` (counted above),
  `secure-migration-reviewer/SKILL.md` (2), `threat-modeler/SKILL.md` (2)
  and `threat-modeler/references/threat-catalog.md` (4).

Main after #416 (`da2636d`) therefore had **610 tracked Markdown files: 560
accepted reader pages, 44 classified synthetic fixtures and six known pending
pages**. The pending pages are, in `.claude/skills/`,
`agent-tool-safety-guard/SKILL.md`, `hidden-context-exposure-reviewer/SKILL.md`
and its `references/hidden-context-checks.md`, `api-event-architect/SKILL.md`
and `llm-output-safety-reviewer/SKILL.md`; and the step-0 reconciliation
record. The named follow-up is one independent full-page re-read of each
pending page against [Acceptance for each page](#acceptance-for-each-page). No
grant or gate changed.

PRs #420 (`dfb0cac`), #421 (`4b205a7`), #423 (`6561944`), #425 (`7b88841`),
#422 (`5d91fa5`), #427 (`0030e73`), #431 (`dfbcf0f`), #429 (`169e8be`), #432
(`7894567`), #426 (`a06f815`), #428 (`0cb0777`), #433 (`9104cff`), #424
(`5711ddf`), #436 (`862dd90`), #430 (`6712ebb`), #435 (`a96b902`), #437
(`96cf65a`), #434 (`b7dc060`) and #439 (`d2d9b05`) merged on 2026-09-27 UTC
after #416, in that order. #427 added
`.claude/skills/prompt-injection-defender/references/multimodal-injection-patterns.md`
and #433 added the
[live startup-routing acceptance record](../evidence/startup-routing/2026-09-live-acceptance.md);
no Markdown file was removed or renamed. #429 changed audit scripts and tests
only. The three `artifacts/audits/` JSON baselines regenerated in #432 and the
evaluation JSON changed in #424, #427, #428 and #435 are not Markdown and are
not counted; no synthetic fixture changed. The verdicts below are the
independent review comments posted on each PR, and every page accepted below is
identical on main to the head its reviewer accepted. Line counts are
`git diff --numstat` from each merge's first parent, added together since the
page's last full-page acceptance.

- **Accepted after full-page reviews (14 pages).** #422:
  `.claude/skills/agent-tool-safety-guard/SKILL.md`,
  `hidden-context-exposure-reviewer/SKILL.md` and its
  `references/hidden-context-checks.md`, accepted on `379c588`. #427:
  `prompt-injection-defender/SKILL.md` and the new
  `references/multimodal-injection-patterns.md`, accepted on `633304b`. #426:
  this ledger, accepted on `6fb5811`. #428:
  `supply-chain-security-reviewer/SKILL.md`, accepted on `3787f74`, and its
  `references/supply-chain-checklist.md`, accepted on `9c9a669` and unchanged
  after. #424: `llm-output-safety-reviewer/SKILL.md` and its
  `references/output-sink-catalog.md`, accepted on `af328b5`. #430: the
  [README](../../README.md), accepted on `b6b4b4e`; the reviewer's check of
  `102dd7b` pre-cleared acceptance if the next diff held exactly two named
  one-line edits, and `git diff 102dd7b b6b4b4e` is exactly those edits. #434:
  `file-upload-storage-architect/SKILL.md` (18 lines with #385), accepted on
  `3c44f4a`, and `agent-tool-safety-guard/references/tool-permission-matrix.md`
  (20 with #405), accepted on `356932a`. #439: the step-0 reconciliation
  record, accepted on `97c8682`, after #423 had added its 27-line D67 entry.
- **Keep acceptance under the targeted-edit rule (7 pages).** The README (2
  since #430, from #437), `code-reviewer/SKILL.md` (10: 6 in #394 and #419, 4
  in #424), `prompt-injection-defender/references/injection-defense-patterns.md`
  (6: 3 in #405, 3 in #427), `project-orchestrator/SKILL.md` (#435, 1), the
  [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md)
  (#436, 2), [CONTRIBUTING](../../CONTRIBUTING.md) (#421, 7) and the
  [Behavioral Eval Runner guide](../../tools/behavioral_eval_runner/README.md)
  (#425, 7). #420, #421 and #423 had no posted review verdict. A targeted
  read-only review on `7b3fbca`, requested on 2026-09-28, passed
  `CONTRIBUTING.md` (#421, 7 lines, its only change since its #238 full-page
  acceptance), so it keeps acceptance. #423's README row (2 lines) and step-0
  log entry (27 lines) are covered by the later full-page acceptances in #430
  (`b6b4b4e`) and #439 (`97c8682`), not by this rule. #435's reviewer noted that
  53 earlier lines on `project-orchestrator/SKILL.md` (#248, #261 and #384)
  predate the rule. This ledger did not then count pre-rule edits; the owner
  decided on 2026-09-28 that they do count (see the update after #442 below).
- **Newly pending (8 pages).** Their reviews checked the changed passages, not
  the whole page: the [approval register](../approvals/APPROVAL_REGISTER.md)
  (76: 36 in #420, 40 in #432), the
  [open-decisions index](aegis-open-decisions-2026-09-23.md) (35: 26 in #420,
  9 in #431), `.github/pull_request_template.md` (#421, 12), the
  [skills catalog](../skills-catalog.md) (15 since #413: 2 each in #423, #427
  and #424, 9 in #428), `ai-threat-modeler/references/llm-top10-threat-catalog.md`
  (18 since #415: 7 in #427, 7 in #428, 4 in #424),
  `model-poisoning-reviewer/references/poisoning-controls.md` (16: 10 in #405,
  6 in #428), the [AEGIS-060+ register](../audits/aegis-060-plus-register.md)
  (29 since #416: 24 in #432, 5 in #436) and the
  [skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md)
  (#432, 253). #432 regenerated that report with the audit script; this ledger
  has no separate class for generated reports, so it is counted as a reader
  page, and #432's review reproduced its content but was not a full-page
  readability review.
- **New and pending:** the live startup-routing acceptance record (#433, 283
  lines). Its review and re-review (SHIP on `339ac90`, which matches main)
  checked the evidence and grant scope but gave no full-page verdict against
  [Acceptance for each page](#acceptance-for-each-page).
- **Still pending:** `.claude/skills/api-event-architect/SKILL.md` (12),
  unchanged since #417.

Main after #439 (`d2d9b05`) therefore has **612 tracked Markdown files: 558
accepted reader pages, 44 classified synthetic fixtures and ten known pending
pages**. The pending pages are the approval register, the open-decisions
index, `.github/pull_request_template.md`, the skills catalog, the AEGIS-060+
register, the skill-contract audit baseline report, the live startup-routing
acceptance record, and in `.claude/skills/`, `api-event-architect/SKILL.md`,
`ai-threat-modeler/references/llm-top10-threat-catalog.md` and
`model-poisoning-reviewer/references/poisoning-controls.md`. The named
follow-up is one independent full-page re-read of each pending page against
[Acceptance for each page](#acceptance-for-each-page). A follow-up ledger
update will record PR #438 (approval-register lifecycle events), which merged after #439 as `5dbf7bc`, and the
upcoming audit-baseline re-run. No grant or gate changed.

PRs #438 (`5dbf7bc`), #440 (`adf54d9`) and #441 (`3c51fb2`) merged on
2026-09-27 UTC after #439, and #442 (`7b3fbca`) merged at 00:04 UTC on
2026-09-28, in that order. #442 added the
[session checkpoint page](session-checkpoint-2026-09-27.md); no Markdown file
was removed or renamed. The three `artifacts/audits/` JSON baselines
regenerated in #441 are not Markdown and are not counted; no synthetic fixture
changed. Line counts are `git diff --numstat` from each merge's first parent,
added together since the page's last full-page acceptance, as above. The
owner made three decisions on 2026-09-28, in chat with the coordinating
agent: edits merged before the 10-line rule count toward it, a small edit
keeps acceptance only if it was reviewed, and generated reports are their own
class (see [Remaining-page review in larger
batches](#remaining-page-review-in-larger-batches)).

- **Accepted after full-page reviews (2 pages).** #440: this ledger (101
  lines since #426). Its review on `4891b66` returned FIX-FIRST for one named
  edit and pre-cleared acceptance if the next diff was exactly that edit;
  `git diff 4891b66 f9e5325` is that one-line edit, so the ledger is
  **accepted** on `f9e5325`, which matches it on main before this update.
  #442: the new [session checkpoint page](session-checkpoint-2026-09-27.md)
  (141 lines), **accepted** after a full-page read on `63387ef`, which
  matches main.
- **Still pending, with more changed lines (3 pages).** The
  [approval register](../approvals/APPROVAL_REGISTER.md) (268: 76 before, 171
  in #438, 21 in #442), the
  [open-decisions index](aegis-open-decisions-2026-09-23.md) (68: 35 before,
  30 in #438, 3 in #442) and the
  [AEGIS-060+ register](../audits/aegis-060-plus-register.md) (44: 29 before,
  15 in #441). #441's SHIP review checked the register note, but was not a
  full-page readability review.
- **Moved to the generated-report class (1 page).** The
  [skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md)
  leaves the pending set. #441's SHIP review reproduced it from the script
  with engine v1.13.2, which is the check this class needs after each
  regeneration; the reproduced file differed only in the hand-written preface
  and the branch name, and that review read the preface and found it accurate. Its status is **generated report, format review pending**
  until an independent review of the script's output format is recorded.
- **Newly pending under the first 2026-09-28 decision (1 page).**
  `.claude/skills/project-orchestrator/SKILL.md` has 50 changed lines since
  its last recorded acceptance in commit `181de4e` (the batch after #223): 14
  in #248, 18 in #261, 17 in #384 and 1 in #435. #435's reviewer counted 53
  before #435 because it added #384's two commits separately. The page is
  **pending** until an independent full-page re-read. This update applies the
  decision only to this page, which #435's reviewer named. Other accepted
  pages also had pre-rule edits since their last full-page acceptance: for
  example, `tenant-modeler/SKILL.md`, accepted in the batch after #229, then
  gained 16 lines in #261, 2 in #395 and 4 in #417 (22). A sweep of every
  accepted page for pre-rule edits is a named follow-up, and the counts below
  hold only until it is done.
- **Keeps acceptance after a targeted review under the second 2026-09-28
  decision (1 page).** #420, #421 and #423 had no posted review verdict. A
  targeted read-only review on `7b3fbca` passed
  [CONTRIBUTING](../../CONTRIBUTING.md) (#421, 7 lines, its only change since
  its #238 full-page acceptance), so it keeps acceptance. The other pages
  those PRs changed were already pending or were later accepted after a
  full-page review (the README in #430, the step-0 log in #439).
- **Still pending, unchanged (6 pages).** `.github/pull_request_template.md`,
  the [skills catalog](../skills-catalog.md), the
  [live startup-routing acceptance record](../evidence/startup-routing/2026-09-live-acceptance.md),
  and in `.claude/skills/`, `api-event-architect/SKILL.md`,
  `ai-threat-modeler/references/llm-top10-threat-catalog.md` and
  `model-poisoning-reviewer/references/poisoning-controls.md`.

Main after #442 (`7b3fbca`) therefore has **613 tracked Markdown files: 558
accepted reader pages, one generated report, 44 classified synthetic fixtures
and ten known pending pages**. The 613 is `git ls-files '*.md'` on a checkout
of `7b3fbca`. Accepted readers go 558 − 1 (the orchestrator) + 1 (the
checkpoint page) = 558, and pending goes 10 + 1 (the orchestrator) − 1 (the
report) = 10. The pending pages are the approval register, the
open-decisions index, `.github/pull_request_template.md`, the skills catalog,
the AEGIS-060+ register, the live startup-routing acceptance record, and in
`.claude/skills/`, `project-orchestrator/SKILL.md`,
`api-event-architect/SKILL.md`,
`ai-threat-modeler/references/llm-top10-threat-catalog.md` and
`model-poisoning-reviewer/references/poisoning-controls.md`. This update
changes this ledger by more than 10 lines, so it needs its own independent
full-page re-read. The named follow-up is one independent full-page re-read
of each pending page against
[Acceptance for each page](#acceptance-for-each-page), and one review of the
audit report's output format, and the pre-rule sweep named above, which is
expected to move more accepted pages to pending. No grant or gate changed.

PRs #450 (`bb3b117`, 08:55 UTC), #445 (`8c52960`), #446 (`7005cda`), #447
(`484d104`), #448 (`2bcbfe6`), #449 (`bb7ed71`), #451 (`0d4b093`) (all
09:03 UTC), #443 (`e251c51`, 09:07 UTC), #452 (`419ad23`, 09:11 UTC) and
#454 (`5bd21fb`, 09:17 UTC) merged on 2026-09-28 after #442, in that order.
No Markdown file was added, removed or renamed. #443 changed only
`.github/workflows/validate-skills.yml` (4 lines), which is not Markdown and
is not counted; no synthetic fixture changed. Line counts are
`git diff --numstat` from each merge's first parent, added plus deleted, as
above. Each review below is posted on its PR, and each accepted head matches
the page on main after #454: `git diff <head> 5bd21fb` is empty for that page,
except the approval register, explained below, and the orchestrator page,
which differs from its accepted head `469d6cb` only by the 8 lines #454
reviewed and matches #454's head `6118210`. Codex posted only usage-limit
notices on these PRs, so no Codex review exists for any of these heads.

- **Accepted after full-page reviews (9 pages, all pending before).**
  - #445 (`api-event-architect/SKILL.md` 8,
    `ai-threat-modeler/references/llm-top10-threat-catalog.md` 12 and
    `model-poisoning-reviewer/references/poisoning-controls.md` 10, all in
    `.claude/skills/`): a full-page review of each page on `c5571a7` accepted
    the first two and asked for one edit to the third. A corrected-candidate
    re-read confirmed that edit and **accepted** all three on `07d002a`.
  - #447: the [open-decisions index](aegis-open-decisions-2026-09-23.md) (55)
    and `.github/pull_request_template.md` (8). A full-page read of both on
    `7fc2fd6` accepted the template and returned FIX-FIRST on the index with
    four named edits (E1–E4). A corrected-candidate check found exactly those
    edits and **accepted** both on `420f823`.
  - #449: the [AEGIS-060+ register](../audits/aegis-060-plus-register.md) (30)
    and the
    [live startup-routing acceptance record](../evidence/startup-routing/2026-09-live-acceptance.md)
    (11). A review of each page against
    [Acceptance for each page](#acceptance-for-each-page) on `5037d6a`
    accepted the record and returned FIX-FIRST on the register with two
    edits. A re-review found exactly those edits and **accepted** the
    register on `04af9d9`; the record did not change after `5037d6a`.
  - #451: the [skills catalog](../skills-catalog.md) (90). A full-page review
    on `39a86e2` returned FIX-FIRST with four edits. A corrected-candidate
    re-read, which scanned all 1,442 lines again, **accepted** it on
    `2e15b23`.
  - #452 and #454: `.claude/skills/project-orchestrator/SKILL.md`. #452 (40)
    glossed abbreviations; a full-page review on `90849c1` returned FIX-FIRST
    with two edits, and a re-review **accepted** the page on `469d6cb`. #454
    then added the Stage 6 manual-only markers (8: 4 added, 4 deleted). Its
    SHIP review on `6118210` checked those lines and confirmed the page was
    unchanged since `469d6cb`; the reviewer counted 4, but this ledger counts
    added plus deleted, so 8. That is a reviewed edit under 10 lines, so the
    page **keeps acceptance**, with 8 lines since `469d6cb`.
- **Accepted again (1 page, already counted as accepted).** #446: this ledger
  (121 since `f9e5325`). A full-page re-read on `7a5b534` returned FIX-FIRST
  and pre-cleared acceptance for exactly its edits F1a, F1b, F2a and F2b;
  `git diff 7a5b534 47c78cb` is exactly those, so the ledger is **accepted**
  on `47c78cb`. The same PR carries the targeted review that kept
  [CONTRIBUTING](../../CONTRIBUTING.md) accepted.
- **Generated report, preface reviewed (1 page, class unchanged).** #449 also
  changed the hand-written preface of the
  [skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md)
  (12). As the [generated-report rule](#remaining-page-review-in-larger-batches)
  requires for hand-written text, the review on `5037d6a` read that preface
  and accepted it. It also found the body byte-identical to main and
  reproduced it from the generator. The page stays a **generated report,
  format review pending**. The reviewer named two generator follow-ups: the
  fixed "BEFORE remediation" text that the preface has to contradict, and
  unexplained codes (P0/P1, CENSUS, §5, SEMANTIC-REVIEW CANDIDATE). Both are
  fixes for the generator's template, not the file.
- **Still pending, with new lines (1 page).** The
  [approval register](../approvals/APPROVAL_REGISTER.md). #448 added a
  reading aid (81). A full-page review of the whole register (1,763 lines)
  on `3b9d74e` returned FIX-FIRST with three edits, and corrected-candidate
  re-reads accepted `b04872c` and `2ee1050`. That full-page read covers the
  268 lines counted before. But #450 (92, the AEGIS-APR-067 to APR-070
  lifecycle events, which grant nothing) merged first, and `2ee1050` does not
  contain it: `git diff 2ee1050 5bd21fb` on the register is exactly #450's 92
  added lines. #450's SHIP review on `de428bf` checked each event's facts and
  format, and the re-read on `2ee1050` confirmed that the reading aid's terms
  cover the four events. Neither was a full-page readability read of the
  merged page, and 92 is past 10, so the register stays **pending**, with 92
  lines since its full-page acceptance.

Main after #454 (`5bd21fb`) therefore has **613 tracked Markdown files: 567
accepted reader pages, one generated report, 44 classified synthetic fixtures
and one known pending page**. The 613 is `git ls-files '*.md'` on a checkout
of `5bd21fb`, unchanged since #442. Accepted readers go 558 + 9 = 567, and
pending goes 10 − 9 = 1; 567 + 1 + 44 + 1 = 613. The pending page is the
approval register. This update changes this ledger by more than 10 lines, so
it needs its own independent full-page re-read. The sweep of every accepted
page for pre-rule edits, which the owner ordered on 2026-09-28, is in
progress separately; its results come in a later ledger update and are
expected to move accepted pages to pending, so these counts hold only until
then. PRs merged after #454, such as #453 (AEGIS-APR-071 to APR-073 in the
approval register) and #455 (D15 enrichment deltas to four shipped skills),
are not counted here; a later ledger update records them. No grant or gate
changed.

PRs #453 (`4226d29`, 09:22 UTC), #455 (`c789f58`, 09:27), #456 (`072a1b0`,
09:29), #459 (`da43362`, 09:32), #461 (`dc3c767`, 09:36), #462 (`ad5c053`),
#458 (`ec8cf3e`) and #463 (`2f61f97`) (09:37 to 09:38), #464 (`c857e56`,
09:39), #460 (`61763d8`) and #457 (`4920686`) (both 09:44), #465 (`5bff21d`,
09:50), #466 (`adea71e`), #467 (`164bea8`), #468 (`45b6118`), #469
(`29435b3`), #471 (`4b44840`), #472 (`f31d665`) and #473 (`0847087`) (all
15:00 UTC), and #470 (`d9bc774`) and #474 (`2be0a77`) (both 15:09 UTC) merged
on 2026-09-28 after #454, in that order. No Markdown file was added, removed
or renamed. The evaluation JSON files in #455 and the audit script, its test
and two JSON baselines in #461 are not Markdown and are not counted; no
synthetic fixture changed. Line counts are `git diff --numstat` from each
merge's first parent, added plus deleted, as above. Each review cited below is
posted on its PR unless this update says otherwise, and for every page counted
as accepted, `git diff <accepted head> 2be0a77` on that page is empty. Codex
posted only usage-limit notices on these PRs, so no Codex review exists for
any of these heads.

**The pre-rule sweep.** The sweep the owner ordered on 2026-09-28 took the 558
pages this ledger counted as accepted after #442 and, for each, added up every
edit since its last full-page acceptance, including edits made before the
2026-09-27 rule. On main after #454 (`5bd21fb`) it kept **455** pages and
returned **103** to pending: 84 `SKILL.md` pages, 5 skill references or
assets, 5 roadmap pages, 4 evidence pages and 5 others. The nine pages
accepted in #445 to #452 had just had full-page reviews and were outside its
scope. Independent reviewers then re-read the 103 pages in full: five in
separate PRs, and 98 in nine batches read on `072a1b0` or `da43362`. The
per-page inventory is a working file of the
coordinating session, not a repository page, so this update records the
results page by page. `SKILL.md` pages are named by their skill directory
under `.claude/skills/`.

- **Accepted again after full-page re-reads (102 of the 103).**
  - Re-read and fixed on their own before the batches: #456,
    `tenant-modeler` (13) and `source-of-truth-reconciler` (10), **accepted**
    on `620b245`; #459, `ai-cost-guardrail-designer` (10) and
    `streaming-event-architect` (11), **accepted** on `378089f`; and #462,
    `ai-closeout-reporter` (see the D15 item below).
  - Fixed in the nine batch PRs (83 pages). In each, a corrected-candidate
    reviewer rebuilt the head by applying the batch's required edits to the
    merge base, found it byte-identical, and re-read each changed page in full
    at the head. Each posted **ACCEPT** for every changed page on the head
    that merged. Batch 1, #466 on `dac42f3`: the
    [Behavioral Eval Runner design](../design/behavioral-eval-runner-v1.md)
    and the
    [routing request-binding review](../evidence/setup/issue-101-routing-request-binding-review.md).
    Batch 2, #471 on `67f577e`: the
    [resumable control-plane backlog](resumable-control-plane-backlog.md),
    `agent-authorization-matrix`, `roadmap-under-uncertainty-planner`,
    `statement-of-applicability-author`, `sunset-deprecation-communicator`,
    `synthetic-monitoring-architect` and `tech-spec-writer`. Batch 3, #473 on
    `8c6750a`: the
    [CP-WP-003 authority packet](cp-wp-003-real-authority-decision-packet.md),
    `authority-invalidation-architect`, `design-review-facilitator`,
    `frontend-perf-engineer`, `integration-test-designer`,
    `operational-vs-analytical-splitter`, `performance-test-harness`,
    `product-analytics-instrumenter`, `product-spec-writer`,
    `saas-cost-architect` and `secrets-identity-hardener`. Batch 4, #467 on
    `eb3ec53`: `audit-log-architect`, `background-job-orchestration-architect`,
    `code-simplifier`, `pii-lifecycle-designer`, `plan-entitlement-architect`,
    `playwright-e2e-engineer`, `soc2-trust-criteria-mapper`,
    `superadmin-observability-console-designer` and `vite-build-qa-engineer`.
    Batch 5, #474 on `14ecd0c`: the [setup route](aegis-setup-routing-plan.md),
    the
    [BER-BKL-009 static source inventory](../evidence/ber-bkl-009-static-source-inventory.md),
    `ai-lifecycle-risk-manager`, `appsec-implementer`, `aws-saas-architect`,
    `docs-first-implementer`, `flaky-test-detective`,
    `iso-27001-isms-architect`, `load-test-planner` and
    `mobile-viewport-craft`. Batch 6, #472 on `6ba6e1a`: the
    [host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md),
    the
    [BER-BKL-009 policy integration review](../evidence/ber-bkl-009-policy-integration-review.md),
    the [host bridge guide](../../tools/aegis_setup/host_bridge/README.md),
    `aegis-setup/references/state-contract.md`, `agentic-loop-designer`,
    `azure-saas-architect`, `docs-as-code-architect`,
    `intra-tenant-scope-architect`, `latency-budget-architect`,
    `realtime-subscription-architect`, `roadmap-to-commitments-translator`,
    `screenshot-evidence-planner` and `share-link-access-architect`. Batch 7,
    #470 on `2a86058`: the
    [Stage 4B decision packet](aegis-setup-package-4b-host-proof-protocol.md),
    the [CP-WP-003 named-candidate matrix](cp-wp-003-named-candidate-matrix.md),
    `adr-sequencer`, `api-doc-generator-designer`,
    `caching-strategy-designer`, `eval-runner-designer`,
    `iso-42001-aims-architect`, `merge-is-deploy-governance`,
    `offline-first-sync-architect`, `query-plan-reader`,
    `regression-suite-curator`, `saas-platform-architect` and
    `schema-evolution-planner`. Batch 8, #469 on `61ca130`: the
    [setup tool guide](../../tools/aegis_setup/README.md),
    `feature-flag-rollout-strategist`, `model-context-designer`,
    `pagination-cursor-designer`, `qa-automation-architect` and
    `skill-usage-instrumenter`. Batch 9, #468 on `54034fa`:
    [AGENTS.md](../../AGENTS.md), `accessibility-test-harness`,
    `docs-retention-index`, `notification-webhook-ux-designer`,
    `profiling-methodology-designer`, `qa-strategy-architect`,
    `search-architecture-designer`, `skill-deprecation-planner`,
    `slo-reliability-architect`, `staff-scope-selector`, and
    `standing-approval-and-auto-advance` with its
    `references/standing-approval-policy.md`.
  - **Accepted on the first full-page read, with no edit (14 pages),** read
    on `072a1b0` or `da43362` and unchanged since: `architecture-designer`
    (batch 1); `requirements-gathering-facilitator` and
    `cell-based-architecture-designer` (batch 4);
    `warehouse-lake-architect` and `authorization-matrix-designer` (batch 5);
    `aegis-setup` (batch 6);
    `merge-is-deploy-governance/references/governance-doc-template.md`
    (batch 7); `ab-test-designer` with its `references/ab-test-sheet.md`,
    `architecture-advisor`, `data-migration-runbook-author`,
    `data-partitioning-sharding-strategist` and `prioritization-frame-picker`
    (batch 8); and `accessibility-test-harness/references/a11y-checklists.md`
    (batch 9). The full verdicts are in the reviewers' batch verdict records,
    which are working files, not PR comments. All 14 are also named as
    accepted on GitHub: `architecture-designer` in #466's description; the
    batch 4, 5, 6 and 9 pages in the corrected-candidate comments on #467,
    #474, #472 and #468; and, in comments posted after #474 merged, the six
    batch 8 pages on #469 and the governance template on #470, each read on
    `072a1b0`.
- **Still pending (1 of the 103).** The
  [Behavioral Eval Runner guide](../../tools/behavioral_eval_runner/README.md)
  (148 lines since its last full-page acceptance). Its batch 4 re-read
  returned FIX-FIRST with six edits, which were held back: the path is
  protected by the `gate-guard` check, so the edits need a separate owner
  exception. The page stays **pending**.
- **The D15 enrichment deltas (#455).** #455 applied decision D15 of the
  [step-0 reconciliation log](../reconciliation/step-0-reconciliation-v4.md)
  to eight reader pages in four skills. Its SHIP review on `16bb924` checked
  every changed line and listed the per-page counts.
  - **Accepted again after full-page re-reads (4 pages).**
    `ai-closeout-reporter/SKILL.md` (32, after 16 counted by the sweep) and
    its `assets/closeout-template.md` (25) got 6 and 3 lines of fixes in
    #462, and a corrected-candidate re-read of both in full **accepted** them
    on `e569a3c`. `ai-sdlc-operating-model/SKILL.md` (11) and its
    `references/stage-gate-map.md` (16, with a new section) got 15 and 22 in
    #463, and its reviewer re-read both in full and **accepted** them on
    `6306232`.
  - **Keep acceptance (3 pages).** `agent-memory-governance/SKILL.md` (8)
    and its `references/memory-rules.md` (8), and
    `adr-writer/assets/adr-template.md` (7: 2 in #236 and 5 in #455).
  - **Newly pending (1 page).** `adr-writer/SKILL.md` has 13 changed lines
    since its acceptance in the full-page batch after #234, merged as #236
    (`39361ba`): 2 in #396, 3 in #417 and 8 in #455. #455's reviewer counted 8
    against main, but this ledger adds the edits since the last full-page acceptance, so the page is
    past 10 and **pending**.
- **Other pages.**
  - The [approval register](../approvals/APPROVAL_REGISTER.md) stays
    **pending**. #453 appended AEGIS-APR-071 to APR-073 (118; SHIP on
    `5be36b3`). #464 applied three reading-aid edits (18) from a full-page
    re-read of the register on `4226d29`, which already held #450's and
    #453's entries. That FIX-FIRST read is described in #464's description
    but was not posted as a review comment; the posted corrected-candidate
    review **accepted** the edits on `e6d0f6a` and re-read the reading-aid
    section and AEGIS-APR-070 in context. Even counting `e6d0f6a` as a
    full-page acceptance, #465 then appended AEGIS-APR-074 to APR-076 (78;
    SHIP on `ab430ad`, which checked facts and format, not the whole page),
    and `git diff e6d0f6a 2be0a77` on the register is exactly those 78 added
    lines. That is past 10, so the page stays pending.
  - The [open-decisions index](aegis-open-decisions-2026-09-23.md) (#460,
    27): a full-page re-read on `36be74b` returned FIX-FIRST, two targeted
    checks followed on `4f474ae` and `a4ac928`, and a one-line check
    **accepted** it on `08f99eb`, which matches main.
  - The [backlog forecast](aegis-backlog-forecast.md) (238) and
    [execution measurements](aegis-execution-metrics.md) (285), #457: a
    full-page review on `86d891e` returned FIX-FIRST with edits F1 to F7 and
    M1 to M3; a corrected-candidate check **accepted** both on `676bc3d`,
    which matches main.
  - This ledger (#458, 109): **accepted** on `9cdfdf8`, which is exactly the
    three edits pre-cleared by the full-page re-read on `5978b33`.
  - The [AEGIS-060+ register](../audits/aegis-060-plus-register.md) (#461,
    10, a dated paragraph with no new heading): #461's SHIP review on
    `ae719e6` listed the paragraph within AEGIS-APR-073's allowed files and
    verified each fact it states: the same frozen commit `5dbf7bc`, 316
    findings, identical rule inventory, vocabulary census and corpus hash, and
    `3c51fb2` as #441's merge. With 10 lines since `04af9d9`, at the limit and
    reviewed, it **keeps acceptance**.
  - The
    [skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md)
    (#461, 76) is a generated report. #461's SHIP review reproduced its body
    byte for byte from engine v1.13.3 on the frozen commit, read the
    hand-written preface and found its history correct. The review also
    checked the new "How to read this report" key and named three small
    format follow-ups. This ledger does not treat that as the one-time review
    of the output format, so the page stays a **generated report, format
    review pending**.
  - `project-orchestrator/SKILL.md` did not change after #454 and **keeps
    acceptance** (8 since `469d6cb`). #463's reviewer noted that its Stage 6
    says the stage-gate map names `local-ci-mirror-preflight`, which the map
    does not; that is a named follow-up, not a readability failure.
- **Open items from the sweep.** Two accepted pages rest on a weak record:
  the [BER selected host capability decision](ber-selected-host-capability-decision.md)
  counts as accepted only if #264's "decision routes" review covered it
  (otherwise 145 lines since #210), and the
  [VirtualBox Stage A setup proposal](ber-virtualbox-stage-a-setup-proposal.md)
  only if it is #264's "host proposal" (otherwise 57 since it was added in
  #260). A check of #264's review would settle both. Also, 51 pages the sweep
  kept had 1 to 10 changed lines (274 in all), and the sweep did not check
  whether each edit was reviewed; under the second 2026-09-28 refinement an
  unreviewed edit needs a targeted review. `adr-writer/SKILL.md` was one of
  them and is now pending by count. The other 50 stay counted as accepted
  until that check.

Main after #474 (`2be0a77`) therefore has **613 tracked Markdown files: 565
accepted reader pages, one generated report, 44 classified synthetic fixtures
and three known pending pages**. The 613 is `git ls-files '*.md'` on a
checkout of `2be0a77`, unchanged since #442. Accepted readers go 567 − 103
(sweep) + 102 (accepted again) − 1 (`adr-writer/SKILL.md`) = 565. The three
D15 pages that went past 10 and were accepted again within this range change
neither count. Pending goes 1 + 103 − 102 + 1 = 3, and 565 + 3 + 1 + 44 = 613.
The pending pages are the approval register, the Behavioral Eval Runner guide
and `.claude/skills/adr-writer/SKILL.md`. This update changes this ledger by
more than 10 lines, so it needs its own independent full-page re-read. No
grant or gate changed.

PRs #475 (`59b2fb7`) and #476 (`8f3d369`) (both 15:31 UTC), #480
(`19d26a9`), #478 (`3ac0c2f`), #477 (`6d2b2f6`) and #481 (`6567fba`) (all
16:21), #479 (`5d0fa76`, 16:28), #482 (`7c8dbf6`, 16:29), #483 (`ecd1e59`,
16:30), #484 (`eb92948`, 16:42), #487 (`5792955`) and #485 (`149d5ac`) (both
16:52), #486 (`2a411fd`, 17:08) and #488 (`ebf210c`, 17:23 UTC) merged on
2026-09-28 after #474, in that order. #477 was the previous ledger update.
#485 added one Markdown file, the
[2026-09-28 session checkpoint](session-checkpoint-2026-09-28.md);
no file was removed or renamed, and no non-Markdown file or synthetic fixture
changed. Line counts are `git diff --numstat`, added plus deleted. Each
accepting review cited below is posted on its PR. Three first re-reads that
only asked for edits were not posted: the register's R1 and R2, the host
pages' C1 to V7 and `ai-evaluation-harness`'s E1 to E5. The accepting
comments cite them. For every page counted as accepted,
`git diff <accepted head> ebf210c` on that page is empty or holds only lines
from another reviewed PR in this range, and stays within the rule. Codex
posted only usage-limit notices on these PRs, so no Codex review exists for
any of these heads.

**Two owner decisions (2026-09-28).**

- **Net difference.** The 10-line rule counts the net difference since the
  page's accepted version, `git diff --numstat <acceptance> <now>`, not the
  sum of every edit; the [rule section](#remaining-page-review-in-larger-batches)
  now says so. Under the old summed count, #486's first review found four
  more pages past 10 besides `ai-evaluation-harness`:
  `code-reviewer/SKILL.md` (14),
  `skill-quality-reviewer/SKILL.md` (14),
  `ai-cost-guardrail-designer/references/cost-guardrail-patterns.md` (13) and
  `iso-42001-aims-architect/references/aims-clause-map.md` (13). Their net
  counts are 8, 8, 7 and 7, so they keep acceptance.
- **"Spell it out everywhere".** "AI" is spelled out as artificial
  intelligence (AI) at its first body use on every page. #486 delivered this
  on 64 pages, one line each (128). Its review returned FIX-FIRST on
  `8459ac7` for one missed line in the
  [add-AI-safely path](../paths/add-ai-safely.md), then **ACCEPT** on
  `2f28cc7`. This update checked the net count of all 64 pages since each
  page's acceptance. Only `.claude/skills/ai-evaluation-harness/SKILL.md`
  went past 10: 10 from #370 since its acceptance at `80fbdbb` (#210), plus
  2, so 12; #488 fixed it (below). Every other page is at 10 or fewer. The
  highest are the
  [efficient execution handoff](aegis-efficient-execution-handoff-2026-09-23.md)
  at exactly 10, and four pages at 8:
  `ai-governance-risk-reviewer/references/ai-governance-framework.md`,
  `sensitive-disclosure-guard/SKILL.md`, `code-reviewer/SKILL.md` and
  `skill-quality-reviewer/SKILL.md`. The forecast, the measurements page and
  this ledger are at 2 since their acceptances below.

**Pages accepted in this range.**

- The [Behavioral Eval Runner guide](../../tools/behavioral_eval_runner/README.md)
  (#475, 17): the six batch 4 edits, held back until the owner granted a
  one-time `gate-guard` exception for head `acdcdad` only (AEGIS-APR-077; its
  consumption is AEGIS-APR-078, both recorded by #479). A corrected-candidate
  reviewer rebuilt the head from the batch 4 re-read, re-read the page in
  full and posted **ACCEPT** on `acdcdad`. Pending to accepted.
- The [approval register](../approvals/APPROVAL_REGISTER.md). A full-page
  re-read of the register on main `8f3d369` found two reading-aid edits, R1
  and R2, which #481 applied (7); the corrected-candidate check **accepted**
  the register on `98eb638`, resting on that read. #479 then appended
  AEGIS-APR-077 and APR-078 (51; REVISE on `21cc486`, SHIP on `b7570af`).
  That is 51 net since `98eb638`, past 10, so a separate full-page re-read of
  the whole register on `2a411fd` returned **ACCEPT** with no edit
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/479#issuecomment-5874887988)).
  Pending to accepted.
- `.claude/skills/adr-writer/SKILL.md` (#482, 20): three edits, R1 to R3,
  and a full-page re-read at the head, **ACCEPT** on `f275356`. Pending to
  accepted.
- The [BER selected host capability decision](ber-selected-host-capability-decision.md)
  (49) and the
  [VirtualBox Stage A setup proposal](ber-virtualbox-stage-a-setup-proposal.md)
  (39), #476: a first full-page re-read asked for 14 edits (C1 to C7 and V1
  to V7), and a corrected-candidate full-page re-read **accepted** both on
  `5f08b3e`. This settles the sweep's open item on their weak acceptance
  record. Both were already counted as accepted.
- `.claude/skills/project-orchestrator/SKILL.md` (#484, 14; 20 net since
  `469d6cb`): a full-page re-read on `2f5858c` returned FIX-FIRST with two
  edits, and the corrected-candidate review **accepted** it on `ad927f7`.
  `ai-sdlc-operating-model/references/stage-gate-map.md` (6 net since
  `6306232`): its changed rows, read in context, were **accepted** on
  `ad927f7`. Both were already counted as accepted.
- The [backlog forecast](aegis-backlog-forecast.md) (172) and
  [execution measurements](aegis-execution-metrics.md) (128), #478: a
  full-page review on `07435c2` returned FIX-FIRST (F1 to F6, M1 and M2), and
  the re-review **accepted** both on `cf86dab`.
- This ledger (#477, 243): a full-page read on `4384548` returned FIX-FIRST
  (E1 to E3), and the corrected-candidate check **accepted** it on `66521f4`.
- `.claude/skills/ai-evaluation-harness/SKILL.md` (#488, 14): a full-page
  re-read on `2a411fd` asked for five edits, E1 to E5, which #488 applied with
  one optional edit; a corrected-candidate full-page review **accepted** it
  on `e225c2f`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/488#issuecomment-5875073652)).
  Pending to accepted.
- The [2026-09-28 session checkpoint](session-checkpoint-2026-09-28.md)
  (#485, new, 177): a full-page review on `7d33df0` returned FIX-FIRST with
  four edits; a fix check on `692b221` asked for one more two-line fix, and
  the fix check on `04d2ce8` **accepted** it. New accepted page.

**Small edits.**

- All 51 pages the sweep kept with 1 to 10 changed lines now have a recorded
  review. Three read-only targeted reviews on `2be0a77` found that 4 pages
  already had an independent verdict on the PR that changed them, 35 passed
  a targeted review, 11 needed FIX-FIRST edits and `adr-writer/SKILL.md` had
  gone past 10 (above). Those reviews are working files of the coordinating
  session, not repository pages. #480 applied ten of the FIX-FIRST edits and
  one optional edit to 11 pages (46); its independent review passed all 11 on
  `9c918ed`, each at 10 or fewer net since acceptance, with
  `ai-governance-risk-reviewer/SKILL.md` exactly at 10. The eleventh
  FIX-FIRST edit, to `code-reviewer`'s description, waited for the owner and
  merged in #482 (2), whose reviewer passed it on `f275356`. The 50 pages
  other than `adr-writer/SKILL.md` keep acceptance.
- #483 (12): one line each on `skill-quality-reviewer/SKILL.md`,
  `frontend-perf-engineer/SKILL.md`, `library-diff-reviewer/SKILL.md`,
  `slo-reliability-architect/SKILL.md`, the README and the skills catalog.
  Its review passed all six on `44c4834`, each at 10 or fewer net, so they
  keep acceptance.
- The [open-decisions index](aegis-open-decisions-2026-09-23.md) (#487, 10):
  exactly 10 net since its acceptance on `08f99eb` (#460). A targeted review
  **accepted** it on `44550cd`, so it keeps acceptance at the limit; any
  further edit needs a full-page re-read.

**Still open.** No reader page is pending. The
[skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md)
stays a **generated report, format review pending**: its one-time review of
the output format has still not been done.

Main after #488 (`ebf210c`) therefore has **614 tracked Markdown files: 569
accepted reader pages, one generated report, 44 classified synthetic fixtures
and zero known pending pages**. The 614 is `git ls-files '*.md'` on a
checkout of `ebf210c`: 613 + 1 (#485's checkpoint). Accepted readers go
565 + 3 (the Behavioral Eval Runner guide, the approval register and
`adr-writer/SKILL.md`) + 1 (the new checkpoint) − 1 (#486 took
`ai-evaluation-harness/SKILL.md` past 10) + 1 (#488 accepted it again) = 569.
Pending goes 3 − 3 + 1 − 1 = 0, and 569 + 0 + 1 + 44 = 614. This update
changes this ledger by more than 10 lines, so it needs its own independent
full-page re-read. No grant or gate changed.

PRs #489 (`80d9dfe`, 17:47 UTC), #491 (`5f581a3`, 18:11), #492 (`e0f1d24`,
20:48), #501 (`c17a567`, 20:59), #493 (`0517700`, 21:51), #490 (`cc4da2c`),
#497 (`654ca2d`), #494 (`4ee2115`), #495 (`e77403c`), #506 (`862d07c`) and
#504 (`6fe634e`) (21:52 to 21:53), #503 (`c14338d`), #499 (`f0c4b24`) and
#496 (`76b399b`) (all 22:07), and #498 (`04fb8aa`), #500 (`53f3cf2`) and
#508 (`d932d2c`) (all 22:39 UTC) merged on 2026-09-28 after #488, in that
order. #490 was the previous ledger update. Eight Markdown files were added:
four skill batch proposals (#492, #494, #495 and #496);
`.claude/skills/acceptance-criteria-reviewer/SKILL.md` and its
`references/criteria-review-sheet.md` (#499); and
`.claude/skills/test-tenant-provisioner/SKILL.md` and its
`references/provisioning-manifest.md` (#500). No file was removed or renamed,
and no synthetic fixture changed. #504 and #506 changed no Markdown file.
Line counts are `git diff --numstat`, added plus deleted: per PR for what a
PR changed, and net since the page's last accepted head for the 10-line
rule. For every page counted as accepted, `git diff <accepted head> d932d2c`
on that page is empty or within the rule. Each accepting review cited below
is posted on its PR. Codex posted only usage-limit notices on these PRs, so
no Codex review exists for any of these heads.

**Pages accepted in this range.**

- The four new proposals, each read in full by an independent reviewer who
  returned FIX-FIRST on the first head and **ACCEPT** on the merged head:
  the quality assurance (QA)
  [Tier 1 skill batch proposal](qa-tier1-skill-batch-proposal.md) (#492,
  597) on `930493c`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/492#issuecomment-5876030965)),
  the [AI-SDLC skill batch proposal](ai-sdlc-skill-batch-proposal.md), for the
  AI-assisted software development lifecycle (SDLC) (#494, 554), on `a87e2c9`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/494#issuecomment-5878693792)),
  the [Phase 7 skill batch proposal](phase7-ai-engineering-skill-batch-proposal.md)
  (#495, 548) on `6d51c8d`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/495#issuecomment-5878705672))
  and the [Phase 6 reliability skill batch proposal](phase6-reliability-skill-batch-proposal.md)
  (#496, 687) on `d34cdb8`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/496#issuecomment-5879459919)).
  New accepted pages.
- The [open-decisions index](aegis-open-decisions-2026-09-23.md) (#493, 10;
  16 net since `08f99eb`, past 10): a full-page re-read on `123ee71` returned
  FIX-FIRST, and the corrected-candidate check **accepted** it on `b6e82e4`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/493#issuecomment-5878694452)).
  It was already counted as accepted.
- The [backlog forecast](aegis-backlog-forecast.md) (198) and
  [execution measurements](aegis-execution-metrics.md) (132), #497: a
  full-page review on `23a1a7c` returned FIX-FIRST (F1 to F4 and M1), and the
  corrected-candidate review **accepted** both on `826f40b`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/497#issuecomment-5878707340)).
- This ledger (#490, 160): a full-page re-read on `ed9ada2` returned
  FIX-FIRST (E1 and E2), and the corrected-candidate check **accepted** it on
  `49f4804`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/490#issuecomment-5877611911)).
- `.claude/skills/test-plan-designer/SKILL.md` (28) and its
  `references/test-plan-template.md` (39), #498, which folds the
  negative-path matrix into that skill: the first review re-read both pages
  in full on `7d4f611` and returned REVISE (S1 to S5, T1 to T8), a check on
  `4dade52` asked for R1 to R3, and the check on `e9cce7d` **accepted** both
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/498#issuecomment-5879535331)).
  A rebase check passed the merged head `2be5052`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/498#issuecomment-5879846892)),
  and `git diff e9cce7d d932d2c` on both pages is empty. Both were already
  counted as accepted.
- The [approval register](../approvals/APPROVAL_REGISTER.md). #491 appended
  AEGIS-APR-079 (74; REVISE on `a66a92e`, SHIP on `351f5de`,
  [comment](https://github.com/ModernNomad-98/Project-Aegis/pull/491#issuecomment-5875748510)).
  That review checked facts and format, not the whole page, and the register
  went to 74 net since `2a411fd`, so it became **pending**. A full-page
  re-read of the register as #491 left it then returned FIX-FIRST with
  edits E1 to E4. That read was not
  posted; #508's description records it and counts from `e6d0f6a`, an
  earlier baseline, which is also past 10. #508 applied E1 to E4 and appended
  AEGIS-APR-080 and APR-081 (72). Its independent review checked the edits
  and new entries and **accepted** the register on `3ccac33`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/508#issuecomment-5879934303)).
  Pending to accepted.

**Small edits that keep acceptance.**

- The [final 16 skill references review record](../evidence/documentation/skill-references-final-16-readability-2026-09-23.md)
  (#489, 2): one link repointed to the renamed hidden-context checks. It is 2
  net since its full-page acceptance in the batch merged as #221
  (`c0a3d1d`), and an independent review passed it on `10147d4`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/489#issuecomment-5875443230)).
- `.claude/skills/product-spec-writer/SKILL.md` (#499, 5): the reciprocal
  hand-off to `acceptance-criteria-reviewer`, 5 net since its acceptance on
  `8c6750a` (#473). #499's reviewer checked it in context on `0100c2e` (see
  the new skill pages below).
- `.claude/skills/test-data-architect/SKILL.md` (5 net since `f3afd19`) and
  `.claude/skills/multi-tenant-security-tester/SKILL.md` (9 net since
  `9ad83be`), #500: its reviewer measured both counts and passed both edits
  on `77319f8`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/500#issuecomment-5879444504)),
  and the rebase check carried that to the merged head `f812245`.

**Newly pending.**

- The [step-0 reconciliation log](../reconciliation/step-0-reconciliation-v4.md)
  (#493, 55: the entry for owner decision D68; #499, 6: two rows in decision
  D10's table and two Tier 1 cells; #498, 2: one Tier 1 cell; and, before
  this range, #486, 2: the "AI" spell-out): 65 net since
  its acceptance on `97c8682` (#439). The reviews checked those passages,
  but none re-read the whole log, so it is **pending**.
- The [skills catalog](../skills-catalog.md) (#499, 19; #500, 9): 28 net
  since `2e15b23` (#451). **Pending.**
- The [README](../../README.md) (#499, 7; #500, 5): 12 net since `b6b4b4e`
  (#430); it was 4 net before this range. #500's reviewer read its
  README and catalog rows for registration only. **Pending.**
- The [offline CI guide](../offline-ci.md) (#501, 14): 14 net since its
  acceptance in #365 (`2aed8dd`). #501's security review passed the diff on
  `9ca82d5`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/501#issuecomment-5878003536)),
  but the page is past 10, so it is **pending**.
- The [AEGIS-060+ register](../audits/aegis-060-plus-register.md) (#503, 12):
  the dated "Report key extended" note, required by #503's first review and
  checked on `52269aa`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/503#issuecomment-5878694559)).
  The register was already at 10 since `04af9d9`, so it is now 22 and
  **pending**.
- Four new skill pages. `.claude/skills/acceptance-criteria-reviewer/SKILL.md`
  (231) and its `references/criteria-review-sheet.md` (81), #499: REVISE on
  `89eec69`, then SHIP on `0100c2e`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/499#issuecomment-5879457154)).
  `.claude/skills/test-tenant-provisioner/SKILL.md` (280) and its
  `references/provisioning-manifest.md` (113), #500: REVISE on `4b31f1f`,
  SHIP on `77319f8` and a rebase check on `f812245`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/500#issuecomment-5879897041)).
  Both were skill-quality reviews that asked for readability fixes but gave
  no full-page verdict against
  [Acceptance for each page](#acceptance-for-each-page), so all four pages
  are **pending**, as the new skill pages in #383 and #409 were.

**Generated report.** The
[skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md)
(#503, 30) was regenerated by engine v1.13.4 under AEGIS-APR-079. The
one-time review of the output format, done on the v1.13.3 report, returned
FIX-FIRST; it was not posted, so APR-079 records its findings, and #503 put
every fix in the generator. #503's first review reproduced the report byte
for byte, read it in full on `9a1d841` and found every code the report prints
explained in its key, with no required edit to the report
([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/503#issuecomment-5878051730)).
The corrected-candidate check **accepted** `52269aa`, where the report is
unchanged. This ledger takes that as the completed format review: the report
stays a **generated report**, no longer "format review pending".

**Still open.** Nine reader pages are pending: the step-0 reconciliation
log, skills catalog, README, offline CI guide, AEGIS-060+ register and the
four new skill pages from #499 and #500.

Main after #508 (`d932d2c`) therefore has **622 tracked Markdown files: 568
accepted reader pages, one generated report, 44 classified synthetic fixtures
and nine known pending pages**. The 622 is `git ls-files '*.md'` on a
checkout of `d932d2c`: 614 + 4 (proposals) + 2 (#499) + 2 (#500). Accepted
readers go 569 + 4 (the new proposals) − 6 (the approval register,
reconciliation log, skills catalog, README, offline CI guide and AEGIS-060+
register) + 1 (#508 accepted the register again) = 568. Pending goes
0 + 6 + 4 (the new skill pages) − 1 = 9, and 568 + 9 + 1 + 44 = 622. This
update changes this ledger by more than 10 lines, so it needs its own
independent full-page re-read. No grant or gate changed.

PRs #502 (`d4bcef1`, 23:15 UTC), #510 (`722134f`) and #509 (`853c64f`)
(both 23:35), #511 (`ec5fd12`, 23:51) and #516 (`7300ef6`, 23:58) merged on
2026-09-28 after #508, and #520 (`3d5e004`, 00:11 UTC) and #515 (`2672b16`,
00:55 UTC) on 2026-09-29, in that order. Three Markdown files were added:
the [2026-09-28 evening session checkpoint](session-checkpoint-2026-09-28-evening.md)
(#509) and `.claude/skills/ci-failure-classifier/SKILL.md` with its
`references/classification-guide.md` (#502). No file was removed or renamed,
and no synthetic fixture changed. Counts and review links follow the rules
of the paragraph above, now against `2672b16`; Codex again posted only
usage-limit notices.

- **Accepted.** The evening checkpoint (#509, new, 182): FIX-FIRST on
  `9850f94`, then **ACCEPT** on `e46eba9`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/509#issuecomment-5880661059)).
  `ai-closeout-reporter/SKILL.md` (53) and its `assets/closeout-template.md`
  (24), #511: a full-page re-read on `81b4234` returned REVISE (A1 to A6,
  B1 to B4), and the corrected-candidate check **accepted** both on `cce2b45`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/511#issuecomment-5880897371)).
  The four new #499 and #500 skill pages, pending above, got readability
  fixes in #520 (15, 3, 24 and 10), and a corrected-candidate check
  **accepted** all four on `b0e149e`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/520#issuecomment-5881095898)).
  Pending to accepted. `code-reviewer/SKILL.md` (32) and its
  `references/severity-rubric.md` (25), #515: a full-page re-read on
  `1b4638f` returned REVISE, and the check on `67abe28` **accepted** both
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/515#issuecomment-5881126385)).
  For each of these pages, `git diff <accepted head> 2672b16` is empty.
- **Keep acceptance.** The [open-decisions index](aegis-open-decisions-2026-09-23.md)
  (#510, 7): 7 net since `b6e82e4`, and #510's corrected-candidate check
  kept it **accepted** on `beb3420`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/510#issuecomment-5880650124)).
  `local-ci-mirror-preflight/SKILL.md` and `systematic-debugger/SKILL.md`
  (#502, 5 each): neither changed between its full-page acceptance and #502,
  so each is 5 net, and #502's review checked both edits; its rebase check
  passed them unchanged on `288e9cd`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/502#issuecomment-5880413437)).
- **Newly pending.** `.claude/skills/ci-failure-classifier/SKILL.md` (259) and
  its `references/classification-guide.md` (82), new in #502: REVISE on
  `ef9b4fb`, SHIP on `08f5502` and a rebase SHIP on `288e9cd` were
  skill-quality reviews with no full-page verdict, so both are **pending**,
  as the #499 and #500 pages were. The
  [approval register](../approvals/APPROVAL_REGISTER.md) (#516, 91): its
  review **accepted** the appended AEGIS-APR-082 to APR-084 on `24423e6`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/516#issuecomment-5880915260))
  but checked facts and format, not the whole page. That is 91 net since
  `3ccac33`, so the register is **pending** again.
- **Still pending, with new counts.** The step-0 reconciliation log (#510,
  228: the D69 to D71 entries; #511, 2) is 295 net since `97c8682`. The
  skills catalog (#502, 13; #515, 2) is 37 net since `2e15b23`. The README
  (#502, 7) is 15 net since `b6b4b4e`. The offline CI guide and the
  AEGIS-060+ register did not change.

Main after #515 (`2672b16`) therefore has **625 tracked Markdown files: 572
accepted reader pages, one generated report, 44 classified synthetic fixtures
and eight known pending pages**. The 625 is `git ls-files '*.md'` on a
checkout of `2672b16`: 622 + 1 (#509's checkpoint) + 2 (#502). Accepted
readers go 568 + 1 (the checkpoint) + 4 (#520) − 1 (the approval register)
= 572. Pending goes 9 + 2 (#502) + 1 (the register) − 4 (#520) = 8: the
step-0 log, skills catalog, README, offline CI guide, AEGIS-060+ register,
approval register and the two `ci-failure-classifier` pages. 572 + 8 + 1 +
44 = 625. This update changes this ledger by more than 10 lines, so it needs
its own independent full-page re-read. No grant or gate changed.

PRs #513 (`a9be465`, 01:06 UTC), #512 (`12bc006`, 01:11), #519 (`fa608ec`,
01:22), #505 (`9f501f3`) and #517 (`8f859ab`) (both 01:36), #514
(`b471a1a`, 01:41), #523 (`019d441`, 02:03), #518 (`daf5445`, 02:27), #529
(`d423d53`, 02:30), #532 (`7bbd4f0`, 02:56), #527 (`3a9a1d1`, 03:09), #522
(`213faa5`, 03:15), #530 (`2697e56`, 03:20), #533 (`ed32107`, 03:23), #526
(`38e1582`, 03:33) and #525 (`a103990`, 03:36 UTC) merged on 2026-09-29
after #515, in that order. #514 was the previous ledger
update; #511, #515 and #520 are recorded above. #512 and #530 changed no
Markdown file. Twenty-six Markdown files were added: fifteen reader pages
(`model-context-designer/references/prompt-contract-template.md` in #519;
`ai-task-decomposer/SKILL.md` and `assets/task-plan-template.md` in #517;
`database-backup-verifier/SKILL.md` and
`references/backup-verification-checks.md` in #523;
`ai-human-in-the-loop-designer/SKILL.md` and
`references/hitl-design-sheet.md` in #518;
`resilience-architecture-reviewer/SKILL.md` and
`references/resilience-review-sheet.md` in #522; and
`cloud-security-baseline-reviewer/SKILL.md` with five provider baseline
references in #526) and eleven synthetic
fixtures, the agent-frontmatter test inputs under
`scripts/tests/fixtures/agents/` in #505. No file was removed or renamed.
Counts follow the rules above, now against `a103990`: per PR in parentheses,
and net since the page's last accepted head for the 10-line rule. Codex
again posted only usage-limit notices.

**Full-page re-reads done and accepted in this range.** Each page below
changed by more than 10 lines or is new, so it needed a full-page re-read;
each got one, and `git diff <accepted head> a103990` on it is empty unless
stated.

- `ai-router-architect/SKILL.md` (#513, 99): REVISE on `232e4d4`, then
  **ACCEPTED** on `579d9ad`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/513#issuecomment-5881587769)).
- `model-context-designer/SKILL.md` (#519, 80) and the new
  `references/prompt-contract-template.md` (87): REVISE on `dfeca93`, then
  both **ACCEPTED** on `602adda`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/519#issuecomment-5881811280)).
- The new `ai-task-decomposer/SKILL.md` (266) and
  `assets/task-plan-template.md` (109), #517: REVISE on `4a00be6`, then both
  **ACCEPTED** on `f5dfe57`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/517#issuecomment-5881858517)).
- This ledger (#514, 233): FIX-FIRST on `5b0e59b`, then **ACCEPT** on
  `8f3ab5d`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/514#issuecomment-5881947373)).
- The new `ai-human-in-the-loop-designer/SKILL.md` (299) and
  `references/hitl-design-sheet.md` (106), and
  `ai-governance-risk-reviewer/SKILL.md` (#518, 7; 17 net since `2c8ecaf`,
  re-read in full on `0df6f2f`): REVISE on `0df6f2f`, then all three
  **accepted** on `288d993`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/518#issuecomment-5882285601)).
- The two `ci-failure-classifier` pages, pending above (#532, 28 and 4):
  **ACCEPTED** on `63597a0`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/532#issuecomment-5882650238)).
  Pending to accepted.
- `data-migration-runbook-author/SKILL.md` (#527, 156) and its
  `references/runbook-skeleton.md` (54): REVISE on `dda146c`, then both
  **ACCEPTED** on `ba190cc` after full-page re-reads
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/527#issuecomment-5882837371)).
- The new `resilience-architecture-reviewer/SKILL.md` (301) and
  `references/resilience-review-sheet.md` (115), #522. The first review
  re-read both in full on `3bb43d8` and said each is ACCEPTED once its
  named edits land
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/522#issuecomment-5881830340)).
  The check on `d75cd58` confirmed those edits exactly and asked for two
  one-line edits on other pages, saying that with them the verdict is ACCEPT
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/522#issuecomment-5882779940));
  the merged head `50dd8ae` adds exactly those two lines. Both pages are
  counted as **accepted** on `d75cd58` on that pre-cleared basis, as the
  README was on `b6b4b4e` in #430; no further comment was posted.
- The [approval register](../approvals/APPROVAL_REGISTER.md), pending above:
  #529 appended AEGIS-APR-087 and APR-088 (60; its review checked facts and
  format), and #533 (11) applied a full-page re-read's edit and two glosses.
  Its corrected-candidate check **accepted** the register on `a890669`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/533#issuecomment-5882995051)),
  but #525 then made it pending again (below).
- The new `cloud-security-baseline-reviewer/SKILL.md` (266) and its five
  baseline references for Amazon Web Services (AWS, 52), Microsoft Azure
  (46), Google Cloud Platform (GCP, 46), Supabase (52) and
  Vercel (46), #526: the first review re-read all six in full on `03d5403`
  (REVISE), and the corrected-candidate check **accepted** all six on
  `65bacc7`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/526#issuecomment-5882836673)).

**Small reviewed edits that keep acceptance.**

- `ai-router-architect/references/ai-router-design.md` (#513, 4): 6 net since
  its full-page acceptance in the batch merged as #224, passed on `579d9ad`.
- `change-classification-gate/SKILL.md` (#517, 6; 9 net since #214),
  `project-orchestrator/SKILL.md` and
  `ai-sdlc-operating-model/references/stage-gate-map.md` (#517, 2 each; 2 net
  since `ad927f7`): #517's reviews checked each edit.
- `human-approval-boundary/SKILL.md` (#518, 6; 10 net since `a56c60d`) and
  `agent-tool-safety-guard/SKILL.md` (#518, 10; 10 net since `379c588`):
  #518's reviewer measured both and passed the edits. Both are at the limit;
  any further edit needs a full-page re-read.
- `horizontal-scalability-reviewer/SKILL.md` (#522, 6; 6 net since #219) and
  `soc2-trust-criteria-mapper/references/tsc-scoping-map.md` (#522, 2; 7 net
  since the full-page batches of 2026-09-24): #522's first review checked
  both.
- `aws-saas-architect/SKILL.md` (6 net since `14ecd0c`), `iac-reviewer/SKILL.md`
  (7 net since #219) and `security-logging-alerting-architect/SKILL.md` (6 net
  since #227), #526: its reviews measured all three and passed the edits.

**Newly pending.**

- [CONTRIBUTING](../../CONTRIBUTING.md) (#505, 6): 13 net since its
  full-page acceptance in #238. #505's reviews were security reviews (SHIP on
  `ebda783`,
  [comment](https://github.com/ModernNomad-98/Project-Aegis/pull/505#issuecomment-5881821301)),
  not a full-page re-read. **Full-page re-read owed.**
- `database-backup-verifier/SKILL.md`: accepted on `d3dcb62` in #523
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/523#issuecomment-5882118820)),
  then #522 changed it by 13 (reviewed as a seam change, not a full page), so
  it is 13 net. **Full-page re-read owed.**
- `database-backup-verifier/references/backup-verification-checks.md`:
  accepted on `d3dcb62`, then #523's last commit `dbed569` reworded one row
  (2) after that review, and no review of it was posted. It is 2 net, but an
  unreviewed edit needs a check, so it is **pending a targeted review**.
- The [approval register](../approvals/APPROVAL_REGISTER.md) (#525, 184:
  AEGIS-APR-085 and APR-086): 184 net since `a890669`. #525's reviews
  **accepted** the entries on `b04d040`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/525#issuecomment-5883090872))
  but checked facts and format, not the whole page. **Full-page re-read owed.**
- The [BER backlog](behavioral-eval-runner-backlog.md) (#525, 111: decision
  BER-DEC-015; 113 net since its acceptance with the AEGIS-APR-053 to APR-056
  change) and the [resumable control-plane backlog](resumable-control-plane-backlog.md)
  (#525, 16; 16 net since `67f577e`): the same fact-and-format reviews.
  **Full-page re-reads owed.**

**Still pending, with new counts.** The step-0 reconciliation log is 328 net
since `97c8682`, the skills catalog 95 since `2e15b23`, the README 46
since `b6b4b4e`, the offline CI guide 32 since `2aed8dd` (#505 added 18) and the
AEGIS-060+ register 22 since `04af9d9`. Each needs a full-page re-read.

Main after #525 (`a103990`) therefore has **651 tracked Markdown files: 584
accepted reader pages, one generated report, 55 classified synthetic fixtures
and eleven known pending pages**. The 651 is `git ls-files '*.md'` on a
checkout of `a103990`: 625 + 15 reader pages + 11 fixtures. Accepted
readers go 572 + 13 (the new pages accepted: one in #519, two each in
#517, #518 and #522, six in #526) + 2 (#532) + 1 (#533's register) − 1
(CONTRIBUTING) − 1 (#525's register) − 2 (the BER and control-plane
backlogs) = 584; the two new `database-backup-verifier` pages count as
pending. Pending goes 8 − 2 (#532) − 1 + 1 (the register, accepted then
pending again) + 1 (CONTRIBUTING) + 2 (`database-backup-verifier`) + 2 (the
backlogs) = 11: the step-0 log, skills catalog, README, offline CI guide,
AEGIS-060+ register, approval register, CONTRIBUTING, BER backlog,
control-plane backlog and the two `database-backup-verifier` pages.
Fixtures go 44 + 11 = 55, and 584 + 11 + 1 + 55 = 651. This update changes
this ledger by more than 10 lines, so it needs its own independent
full-page re-read. No grant or gate changed.

PRs #528 (`3e11d6b`, 06:52 UTC), #507 (`e143daf`, 15:44), #521 (`f728880`,
15:49), #524 (`8fcb4e4`, 16:19), #535 (`5d006ac`, 16:31), #534 (`573ddf3`,
16:39) and #531 (`8dc3b00`, 16:45 UTC) merged on 2026-09-29 after #525, in
that order. #535 and #531 changed no Markdown file. #521 added two reader
pages, `environment-parity-reviewer/SKILL.md` and
`references/parity-matrix-sheet.md`; no fixture was added and no file was
removed or renamed. Counts follow the rules above, now against `8dc3b00`:
per PR in parentheses, and net since the page's last accepted head for the
10-line rule. Codex again posted only usage-limit notices.

**Full-page re-reads done and accepted in this range.** For each page below,
`git diff <accepted head> 8dc3b00` on it is empty.

- The new `environment-parity-reviewer/SKILL.md` (#521, 314) and
  `references/parity-matrix-sheet.md` (121): REVISE on `fea01d6`, then both
  **ACCEPTED** after full-page re-reads on `7f98950`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/521#issuecomment-5882300536)).
  The later checks on `8ccc5ee` and `f5a6dab` kept both accepted.
- `iac-reviewer/SKILL.md` (#521, 30): after the rebase it was 11 net since
  `93f6162`, so it got a full-page re-read on `8ccc5ee` (FIX-FIRST with
  three named edits, I1 to I3,
  [comment](https://github.com/ModernNomad-98/Project-Aegis/pull/521#issuecomment-5885328158)).
  A re-read confined to I1 to I3 **accepted** it on `f5a6dab`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/521#issuecomment-5893664512)),
  its new acceptance point.
- This ledger (#534, 162): FIX-FIRST on `4149221`, then **ACCEPT** on
  `7b51c88`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/534#issuecomment-5894470757)).

**Small reviewed edits that keep acceptance.**

- `local-ci-mirror-preflight/SKILL.md` (#521, 6; 9 net since `bf7a4b8`) and
  `vite-build-qa-engineer/SKILL.md` (#521, 6; 6 net since `eb3ec53`): #521's
  reviews measured both and passed the edits.
- `.claude/skills/_template/SKILL.md` (#528, 4; 4 net since #408's
  `0533764`): two edits in `1e1cc70`, the removed `allowed-tools` comment
  line and a reworded validator-exemption note. #528's corrected-candidate
  security review on `1e1cc70` checked the first by name
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/528#issuecomment-5883096195)),
  and a targeted review on `8dc3b00` passed both
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/538#issuecomment-5897153529)).

**Newly pending.** The [skill generation
standard](../skill-generation-standard.md) (#528, 9): with #486's 2 it is 11
net since its full-page acceptance in #408 (`0533764`). #528's reviews were
security reviews, not a full-page re-read. **Full-page re-read owed.**

**Still pending, with new counts.** [CONTRIBUTING](../../CONTRIBUTING.md)
(#528, 5) is 16 net since #238. The README (#528, 6; #521, 7; #524, 6) is 57
net since `b6b4b4e`. The offline CI guide (#528, 24; #507, 62; #524, 54) is
168 net since `2aed8dd`. The step-0 reconciliation log (#521, 6) is 334 net
since `97c8682`, and the skills catalog (#521, 9) 98 net since `2e15b23`.
The other six pending pages did not change. Each needs a full-page re-read.

Main after #531 (`8dc3b00`) therefore has **653 tracked Markdown files: 585
accepted reader pages, one generated report, 55 classified synthetic
fixtures and twelve known pending pages**. The 653 is `git ls-files '*.md'`
on a checkout of `8dc3b00`: 651 + 2 (#521). Accepted readers go 584 + 2
(#521) − 1 (the skill generation standard) = 585. Pending goes 11 + 1 = 12:
the step-0 log, skills catalog, README, offline CI guide, AEGIS-060+
register, approval register, CONTRIBUTING, BER backlog, control-plane
backlog, the two `database-backup-verifier` pages and the skill generation
standard. 585 + 12 + 1 + 55 = 653. This update changes this ledger by more
than 10 lines, so it needs its own independent full-page re-read. No grant
or gate changed.

PRs #537 (`43d8b6b`, 18:11 UTC), #539 (`2bb44db`, 19:43), #540 (`0ca4a83`,
20:10), #541 (`32a62f0`, 20:10), #538 (`f4c3cec`, 20:54) and #542
(`22a6b7a`, 20:54 UTC) merged on 2026-09-29 after #531, in that order. None
added, removed or renamed a Markdown file. Counts follow the rules above,
now against `22a6b7a`: per PR in parentheses, and net since the page's last
accepted head for the 10-line rule. Codex again posted only usage-limit
notices.

**Full-page re-reads done and accepted in this range.** For each page below,
`git diff <accepted head> 22a6b7a` on it is empty.

- The [skill generation standard](../skill-generation-standard.md) (#541,
  16): a full-page re-read **accepted** it on `5e4cdd4`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/541#issuecomment-5897799994)),
  so it moves from pending to accepted.
- This ledger (#538, 73): FIX-FIRST on `602c8bd`, then **ACCEPT** on
  `51860f3`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/538#issuecomment-5897922136)).

**Small reviewed edits that keep acceptance.**
`library-diff-reviewer/SKILL.md` (#542, 2; 4 net since #33's `700aa1d`,
with #483's 2): #542's review read the one changed line
([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/542#issuecomment-5897928657)).

**Newly pending.** Each needs a full-page re-read.

- The [delivery control-plane guide](../../tools/aegis_delivery_control/README.md)
  (#539, 15): 15 net since #196 (`437e73a`), its last change before #539.
  #539's code review checked the corrected row's facts, not the whole page.
- The [host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md)
  (#540, 47; 47 net since `6ba6e1a`) and the
  [Stage 4A offline review](../evidence/setup/issue-101-package-4a-offline-review.md)
  (#540, 13; 13 net since #281's `ea40ab4`): each gained a new dated
  section. #540's supply-chain review checked the appended facts, not the
  whole pages.

**Still pending, with new counts.** The approval register (#537, 221) is
405 net since `a890669`, and the BER backlog (#537, 42) is 149 net since
#381's `032e030`. No review verdict was posted on #537. The other nine
pending pages did not change.

**This update's own edits.** Under owner decisions of 2026-09-29, the
[targeted-edit rule](#remaining-page-review-in-larger-batches) now says a
small edit's review must cover every changed line and may be any kind of
independent review, and §5 of the skill generation standard gains a dated
note that `allowed-tools` has been forbidden in every shipped skill since
#528 (2 net since `5e4cdd4`). That note needs this update's independent
review to name or read it before the standard keeps acceptance.

Main after #542 (`22a6b7a`) therefore has **653 tracked Markdown files: 583
accepted reader pages, one generated report, 55 classified synthetic
fixtures and fourteen known pending pages**. The 653 is `git ls-files
'*.md'` on a checkout of `22a6b7a`, unchanged from `8dc3b00`. Accepted
readers go 585 + 1 (the skill generation standard) − 3 (the control-plane
guide and the two evidence pages) = 583. Pending goes 12 − 1 + 3 = 14: the
step-0 log, skills catalog, README, offline CI guide, AEGIS-060+ register,
approval register, CONTRIBUTING, BER backlog, control-plane backlog, the
two `database-backup-verifier` pages, the control-plane guide and the two
evidence pages. 583 + 14 + 1 + 55 = 653. This update changes this ledger by
more than 10 lines, so it needs its own independent full-page re-read. No
grant or gate changed.

PRs #543 (`74411bc`, 21:36 UTC), #545 (`a841f5f`, 22:02), #544
(`5893a07`, 22:06), #546 (`4983fa2`, 22:21), #547 (`6640e1c`, 22:51) and
#548 (`b5ec558`, 23:18 UTC) merged on 2026-09-29 after #542, followed by
#549 (`6732762`, 00:03 UTC) and #550 (`8ed228ee`, 00:13 UTC) on 2026-09-30,
in that order. None added, removed or renamed a Markdown file. Counts follow
the rules above, now against `8ed228ee`: per PR in parentheses, and net since
the page's last accepted head for the 10-line rule. Codex again posted only
usage-limit notices on every PR.

- #543 changed `.github/workflows/validate-skills.yml` (+4/−1), the
  [offline CI guide](../offline-ci.md) (+4/−1) and
  `scripts/tests/test_offline_ci.py` (+7/−2). Its review returned **SHIP** on
  `8fce63f6`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/543#issuecomment-5899042081));
  the exact-head protected-file exception and its consumption are recorded as
  AEGIS-APR-096 and AEGIS-APR-097.
- #545 changed [README](../../README.md) (+23/−14): FIX-FIRST on `10b38aae`,
  then **ACCEPT** on `1c2d6f03`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/545#issuecomment-5899861232)).
- #544 changed this ledger (+70/−4) and the
  [skill generation standard](../skill-generation-standard.md) (+1/−1):
  FIX-FIRST on `77fca55d`, then **ACCEPT** on `412b5de1`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/544#issuecomment-5899946382)).
- #546 appended 63 lines to the
  [approval register](../approvals/APPROVAL_REGISTER.md) and was **ACCEPTED**
  on `c5615791`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/546#issuecomment-5900199285)).
- #547 changed [CONTRIBUTING](../../CONTRIBUTING.md) (+12/−7) and was
  **ACCEPTED** on `434c6835`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/547#issuecomment-5900336791)).
- #548 changed the [offline CI guide](../offline-ci.md) (+37/−22):
  FIX-FIRST on `61d55a38`, then **ACCEPT** on `640f87b9`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/548#issuecomment-5900899795)).
- #549 changed [CONTRIBUTING](../../CONTRIBUTING.md) (+5/−3) and received
  **SHIP** on `5715f07f`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/549#issuecomment-5901365257)).
- #550 changed the [approval register](../approvals/APPROVAL_REGISTER.md)
  (+51/−0) and the
  [resumable control-plane backlog](resumable-control-plane-backlog.md)
  (+36/−1): REVISE on `2269a5f4`, then **ACCEPT** on `e04cc961`
  ([comment](https://github.com/ModernNomad-98/Project-Aegis/pull/550#issuecomment-5901479210)).

**Full-page re-reads done and accepted in this range.** For each page below,
`git diff <accepted head> 8ed228ee` on it is empty.

- [README](../../README.md) was accepted on #545's `1c2d6f03`.
- [CONTRIBUTING](../../CONTRIBUTING.md) was accepted on #547's `434c6835`;
  #547's owner-decided wording identifies the security-relevant surfaces and
  #549's owner-decided follow-up names the guard-matched paths.
- The [offline CI guide](../offline-ci.md) was accepted on #548's
  `640f87b9`.

**Small reviewed edits that keep acceptance.**

- The [skill generation standard](../skill-generation-standard.md) (#544, 2
  net since `5e4cdd4`) keeps acceptance. #544's review read the changed
  targeted-edit-rule clarification in this ledger and the owner-decided,
  dated §5 note about `allowed-tools`.
- [CONTRIBUTING](../../CONTRIBUTING.md) (#549, 8 net since `434c6835`) keeps
  acceptance because #549's review read every changed line.

**Newly pending.** This ledger changes by more than 10 lines in this update,
so it needs its own independent full-page re-read against
[Acceptance for each page](#acceptance-for-each-page).

**Still pending, with new counts.** The
[approval register](../approvals/APPROVAL_REGISTER.md) is 519 net since
`a890669`. The
[resumable control-plane backlog](resumable-control-plane-backlog.md) is 51
net since its last full-page acceptance at `67f577e`; #550 changed it by
37 lines. #546 and #550 reviewed their changed facts and format, not either
whole page. The other nine pending pages did not change. Each needs a
full-page re-read.

Main after #550 (`8ed228ee`) therefore has **653 tracked Markdown files: 586
accepted reader pages, one generated report, 55 classified synthetic
fixtures and eleven known pending pages**. The tracked total is unchanged
because none of these PRs added, removed or renamed a Markdown file. Accepted
readers go 583 + 3 (README, CONTRIBUTING and the offline CI guide) = 586.
Pending goes 14 − 3 = 11: the step-0 log, skills catalog, AEGIS-060+
register, approval register, BER backlog, control-plane backlog, the two
`database-backup-verifier` pages, the control-plane guide and the two setup
evidence pages. 586 + 11 + 1 + 55 = 653. This ledger round changes the ledger
by more than 10 lines, so the ledger needs its own independent full-page
re-read. No grant or gate changed.

PR #554 (`e0c9a000`, 2026-09-30) changed only the
[approval register](../approvals/APPROVAL_REGISTER.md), +4/−2. Its independent
review accepted the corrected reading aid and verified that all 98 immutable
entries were byte-identical (normalized SHA-256
`c80d02f5987747728a1eb28573e822250e80973d6c577039ad8bf67d2c52591a`). The register is
therefore **accepted** on `e0c9a000`; it is the only page that moved to
accepted in this round. **That range hash is now superseded:** PR #569 and
PR #571 appended inside that span, so it no longer reproduces. The span is
`### AEGIS-APR-001` **to end of file at `e0c9a000`** (169,099 bytes, trailing
newline stripped) — **not** "up to APR-099", which did not exist at that
commit. This is expected growth on an append-only register, not a tamper
signal; the register itself carries the re-verification convention (see its
note under `AEGIS-APR-086`).

The prior current-reading pointer to #542 was stale: its dated snapshot
records 583 accepted and fourteen pending, whereas the later, dated #550
snapshot records 586 accepted and eleven pending. The #550 snapshot's
statement that every listed re-read page had an empty diff through `8ed228ee`
was also too broad: `git diff --numstat 434c6835 8ed228ee -- CONTRIBUTING.md`
is +5/−3. The #550 status prose listed eleven pages but did not include this
ledger, although that snapshot says the ledger's more-than-10-line update
needed an independent full-page re-read. Thus its written arithmetic,
586 + 11 + 1 + 55 = 653, closed only by omitting the ledger: its literal
statuses were 586 + 12 + 1 + 55 = 654, and a disjoint post-#550 partition
would have required 585 accepted readers. This round corrects the live
classification without rewriting either dated snapshot.

Main after #554 (`e0c9a000`) therefore has **653 tracked Markdown files: 586
accepted reader pages, one generated report, 55 classified synthetic fixtures
and eleven known pending pages**. `git ls-files '*.md'` gives 653; the 55
classified fixtures are the 56 Markdown files under `scripts/` other than
their fixture index, and the generated report is
[the skill-contract audit baseline](../audits/skill-contract-audit-baseline.md).
The classifications reconcile as 586 + 1 + 55 + 11 = 653. The pending pages
are the [step-0 reconciliation log](../reconciliation/step-0-reconciliation-v4.md),
the [skills catalog](../skills-catalog.md), the
[AEGIS-060+ register](../audits/aegis-060-plus-register.md), the
[BER backlog](behavioral-eval-runner-backlog.md), the
[resumable control-plane backlog](resumable-control-plane-backlog.md), both
[database-backup-verifier pages](../../.claude/skills/database-backup-verifier/SKILL.md)
and [their checks sheet](../../.claude/skills/database-backup-verifier/references/backup-verification-checks.md),
the
[delivery control-plane guide](../../tools/aegis_delivery_control/README.md),
the [host-feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md),
the [Stage 4A offline review](../evidence/setup/issue-101-package-4a-offline-review.md)
and this ledger. This ledger update changes more than 10 lines, so the ledger
returns to **pending** until an independent full-page re-read records
acceptance. No grant or gate changed.

PRs #555 (`9e88a581`), #557 (`41764593`), #558 (`4012161e`), #559
(`52f1b9a2`), #560 (`d9314437`) and #561 (`410b90aa`) merged on 2026-09-30
UTC after #554, in that order, and #556 (`afe703a4`) merged between #554 and
#555. None added, removed or renamed a Markdown file, so the tracked total is
unchanged at 653. Each merge carries an independent review, and #561's was
posted at review time rather than retrospectively. None of them recorded an
independent **full-page** review of the whole page against every criterion, so
none confers acceptance. #555 changed the [backlog
forecast](aegis-backlog-forecast.md) by 86 added and 2 deleted lines (88),
adding a catch-up checkpoint section; its retrospective review is an **ACCEPT**
bound to `c199e57`. #557 changed the [BER
backlog](behavioral-eval-runner-backlog.md) by 1 added and 1 deleted line (2),
with a retrospective **SHIP** bound to `665b2829`. #558 changed the [step-0
reconciliation log](../reconciliation/step-0-reconciliation-v4.md) by 7 added
and 2 deleted lines (9) with a retrospective **ACCEPT**, and #559 changed the
[AEGIS-060+ register](../audits/aegis-060-plus-register.md) by 2 added and 1
deleted line (3) with a retrospective **SHIP**. #560 changed the [skills
catalog](../skills-catalog.md) by 6 added and 4 deleted lines (10), with a
retrospective **SHIP** bound to `1b9e7049`, and #561 changed
`.claude/skills/scoped-approval-register/SKILL.md` by 10 added lines with a
quality **SHIP** at `41c7a649` and a security **SHIP**. Under [Targeted edits
to accepted pages](#remaining-page-review-in-larger-batches), a review of a
small edit covers the changed lines, which is what these reviews did; the
exemption retains an existing acceptance and cannot confer one, so no pending
page gains acceptance. A review is not discounted for declining to assert a
standard the rule never imposes: the ledger says "any kind of independent
review counts", such as a readability, security or fact review. The [approval
register](../approvals/APPROVAL_REGISTER.md) is then the one page that must
**lose** an acceptance: the #554 paragraph above recorded it as accepted on
`e0c9a000` for a 4+2=6-line targeted reading-aid correction, but the register
was pending, and a targeted review cannot confer full-page acceptance. It was
already pending at #550 (519 net since `a890669`) and is still 525 net, so it
returns to pending. The forecast likewise returns to pending under the
exemption's second sentence: 88 changed lines exceed 10, and its last full-page
acceptance is `826f40b`. The remaining pages were pending and stay pending. No
dated snapshot is rewritten; the #554 paragraph above stands as recorded, with
its register classification corrected in the live reading rather than in place.

Main after #561 (`410b90aa`) therefore has **653 tracked Markdown files: 584
accepted reader pages, one generated report, 55 classified synthetic fixtures
and thirteen known pending pages**. The 653 is `git ls-files '*.md'` at
`410b90aa`; 56 Markdown files sit under `scripts/`, and the 55 classified
fixtures are those 56 less their fixture index
(`scripts/tests/fixtures/README.md`). The generated report is [the
skill-contract audit baseline](../audits/skill-contract-audit-baseline.md).
Two pages move from accepted to pending — the forecast and the approval
register — so accepted readers go 586 − 2 = 584 and pending goes 11 + 2 = 13.
The thirteen pending pages are the [approval
register](../approvals/APPROVAL_REGISTER.md) (525 net since `a890669`), the
[backlog forecast](aegis-backlog-forecast.md) (88 net since `826f40b`), the
[BER backlog](behavioral-eval-runner-backlog.md) (151 net since `032e030`),
the [step-0 reconciliation
log](../reconciliation/step-0-reconciliation-v4.md) (343 net since
`97c8682`), the [AEGIS-060+
register](../audits/aegis-060-plus-register.md) (25 net since `04af9d9`), the
[skills catalog](../skills-catalog.md) (108 net since `2e15b23`), the
[resumable control-plane backlog](resumable-control-plane-backlog.md) (51 net
since `67f577e`), both [database-backup-verifier
pages](../../.claude/skills/database-backup-verifier/SKILL.md) and [their
checks
sheet](../../.claude/skills/database-backup-verifier/references/backup-verification-checks.md),
the [delivery control-plane
guide](../../tools/aegis_delivery_control/README.md), the [host-feasibility
evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md), the
[Stage 4A offline
review](../evidence/setup/issue-101-package-4a-offline-review.md) and this
ledger — thirteen entries in all, and this ledger is counted in that number.
As at #554, whose `11` likewise counted the ledger, the list is the pending
set itself. The [open-decisions
index](aegis-open-decisions-2026-09-23.md) and the
`aegis-backlog-forecast.md` link references in this paragraph are not separate
pending pages, so the list is not double counting. The arithmetic closes:
584 + 1 + 55 + 13 = 653. This
ledger changes by more than 10 lines, so it returns to **pending** until an
independent full-page re-read records acceptance. No grant or gate changed.

Merged PR #331 established **602 Markdown files: 558 accepted reader pages
and 44 classified synthetic fixtures**, with zero known pending pages. It added
the [Behavioral Eval Runner (BER) selected-precheck aggregate decision page](ber-precheck-aggregate-validation-proposal.md)
after independent technical and full-page readability review, including a
first-use terminology correction. This count and review do not approve its
implementation, private labels, a host probe or provider use.

Merged PR #333 added the [protected-file guard decision packet](gate-guard-friction-decision.md),
bringing the merged tree to **603 Markdown files: 559 accepted reader
pages and 44 classified synthetic fixtures, with zero known pending pages**.
Independent technical, full-page readability and ledger review accepted the
packet and this ledger after corrections to the four-file scope and first-use
terminology. The packet remains a proposal: neither review nor merging it
selects an option or creates a standing exception. Its recommended option preserves
separate owner decisions for all other protected paths and work-package rules.

Merged PR #329 established 601 Markdown files: 557 accepted reader pages and
44 fixtures. PR #330 changed existing forecast and measurement pages only.

The Stage 4B preflight draft adds one independently reviewed reader page to
the 600-page #319 tree. Its source pins, canonical Git-byte hashes, three
host-path choices, unknown preflight facts, no-grant boundary and all relative
links passed full-page factual and readability review after a correction to
the hash basis. That reviewed candidate had **601 Markdown files: 557 accepted reader
pages and 44 classified synthetic fixtures**, with zero known pending pages.
The draft prepares a later owner decision; it does not prove a host or permit
a session. The #319 tree contains **600 Markdown files**: **556 accepted reader
pages** and **44 synthetic fixtures**, with zero known pending pages. The new
[offline routing request-binding review](../evidence/setup/issue-101-routing-request-binding-review.md)
is one accepted reader page. Its contract, authority boundary, test results,
merge and check receipts were reviewed for factual accuracy and full-page
readability; it adds no fixture and proves no real host integration. The
previous candidate contained **599 Markdown files**: **555 accepted reader
pages** and **44 synthetic fixtures**. An independent
technical and full-page readability review accepted the new [routing
request-binding proposal](aegis-setup-routing-request-binding-proposal.md),
including its choice guidance, exact scope, first-use terms and links. It is a
proposal only; its new page adds no implementation or host authority. The
previous merged tree contained **598 Markdown files**: **554 accepted reader
pages** and **44 synthetic fixtures**. Independent factual
and full-page readability reviews accepted the [CP-WP-003 DynamoDB public
contract inspection](cp-wp-003-dynamodb-public-contract-inspection.md) after
corrections to table-incarnation identity, source-head hashes, missing-event
reconciliation, first-use terms and the packet's completed-versus-future step.
The previous merged tree contained **597 tracked Markdown files**: **553
reader pages** with recorded full-checklist acceptance and **44 synthetic
fixtures** with classification and integrity checks. The new
[Stage 4B preflight manifest template](aegis-setup-package-4b-preflight-manifest-template.md)
adds one reviewed reader page after the 596-page named-candidate checkpoint;
independent technical and readability reviews accepted it after corrections
to the preflight/post-run split and approval-bound profile digest.
The earlier
[CP-WP-003 named-candidate matrix](cp-wp-003-named-candidate-matrix.md)
adds one reviewed reader page after the 595-page three-packet checkpoint;
independent factual and readability reviews accepted its source-backed comparison
after corrections to receipt consistency and append-only proof wording.
PR #286 added the reviewed
[Stage 4B decision packet](aegis-setup-package-4b-host-proof-protocol.md)
as one accepted reader page after the #285 inventory of 589. The protected
`scripts/tests/fixtures/README.md` and its new
[review record](../evidence/documentation/fixture-readme-closure-after-238-2026-09-24.md)
merged in #239, closing the original bounded pending set. PRs #139 and #197
had each added an evidence note before that merge. Their dated current-reading
corrections passed two independent full-page reviews in this checkpoint.
PRs #248 and #249 each added a reader page; both passed full-page review after
the corrections recorded below and merged through #250. PR #253 added the
reviewed Behavioral Eval Runner (BER) BKL-009 scope proposal and reaccepted
the corrected candidate
summary. PRs #254 and #255 changed existing governance and tracking pages;
the [five-merge checkpoint](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-260)
reconciles their status. PR #257 added the reviewed operator runbook and
integration evidence record; both passed full-page review. The new
[VirtualBox Stage A setup proposal](ber-virtualbox-stage-a-setup-proposal.md)
merged in #260 with one reviewed reader page. PR #261 updated build-choice
guidance in existing skill and project pages; it added no Markdown file.
PR #262 updated three existing forecast, measurement and readability pages.
PR #263 corrected the setup skill's choice guidance. This current-route and
virtual machine (VM) approval update in #264 changed existing pages only; its
approval register, decision routes, host proposal and this ledger received
full-page review. The tracked count then remained 588.
PR #265's issue #101 package-4A candidate refresh reaccepted its existing proposal
after an independent full-page review and a separate source check; it adds no
Markdown file.
PR #266's post-#265 checkpoint rechecked the existing forecast, execution
metrics and this ledger through independent full-page reviews; no page entered
the pending set and the tracked count remained 588.
Merged PR #267 revised five existing reader pages for the issue #101 host path: its
setup plan, Stage 4A proposal, feasibility evidence, forecast and this ledger.
Two independent read-only reviews accepted their full pages after terminology,
forecast and lockfile corrections, and checked their relative links. It added
no page; the accepted reader and fixture counts then remained 544 and 44.
The [BER-BKL-009 static source inventory](../evidence/ber-bkl-009-static-source-inventory.md)
merged in PR #269 as one new reader page. It records the shipped source
boundaries and remaining host, runtime, privacy and cleanup connections without
running a host probe. Two independent read-only reviews accepted the inventory
and this ledger after corrections to deadline-check attribution, inventory
scope, first-use terms and #267 status. Its exact-head GitHub checks and merge
made **589 pages**, 545 accepted readers and 44 classified fixtures, the
merged-tree inventory. **Zero known pages** remain pending in that tree.
PR #270 revised four existing architecture skill pages to teach user-facing
choices; two independent reviews accepted their explanations. PR #271's
issue #101 public software development kit (SDK) archive packet revised two
existing accepted
reader pages: the [host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md)
and [Stage 4A proposal](aegis-setup-package-4a-host-preparation-proposal.md).
Two independent full-page reviews accepted the corrected packet, including its
110-archive and alternate 107-archive static checks, exact dependency limits,
links and the then-pending implementation grant. The owner granted bounded
offline Stage 4A work after #271; actual host work remains separate. A separate
independent review accepted
the ledger; local checks and GitHub Actions passed before merge. The merged
tree remains **589 tracked Markdown pages**: 545 reader pages and 44 classified
fixtures, with zero known pending pages. PRs #272 and #273 changed existing
skill pages, and #274 changed existing Behavioral Eval Runner (BER) source and
tests. PR #278 recorded the consumed #274 guard exception and the bounded
Stage 4A grant in the existing approval register. PR #279 revised existing
choice skills; PR #280 accepted the previous three-page checkpoint after two
independent full-page reviews. PR #282 refreshed two existing current-route
reader pages after an independent full-page review. None added a Markdown page.
PR #283 updated the existing three checkpoint pages and #284 improved choice
guidance in eleven existing skill pages. Both added no Markdown file. The #284 tree
still has 589 tracked pages: 545 accepted readers and 44 classified fixtures,
with zero known pending pages.

The [five-merge checkpoint after #284](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-25-after-pull-request-284)
covers #279, #280, #282, #283 and #284. GitHub merge receipts span **40m31s
observed wall time**, including review, checks and waiting, so they do not
measure an active-work rate. Ten selected ranges remain **71–146 active hours**;
at that #284 checkpoint, issue #101 Stages 4A/4B and the BER host, runtime,
privacy and cleanup residual had no reliable estimated time of arrival (ETA). The selected total had no
finite estimate. Stage 4A's approved 12-hour limit was a ceiling, not a
remaining estimate. [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
was then open at `0bb51c19bd42261a5604fb25762069ce7867141b` with Linux
and Windows green, the protected-path guard failing and its one-time exception
question pending. This historical checkpoint revised the same three tracking pages and
adds no Markdown page or fixture. Two independent full-page reviews of these
revised pages accepted the content, counts and 340 local links and anchors.

The Stage 4B host-proof decision packet added one reader page after #285.
Two independent full-page reviews accepted
its factual boundary, user-choice explanations and local links after the
planning-only decision wording was clarified. The [setup route](aegis-setup-routing-plan.md)
now links the packet and corrects its stale Stage 4A grant status. The packet
does not close Stage 4B execution or authorize a host session. The current
readability inventory at #286 was **590 tracked Markdown pages: 546 accepted
readers and 44 classified fixtures**, with zero known pending pages.

Merged [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
added two reviewed offline reader pages, the
[Stage 4A offline review](../evidence/setup/issue-101-package-4a-offline-review.md)
and [host bridge guide](../../tools/aegis_setup/host_bridge/README.md).
Its protected guard exception was consumed at the exact merged head; neither
page proves real host interception. This update adds three independently
reviewed reader pages: the
[WP-2B-3 measurement prerequisite packet](ber-wp2b3-measurement-prerequisite-decision-packet.md),
[CP-WP-003 authority candidate packet](cp-wp-003-real-authority-decision-packet.md),
and [BER-BKL-009 residual proposal](ber-bkl-009-residual-host-runtime-privacy-cleanup-proposal.md).
Their factual and full-page readability reviews accepted the corrected
authority boundaries, choices, estimates and links. They add no fixture and
close no implementation gate. The resulting inventory is **595 pages: 551
accepted readers and 44 classified fixtures**, with zero known pending pages.

The fixture files remain test inputs, so prose rewriting would damage their
positive and negative cases. The #237 bucket split and prior pending counts
below are historical snapshots; the
[129-page review record](../evidence/documentation/full-page-readability-all-remaining-after-237-2026-09-24.md)
accounts for the earlier batch. The [#244 forecast](aegis-backlog-forecast.md#start-here--current-reading)
gave a conditional **95–194 selected active-hour** residual after #239's
accepted merge. The [five-merge checkpoint after #245](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-245)
records the #245 baseline's **1–3 documentation active hours** for the two
notes. Their acceptance closes that residual, and #249 separately delivered
the 8–16-hour offline holdout-support item. The **87–178 active-hour** selected
residual after #250 is historical. The owner's bounded BER-BKL-009 approval,
effective on #255, left one offline implementation package capped at 16 active
hours. PR #257 delivered that package. The later issue #101 host-path choice
split its former 8–16-hour combined package-4 row into separately unestimated
offline Stage 4A and actual-host Stage 4B work. PR #281 later delivered the
bounded Stage 4A offline package. The current
[forecast](aegis-backlog-forecast.md#material-owner-decision--2026-09-25-issue-101-host-path)
therefore has **71–146 active hours** for ten unaffected rows, plus unestimated
Stage 4B host proof and the BER-BKL-009 residual. The later helper comparison
is conditional and outside the selected total. The selected total has
no finite current estimate.
Future new or changed pages still need the acceptance check below. The
[Behavioral Eval Runner guide](../../tools/behavioral_eval_runner/README.md)
and [delivery control-plane guide](../../tools/aegis_delivery_control/README.md)
explain their shipped offline workflows and limits. This reading route grants
no provider call, private-input use, real-host activation or deployment.

Created 2026-09-23 from Peter Nguyen's request to explain what the Behavioral
Eval Runner and delivery control plane are for, what their functions do, and
to make **all repository documentation understandable to human developers and
artificial intelligence (AI) agents**. Peter specifically identified the dense
[Behavioral Eval Runner README](../../tools/behavioral_eval_runner/README.md).
This is a required documentation quality item, not a claim that the current
pages already meet it.

## Purpose and scope

Readers should be able to find a component, understand the problem it solves,
follow a normal workflow, identify what each public entry point does, and see
its current limits without decoding project shorthand or reading a chronological
wall of implementation notes. Preserve exact technical facts and historical
evidence, but give them a clear explanation and a suitable home.

The tracked-file inventory found **491 Markdown files**, including **344 skill
documentation files** and **84 under `docs/`**. The root README has 1,353
lines; the Behavioral Eval Runner README
has 233; the delivery control kernel README has 410. These counts describe
review scope, not the number of defective files. The full sweep includes root
guides, component guides, roadmaps, evidence, and skill documentation. Review
the files in bounded batches so unrelated technical changes stay separate.

## Required order of work

1. **Explain the two components first.** Rewrite the Behavioral Eval Runner
   and delivery control kernel READMEs around purpose, audience, examples,
   supported use, key concepts, module/function map, commands, safety gates,
   current delivery status, and limits. Explain how they relate to the Aegis
   skills library. Keep historical transition details in linked design,
   backlog or evidence records instead of making them the entry point.
2. **Fix navigation.** Give the root README and documentation index a short,
   accurate description of each component and links to the right starting
   pages. A reader should not have to infer purpose from a package path.
3. **Sweep the remaining documentation.** Review every Markdown file in a
   recorded inventory. Prioritize active instructions and public guides, then
   roadmaps/evidence and skill docs. Record the checked batch, findings,
   changes and deliberately retained historical text. Do not rewrite an
   immutable approval or evidence record merely to modernize its language;
   add a linked, dated explanation where the original must remain intact.
4. **Keep future pages readable.** Add a short writing standard to the
   contribution guide and check new or changed documentation against it in
   review. Automation may find obvious structural problems, but human review
   must judge whether the explanation is understandable.

## Acceptance for each page

- Open with what the page or component is for and who should read it.
- Define an abbreviation or coded identifier at first use. For example,
  “Behavioral Eval Runner (BER)” and “work package (WP)” are explained before
  later shorthand. Explain lifecycle/status codes in plain words or link to
  a nearby glossary; do not assume a reader knows `CP-WP-003` (control-plane
  work package 003), `OD-1` (owner decision 1), `T03` (transition 03), or
  internal class names.
- Use descriptive headings, short paragraphs, lists or tables for distinct
  functions, and at least one concrete example where a component's purpose
  would otherwise remain abstract. Explain what a function or command accepts,
  produces, changes, and refuses when those details matter to safe use.
- State shipped behavior separately from proposed or blocked behavior. A
  synthetic test, passing check or approved design is not described as a
  deployed integration or measured model result.
- Keep navigation links current and check that every referenced file or
  command exists. Preserve the technical contract while making the prose
  approachable; do not remove a safety boundary for brevity.
- Obtain a read-only review from someone who did not write the page. Ask the
  reviewer to explain the component's purpose and normal use from the page
  alone, and correct gaps before marking that batch complete.

## Delivery and estimate

Status at launch: **IN PROGRESS**. The original sequence began with the two
component READMEs and the root/index navigation, then the full inventory in
reviewable batches. The following estimates are historical; use the current
reading above for remaining work.
Previously stated estimate for the narrower component-guide item was 4–8
active hours; after the repository-wide clarification an interim estimate
was 24–60. The inventory-based provisional estimate was **80–200 active hours**
for the entire documentation sweep, excluding owner waiting and GitHub queue
time. The plan called for re-estimation from batch measurements and did not
allow DONE status after only the two component READMEs were improved.

This documentation work does not authorize provider calls, deployment,
private calibration input publication, approval changes or later-phase runtime
implementation.

## Documentation batches

### Progress accounting after pull request #205

The exact #205 merge is `6051ab0ad4a3ccd1e1a67d315ba9a8b2c72cc31b`.
Its **553 tracked Markdown files** are 62 more than the original 491-file
inventory. The additional files are mostly dated evidence and tracking pages,
so a count of merged documentation requests alone is not a remaining-work
estimate. A deduplicated read of the delivered sorted skill screens and 61
readability/correction requests through #205 gives this inventory:

| Disjoint set | Pages | Evidence already recorded | Remaining acceptance work |
| --- | ---: | --- | --- |
| Skill entrypoints and references | 342 | Sorted screens and 83 targeted corrections | Apply the full page checklist; record each result |
| Corrected primary pages outside those skill paths | 83 | Bounded guide, roadmap, governance and evidence corrections | Apply the full page checklist; large records may take longer |
| Dated evidence notes and tracking pages | 55 | Written with the completed correction batches | Confirm current links, scope and readable first use |
| Other reader-facing pages and templates | 29 | No recorded sorted screen in those batches | Read and correct each full page |
| Synthetic fixture Markdown | 44 | Kept as test input | Classify and check that explanatory entrypoints are readable; do not rewrite fixtures merely for prose style |
| **Tracked total** | **553** | **342 + 83 + 55 + 29 + 44** | **Full-page acceptance status still needs recording** |

The 61 requests touched 221 distinct Markdown paths: 166 primary pages,
52 dated notes and three tracking records. Of the primary paths, 83 were
already in the 342 sorted skill paths, leaving the 83 outside-skill row above.
The 29 other reader-facing paths include four skill asset templates; they are
not treated as synthetic fixtures. **No per-page full-checklist acceptance
result was recorded for these batches.** This is a measurement gap, not a
claim that zero pages are satisfactory. The correction work is retained;
the next review should build on it.

For a reproducible count, take tracked `.md` paths from the exact #205 tree,
then union the changed Markdown paths in these merged readability/correction
requests. Count each path once and intersect with the current tree:

```text
119 120 122 126 127 128 133 135 138 140 141 142 144 145 146
147 149 150 151 152 154 155 156 157 158 159 160 161 163 164
165 166 167 168 169 171 172 173 175 176 178 179 181 182 183
184 186 187 188 190 191 192 193 195 196 199 200 201 202 203 205
```

The source for each request is its first-parent merge diff, including any
squash commit carrying its request number. The sorted skill screens supply
the 342 skill paths; the 44 fixture paths are under `scripts/`, except the
reader-facing `scripts/tests/fixtures/README.md`.

At the #205 progress-accounting checkpoint, the **80–200 active-hour
documentation estimate** remained a broad provisional remaining-work range.
It fell neither automatically with a request count nor
from a short residual-screen model: the latter could undercount full-page
review of long records. Before revising that historical range, measure a
representative batch of eight to ten pages across short skills, medium guides,
large roadmaps/evidence and templates. Record each page's actual active review and
correction time when available, independent reviewer result, and source
revision. Recalculate remaining effort by page type and include integration,
new-page and rework allowances. Keep active time distinct from PR wall time,
GitHub queue and owner wait. The [current forecast](aegis-backlog-forecast.md#start-here--current-reading)
holds the selected-backlog total until that measurement supports a change.

### Remaining-page review in larger batches

Use the repository's tracked Markdown inventory as the denominator. For each
batch, record the exact source revision, assigned paths, page-level result,
reviewer, correction pull request and observed time. A page has a **full-page
acceptance** result only when an independent reader checked all criteria in
[Acceptance for each page](#acceptance-for-each-page) on that revision. A
targeted correction or a sorted terminology screen is useful progress, but
must retain its narrower label until this check is done.

**Targeted edits to accepted pages (owner decision, 2026-09-27).** An
independently reviewed targeted edit that changes at most 10 lines on an
already-accepted page and adds no new section keeps that page's full-page
acceptance. A larger change, meaning more than 10 changed lines on that page
or any new section, returns the page to **pending** until an independent
reader re-reads the whole page against [Acceptance for each
page](#acceptance-for-each-page). This ledger counts changed lines as added
plus deleted lines from `git diff --numstat`, and adds together the edits a
page receives before its next full-page re-read. A renamed or renumbered
existing heading is not a new section.

**Two refinements (owner decisions, 2026-09-28).** Edits merged before the
2026-09-27 rule count toward the 10 lines, added together since the page's
last full-page acceptance. A small edit keeps acceptance only if an
independent reviewer checked it; an unreviewed edit, however small, needs a
targeted review before the page counts as accepted. Either review must cover
every changed line, by naming or reading it, and any kind of independent
review counts, such as a readability, security or fact review (owner
decision, 2026-09-29).

**Net difference (owner decision, 2026-09-28).** The 10 lines are the net
difference between the page's accepted version and now: `git diff --numstat
<acceptance> <now>` on that page, added plus deleted. They are not the sum of
every edit since acceptance, so an edit that rewrites a line already changed
since acceptance adds nothing new. Edits made before the 2026-09-27 rule still
count. This replaces the adding together described in the two paragraphs
above; entries in this ledger made before this decision used the summed count.

**Generated reports (owner decision, 2026-09-28).** A generated report is a
Markdown file written by a script, such as the
[skill-contract audit baseline report](../audits/skill-contract-audit-baseline.md),
which `scripts/audit-skill-contracts.py` produces. It is its own class, not a
reader page. Each regeneration is verified by reproducing the file from the
script, not by a full-page re-read. Its readability is judged once, on the
script's output format, and readability fixes go in the generator, not in
the file. Text written by hand into the file, such as the audit report's
regeneration preface, is not script output, so reproduction cannot verify
it; each change to it needs an independent review, as for any small edit.

**Manual-only markers (owner decision, 2026-09-28): "Mark real handoffs
only".** A manual-only skill sets `disable-model-invocation: true` in its
frontmatter, so it runs only when a person names it. A page marks such a
skill *(manual-only)* where it sends work to it: in running text, a "Do NOT
use" route or a Stop Condition. A bare mention needs no marker: a line in an
output-format template, a validation checklist item, a Supporting Files or
evaluation list, a source listed under Inputs, or a citation or contrast
that sends no work there. The owner gave this rule in chat with the
coordinating agent during the 2026-09-28 sweep, and its batch reviewers
applied it; required edits that would have marked a bare mention were
skipped.

To reduce repeated integration and hosted-check waits, group roughly 10–20
related pages in one pull request when their owners and authority boundaries
are compatible. Give up to three read-only agents disjoint page sets for
parallel review when the estimated elapsed-time saving exceeds 20 percent,
including coordination and final audit. One coordinator owns edits, shared
terms, the page ledger, conflict resolution and the final pull request.
Additional writers need separate worktrees and nonoverlapping files.

For each page, the review record must say **accepted**, **corrected and
accepted**, **needs a named follow-up**, or **classified as a synthetic
fixture**. Record the reason and an owning follow-up for anything not accepted.
Check local links and commands, run the skill validator and relevant offline
checks, obtain an independent whole-batch audit, and require the applicable
GitHub Actions before merging. Estimate the next batch from its own page mix;
report the previous ETA, new ETA, selected-backlog total and observed
first-work-to-merge wall time. Recalculate the remaining-page estimate after
each batch and the whole backlog every five merged pull requests.

This batching procedure is a work plan. It does not mark earlier screens as
full-page acceptance or grant provider, private-input, real-host or deployment
authority.

**Named page follow-up found during the batch after PR #209:**
`.claude/skills/agentic-loop-designer/SKILL.md` previously treated a second
identical transient failure as proof of a deterministic failure. The focused
correction in [the retry review record](../evidence/documentation/agentic-loop-retry-correction-2026-09-24.md)
distinguishes retry exhaustion from a proven permanent error and stops an
uncertain side effect without safe repetition. The revised page is **corrected
and accepted** after independent review; its two evaluation files were updated.
The original and current estimate were **1–2 active hours** within the
documentation range. No provider call or live retry was authorized.

| Batch | Tracked pages | Progress and remaining review |
| --- | --- | --- |
| Targeted-edit round over PRs #555, #557, #558, #559, #560 and #561, after #554, 2026-09-30 | The [backlog forecast](aegis-backlog-forecast.md), [BER backlog](behavioral-eval-runner-backlog.md), [step-0 reconciliation log](../reconciliation/step-0-reconciliation-v4.md), [AEGIS-060+ register](../audits/aegis-060-plus-register.md), [skills catalog](../skills-catalog.md), `.claude/skills/scoped-approval-register/SKILL.md`, the [approval register](../approvals/APPROVAL_REGISTER.md) and this ledger | **No acceptance was conferred, and two erroneous acceptances were corrected.** Each merge carries an independent review (#561's posted at review time, the rest retrospectively on 2026-09-30), but none is a full-page re-read against every criterion. Changed lines (`git diff --numstat`, added plus deleted): forecast 88 (#555, plus a new section), BER backlog 2 (#557), step-0 log 9 (#558), AEGIS-060+ register 3 (#559), skills catalog 10 (#560), `scoped-approval-register/SKILL.md` 10 (#561). The 10-line exemption **retains** an acceptance and cannot confer one, so the five pages that were pending gain nothing; a review is not discounted for declining a standard the rule never imposes. Two pages **move to pending**: the forecast (88 lines, past 10, so the exemption's second sentence applies) and the **approval register**, whose `accepted` line came from a prior merged PR recording a 6-line targeted review as a full-page acceptance while the page was pending (525 net since `a890669`). Main after #561 (`410b90aa`) has 653: 584 accepted readers, one generated report, 55 classified fixtures and thirteen pending. 584 + 1 + 55 + 13 = 653. This ledger changes by more than 10 lines and is **pending** an independent full-page re-read. |
| Approval-register reading aid and live-ledger reconciliation, PR #554, 2026-09-30 | The [approval register](../approvals/APPROVAL_REGISTER.md) and this ledger | The register's +4/−2 reading-aid correction was independently **accepted** on `e0c9a000`; the 98 immutable entries remained byte-identical. This round corrects the stale #542 current pointer, the omitted-ledger pending set, the classification arithmetic and the overbroad #550 empty-diff claim. Main after #554 has 653: 586 accepted readers, one generated report, 55 classified fixtures and eleven pending. This ledger changes by more than 10 lines and is **pending** an independent full-page re-read. |
| Guard coverage, README and guide re-reads, ledger and standard clarifications, register entries, CONTRIBUTING wording and control-plane delivery, PRs #543, #545, #544, #546, #547, #548, #549 and #550, after #542, 2026-09-29 to 2026-09-30 | [README](../../README.md), [CONTRIBUTING](../../CONTRIBUTING.md), the [offline CI guide](../offline-ci.md), [skill generation standard](../skill-generation-standard.md), [approval register](../approvals/APPROVAL_REGISTER.md), [resumable control-plane backlog](resumable-control-plane-backlog.md) and this ledger | README, CONTRIBUTING and the offline CI guide were **accepted** on `1c2d6f03`, `434c6835` and `640f87b9`; #549's 8-line CONTRIBUTING edit and #544's 2-line standard edit keep acceptance. The register (519) and control-plane backlog (51) stay **pending**. Main after #550 (`8ed228ee`) has 653: 586 accepted readers, one generated report, 55 classified fixtures and eleven known pending. This ledger changes by more than 10 lines and needs an independent full-page re-read. |
| Register exceptions, guard traceability, host-bridge SDK pin, standard re-read, ledger and reviewer description, PRs #537, #539, #540, #541, #538 and #542, after #531, 2026-09-29, and this update's two owner-decided edits | The [approval register](../approvals/APPROVAL_REGISTER.md), [BER backlog](behavioral-eval-runner-backlog.md), [delivery control-plane guide](../../tools/aegis_delivery_control/README.md), [host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md), [Stage 4A offline review](../evidence/setup/issue-101-package-4a-offline-review.md), [skill generation standard](../skill-generation-standard.md), `library-diff-reviewer/SKILL.md` and this ledger | The standard was **accepted** on `5e4cdd4` (pending to accepted) and this ledger on `51860f3`; `library-diff-reviewer` (4 net) keeps acceptance. The control-plane guide (15) and both evidence pages (47 and 13, each with a new section) become **pending**; the register (405) and BER backlog (149) stay pending. Main after #542 (`22a6b7a`) has 653: 583 accepted readers, one generated report, 55 classified fixtures and fourteen known pending. |
| Config-surface guards, isolated tools tests, environment parity reviewer, hash-locked CI dependencies and ledger, PRs #528, #507, #521, #524 and #534, after #525, 2026-09-29; #535 and #531 changed no Markdown | New `environment-parity-reviewer/SKILL.md` and `references/parity-matrix-sheet.md`, `iac-reviewer/SKILL.md`, two manual-only neighbour skills, `.claude/skills/_template/SKILL.md`, the [skill generation standard](../skill-generation-standard.md), [CONTRIBUTING](../../CONTRIBUTING.md), README, [offline CI guide](../offline-ci.md), skills catalog, step-0 reconciliation log and this ledger | Both new pages were **accepted** on `7f98950`; `iac-reviewer` (11 net) was re-read and **accepted** on `f5a6dab`; this ledger was **accepted** on `7b51c88`. `local-ci-mirror-preflight` (9), `vite-build-qa-engineer` (6) and the template (4) keep acceptance. The skill generation standard (11 net since #408) becomes **pending**. Main after #531 (`8dc3b00`) has 653: 585 accepted readers, one generated report, 55 classified fixtures and twelve known pending. |
| Cloud security baseline reviewer and owner grants for code-health findings P2-4 and P2-6, PRs #526 and #525, after #533, 2026-09-29 | New `cloud-security-baseline-reviewer/SKILL.md` and five baseline references, three neighbour skills, the [approval register](../approvals/APPROVAL_REGISTER.md), the [BER backlog](behavioral-eval-runner-backlog.md) and the [resumable control-plane backlog](resumable-control-plane-backlog.md) | All six new pages were **accepted** on `65bacc7`; `aws-saas-architect`, `iac-reviewer` and `security-logging-alerting-architect` (6, 7 and 6 net) keep acceptance. #525's fact-and-format reviews leave the register (184 since `a890669`), BER backlog (113) and control-plane backlog (16) **pending** full-page re-reads. Main after #525 (`a103990`) has 651: 584 accepted readers, one generated report, 55 classified fixtures and eleven known pending. |
| Backup verifier, human-in-the-loop (HITL) designer, CI classifier fixes, runbook extension, resilience reviewer and register re-read, PRs #523, #518, #529, #532, #527, #522 and #533, after #514, 2026-09-29; #530 changed no Markdown | New `database-backup-verifier`, `ai-human-in-the-loop-designer` and `resilience-architecture-reviewer` pages, `ai-governance-risk-reviewer/SKILL.md`, both `ci-failure-classifier` pages, both `data-migration-runbook-author` pages, the [approval register](../approvals/APPROVAL_REGISTER.md) and small neighbour edits | **Accepted:** the HITL pages and `ai-governance-risk-reviewer` on `288d993`; the classifier pages on `63597a0` (pending to accepted); the runbook pages on `ba190cc`; the resilience pages on `d75cd58` (pre-cleared; the merged head adds only the two named lines); the register on `a890669` (pending to accepted, until #525). `human-approval-boundary` and `agent-tool-safety-guard` keep acceptance at exactly 10. **Pending:** `database-backup-verifier/SKILL.md` (13 net since `d3dcb62`, full-page re-read owed) and its checks sheet (an unreviewed 2-line edit, targeted review owed). |
| Router adapters, prompt contract, agent-frontmatter guard, task decomposer and ledger, PRs #513, #519, #505, #517 and #514, after #515, 2026-09-29; #512 changed no Markdown | `ai-router-architect/SKILL.md`, `model-context-designer/SKILL.md` and its new template, the new `ai-task-decomposer` pages, [CONTRIBUTING](../../CONTRIBUTING.md), 11 new agent-frontmatter fixtures, this ledger and small neighbour edits | **Accepted:** the router page on `579d9ad`; both prompt-contract pages on `602adda`; both decomposer pages on `f5dfe57`; this ledger on `8f3ab5d`. The router reference, `change-classification-gate`, `project-orchestrator` and the stage-gate map keep acceptance. CONTRIBUTING (13 net since #238; security reviews only) is **pending** a full-page re-read. The 11 fixtures are classified synthetic fixtures. |
| CI failure classifier, D69 to D71, evening checkpoint, closeout trace, register APR-082 to 084, D68 page fixes and code-reviewer checks, PRs #502, #510, #509, #511, #516, #520 and #515, after #508, 2026-09-28 to 2026-09-29 | New `ci-failure-classifier/SKILL.md` and `references/classification-guide.md`, the new [evening session checkpoint](session-checkpoint-2026-09-28-evening.md), `ai-closeout-reporter/SKILL.md` and its template, the four #499 and #500 skill pages, `code-reviewer/SKILL.md` and `references/severity-rubric.md`, the [open-decisions index](aegis-open-decisions-2026-09-23.md), the [approval register](../approvals/APPROVAL_REGISTER.md), two #502 neighbour skills, README, skills catalog and step-0 log | The checkpoint (182) was **accepted** on `e46eba9`; `ai-closeout-reporter` (53 and 24) on `cce2b45`; the four #499 and #500 pages on `b0e149e` (pending to accepted); `code-reviewer` (32 and 25) on `67abe28`. The index (7 net) and the two neighbours (5 each) keep acceptance. Both new `ci-failure-classifier` pages (skill-quality reviews only) and the register (91 since `3ccac33`) are **pending**. Main after #515 (`2672b16`) has 625: 572 accepted readers, one generated report, 44 classified fixtures and eight known pending. |
| Test-plan negative paths, test-tenant provisioner and register APR-080/081, PRs #498, #500 and #508, after #496, 2026-09-28 | `test-plan-designer/SKILL.md` and `references/test-plan-template.md`, new `test-tenant-provisioner/SKILL.md` and `references/provisioning-manifest.md`, `test-data-architect/SKILL.md`, `multi-tenant-security-tester/SKILL.md`, README, skills catalog, step-0 reconciliation log and the [approval register](../approvals/APPROVAL_REGISTER.md) | The test-plan pages (28 and 39) were re-read in full and **accepted** on `e9cce7d`. #500's skill review (SHIP on `77319f8`) gave no full-page verdict, so both new pages are **pending**; the two neighbours (5 and 9 net) keep acceptance. #508 applied re-read edits E1 to E4 and **accepted** the register on `3ccac33`. Main after #508 (`d932d2c`) has 622: 568 accepted readers, one generated report, 44 classified fixtures and nine known pending. |
| Acceptance-criteria reviewer skill, report key and Phase 6 proposal, PRs #503, #499 and #496, after #504, 2026-09-28 | New `acceptance-criteria-reviewer/SKILL.md` and `references/criteria-review-sheet.md`, `product-spec-writer/SKILL.md`, README, skills catalog, step-0 reconciliation log, [AEGIS-060+ register](../audits/aegis-060-plus-register.md), generated [audit baseline report](../audits/skill-contract-audit-baseline.md) and the new [Phase 6 reliability skill batch proposal](phase6-reliability-skill-batch-proposal.md) | The Phase 6 proposal (687) was **accepted** on `d34cdb8`. #499's skill review (SHIP on `0100c2e`) gave no full-page verdict, so both new skill pages are **pending**; `product-spec-writer` (5 net) keeps acceptance, and the README and skills catalog go past 10 and become **pending**; the log stays **pending**. The register note takes the AEGIS-060+ register to 22 net: **pending**. The report's format review is done (ACCEPT on `52269aa`). |
| Forecast checkpoint and three skill batch proposals, PRs #497, #494 and #495, after #490, 2026-09-28; #504 and #506 changed no Markdown | [Backlog forecast](aegis-backlog-forecast.md), [execution measurements](aegis-execution-metrics.md), the new [AI-SDLC](ai-sdlc-skill-batch-proposal.md) and [Phase 7](phase7-ai-engineering-skill-batch-proposal.md) skill batch proposals | Forecast (198) and measurements (132): FIX-FIRST on `23a1a7c`, **accepted** on `826f40b`. The proposals (554 and 548) got FIX-FIRST first reads and were **accepted** on `a87e2c9` and `6d51c8d`. |
| Link fix, register APR-079, QA Tier 1 proposal, gate-guard fix, D68 and ledger, PRs #489, #491, #492, #501, #493 and #490, after #488, 2026-09-28 | Final 16 references review record, [approval register](../approvals/APPROVAL_REGISTER.md), new [QA Tier 1 skill batch proposal](qa-tier1-skill-batch-proposal.md), [offline CI guide](../offline-ci.md), [open-decisions index](aegis-open-decisions-2026-09-23.md), step-0 reconciliation log and this ledger | The review record (2) keeps acceptance after a PASS on `10147d4`. The register (74 since `2a411fd`; SHIP on `351f5de`) became **pending** until #508 (row above). The QA Tier 1 proposal (597) was **accepted** on `930493c`. The offline CI guide (14) and the step-0 log (55, the D68 entry) are **pending**. The index (16 net) was **accepted** on `b6e82e4`, and this ledger on `49f4804`. |
| `ai-evaluation-harness` re-read fixes, PR #488, after #486, 2026-09-28 | `.claude/skills/ai-evaluation-harness/SKILL.md` | 14 lines. A full-page re-read on `2a411fd` asked for E1 to E5; a corrected-candidate full-page review **accepted** it on `e225c2f`, which matches main. Main after #488 (`ebf210c`) has 614: 569 accepted readers, one generated report, 44 classified fixtures and zero known pending. |
| "AI" spelled out at first body use, PR #486, after #485, 2026-09-28 | 64 existing reader pages, one line each | Owner decision "Spell it out everywhere". FIX-FIRST on `8459ac7` (one missed line), then **ACCEPT** on `2f28cc7`. By net count only `.claude/skills/ai-evaluation-harness/SKILL.md` went past 10 (12), which #488 then fixed. The others are at 10 or fewer and keep acceptance. |
| Session checkpoint and open decisions, PRs #487 and #485, after #484, 2026-09-28 | [Open-decisions index](aegis-open-decisions-2026-09-23.md) and the new [2026-09-28 session checkpoint](session-checkpoint-2026-09-28.md) | The index is exactly 10 net since `08f99eb`; a targeted review **accepted** it on `44550cd`. The checkpoint (177, new) got FIX-FIRST on `7d33df0` and was **accepted** on `04d2ce8`. |
| Orchestrator labels and stage-gate map, PR #484, after #483, 2026-09-28 | `project-orchestrator/SKILL.md` and `ai-sdlc-operating-model/references/stage-gate-map.md` | 14 and 6. A full-page re-read of the orchestrator on `2f5858c` returned FIX-FIRST; the corrected-candidate review **accepted** both on `ad927f7`, which matches main. |
| ADR writer re-read and reviewer follow-ups, PRs #482 and #483, after #479, 2026-09-28 | `adr-writer/SKILL.md`, `code-reviewer/SKILL.md` and six pages in #483 | `adr-writer` (20) got a full-page re-read and **ACCEPT** on `f275356`, so it is accepted again. The `code-reviewer` description edit (2) and #483's six one-line edits passed targeted reviews on `f275356` and `44c4834`; each page is at 10 or fewer net. |
| Approval register reading aid and APR-077/078, PRs #481 and #479, after #477, 2026-09-28 | [Approval register](../approvals/APPROVAL_REGISTER.md) | #481 (7) applied R1 and R2 from a full-page re-read on `8f3d369`, **accepted** on `98eb638`. #479 appended 51 (SHIP on `b7570af`), and a full-page re-read on `2a411fd` returned **ACCEPT**, so the register is accepted again. |
| Small-edit fixes, forecast checkpoint and ledger, PRs #480, #478 and #477, after #476, 2026-09-28 | 11 small-edit pages, the [backlog forecast](aegis-backlog-forecast.md), the [execution measurements](aegis-execution-metrics.md) and this ledger | #480 (46) passed on `9c918ed`; all 51 small-edit pages now have a recorded review. The forecast and measurements were **accepted** on `cf86dab`, and this ledger on `66521f4`. |
| BER guide and host pages, PRs #475 and #476, after #474, 2026-09-28 | [Behavioral Eval Runner guide](../../tools/behavioral_eval_runner/README.md), [BER selected host capability decision](ber-selected-host-capability-decision.md) and [VirtualBox Stage A setup proposal](ber-virtualbox-stage-a-setup-proposal.md) | The guide (17) was **accepted** on `acdcdad` under the one-time `gate-guard` exception AEGIS-APR-077, so it is accepted again. Full-page re-reads **accepted** both host pages on `5f08b3e`, which settles their weak acceptance record. |
| Pre-rule sweep batch fixes, PRs #466 to #474, after #465, 2026-09-28 | 83 changed pages in nine batches, 14 accepted with no edit, and the [Behavioral Eval Runner guide](../../tools/behavioral_eval_runner/README.md) | The owner-ordered sweep returned 103 of 558 accepted pages to pending on `5bd21fb`. Corrected-candidate reviewers **accepted** every changed page on its merged head: #466 `dac42f3`, #471 `67f577e`, #473 `8c6750a`, #467 `eb3ec53`, #474 `14ecd0c`, #472 `6ba6e1a`, #470 `2a86058`, #469 `61ca130` and #468 `54034fa`. 14 pages passed the first full-page read with no edit; all 14 are named as accepted on GitHub, seven of them in comments posted on #469 and #470 after #474 merged. The guide's six edits were held back for a protected-path exception, so it stays **pending**. With #456, #459 and #462, 102 of the 103 are accepted again. Main after #474 (`2be0a77`) has 613: 565 accepted readers, one generated report, 44 classified fixtures and three known pending. No grant or gate changed. |
| Register APR-074 to APR-076, PR #465, after #457, 2026-09-28 | [Approval register](../approvals/APPROVAL_REGISTER.md) | 78 lines appended; SHIP on `ab430ad` after one REVISE edit. It checked facts and format, not the whole page, so the register stays **pending** with 78 since `e6d0f6a`. |
| Forecast and measurement checkpoint, PR #457, after #460, 2026-09-28 | [Backlog forecast](aegis-backlog-forecast.md) and [execution measurements](aegis-execution-metrics.md) | 238 and 285 lines. A full-page review on `86d891e` returned FIX-FIRST (F1 to F7, M1 to M3); a corrected-candidate check **accepted** both on `676bc3d`, which matches main. |
| Later owner decisions, PR #460, after #464, 2026-09-28 | [Open-decisions index](aegis-open-decisions-2026-09-23.md) | 27 lines. A full-page re-read on `36be74b` returned FIX-FIRST; after targeted checks of two fix commits, a one-line check **accepted** it on `08f99eb`, which matches main. |
| Register reading-aid fixes, PR #464, after #463, 2026-09-28 | [Approval register](../approvals/APPROVAL_REGISTER.md) | 18 lines from a full-page re-read on `4226d29` that #464's description reports but no comment posts. A corrected-candidate review **accepted** the edits on `e6d0f6a`. #465 later added 78, so the register stays **pending**. |
| Re-read fixes, PR #463, after #458, 2026-09-28 | `ai-sdlc-operating-model/SKILL.md` and `references/stage-gate-map.md` | 15 and 22 lines, after #455's 11 and 16. A corrected-candidate reviewer re-read both in full and **accepted** them on `6306232`, which matches main. |
| Ledger for #443 to #454, PR #458, after #462, 2026-09-28 | This ledger | 109 lines. A full-page re-read on `5978b33` pre-cleared three edits; `9cdfdf8` is exactly those, so the ledger is **accepted** on `9cdfdf8`. |
| Re-read fixes, PR #462, after #461, 2026-09-28 | `ai-closeout-reporter/SKILL.md` and `assets/closeout-template.md` | 6 and 3 lines, after #455's 32 and 25. A corrected-candidate re-read of both in full **accepted** them on `e569a3c`, which matches main. |
| Audit report format, engine v1.13.3, PR #461, after #459, 2026-09-28 | [AEGIS-060+ register](../audits/aegis-060-plus-register.md) and the generated [audit baseline report](../audits/skill-contract-audit-baseline.md) | Register note (10): the SHIP review on `ae719e6` verified its facts, so the register **keeps acceptance** (10 since `04af9d9`). Report (76): reproduced byte for byte and its preface reviewed; it stays a generated report, format review pending. The script, test and JSON baselines are not Markdown. |
| Re-read fixes, PR #459, after #456, 2026-09-28 | `ai-cost-guardrail-designer/SKILL.md` and `streaming-event-architect/SKILL.md` | 10 and 11 lines. A corrected-candidate full-page re-read **accepted** both on `378089f`, which matches main. Both were sweep pages. |
| Re-read fixes, PR #456, after #455, 2026-09-28 | `tenant-modeler/SKILL.md` and `source-of-truth-reconciler/SKILL.md` | 13 and 10 lines. A corrected-candidate full-page review **accepted** both on `620b245`, which matches main. Both were sweep pages. |
| D15 enrichment deltas, PR #455, after #453, 2026-09-28 | Eight pages in `ai-closeout-reporter`, `ai-sdlc-operating-model`, `adr-writer` and `agent-memory-governance` | SHIP on `16bb924`. Four pages went past 10 and were accepted again in #462 and #463. `agent-memory-governance/SKILL.md` (8), `references/memory-rules.md` (8) and `adr-writer/assets/adr-template.md` (7 in all) **keep acceptance**. `adr-writer/SKILL.md` (13: 5 before and 8 here) becomes **pending**. The evaluation JSON is not Markdown. |
| Register APR-071 to APR-073, PR #453, after #454, 2026-09-28 | [Approval register](../approvals/APPROVAL_REGISTER.md) | 118 lines appended; SHIP on `5be36b3` after one REVISE. Not a full-page read; the register stays **pending**. |
| Orchestrator Stage 6 markers, PR #454, after #452, 2026-09-28 | `project-orchestrator/SKILL.md` | 8 lines (+4/−4) after the #452 acceptance on `469d6cb`. The SHIP review on `6118210` checked them, so the page **keeps acceptance** (8 since `469d6cb`). Main after #454 (`5bd21fb`) has 613: 567 accepted readers, one generated report, 44 classified fixtures and one known pending. No grant or gate changed. |
| Orchestrator glosses, PR #452, after #443, 2026-09-28 | `project-orchestrator/SKILL.md` | 40 lines. A full-page review on `90849c1` returned FIX-FIRST with two edits; a re-review **accepted** the page on `469d6cb`. It had been pending since #442 (50 lines, counting pre-rule edits). |
| Setup-node action bump, PR #443, after #451, 2026-09-28 | None | Changed only `.github/workflows/validate-skills.yml` (4 lines), which is not Markdown. |
| Skills catalog glossary, PR #451, after #449, 2026-09-28 | [Skills catalog](../skills-catalog.md) | 90 lines. A full-page review on `39a86e2` returned FIX-FIRST with four edits; a corrected-candidate re-read **accepted** it on `2e15b23`, which matches main. |
| Audit and evidence readability, PR #449, after #448, 2026-09-28 | AEGIS-060+ register, live startup-routing acceptance record and the audit report preface | Register (30) **accepted** on `04af9d9` after a FIX-FIRST on `5037d6a`; record (11) **accepted** on `5037d6a`, unchanged since. The report's hand-written preface (12) was reviewed and accepted on `5037d6a`; the report stays a generated report, format review pending. |
| Register reading aid and closeout events, PRs #450 and #448, after #447, 2026-09-28 | [Approval register](../approvals/APPROVAL_REGISTER.md) | #448 (81): a full-page review on `3b9d74e`, then corrected-candidate re-reads, accepted the reading aid on `2ee1050`. #450 (92, APR-067 to APR-070) merged first and is not in `2ee1050`; its SHIP review was not a full-page readability read. 92 lines since the full-page acceptance, so the register stays **pending**. |
| Open decisions and PR template fixes, PR #447, after #446, 2026-09-28 | [Open-decisions index](aegis-open-decisions-2026-09-23.md) and `.github/pull_request_template.md` | Index (55) and template (8): a full-page read on `7fc2fd6` accepted the template and returned FIX-FIRST on the index; a corrected-candidate check **accepted** both on `420f823`, which matches main. |
| Ledger for #438–#442, PR #446, after #445, 2026-09-28 | This ledger | 121 lines. A full-page re-read on `7a5b534` pre-cleared four named edits; `47c78cb` is exactly those, so the ledger is **accepted** on `47c78cb`. |
| Re-read fixes to three skill pages, PR #445, after #450, 2026-09-28 | `api-event-architect/SKILL.md`, `llm-top10-threat-catalog.md` and `poisoning-controls.md` | 8, 12 and 10 lines. A full-page review on `c5571a7` accepted two and asked one edit on the third; a corrected-candidate re-read **accepted** all three on `07d002a`, which matches main. |
| Session checkpoint, PR #442, after #441, 2026-09-28 | New [session checkpoint page](session-checkpoint-2026-09-27.md); approval register and open-decisions index | After a REVISE review and its four named edits, a corrected-candidate check **accepted** the new page on `63387ef`, which matches main. The approval register (21) and open-decisions index (3) stay **pending**. Under the owner's 2026-09-28 decisions, `project-orchestrator/SKILL.md` (50 lines, counting pre-rule edits) becomes **pending**, `CONTRIBUTING.md` keeps acceptance after a targeted review, and the audit baseline report moves to the generated-report class. Main after #442 (`7b3fbca`) has 613: 558 accepted readers, one generated report, 44 classified fixtures and ten known pending. No grant or gate changed. |
| Audit baselines regenerated with engine v1.13.2, PR #441, after #440, 2026-09-27 | AEGIS-060+ register and the generated [audit baseline report](../audits/skill-contract-audit-baseline.md) | SHIP review on `d864597` reproduced the regenerated files; it was not a full-page review. The register (44 with earlier edits) stays **pending**. Under the owner's 2026-09-28 decision the report is a generated report: the reproduction verifies it, and its output format awaits one review. The three JSON baselines are not Markdown. |
| Ledger for #420–#439, PR #440, and register lifecycle events, PR #438, after #439, 2026-09-27 | This ledger; approval register and open-decisions index | The ledger's review pre-cleared acceptance for one named edit, and `f9e5325` is exactly that edit, so the ledger is **accepted** on `f9e5325`. #438 added 171 lines to the approval register and 30 to the open-decisions index; both stay **pending**. |
| Reconciliation log D65 closure, PR #439, after #434, 2026-09-27 | `docs/reconciliation/step-0-reconciliation-v4.md` | An independent full-page re-read **accepted** the log on `97c8682`, which matches main; it had been pending since #405, and #423 had added 27 lines. Main after #439 (`d2d9b05`) has 612: 558 accepted readers, 44 classified fixtures and ten known pending. No grant or gate changed. |
| Upload and tool-matrix fixes, PR #434, after #437, 2026-09-27 | `file-upload-storage-architect/SKILL.md` and `agent-tool-safety-guard/references/tool-permission-matrix.md` | Past 10 lines (18 and 20), so both needed full-page re-reads; independent reviews **accepted** the skill on `3c44f4a` and the matrix on `356932a`, both matching main. |
| README glossary and routing citation, PRs #430 and #437, after #436, 2026-09-27 | [README](../../README.md) | #430: after two FIX-FIRST rounds the reviewer pre-cleared acceptance for two named one-line edits, and `b6b4b4e` contains exactly those, so the README is **accepted** on `b6b4b4e`. #437 (SHIP) changed 2 lines; it **keeps acceptance**. |
| Orchestrator setup pointer, PR #435, and ROUTE-002 recount, PR #436, 2026-09-27 | `project-orchestrator/SKILL.md`; ROUTE-002 dispositions record and AEGIS-060+ register | SHIP reviews. The orchestrator (1) and dispositions record (2) keep acceptance; the AEGIS-060+ register becomes **pending** (29 with #432). |
| Output-safety, promoted-model and multimodal-injection skills, PRs #424, #428 and #427, 2026-09-27 | Three `SKILL.md` pages, four reference sheets (one new), `code-reviewer/SKILL.md`, the threat catalog and the skills catalog | Full-page reviews **accepted** both `llm-output-safety-reviewer` pages (`af328b5`), both `supply-chain-security-reviewer` pages (`3787f74`, checklist `9c9a669`) and both `prompt-injection-defender` pages including the new multimodal sheet (`633304b`). `code-reviewer` (10) and `injection-defense-patterns.md` (6) keep acceptance; the skills catalog (15), `llm-top10-threat-catalog.md` (18) and `poisoning-controls.md` (16) become **pending**. |
| Live startup-routing record, PR #433, after #428, 2026-09-27 | New [live startup-routing acceptance record](../evidence/startup-routing/2026-09-live-acceptance.md) | Evidence and grant-scope review SHIP on `339ac90`, which matches main; no full-page verdict, so the new page is **pending**. |
| Ledger catch-up, PR #426, after #432, 2026-09-27 | This ledger | A corrected-candidate full-page re-read **accepted** it on `6fb5811`, which matches the ledger on main before this update. |
| Audit baselines regenerated, PR #432, and ROUTE-002 engine fix, PR #429, 2026-09-27 | Approval register, AEGIS-060+ register and the generated [audit baseline report](../audits/skill-contract-audit-baseline.md) | #429 changed scripts only. #432's review reproduced the regenerated files but was not a full-page review: the approval register (76 with #420), the AEGIS-060+ register (24) and the report (253) become **pending**. The three JSON baselines are not Markdown. |
| Owner decisions, contribution rules, D67 and BER guide, PRs #420, #421, #423, #425 and #431, after #416, 2026-09-27 | Approval register, open-decisions index, `CONTRIBUTING.md`, `.github/pull_request_template.md`, README, skills catalog, step-0 log and Behavioral Eval Runner guide | Only #425 (SHIP) and #431 (SHIP) posted review verdicts. `CONTRIBUTING.md` (7) and the BER guide (7) keep acceptance; the open-decisions index (35) and pull request template (12) become **pending**. The README, catalog, register and log are counted in the rows above. |
| Hidden-context and tool-guard re-read fixes, PR #422, after #425, 2026-09-27 | `hidden-context-exposure-reviewer/SKILL.md` and `references/hidden-context-checks.md`; `agent-tool-safety-guard/SKILL.md` | A corrected-candidate full-page re-read **accepted** all three pending pages on `379c588`, which matches main. |
| ROUTE-002 record and register re-read fixes, PR #416, after #415, 2026-09-27 | [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md) and [AEGIS-060+ register](../audits/aegis-060-plus-register.md) | Minimal edits from a full-page re-read (FIX-FIRST); a separate independent corrected-candidate review **accepted** both on `a548dcb`, which matches main. Main after #416 (`da2636d`) has 610: 560 accepted readers, 44 classified fixtures and six known pending. No grant or gate changed. |
| OWASP security page re-read fixes, PR #415, after #413, 2026-09-27 | In `.claude/skills/`: `ai-threat-modeler/SKILL.md` and its `references/llm-top10-threat-catalog.md`, `rag-security-architect/SKILL.md`, `ai-misinformation-guard/SKILL.md`, `model-poisoning-reviewer/SKILL.md` and `supply-chain-security-reviewer/SKILL.md` | Minimal edits from full-page re-reads (FIX-FIRST); separate independent corrected-candidate full-page reviews **accepted** all six on `79cee79`, which matches main. |
| Master-prompt citation fix, PR #413, after #403, 2026-09-27 | [Skills catalog](../skills-catalog.md) and seven skill pages: six `SKILL.md` pages (2 lines each) and `threat-modeler/references/threat-catalog.md` (4) | The catalog (20 lines) received an independent full-page re-read on `2ceea06`, which matches main, and is **accepted**. The seven skill pages keep acceptance under the targeted-edit rule; the largest totals, 8 lines, are `security-pr-reviewer` and `static-analysis-reviewer` with #395 and #417. |
| Use When hand-back bullets, PRs #419, #417 and #418, after #414, 2026-09-27 | 27 `SKILL.md` pages (10, 11 and 6), 3–7 lines each | Independent reviews returned SHIP, not full-page reviews. Under the targeted-edit rule 25 pages keep acceptance (largest 8); `api-event-architect/SKILL.md` (12 with #385 and #396) and `llm-output-safety-reviewer/SKILL.md` (11 with #396 and #405) become **pending**. `human-approval-boundary/SKILL.md` keeps its #410 acceptance (4 lines since). |
| Instruction map, decision inputs and log re-read fixes, PR #414, after #412, 2026-09-27 | `instruction-file-map.md`, `cloud-architecture-decider/references/decision-inputs.md` and `docs/reconciliation/step-0-reconciliation-v4.md` | Full-page corrected-candidate reviews **accepted** the map and decision inputs on `bd3219f`, which matches main for both. The log's review covered only its banner, new "How to read this log" paragraph and historical-edition note, so it stays **pending** (83 lines since its last acceptance). |
| README re-read fixes, PR #412, after #410, 2026-09-27 | [README](../../README.md) | Minimal edits from a full-page re-read; a separate independent corrected-candidate review **accepted** it on `ecbd860`, which matches main. |
| Four-page re-read fixes, PR #410, after #397, 2026-09-27 | In `.claude/skills/`: `multi-tenant-data-architect/SKILL.md`, `ci-pipeline-architect/SKILL.md`, `human-approval-boundary/SKILL.md` and `cloud-architecture-decider/references/managed-platform-tier.md` | Minimal edits from full-page re-reads; separate independent corrected-candidate reviews **accepted** all four on `a56c60d`, which matches main. |
| ROUTE-002 census dispositions, PR #397, after #411, 2026-09-27 | New [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md) (plus a JSON data file), the [AEGIS-060+ register](../audits/aegis-060-plus-register.md) and the step-0 reconciliation record's D64 amendment | No full-page review was recorded at merge. The new record is **pending** until a full-page re-read. The AEGIS-060+ register becomes **pending** (21 lines). The step-0 reconciliation record gained 8 lines and was already pending (64 since its last acceptance). Main after #397 (`4a68ace`) has 610: 546 accepted readers, 44 classified fixtures and 20 known pending. No grant or gate changed. |
| Catalog and cloud decider re-read fixes, PR #411, after #409, 2026-09-27 | [Skills catalog](../skills-catalog.md) and `.claude/skills/cloud-architecture-decider/SKILL.md` | Full-page re-reads of both pages: the first review returned FIX-FIRST; after minimal edits a separate independent corrected-candidate review **accepted** both on #411's branch head (`4e643c6`). `cloud-architecture-decider/SKILL.md` on main matches that head and is **accepted**. The head did not contain #409's 11-line catalog edit (7 added, 4 deleted), so the catalog on main stays **pending** under the targeted-edit rule. Main after #411 (`7693c26`) had 609: 547 accepted readers, 44 classified fixtures and 18 known pending. |
| LLM08 skill extended and renamed, PR #409, after #408, 2026-09-27 | New `.claude/skills/hidden-context-exposure-reviewer/SKILL.md` and `references/hidden-context-checks.md`, replacing the two accepted `system-prompt-leakage-reviewer` pages (D66); nine existing reader pages | The independent review was a skill review whose REVISE verdict asked for two edits, not a full-page review, so both new pages are **pending**. `agent-tool-safety-guard/SKILL.md` becomes **pending** (17 lines with #405). `prompt-injection-defender/SKILL.md` (8), `sensitive-disclosure-guard/SKILL.md` (6) and `ai-evaluation-harness/references/eval-harness-design.md` (5) keep acceptance. The README (167), skills catalog (77), `ai-threat-modeler/SKILL.md` (25), its threat catalog (121) and the step-0 reconciliation record (56) were already pending. Main after #409 (`4416c6d`) had 609: 546 accepted readers, 44 classified fixtures and 19 known pending. |
| Skill authoring standard, PR #408, after #406, 2026-09-27 | `docs/skill-generation-standard.md` | Codified the owner's 2026-09-27 one-missing-fact-per-turn loop in §4, defined `when_to_use` in §2, dated the D49 measurement and aligned the §6 census wording with `census.py`; §5 unchanged. A first independent full-page review returned FIX-FIRST (three edits plus the optional D49 date); a separate independent corrected-candidate review **accepted** it against Acceptance for each page. |
| Skill template, PR #408, after #406, 2026-09-27 | `.claude/skills/_template/SKILL.md` | Workflow's missing-fact sentence aligned with standard §4; full-page re-read in the same corrected-candidate review **accepted** it. No Markdown file added; count unchanged. Main after #408 (`0533764`) has 609: 549 accepted readers, 44 classified fixtures and 16 known pending. |
| Targeted-edit rule applied to PRs #404–#406, after #407, 2026-09-27 | 30 existing reader pages and this ledger: the agent instruction file map in #404; 11 `SKILL.md` pages, 13 reference sheets, the README, the skills catalog and the step-0 reconciliation record in #405; `.claude/skills/cloud-architecture-decider/SKILL.md`, its `references/decision-inputs.md` and the README in #406 | No full-page review was recorded for these merges. Counting added plus deleted lines per page and adding together every edit since the page's last full-page acceptance, 18 pages stay accepted and nine become **pending**: `instruction-file-map.md` (19), `ai-misinformation-guard/SKILL.md` (12), `ai-threat-modeler/SKILL.md` (21), `llm-top10-threat-catalog.md` (115), `model-poisoning-reviewer/SKILL.md` (15), `rag-security-architect/SKILL.md` (14), `supply-chain-security-reviewer/SKILL.md` (18), `docs/reconciliation/step-0-reconciliation-v4.md` (14) and `cloud-architecture-decider/references/decision-inputs.md` (12, previously kept). The README (165), skills catalog (66) and `cloud-architecture-decider/SKILL.md` (204) stay pending. By owner decision (2026-09-27) a renamed existing heading is not a new section; #405 added no section. No Markdown file added: main after #406 (`6488eaa`) had 609: 548 accepted readers, 44 classified fixtures and 17 known pending. No grant or gate changed. |
| Targeted-edit rule applied to PRs #385, #389, #392, #393, #398–#402 and #407, after #396, 2026-09-27 | 11 existing reader pages, one new page and this ledger: five `SKILL.md` pages in #385, the README and skills catalog in #389, the README in #392, `.claude/skills/cloud-architecture-decider/SKILL.md`, its `references/decision-inputs.md`, the README and skills catalog in #393, which also added `references/managed-platform-tier.md`, and the [skill generation standard](../skill-generation-standard.md) and one reference sheet in #402 | No full-page review was recorded for these merges. Under the owner's 2026-09-27 targeted-edit rule, counting added plus deleted lines per page and adding together every edit since the page's last full-page acceptance, four pages stay accepted and eight are **pending**: the README (111 lines), skills catalog (16), skill generation standard (15), `cloud-architecture-decider/SKILL.md` (198), `multi-tenant-data-architect/SKILL.md` (22), `ci-pipeline-architect/SKILL.md` (13), `human-approval-boundary/SKILL.md` (11) and the new managed-platform sheet. No edit added a heading to an existing page. #398–#401 and #407 changed evaluation JSON only. Main after #407 (`1ec01bf`) has 609: 557 accepted readers, 44 classified fixtures and eight known pending; the named follow-up is one independent full-page re-read of each pending page. No grant or gate changed. |
| Targeted corrections to accepted pages merged in PRs #388, #390, #394, #395 and #396, after #386, 2026-09-27 | 37 existing reader pages: seven in #388 (six skill reference sheets and `.claude/skills/supply-chain-security-reviewer/SKILL.md`), six in #390 (`README.md`, [skills catalog](../skills-catalog.md) and four reference sheets) and 24 `SKILL.md` pages in #394–#396, and this ledger | #388 marked volatile facts, #390 dated and verified standards and edition anchors, and #394–#396 added one hand-back clause to each of 23 target skills' frontmatter descriptions and corrected one source description (`data-migration-runbook-author`, #396) under the owner's 2026-09-26 ROUTE-002 decision, adding trigger-evaluation cases for seams that lacked one (five trigger-evaluation files). The changed passages were reviewed before merge as targeted corrections, not full-page reviews. Under the owner's 2026-09-27 targeted-edit rule each edit changed at most 10 lines on its page (added plus deleted) and added no section, so the pages kept their earlier full-page acceptance and counts were unchanged; later merges returned the README, the skills catalog and `.claude/skills/human-approval-boundary/SKILL.md` to pending (row above). #391 changed evaluation JSON only. No Markdown file was added: main after #396 had 608: 564 accepted readers, 44 classified fixtures and zero known pending. No grant or gate changed. |
| Full-page review of construction history skill-count dating, after #383, 2026-09-26 | [Construction history](../HISTORY.md) and this ledger | The library-meta (D13) and OWASP gap-closure (D28) claims now read in the past tense, D63 is dated, and the 2026-09-12 update states the D47 total of 184 and the unfinished calibration (inputs unavailable, OD-1 open, WP-2B-4 blocked) as of that update. It routes readers to the skills catalog, the README's library overview and the BER backlog start-here table. An independent read-only full-page review checked every acceptance criterion and accepted the page with no edits; all 12 relative links and anchors resolve. The page was already accepted, so counts are unchanged. No skill, grant or gate changes. |
| Final full-page check of pages merged in PR #383, after #387, 2026-09-27 | `.claude/skills/feature-flag-architect/SKILL.md`, `.claude/skills/feature-flag-architect/references/flag-system-sheet.md` and this ledger | Round 1: an independent full-page review returned FIX-FIRST for terms not defined at first use; PR #387 applied its minimal edits (term definitions on both pages). Round 2: a separate corrected-candidate review returned FIX-FIRST for one edit, the sheet's claim to serve Workflow steps 2–9, corrected in #387's final commit `037f883` to steps 2, 4 and 6–9. Round 3: a final independent read-only check of both pages on main after #387 checked every acceptance criterion and **accepted both** with no further edits; the step list matches the sheet's section headings, every named skill, evaluation case and trigger-evaluation discrimination target exists, and both relative links resolve. The #383 tree had 608 pages with two known pending; main after #387, #379 and #386 has 608: 564 accepted readers, 44 classified fixtures and zero known pending. No skill behavior, grant or gate changed. An independent full-page review then **accepted this ledger change**, including this paragraph and its batch row, against [Acceptance for each page](#acceptance-for-each-page). |
| Ledger gap for pages merged in PR #383, found during the #379 reconciliation, 2026-09-27 | `.claude/skills/feature-flag-architect/SKILL.md`, `.claude/skills/feature-flag-architect/references/flag-system-sheet.md` and this ledger | Two new skill reader pages (the 186th skill's entrypoint and its reference sheet), not synthetic fixtures. #383 recorded a skill-quality and library-diff review but no full-page acceptance, so both are **pending**; the named follow-up is one independent full-page review. The #381 tree had 606 pages; the #383 tree has 608: 562 accepted readers, 44 fixtures and two known pending. |
| Catch-up forecast checkpoint after #370, 2026-09-26 | [Backlog forecast](aegis-backlog-forecast.md), [execution measurements](aegis-execution-metrics.md), [open-decisions index](aegis-open-decisions-2026-09-23.md) and this ledger | Three changed existing reader pages plus this ledger, no new page: a new catch-up checkpoint section in the forecast and measurements, and dated decided, still-open and owner-requested items in the index. #352 had also changed the forecast and measurements. A first independent full-page review returned FIX-FIRST (stale S5 horizon, inconsistent feature-flag status, batch-count arithmetic, open-PR list); after its minimal edits all three pages are re-accepted after a separate corrected-candidate review against every acceptance criterion. A Codex-driven follow-up revision of all four pages then returned FIX-FIRST and was accepted, with this ledger, by a corrected-candidate review; a 2026-09-27 reconciliation recorded #378, #375, #376, #377, #371, #381, #383 and #384 (see [Start here](#start-here--current-reading)). Links and anchors resolve. Main after #381 had 606 pages: 562 accepted readers, 44 classified fixtures and zero known pending; this checkpoint adds none, and #383's two pending pages have their own row. |
| Full-page review of feature-flag skill scope proposal, after #370, 2026-09-26 | [Feature-flag system skill proposal](feature-flag-architect-skill-proposal.md) and this ledger | A first independent full-page review returned FIX-FIRST; its minimal edits corrected the highest decision number seen on `main` to D63 and defined `project-orchestrator` stages (2, 3, 8, 9) and the Use When and Stop Conditions skill sections at first use, and a corrected-candidate review accepted the page. Fixes for eight Codex findings on PR #378 then changed it materially: the tenant early-access case names the override data model (strategist should not trigger), the draft description yields cross-tenant leak reviews to `tenant-isolation-reviewer` (1,020 characters; the strategist draft stays 943), the store step is skipped when a store is already adopted, the orchestrator asks staged release and fast shutdown as two queued atomic questions, merges follow AEGIS-APR-048 to 050, and the premature check 1 pass is removed. The owner's 2026-09-26 decisions are recorded: PR 2 adds the Stage 9 route, PR 1 adds a D64 row, the `caching-strategy-designer` seam stays as cases 15 and 16, and the four hub ROUTE-002 findings stay census data. An independent re-review returned FIX-FIRST; its one minimal edit aligned the merge step with AEGIS-APR-050's Codex-unavailable path and defined Codex, P1/P2 and `gate-guard`. A separate independent corrected-candidate review accepted the page against every acceptance criterion. Links and anchors resolve. The candidate has 606 pages: 562 accepted readers, 44 classified fixtures and zero known pending. No skill is built and no grant is added. |
| Full-page review of skill-contract disposition record, after #360, 2026-09-26 | [Candidate dispositions](../evidence/skill-contract-dispositions-2026-09-26/candidate-dispositions.md) and this ledger | A first independent full-page review returned FIX-FIRST; its minimal edits added the audience, a linked audit engine, first-use definitions for semantic candidate, fingerprint, EVAL-002, STATE-001, P0, architecture decision record (ADR) and continuous integration (CI), corrected the adr-sequencer prior disposition to confirmed-fixed, and linked skill-quality-reviewer check 7. A separate independent corrected-candidate review accepted the page against every acceptance criterion; no disposition changed: five false positives, four drift-same, zero defects, no skill text changed. Links and anchors resolve. The tree has 605 pages: 561 accepted readers, 44 classified fixtures and zero known pending. |
| Full-page review of page merged in PR #335, after #354, 2026-09-26 | [Stage 4B synthetic case fixture draft](aegis-setup-package-4b-synthetic-case-fixtures.md) and this ledger | A first independent full-page review returned FIX-FIRST; its nine minimal edits added the audience and Stage 4B/4A purpose, first-use expansions for SDK, VM and CLI, glosses for `canUseTool` and `UserPromptExpansion`, register links for APR-031 and APR-040, and the F0n-to-case-0n mapping. A separate independent corrected-candidate review accepted the page against every acceptance criterion; no claim changed: all eight cases remain NOT RUN, nothing is host proof, and no grant, fixture or host statement was altered. Links and anchors resolve. The tree stays at 604 pages: 560 accepted readers, 44 classified fixtures and zero known pending. |
| Ledger gap for page merged in PR #335, found after #347, 2026-09-26 | [Stage 4B synthetic case fixture draft](aegis-setup-package-4b-synthetic-case-fixtures.md) and this ledger | One reader page, not a synthetic fixture: an offline planning draft whose eight cases are all NOT RUN and which is not host proof. No full-page acceptance is recorded, so it is **pending**; the named follow-up is one independent full-page review. The #333 tree had 603 pages; the #347 tree has 604: 559 accepted readers, 44 fixtures and one known pending. |
| BER selected-precheck aggregate decision candidate after merged #330, 2026-09-26 | [Owner decision proposal](ber-precheck-aggregate-validation-proposal.md) and this ledger | One new reader page; synthetic reproduction, two-path proposed implementation, explicit non-grant boundary and local links were accepted in independent full-page technical/readability review after first-use terms were explained. The merged #330 tree has 601 pages: 557 accepted readers and 44 classified fixtures. This reviewed candidate has 602 pages: 558 accepted readers, 44 fixtures and zero known pending. No source implementation or merge is included. |
| Issue #101 public archive packet merged in PR #271, 2026-09-25 | [Host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md) and [Stage 4A proposal](aegis-setup-package-4a-host-preparation-proposal.md) | Two existing reader pages were revised for the 110-entry and preferred 107-entry static archive checks. Two independent full-page reviews accepted the corrected pages and their links. Local checks and exact-head GitHub Actions passed before merge. The merged tree stayed at 589 tracked Markdown files: 545 accepted reader pages, 44 classified fixtures and zero known pending. |
| Current-reading follow-up merged in PR #253 after #252, 2026-09-24 | [BER-BKL-009A historical proposal](ber-bkl-009a-offline-policy-scope-proposal.md) and root `AGENTS.md` | The proposal's current-status banner was corrected from an unmerged #139 claim to its verified merge and partial BKL-009 status; the historical proposal below remains unchanged. The source-library skill-use preference added in #252 received two independent read-only reviews, preserving Role A scope, the manual-only boundary and user authority. Both existing pages retain accepted status. |
| BER evidence-policy scope and candidate-summary follow-up merged in PR #253, 2026-09-24 | [BER-BKL-009 scope proposal](ber-bkl-009-policy-scope-amendment-proposal.md) and [replacement candidate summary](../evidence/ber-replacement-candidate-1-summary.md) | Two independent full-page reviews accepted the new proposal after first-use, attribution, proposed-versus-delivered, and rollback wording corrections. They also reaccepted the corrected candidate summary after its stale holdout-support sentence was replaced with the merged #249 status and unset production pins. Links, authority limits, and exact ten-path scope were checked. The merged tree has 585 tracked Markdown files: 541 accepted readers and 44 classified fixtures, with zero known pending pages. |
| Reader-page follow-up after merged PRs #248 and #249, 2026-09-24 | [Multi-agent release path](../paths/release-with-agents.md) and [BER offline holdout review](../evidence/ber-wp2b3-holdout-offline-review.md) | Both new pages received full-page review and corrected-candidate acceptance in this PR. The release path's links and manual-only boundaries were checked, and first-use abbreviations were expanded. The holdout note now identifies the merged #249 source and separates historical premerge checks from the current status. On this PR's accepted merge, the candidate has 584 tracked Markdown files: 540 accepted reader pages, 44 classified fixtures and zero known pending pages. |
| Setup skill follow-up after merged PR #246, 2026-09-24 | `.claude/skills/aegis-setup/SKILL.md` changed its Windows command example in #246 | Two read-only full-page reviews found one false cross-host key claim and first-use abbreviations. This checkpoint corrects them and obtains corrected-candidate review; prior accepted-page status remains valid on this PR's merge. The script's 44 synthetic selection assertions and #246 exact-head Actions passed. |
| Current-tree note follow-up after PR #245, 2026-09-24 | [BER offline policy review](../evidence/ber-bkl-009a-offline-review.md) and [runner command-effects note](../evidence/documentation/ber-runner-command-effects-2026-09-23.md) added by PRs #139 and #197 | The #245 baseline had 582 Markdown files: 536 accepted readers, 44 classified fixtures and these two pending notes. Dated current-reading corrections passed two independent full-page reviews; links, first-use terms and historical status were checked. At that checkpoint, accepting the two notes would have yielded 538 accepted readers, 44 classified fixtures and zero known pending pages. Previous ETA 1–3 active hours; new ETA 0. Later #248 and #249 additions are counted in the row above. |
| Last protected reader page, merged as PR #239 on 2026-09-24 | `scripts/tests/fixtures/README.md` and its new [review record](../evidence/documentation/fixture-readme-closure-after-238-2026-09-24.md) | Owner approved a PR-specific protected guard exception after independent review; Linux and Windows passed, and PR #239 merged as `66ae4deb5f5600a4ab54f0a86bee858b8b9d7c76`. The original #238 pending set closed; the #239 tree had 582 Markdown pages because PRs #139 and #197 had added two evidence notes. Confidential conduct intake remains a separate owner decision. |
| Last protected reader page after merged PR #238, draft PR #239 | `scripts/tests/fixtures/README.md`; [one-page review and guard record](../evidence/documentation/fixture-readme-closure-after-238-2026-09-24.md) | The reader correction passed independent review and offline checks. It remains pending because the exact PR's `gate-guard` exception has not been granted. Previous and current remaining documentation ETA are 1–3 active hours until owner disposition and merge; on accepted merge, the bounded inventory closes at zero known pages. Confidential conduct intake remains a separate owner decision. |
| Whole remaining-page batch after merged PR #237, merged as PR #238 | All 129 pending pages reviewed: 85 reader pages and 44 synthetic fixtures; [exact page-level disposition](../evidence/documentation/full-page-readability-all-remaining-after-237-2026-09-24.md) | Six disjoint read-only reviewers completed baseline full-page reviews; 84 reader pages and the new note passed corrected-candidate or unchanged review, while the protected fixture README remained pending. Ten hash-pinned Scenario A fixtures matched their manifest; all 44 fixtures were unchanged since #205. Previous and whole-batch documentation ETA was 25–105 active hours; the merged tree has one page left at 1–3 active hours excluding owner wait, making the selected total 96–197. Exact-head checks passed; post-merge verification is recorded in the PR. Confidential conduct intake remains a separate owner decision. |
| Full-page batch after PR #234, merged as PR #236 | Eighteen remaining skill pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md) | Six read-only reviewers accepted all 18 after correction or unchanged: 16 corrected, two unchanged. PR #236 merged with exact-head and post-merge checks green. Its merged inventory was 576 Markdown pages, 449 accepted existing pages and 127 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-234) was 25–105 documentation and 120–299 selected active hours. |
| Full-page batch after PR #233, merged as PR #234 | Forty skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-233-2026-09-24.md) | Two independent read-only reviewers accepted all 40 pages after correction or unchanged: 38 corrected, two unchanged. PR #234 merged with exact-head and post-merge checks green. Its merged inventory was 575 Markdown pages, 431 accepted existing pages and 144 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-233) was 25–110 documentation and 120–304 selected active hours. |
| Full-page batch after PR #231, started 2026-09-24 | Twenty skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-231-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; sixteen references corrected and four accepted unchanged. Candidate inventory: 574 Markdown pages, 391 accepted existing pages and 183 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-231) is 30–115 documentation and 125–309 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required; full checkpoint follows this fifth merge. |
| Full-page batch after PR #230, started 2026-09-24 | Seven skill entrypoints and thirteen skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-230-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; seven entrypoints and ten references were corrected, three references accepted unchanged. Candidate inventory: 573 Markdown pages, 371 accepted existing pages and 202 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-230) is 30–120 documentation and 125–314 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #229, started 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-229-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine entrypoints and nine references were corrected, one entrypoint and one reference accepted unchanged. Candidate inventory: 572 Markdown pages, 351 accepted existing pages and 221 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-229) remains 30–125 documentation and 125–319 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #228, started 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-228-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; eight entrypoints and nine references were corrected, two entrypoints and one reference accepted unchanged. Candidate inventory: 571 Markdown pages, 331 accepted existing pages and 240 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-228) is 30–125 documentation and 125–319 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #226, started 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-226-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; eight entrypoints and ten references were corrected, two entrypoints accepted unchanged. Candidate inventory: 570 Markdown pages, 311 accepted existing pages and 259 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-226) is 35–130 documentation and 130–324 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required; full per-item checkpoint follows this fifth merge. |
| Full-page batch after PR #225, started 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-225-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine entrypoints and nine references were corrected, one of each accepted unchanged. Candidate inventory: 569 Markdown pages, 291 accepted existing pages and 278 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-225) is 35–135 documentation and 130–329 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #224, started approximately 04:31 UTC on 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-224-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine entrypoints and eight references were corrected, one entrypoint and two references accepted unchanged. One previously accepted entrypoint was replaced before counting. Candidate inventory: 568 Markdown pages, 271 accepted existing pages and 297 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-224) remains 35–140 documentation and 130–334 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #223, started approximately 04:12 UTC on 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-223-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine entrypoints and ten references were corrected, one entrypoint accepted unchanged. Two previously accepted references were replaced before counting. Candidate inventory: 567 Markdown pages, 251 accepted existing pages and 316 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-223) is 35–140 documentation and 130–334 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #221, started approximately 03:42 UTC on 2026-09-24 | Ten skill entrypoints and ten skill references; [page-level review](../evidence/documentation/full-page-readability-batch-after-221-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; six entrypoints and ten references were corrected, four entrypoints accepted unchanged. Hash-pinned Scenario A fixtures were excluded from acceptance after preliminary audit. Candidate inventory: 566 Markdown pages, 231 accepted existing pages and 335 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-221) is 40–145 documentation and 135–339 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #220, started approximately 03:24 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-220-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; nine skills and nine evidence pages were corrected, one skill and one evidence page accepted unchanged. Candidate inventory: 565 Markdown pages, 211 accepted existing pages and 354 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-220) is 40–150 documentation and 135–344 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #219, started approximately 03:09 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-219-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; eight skills and ten evidence pages were corrected, two skills accepted unchanged. Candidate inventory: 564 Markdown pages, 191 accepted existing pages and 373 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-219) remains 40–155 documentation and 135–349 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #218, started approximately 02:53 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-218-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; ten skills and seven evidence pages were corrected, three evidence pages accepted unchanged. Candidate inventory: 563 Markdown pages, 171 accepted existing pages and 392 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-218) is 40–155 documentation and 135–349 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #216, started approximately 02:28 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-216-2026-09-24.md) | Disjoint read-only audits selected 20 distinct pending pages; ten skills and seven evidence pages were corrected, three evidence pages accepted unchanged. Candidate inventory: 562 Markdown pages, 151 accepted existing pages and 411 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-216) is 40–160 documentation and 135–354 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #215, started approximately 02:12 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-215-2026-09-24.md) | Disjoint read-only audits selected 20 existing pages; ten skills and nine evidence pages were corrected, one evidence page accepted unchanged. Candidate inventory: 561 Markdown pages, 131 accepted existing pages and 430 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-215) is 45–165 documentation and 140–359 selected active hours. Independent corrected-candidate review, exact-head Actions and merge remain required. |
| Full-page batch after PR #214, started approximately 01:55 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-214-2026-09-24.md) | Disjoint read-only audits and corrected-candidate cross-reviews accepted all 20 existing pages; nine skills and eight evidence pages were corrected, three pages were accepted unchanged. Candidate inventory: 560 Markdown pages, 111 accepted existing pages and 449 pending. The [interim estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-214) remains 45–170 documentation and 140–364 selected active hours after outward rounding. Exact-head Actions and merge remain required. |
| Full-page batch after PR #213, started approximately 01:37 UTC on 2026-09-24 | Ten skill entrypoints and ten historical evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-213-2026-09-24.md) | Disjoint read-only audits and corrected-candidate cross-reviews accepted all 20 existing pages; eight evidence and ten skill pages were corrected, two evidence pages were accepted unchanged. The candidate inventory is 559 Markdown pages, 91 accepted existing pages and 468 pending. The [interim documentation estimate](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-213) is 45–170 active hours; selected backlog 140–364. Exact-head Actions and merge remain required. |
| Full-page batch after PR #211, started 2026-09-24 approximately 01:06 UTC | Ten skill entrypoints and ten dated evidence pages; [page-level review](../evidence/documentation/full-page-readability-batch-after-211-2026-09-24.md) | Two disjoint initial reviews found corrections, and two independent cross-reviews accepted all 20 pages after correction. Confirmed at the exact #212 merge: 558 Markdown pages, 71 accepted existing pages, 487 without full-page acceptance. The selected backlog forecast at batch start was 150–394 active hours; the [five-merge forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-212) is now 145–369. |
| Agentic loop retry correction, started 2026-09-24 approximately 00:55 UTC | One skill page and its two evaluation files; [page-level review](../evidence/documentation/agentic-loop-retry-correction-2026-09-24.md) | The skill page is corrected and accepted after independent review. The error taxonomy, safe retry rule, terminal states and evaluation cases now agree. Expected post-merge inventory: 557 Markdown pages, 51 accepted existing pages, 506 without full-page acceptance; reconcile against the exact merge tree. |
| Full-page batch after PR #209, started 2026-09-24 approximately 00:29 UTC | Nine skill pages, one evaluation-harness reference and ten runner evidence pages; [page-level record](../evidence/documentation/full-page-readability-batch-after-209-2026-09-24.md) | Two independent read-only reviewers accepted 20 distinct pages after correction. A separate agentic-loop retry defect remains open in the named follow-up above. Historical evidence, manual-only gates and human incident routing were checked. Expected post-merge inventory: 556 Markdown pages, 50 previously existing pages with full-page acceptance, 506 without it; reconcile against the exact merge tree. The selected backlog forecast at start remains 150–394 active hours. |
| Full-page batch after PR #208, started 2026-09-24 approximately 00:09 UTC | Ten agent skill pages, one startup reference and ten other reader pages; [page-level evidence](../evidence/documentation/full-page-readability-batch-after-208-2026-09-24.md) | Independent read-only reviewers accepted 21 existing pages after correction or unchanged. The evidence note records each outcome and reviewer interval. At the expected 555-page post-merge inventory, 30 existing pages have recorded full-page acceptance and 525 do not; reconcile with the exact merge tree. The selected backlog forecast at start is 150–394 active hours, with 55–200 for documentation. |
| First component guides, started 2026-09-23 16:12 UTC | `tools/behavioral_eval_runner/README.md`, `tools/aegis_delivery_control/README.md`, `docs/README.md` | Rewritten around purpose, workflow, examples, functions and limits. Local commands and links passed; independent read-only review found no remaining blocker after corrections. Root README navigation remains a separate batch. |
| Maintainer guide batch, PR #122 | `docs/offline-ci.md`, `docs/approval-lifecycle-grading.md`, `SECURITY.md` | Added purpose, normal use and terms to three active guides; [batch evidence](../evidence/documentation/readability-maintainer-guides-2026-09-23.md). Other documentation remains open. |
| Technical guide batch, PR #126 | `docs/behavioral-eval-runner-schema-compatibility.md`, `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md` | Clarified reader steps, codes and policy limits in two guides; [batch evidence](../evidence/documentation/readability-technical-guides-2026-09-23.md). No schema or authority change. |
| Skill authoring standard, PR #127 | `docs/skill-generation-standard.md` | Added an authoring route and terms while retaining the normative contract and action table; [batch evidence](../evidence/documentation/skill-standard-readability-2026-09-23.md). |
| Skills catalog, PR #128 | `docs/skills-catalog.md` | Added first-screen navigation and labels; underlying entries and history were retained; [batch evidence](../evidence/documentation/2026-09-23-skills-catalog-readability-batch.md). It was not a review of every skill entry. |
| Scenario A runbook, PR #133 | `docs/acceptance/scenario-a-runbook.md`, `docs/README.md` | Added an offline quickstart, evidence-reading route and index link. Fresh-session behavioral acceptance remains separate; the [dated review record](../evidence/documentation/scenario-a-runbook-readability-2026-09-23.md) limits the claim to the checked runbook and index entry. |
| Root README workspace routing, started 2026-09-23 17:37:09 UTC | `README.md`, `docs/evidence/documentation/root-readme-workspace-routing-2026-09-23.md`, this backlog row | The first-screen start sequence now directs product users to copy the skills into their own repository and keeps source-library maintenance in this checkout. Component descriptions remain in place. Local checks and independent read-only review found no blocker, as recorded in the [batch note](../evidence/documentation/root-readme-workspace-routing-2026-09-23.md); the wider sweep remains open. |
| Offline setup routing guide, started 2026-09-23 17:58:19 UTC | `tools/aegis_setup/README.md`, `docs/README.md`, `docs/evidence/documentation/aegis-setup-routing-readability-2026-09-23.md`, this backlog row | Added maintainer purpose, a tested synthetic example, function map and direct index link. The detailed contract and no-dispatch boundary remain. Focused offline checks passed; independent read-only review found two correctable issues, then cleared the revised guide. See the [batch note](../evidence/documentation/aegis-setup-routing-readability-2026-09-23.md). The wider sweep remains open. |
| Guided user paths, started 2026-09-23 18:10:57 UTC | `docs/paths/something-is-broken.md`, `docs/paths/check-your-app.md`, `docs/paths/add-ai-safely.md`, `docs/evidence/documentation/user-paths-readability-2026-09-23.md`, this backlog row | Corrected live-incident and release-verdict routing, qualified secret/database and AI-safety claims, defined terms, and added copyable prompts. Local checks and independent review are recorded in the [batch note](../evidence/documentation/user-paths-readability-2026-09-23.md). The wider sweep remains open. |
| Setup routing plan, started 2026-09-23 18:25:36 UTC | `docs/roadmaps/aegis-setup-routing-plan.md`, `docs/evidence/documentation/setup-routing-plan-readability-2026-09-23.md`, this backlog row | Added a current delivery map and navigation, identified the PR #108 source snapshot and broad candidate screen as historical, and aligned package 2/3 descriptions with shipped contracts while keeping package 4–7 boundaries explicit. See the [batch note](../evidence/documentation/setup-routing-plan-readability-2026-09-23.md). The wider sweep remains open. |
| Historical skill category maps, started 2026-09-23 18:28:52 UTC | `docs/skills/08-ai-era-sdlc-agent-ops.md`, `docs/skills/09-ai-software-engineering.md`, `docs/evidence/documentation/skill-category-map-readability-2026-09-23.md`, this backlog row | Explained that the 40 numbered entries are original candidates, linked current shipped status and the authoring standard, and defined shorthand without changing any candidate row. See the [batch note](../evidence/documentation/skill-category-map-readability-2026-09-23.md). The other category maps and wider sweep remain open. |
| Historical skill category maps 01–07, started 2026-09-23 18:38:59 UTC | `docs/skills/01-software-architecture-engineering.md` through `docs/skills/07-devops-release-reliability.md`, `docs/evidence/documentation/skill-category-01-07-readability-2026-09-23.md`, this backlog row | Explained that 260 numbered entries are historical candidates, linked current catalog and authoring guidance, and defined first-use terms while preserving every original candidate row. See the [batch note](../evidence/documentation/skill-category-01-07-readability-2026-09-23.md). The wider sweep remains open. |
| Control-plane backlog navigation, started 2026-09-23 about 18:56 UTC | `docs/roadmaps/resumable-control-plane-backlog.md`, `docs/evidence/documentation/control-plane-backlog-readability-2026-09-23.md`, this backlog row | Added a dated current-status table, reader routes and terms so the historical CP-WP-001 opening cannot be mistaken for the shipped synthetic kernel or 003A proof. Kept the detailed package and transition contracts. See the [batch note](../evidence/documentation/control-plane-backlog-readability-2026-09-23.md). The wider sweep remains open. |
| Open decisions index, started 2026-09-23 18:56:54 UTC | `docs/roadmaps/aegis-open-decisions-2026-09-23.md`, `docs/evidence/documentation/open-decisions-readability-2026-09-23.md`, this backlog row | Added a dated current disposition and glossary above the unchanged post-#107 owner proposal, with links to approvals and owning backlogs. The [batch note](../evidence/documentation/open-decisions-readability-2026-09-23.md) records the checks and remaining gates; the wider sweep remains open. |
| Behavioral Eval Runner backlog navigation, started 2026-09-23 19:05:27 UTC | `docs/roadmaps/behavioral-eval-runner-backlog.md`, `docs/evidence/documentation/ber-backlog-readability-2026-09-23.md`, this backlog row | Added a dated status map, terms and reader routes above the preserved historical register. The map separates authorized synthetic policy proof from pending real-host and calibration work. See the [batch note](../evidence/documentation/ber-backlog-readability-2026-09-23.md); the wider sweep remains open. |
| Execution handoff current-reading guide, started 2026-09-23 19:18:33 UTC | `docs/roadmaps/aegis-efficient-execution-handoff-2026-09-23.md`, `docs/evidence/documentation/execution-handoff-readability-2026-09-23.md`, this backlog row | Added a dated current-state and navigation banner above the preserved original handoff, including its now-historical first task. The [batch note](../evidence/documentation/execution-handoff-readability-2026-09-23.md) records verification and remaining gates; the wider sweep remains open. |
| Control-plane design entry point, started 2026-09-23 about 19:18 UTC | `docs/design/resumable-control-plane-v1.md`, `docs/evidence/documentation/control-plane-design-readability-2026-09-23.md`, this backlog row | Corrected the dated current-state and reader routes within the design's first 13 physical lines, preserving all later line positions used by evidence links. The [batch note](../evidence/documentation/control-plane-design-readability-2026-09-23.md) records the line check and synthetic-only boundary; the wider sweep remains open. |
| Backlog forecast current reading, started 2026-09-23 19:26:04 UTC | `docs/roadmaps/aegis-backlog-forecast.md`, `docs/evidence/documentation/forecast-navigation-2026-09-23.md`, this backlog row | Added a dated pointer to the latest #146 estimate and labeled the old #106 baseline as history while preserving every prior table and heading. See the [batch note](../evidence/documentation/forecast-navigation-2026-09-23.md); the wider sweep remains open. |
| Skill documentation, first 20 sorted files, started 2026-09-23 19:31:24 UTC | `.claude/skills/ab-test-designer/SKILL.md`, `.claude/skills/accessibility-test-harness/SKILL.md`, `docs/evidence/documentation/skill-docs-first-20-readability-2026-09-23.md`, this backlog row | Audited the first 20 sorted skill pages and clarified previously undefined testing and accessibility terms in the two affected skills and their output labels. See the [batch note](../evidence/documentation/skill-docs-first-20-readability-2026-09-23.md); the wider sweep remains open. |
| Cloud architect skills in second 20-page screen, started 2026-09-23 19:34:25 UTC | `.claude/skills/aws-saas-architect/SKILL.md`, `.claude/skills/azure-saas-architect/SKILL.md`, `docs/evidence/documentation/cloud-skill-readability-2026-09-23.md`, this backlog row | Defined provider and security terms before use and clarified copyable output labels in the two affected skills, while preserving frontmatter, evaluation fixtures and architecture criteria. See the [batch note](../evidence/documentation/cloud-skill-readability-2026-09-23.md); the wider sweep remains open. |
| Third 20 skill pages, started 2026-09-23 19:44:38 UTC | `.claude/skills/ci-pipeline-architect/SKILL.md`, `.claude/skills/compliance-gap-auditor/SKILL.md`, `.claude/skills/data-quality-monitor-designer/SKILL.md`, `docs/evidence/documentation/skill-docs-third-20-readability-2026-09-23.md`, this backlog row | Audited the next 20 sorted skill entrypoints and defined first-use terms in the three affected pages while preserving frontmatter, evaluation fixtures and technical criteria. The [batch note](../evidence/documentation/skill-docs-third-20-readability-2026-09-23.md) records checks and independent review; the wider sweep remains open. |
| Fourth 20 skill pages, started 2026-09-23 19:52:03 UTC | `.claude/skills/docs-first-implementer/SKILL.md`, `.claude/skills/docs-retention-index/SKILL.md`, `.claude/skills/gated-deployment-prompt-template/SKILL.md`, `docs/evidence/documentation/skill-docs-fourth-20-readability-2026-09-23.md`, this backlog row | Audited the next 20 sorted skill entrypoints and explained authority terms, retention labels and execution placeholders in the three affected guides. The [batch note](../evidence/documentation/skill-docs-fourth-20-readability-2026-09-23.md) records independent review and preserved manual-only gates; the wider sweep remains open. |
| Fifth 20 skill pages, PR #156 | Four corrected skill entrypoints in the sorted screen; [exact paths and review](../evidence/documentation/skill-docs-fifth-20-readability-2026-09-23.md) | Clarified agent communication, incident response, manual test and mobile viewport terms. The manual-test reference also received a later standalone review in PR #168; neither batch claims full skill acceptance. |
| Sixth 20 skill pages, PR #158 | Three corrected skill entrypoints; [exact paths and review](../evidence/documentation/skill-docs-sixth-20-readability-2026-09-23.md) | Clarified manual-only authority and security, query and prioritization shorthand while preserving criteria and evaluation fixtures. |
| Seventh 20 skill pages, PR #159 | Four corrected skill entrypoints; [exact paths and review](../evidence/documentation/skill-docs-seventh-20-readability-2026-09-23.md) | Clarified database, review, retrieval security and real-time transport terms without changing technical or invocation boundaries. |
| Eighth 20 skill pages, PR #160 | Four corrected skill entrypoints; [exact paths and review](../evidence/documentation/skill-docs-eighth-20-readability-2026-09-23.md) | Defined scan, service-level and access terms while retaining security triage and manual-only boundaries. |
| Final 26 skill entrypoints, PR #161 | Three corrected skill entrypoints; [exact paths and review](../evidence/documentation/skill-docs-final-screen-readability-2026-09-23.md) | Clarified testing and static-analysis terms and verdict labels. This closes the sorted entrypoint screen, not full behavior or page acceptance. |
| Skill references 1–20, PR #163 | Three corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-first-20-readability-2026-09-23.md) | Added purpose and first-use accessibility, identity and governance terms while preserving parent-skill authority. |
| Skill references 21–40, PR #164 | Four corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-second-20-readability-2026-09-23.md) | Explained threat, stale-authority and cloud terms without changing control tables. |
| Skill references 41–60, PR #166 | Three corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-third-20-readability-2026-09-23.md) | Defined migration, compliance and error-model terms and made abort-action labels traceable without changing commands or approval gates. |
| Skill references 61–80, PR #167 | Four corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-fourth-20-readability-2026-09-23.md) | Added standalone purpose and first-use incident, management-system and output-safety terms. |
| Skill references 81–90, PR #168 | Ten corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-fifth-a-readability-2026-09-23.md) | Added purpose, owning-skill links and terms; corrected copyable Git revert/range guidance and routed live poisoning incidents to the human incident owner. |
| Skill references 91–100, PR #169 | Ten corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-fifth-b-readability-2026-09-23.md) | Added purpose, owning-skill links and terms; kept performance evidence thresholds and manual-only boundaries explicit. |
| Skill references 101–120, PR #171 | Four corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-sixth-20-readability-2026-09-23.md) | Restored a safe SQL test guard, routed live prompt injection to human incident response, and clarified draft status and terms. |
| Skill references 121–140, PR #172 | Six corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-seventh-20-readability-2026-09-23.md) | Clarified evidence, secret, alerting, reliability, trust-criteria and streaming terms while preserving the owning skills' gates. |
| Skill references 141–156, PR #173 | Five corrected standalone reference pages; [exact paths and review](../evidence/documentation/skill-references-final-16-readability-2026-09-23.md) | Clarified leakage, tenancy, threat, observability and supply-chain guidance. This closes the sorted reference screen, not full page or runtime acceptance. |
| Owning-skill governance and incident routing, PR #165 | Two owning skill pages and one governance evaluation; [exact paths and review](../evidence/documentation/governance-poisoning-routing-correction-2026-09-23.md) | Corrected squash-revert wording and live poisoning-incident routing. PR #168 separately reviewed the related reference pages; neither correction grants execution authority. |
| Scoped standing-grant clarification, [PR #175](https://github.com/ModernNomad-98/Project-Aegis/pull/175) | Two governance skill pages, their two evaluations and two references in `agent-authorization-matrix` and `standing-approval-and-auto-advance` | Explained that a still-active scoped human grant can satisfy an approval-required action while green checks and this skill grant no authority. Manual-only posture and separate auto-merge gate remain; this row records a correction, not a new approval. |
| Changelog and startup routing, pull request (PR) #176 | `CHANGELOG.md` and `CLAUDE.md`; [exact scope and checks](../evidence/documentation/root-status-docs-readability-2026-09-23.md) | Marked old changelog highlights as historical and clarified local role checks before task work. Original history and source-library versus product-repository boundaries remain. |
| Seven operational guides, PR #178 | Storage, selected-host and holdout proposals; control-plane proof proposal; successor design; audit rubric and register; [exact paths and checks](../evidence/documentation/operational-guides-seven-readability-2026-09-23.md) | Added dated reading notes and routes to current records. Original proposals, thresholds and decision text remain; no implementation or live-execution gate closed. |
| Five authorization proposals, PR #179 | Setup packages 2/3, measured calibration, evidence-policy choice and offline proof scope; [exact paths and checks](../evidence/documentation/operational-proposals-five-readability-2026-09-23.md) | Distinguished delivered synthetic scopes, historical decisions and pending live work. The policy choice and offline proof grant remain separate; original decision bodies were preserved. |
| Seven historical plans and research pages, PR #181 | Four generation-prompt pages, one reconciliation and two research reports; [exact scope and checks](../evidence/documentation/legacy-prompts-current-reading-2026-09-23.md) | Labeled the former repository and foundation-phase instructions as historical and linked current authoring routes. Original prompts and numbered decisions remain; no legacy prompt was executed. |
| Three roadmap and audit reading keys, PR #183 | The 300-skill candidate roadmap, frozen skill-contract baseline and VolunteerFlow handoff; [exact paths and corrected review](../evidence/documentation/remaining-active-docs-readability-2026-09-23.md) | Defined terms and explained historical baseline limits. Later corrections do not establish a current disposition for every old defect; the original candidate rows and observations remain. |
| Evidence index and seven dated status banners, PR #184 | `docs/evidence/README.md`, the documentation-index link and seven evidence pages; [reading index](../evidence/README.md) and [exact changed paths](https://github.com/ModernNomad-98/Project-Aegis/pull/184/files) | Indexed 15 selected decision/delivery records and corrected stale first-screen status readings on seven pages. This is a bounded index and correction, not review of every evidence page or a new approval. |
| Five historical verification reading notes, PR #186 | Earlier review corrections, two calibration-closeout records, the hosted-run record and shared-contract verification; [exact scope and review](../evidence/documentation/evidence-followup-current-reading-2026-09-23.md) | Distinguished candidate-specific results and an earlier guard failure from later deliveries. All original findings, test counts, skips, candidate identities and failure evidence remain. |
| Nine-page full-checklist sample, 2026-09-23 | Runner backlog, execution measurements, offline continuous integration guide, Scenario A runbook, two skills, two templates and one evidence note; [per-page result and review limits](../evidence/documentation/full-page-readability-sample-2026-09-23.md) | All nine required targeted corrections and then passed independent page review at the corrected candidate revision. This is the first recorded full-page acceptance batch; the other tracked pages retain their earlier screen or pending status. |


This table records bounded page progress, not completion of the full sweep.
The original inventory had 491 Markdown files. The #146 five-merge forecast
checkpoint counted 513; the later post-#151 main head counted 517. Add each later batch with its exact files, findings, verification
and disposition.

That instruction records the earlier ledger checkpoint; the rows above now
include the delivered batches through PR #173.

At the exact [PR #173 merge](https://github.com/ModernNomad-98/Project-Aegis/pull/173)
(`e6148322eefd085eeba9c58ef0c89876b90c9f71`), the tree has **536 tracked
Markdown files**, including **156 skill reference pages** and **185 shipped skill
entrypoints plus one template**. The nine sorted skill-entrypoint batches
corrected 28 skill pages, and the nine reference batches corrected 49 reference
pages. Some references were also touched in skill-entrypoint batches. These are bounded
readability checks, not full page, behavioral, provider or runtime acceptance.
The remaining selected-backlog estimate at this checkpoint is provisionally
**175–394 active hours**; see the [five-merge forecast recorded after PR #173](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-173).
The previous integration estimate was none; this ledger update is estimated at
1–3 active hours. Repository-wide documentation acceptance remains **IN
PROGRESS**.

## Correction to the pending floor — 2026-10-02

The counts in the readings above are dated snapshots. They are annotated here,
never rewritten. This note records an independent re-derivation of the pending
floor at `origin/main` = `d6e484189cc30c67dc69aeb973e15f89b693537d`. The
revision is one commit past `914dcbb8`: `git diff --stat 914dcbb8 d6e48418`
returns only `.coord/coordinator-cadence.jsonl | 1 +`, so no Markdown page
changed and every figure below holds at both.

**The floor is 35 named pages, not 13 or 16, and the recorded "at least 26" is
proven too low by at least 9.** The six stated per-page `--numstat` figures all
reproduce exactly at `410b90aa` (`523 2`, `86 2`, `145 6`, `329 14`, `24 1`,
`79 29`), and all nine 2026-10-01 relabel rows reproduce exactly
(31/26/18/17/14/14/12/12/11). The defect is coverage, not arithmetic. The floor
is the total the rule actually catches, and it was reached by re-deriving each
page rather than trusting the earlier statement.

**Measurement basis.** Numbers marked *added+deleted* come from `git diff
--numstat <sha> <origin/main> -- <path>`, added plus deleted, the measure the
net-difference decision above defines. File counts come from
`git ls-tree -r --name-only <ref>` filtered with the anchored global regex
`\.md$`, counted per emitted record. No file blob was split on newlines: at
`d6e48418` this page has 3,231 lines (its blob contains 3,231 `\n` bytes and
2,980 non-blank lines), which is why `Measure-Object -Line` — which drops blank
lines — is not used anywhere in this note.

### The ten pages the 2026-10-01 audit did not catch

| Page | Base SHA | Changed lines (added+deleted) |
| --- | --- | ---: |
| `compliance-control-foundation/SKILL.md` | `cdacb2ff9344` | 63 (`38 25`) |
| `agent-startup-context-gate/SKILL.md` | `754fc7a02f85` | 72 (`47 25`) |
| `lane-authoring-guide/SKILL.md` | `dbad6c25c111` | 38 (`25 13`) |
| `rls-policy-auditor/SKILL.md` | `cf1963933515` | 92 (`62 30`); 20 (`15 5`) from `5e0e9ad7` |
| `compliance-evidence-collector/SKILL.md` | `cdacb2ff9344` | 32 (`22 10`) |
| `local-ci-mirror-preflight/SKILL.md` | `bf7a4b86b46b` | 29 (`24 5`) |
| `chat-backlog-reconciliation/SKILL.md` | `620f0268edca` | 20 (`16 4`) |
| `cloud-security-baseline-reviewer/SKILL.md` | `65bacc7d6b85` | 12 (`8 4`) |
| `adr-writer/SKILL.md` | `f27535695b34` | 12 (`8 4`) |
| `phased-work-handoff-designer/SKILL.md` | `c0a3d1d4de64` | 11 (`6 5`) |

Each base SHA is the page's last recorded acceptance and is an ancestor of
`origin/main`, and each figure exceeds 10, so every one of the ten returns to
pending under the net-difference rule quoted above. That rule *retains* an
acceptance and *confers* none, and `git log -1 --format='%h' <base> -- <path>`
confirms the base is the recorded acceptance for each page: for
`local-ci-mirror-preflight` the base `bf7a4b8` is the merge
"docs: accept next twenty full-page reviews after 219" the tracker's own row
cites when it says "keep acceptance" at 9 net.

### Correction: one base SHA in the table above is not an ancestor of `origin/main` — 2026-10-02

**The sentence above is false as written.** It says: *"Each base SHA is the page's
last recorded acceptance and is an ancestor of `origin/main`, and each figure
exceeds 10, so every one of the ten returns to pending under the net-difference
rule quoted above."* The table's `cloud-security-baseline-reviewer/SKILL.md` base
`65bacc7d6b854205cf8bdcc7a1a58f8ef76dc6c7` is a dangling pre-rebase object, not an
ancestor of `origin/main`. Re-run at `origin/main` `26b7cd68` with a `git fetch
origin --prune` first: (1) `git merge-base --is-ancestor 65bacc7d6b85 origin/main`
exits **1**; (2) `git for-each-ref --contains 65bacc7d6b85 --format='%(refname)'`
returns **nothing** (0 refs); (3) `git rev-list --all` — 1907 commits, which by
Git's definition includes branches, remotes, tags, the stash and other refs —
does **not** contain it; (4) `git cat-file -t 65bacc7d6b85` returns **`commit`**.
Its subject is `chore: set SKILL-COUNT to 193 after rebase onto d423d53 (#523,
#518)`, dated 2026-09-28, so it is not an acceptance commit for that page either,
and its 12 changed lines are therefore not reproducible outside a clone that
still holds the dangling object. The fourth result is the point: **an object
resolving is not evidence of reachability**, tests (1) and (2) are the ref graph
and test (4) is evidence of nothing about it. `reflog --all` does not name the
object either, so no reflog entry reaches it. This is already a standing rule —
`PROC-01`, *"A claim that a revision is reachable must be verified by an explicit
reachability test against the ref graph, never by the mere resolution of the
object"* — in the process register proposed by **open PR #633**, which is
**not merged**, so a path link here does not resolve on `main` and this citation
is **unverified** in this repository as written; correct it when #633 merges.

**The other nine rows are unaffected, and that is measured, not assumed.** Each of
the ten other SHAs cited in this passage — `cdacb2ff9344`, `754fc7a02f85`,
`dbad6c25c111`, `cf1963933515`, `5e0e9ad7`, `bf7a4b86b46b`, `620f0268edca`,
`f27535695b34`, `c0a3d1d4de64` and the abbreviation `bf7a4b8` (the same commit as
`bf7a4b86b46b`) — passes **both** tests: `merge-base --is-ancestor` exits **0**,
and `for-each-ref --contains` returns refs in the hundreds (at least 340, the
lowest measured). Only
`65bacc7d6b85` fails. The section's conclusion still holds for all ten rows,
because the cited figures (11 to 92 changed lines) each exceed 10 whether or not
the base is reachable; what fails is the sentence's reachability claim, and for
one row the reproducibility of its changed-line figure.

**The two incompatible upper bounds are both still present.** This page says `at
most **575**` against the recorded 584, and later says `at most **567**` are
counted accepted or unknown; neither has been withdrawn, and the page's own
2026-10-02 text already records both as figures no command reproduces. They are
also arithmetically incompatible on one inventory: 602 reader pages less 575 is
27, while the same passing text puts the floor at at least 35. That observation is
added here; no figure above is changed.

**Self-cost.** `git diff --numstat origin/main -- docs/roadmaps/
aegis-documentation-readability-backlog.md` reports **`52 0`** for this
correction: **52 lines added, 0 deleted**, to a file that was already pending and
owing its own independent full-page re-read. It compounds that debt rather than
clearing it, confers no acceptance, and the page **remains pending**.

**Root cause.** Six of the ten have their **only** acceptance recorded outside
this ledger, in the batch evidence files under `docs/evidence/documentation/`,
and this ledger does not mention them at all:

| Page | Acceptance recorded only in | Line |
| --- | --- | ---: |
| `compliance-control-foundation/SKILL.md` | [batch after 214](../evidence/documentation/full-page-readability-batch-after-214-2026-09-24.md) | 30 |
| `compliance-evidence-collector/SKILL.md` | [batch after 214](../evidence/documentation/full-page-readability-batch-after-214-2026-09-24.md) | 31 |
| `agent-startup-context-gate/SKILL.md` | [batch after 208](../evidence/documentation/full-page-readability-batch-after-208-2026-09-24.md) | 39 |
| `chat-backlog-reconciliation/SKILL.md` | [batch after 213](../evidence/documentation/full-page-readability-batch-after-213-2026-09-24.md) | 30 |
| `lane-authoring-guide/SKILL.md` | [batch after 219](../evidence/documentation/full-page-readability-batch-after-219-2026-09-24.md) | 21 |
| `phased-work-handoff-designer/SKILL.md` | [batch after 221](../evidence/documentation/full-page-readability-batch-after-221-2026-09-24.md) | 24 |

A global search of this ledger at `d6e48418` for each of those six path names
returns **0** matches, while the four whose acceptance this ledger does record
return 2, 4, 3 and 15. **A tracker-only audit therefore misses them
structurally, not incidentally:** the audit can only re-derive pages whose
acceptance this ledger happens to name, and these six are named only in the
evidence files. The remaining four are caught in this ledger only as prose
("keep acceptance" at 9, "accepted on `65bacc7`", "ACCEPT on `f275356`") and
`phased-work-handoff-designer` is named nowhere in it either. An audit scoped
to this file cannot see an acceptance that lives only in another one; the fix
is the index described below, not a more careful reading of this page.

### The omitted page is one of the pages added after `410b90aa`

`git diff --name-status --diff-filter=A 410b90aa d6e48418 | Select-String
'\.md$'` returns five page additions, and no Markdown page was deleted
(`--diff-filter=DR` returns nothing). The tracker's floor for that set counts
**4** and records "+ 0" for the fifth: it declines to add
`docs/evidence/session-continuation-2026-09-30-evening.md`, even while
observing that "the rule above therefore leaves a new page pending" and calling
the omission "a text gap rather than a review gap". Under the rule the tracker
quotes, a new page starts pending and never had an acceptance to retain, so all
five count. `git log --diff-filter=A` shows the omitted page was added by
`1955c222` (PR #586, 2026-09-30) and `git ls-tree -r --name-only d6e48418 --
<path>` confirms it is tracked at `origin/main`. Counting it is what the rule
requires; the tracker's own `17 + 0 = 17` is therefore a text undercount of
`17 + 1 = 18` before the ten above are added.

### Why the exact count is still not derivable

The same reason recorded above still holds, and this correction does not
remove it. The 10-line rule decides acceptance **per page, per revision**, but
acceptance is stored as prose in two places that do not index each other, and
this ledger's default remains accepted-unless-listed. The provable floor is 35:
the tracker's own carried set of 16 at `410b90aa`, plus the 9 relabel pages it
caught, plus the 10 it missed — each proven above and disjoint by path. Because
`410b90aa`'s recorded 13 becomes 16 under its own later correction, the same
reading without this note's second limb is a floor of 26, not 35.

The exact count is not derivable from a command and **no exact count is
asserted here**. What the repository can show is the floor of 35 named pages,
and that "at least 26" is too low by at least 9. The unknown remainder is
unchanged: at `d6e48418` the tracked Markdown inventory is 658 (653 at
`410b90aa`), of which one file is a generated report
(`docs/audits/skill-contract-audit-baseline.md`, the only tracked Markdown a
production script writes — `scripts/audit-skill-contracts.py` line 2072) and 55
are classified synthetic fixtures (the 56 Markdown paths under `scripts/` minus
the reader-facing `scripts/tests/fixtures/README.md`). That leaves 602 reader
pages, so at most **567** are counted accepted or unknown with no per-page
recorded full-page re-read that a command can bind. The tracker's 584, and its
own later "at most 575", remain figures no command reproduces. This note ran
only the >10-line limb; the "any new section" limb needs the same index, and it
can only raise the floor.

**What would make it exact.** One per-path acceptance index — path, last
full-page-acceptance SHA, reviewer, PR link and date — maintained beside this
ledger. Then `git diff --numstat <acceptance-sha> origin/main -- <path>` greater
than 10, plus the "new section" test (`git diff <acceptance-sha> origin/main --
<path> | Select-String '^\+#{1,6} '`, where a renamed or renumbered existing
heading is not a new section), becomes a complete decision procedure, and the
pending count becomes one command. Pages absent from the index, or with no SHA,
are pending by definition — which removes the accepted-unless-listed default
that produced this undercount.

**This note is not an acceptance.** It is an edit to a page that is already
pending, so it confers no acceptance. `git diff --numstat 410b90aa <this
branch> -- docs/roadmaps/aegis-documentation-readability-backlog.md` exceeds 10
lines, so under the rule above this ledger returns to **pending** and owes an
independent full-page re-read against [Acceptance for each
page](#acceptance-for-each-page) by a reader who did not write this note.

## First ledger-keeper recording — owner-ratified role, 2026-10-02

The owner has **ratified** the *ledger keeper* role defined in
[the acceptance conversion process](../evidence/documentation/acceptance-conversion-process-2026-10-02.md)
(merged by PR #630). That note recorded the role as a proposal with "Owner
ratification is owed"; the owner has now given it, and this section is the
role's **first use**. The ledger keeper's authority is **recording only**: it
does not re-review a page, does not judge readability, does not confer an
acceptance a reviewer declined, and does not merge. Nothing below re-reads
anything, and nothing below is a readability verdict by the ledger keeper.

Two pages qualified. Both satisfied all three conjunctive evidence conditions
of that process: a posted review record bound to an exact head SHA, a full-page
read declared against every criterion in
[Acceptance for each page](#acceptance-for-each-page), and an acceptance the
rule can actually give — each page was pending and this record is the
full-page re-read it owed.

| Page | Acceptance revision | Reviewer | Evidence source | Date |
| --- | --- | --- | --- | --- |
| [The host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md) | `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e` | REVIEW-2 | [PR #625 comment 5963410567](https://github.com/ModernNomad-98/Project-Aegis/pull/625#issuecomment-5963410567) | 2026-10-02 |
| [The Stage 4A offline review](../evidence/setup/issue-101-package-4a-offline-review.md) | `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e` | REVIEW-2 | [PR #625 comment 5963410567](https://github.com/ModernNomad-98/Project-Aegis/pull/625#issuecomment-5963410567) | 2026-10-02 |

REVIEW-2's record **confers** acceptance. Its per-file table carries
`ACCEPT (full-page re-read)` for exactly these two rows, and its section 8
states: "for the two pending pages this review is offered as the independent
**full-page** re-read they owe — I read each in full at the head and checked
every criterion in 'Acceptance for each page'." It binds to the head and states
that a moved head voids it.

**The ledger keeper is neither the author nor the reviewer.** REVIEW-2 is not
the author of PR #625. The ledger keeper that records these rows wrote neither
page, took no part in PR #625, and is not any reviewer on it or on this
recording pull request.

**Candidates examined and NOT recorded.** Recording nothing is the correct
outcome for a candidate that fails a condition, so each refusal is stated with
its reason rather than left silent.

| Candidate | Reviewer | Bound head | Disposition | Why nothing was recorded |
| --- | --- | --- | --- | --- |
| [Behavioral Eval Runner design](../design/behavioral-eval-runner-v1.md), [resumable control plane design](../design/resumable-control-plane-v1.md), [BER fast-track successor](../design/behavioral-eval-runner-v1-fast-track-successor.md) | DESIGN-1 | none | no posted record | No PR and no artifact was produced; the evidence survives only in an agent's own report. Condition (b)(1) needs a posted review record bound to an exact head, and this page's own charter rule is that a self-reported "read it, changed nothing" is not evidence because no artifact exists — it is not independently falsifiable from the diff. |
| The two setup evidence pages **as reviewed by REVIEW-3** | REVIEW-3 | `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e` | **declines** | Its record self-declares: "this is a **targeted** review, not a full-page re-read. It therefore confers and records no full-page acceptance." Condition (b)(2) fails, and its per-file `ACCEPT` rows do not override its own prose disclaimer. The two pages are recorded above on REVIEW-2's separate conferring record, not on this one. |
| `docs/README.md`, `docs/roadmaps/aegis-open-decisions-2026-09-23.md`, `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/approvals/APPROVAL_REGISTER.md`, `docs/roadmaps/aegis-backlog-forecast.md`, `docs/roadmaps/aegis-execution-metrics.md`, `docs/skills-catalog.md` | Audit-1, REMEDY-1 | `4e28afa17c86aa4be37b3c6f6b0aea29be00c956` | **declines** | REMEDY-1 writes "**This review does not discharge that debt and confers no acceptance on any page** — I read only the three changed files in full", and Audit-1 explicitly marks six further pages NOT CONFERRED. Independently, `docs/README.md` changed 81 added / 60 deleted = 141 lines, far past 10. |
| `docs/evidence/session-continuation-2026-09-30.md`, `docs/evidence/session-continuation-2026-09-30-evening.md` | Audit-2, REBIND-1 | `3bdb217f`, then `a0634422` | **declines** | Audit-2 records "**No acceptance was conferred — the trap was avoided**", and "no page here is marked accepted in any case". REBIND-1's later record is a targeted fix verification whose per-file `ACCEPT` means "the two fixes are correctly applied", not a full-page re-read against the criteria. Both heads are squash-merged and are not ancestors of `origin/main`. |
| This ledger itself (PR #626) | CLOSE-BOTH | `1e8b81e74b4d64ce86884807df4bee4ee557c208` | **neither** | Its record's verdict is FIX-FIRST, not one of the four dispositions, so no acceptance was conferred — and an edit to this ledger cannot be recorded as this ledger's own acceptance without collapsing the author/reviewer separation this role exists to keep. |
| `.coord/coordinator-cadence.jsonl` (PR #627) | PR #627 record | `fc29229d8c0e879ec271b9c5cd6596fa0bc47e44` | not a reader page | Its own record states "There is ONE review stage here — a governance log append; readability acceptance does not apply." It is not tracked Markdown, so no page acceptance exists to record. |
| `docs/evidence/documentation/acceptance-conversion-process-2026-10-02.md` (PR #630) | REVIEW-630 | `20857201c8e3d8ed028cf713419a91369c520d1f` | **ACCEPT, but not a full-page acceptance** | Its own record scopes itself to re-deriving the note's measurements and records a required correction; it neither claims a full-page read against every criterion nor names the note as an accepted page. Conditions (b)(2) and (b)(3) do not hold, so the note remains pending. REVIEW-630's independent confirmation that REVIEW-2's full-page claim is real is what this recording relies on; that confirmation is not itself an acceptance of the note. |

**The acceptance revision is `e6fc8d24`, the head REVIEW-2 read.** Measured, not
assumed: `git merge-base --is-ancestor e6fc8d24 origin/main` is **false** —
PR #625 was squash-merged as `2ba20c71`, so the branch commit is not an ancestor
of this ledger's default branch, while `git for-each-ref --contains e6fc8d24`
shows it is still reached by `origin/docs/readability-batch-b`. The acceptance
is not void: `git rev-parse e6fc8d24:<path>` and `git rev-parse origin/main:<path>`
return the **same blob** for both pages (`9bf204cc4b92543c5cf7e18555ce3095850ce3b3`
and `ed40be87d4d452c4fe48e59a2894ef7b1e1ae264`), and `git diff --numstat
e6fc8d24 origin/main -- <path>` is **empty** for both. The bytes REVIEW-2 read
are the bytes on main; neither page has moved since.

**Changed lines since last recorded acceptance.** Neither page is accepted
earlier in this ledger — PR #542 returned both to pending — so no acceptance
existed to retain, and the 10-line exemption could not have applied to either.
For completeness: `git diff --numstat 22a6b7a origin/main` gives **11 added /
7 deleted = 18** for the feasibility page and **127 added / 0 deleted = 127**
for the offline-review page. Two different measurements are easy to confuse
here, and both are correct about different spans: REVIEW-2's own `7/5 = 12`
and `6/3 = 9` measure **only what PR #625 itself changed**, while 18 and 127
measure **cumulative change since the last recorded acceptance**. The larger
figures are what the retention rule reads, and because both pages were already
pending they do not block a full-page re-read; they would have voided any
retained acceptance. Under the owner's 2026-09-28 counting rule, changed lines
are added plus deleted from `git diff --numstat`, counted newline-based.

**Owner-ratified role, first use — the convention is new and may need
refinement.** This is the first time any agent has recorded through this role.
Two points are recorded rather than settled: the process's canonical per-path
acceptance index (section (c) of the conversion note) does not exist on main,
so these rows are recorded in this ledger as dated prose instead of as index
rows; and the acceptance revision `e6fc8d24` is a branch commit reachable only
from `origin/docs/readability-batch-b`, so a reader who deletes that branch
could no longer reproduce the revision even though the committed bytes survive
on main. Both deserve an owner ruling before the convention is relied on
again.

**Correction (appended 2026-10-03).** The first point above is wrong as written:
the canonical per-path acceptance index **does exist on main**, at
[`tools/readability_acceptance/acceptance-index.json`](../../tools/readability_acceptance/acceptance-index.json),
tracked, with this ledger as its `rule_text_file`. The original sentence stands
as the record of what was believed on 2026-10-02. See
[Premises correction](#premises-correction--appended-2026-10-03-measured-at-c3527560).

**This ledger returns to pending.** This recording section is itself more than
10 changed lines, so by the owner's targeted-edit rule of 2026-09-27 — the rule
stated in this page's prose under
[Remaining-page review in larger batches](#remaining-page-review-in-larger-batches),
which has no heading of its own —
this ledger returns to **pending** and owes its own independent full-page
re-read against [Acceptance for each page](#acceptance-for-each-page) by a
reader who did not write this section. That self-cost is the one named in the
[floor correction](#correction-to-the-pending-floor--2026-10-02) and in PR #626:
recording acceptance in this ledger spends the ledger's own acceptance. It is
recorded here as a cost actually paid, not as a reason to withhold the
recording.

**The tracked Markdown count does not change.** This section edits an existing
tracked page; it adds no file. `git ls-tree -r --name-only origin/main` filtered
to `.md` remains **659** before and after, and the pending floor is therefore
unchanged by this recording.

## Consistency note — the ledger keeper entry, 2026-10-02 local / recorded 2026-10-03 UTC

The ledger keeper role and the two historical recording acts above are recorded as [AEGIS-APR-101: Ledger keeper role and two historical recording acts](../approvals/APPROVAL_REGISTER.md#aegis-apr-101-ledger-keeper-role-and-two-historical-recording-acts) in the [owner approval register](../approvals/APPROVAL_REGISTER.md), appended 2026-10-03 UTC. The register entry is the authority; this section is a pointer and a record of what did and did not change here.

**The approval postdates the recording it ratifies.** The owner approved the role on 2026-10-02 at 18:05:09 America/Los_Angeles = 2026-10-03 at 01:05:09 UTC. PR #635 merged at 2026-10-03 00:46:52 UTC, roughly eighteen minutes **earlier**. So the [First ledger-keeper recording](#first-ledger-keeper-recording--owner-ratified-role-2026-10-02) section above was merged before the owner gave that approval, and the ratification is of those two acts after the fact. Its heading's "owner-ratified role" reads as a claim about the state at its own merge; correct forward here rather than rewriting it.

**What the entry ratifies.** The two historical recording acts:

- [The host feasibility evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md), acceptance revision `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e`.
- [The Stage 4A offline review](../evidence/setup/issue-101-package-4a-offline-review.md), acceptance revision `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e`.

Both rest on REVIEW-2's [PR #625 comment 5963410567](https://github.com/ModernNomad-98/Project-Aegis/pull/625#issuecomment-5963410567). The register limits this ratification to those two acts and expressly does not assert that the keeper held authority beforehand.

**Acceptance stays bound to the reviewed revision.** The ratified revision is the revision REVIEW-2 read, and the ratification does not accept any later version of either page. Acceptance-retention rules continue in force: any page that moves beyond them is pending again.

**No row, revision or count changes here.** The two rows above keep their recorded acceptance revisions; no acceptance row is recreated and no row is reset. The accepted-page counts are unchanged, and this ledger is **not** accepted by this note — it remains **pending** and still owes its own independent full-page re-read by a reader who did not write the earlier section or this one. The keeper may not itself supply that re-read: it checks that required review evidence exists and qualifies, and cannot perform another readability review or manufacture a missing acceptance. The keeper may also be neither the page's author, nor its accepting reviewer, nor the coordinator.

**Still separately unresolved, and still undecided.** The charter's proposed canonical index — its ownership, path, precedence and changed counting rules — is **not** approved by this entry. Stage 4B remains **OPEN AND UNDECIDED**: it is not parked, deferred or otherwise settled, and this note grants it nothing. The private BER candidates remain outside this work. Ratifying a documentation role grants no installation, host-session, provider-call, credential-access, private-data-access or deployment authority.

**Cost of this note.** It exceeds 10 changed lines on this ledger, so the ledger stays **pending** and its own independent full-page re-read remains owed. That is a cost recorded as incurred, not a reason to withhold the note, and no acceptance was manufactured to offset it.

## Ledger checkpoint through pull request #186 — 2026-09-23

The seven rows above record documentation batches delivered after the earlier
#173 checkpoint. Pull request #182 already integrated the skill and reference
screen rows and the separate owning-skill corrections; those rows are not
counted again. Pull requests #180 and #185 updated the forecast and execution
measurements, rather than adding another readability screen.

At the exact #186 merge
`d5b007b0a3cc2bd43806a16970f19c84be9a86b0`, the repository contains
**543 tracked Markdown files**. The older 491, 513, 517 and 536 counts above
remain historical snapshots. The increase from 536 after #173 consists of
six dated evidence notes and one evidence index; it is not seven more pages
accepted against every documentation criterion.

The later forecast recording this #186 tree was delivered by pull request
#189. Its [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-186)
and [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-186--2026-09-23)
retain the individual package estimates, observed wall intervals and limits.
The previous ledger-update estimate was **1–3 active hours**; this update's
estimate is **1–3 active hours**. The selected backlog remains
**175–394 active hours**, or **191–434** if both optional issue #101
helpers are selected. The full all-options backlog has no finite estimate
while optional quantities and architecture choices remain open.

Documentation acceptance remains **IN PROGRESS**. These rows record bounded
reading improvements, navigation and preservation of historical evidence.
They do not certify full page acceptance, model behavior, a real host or
provider readiness, and they grant no new execution authority.

## Ledger checkpoint through pull request #212 — 2026-09-24

The five merges since the #207 forecast are #208, #209, #210, #211 and #212.
Their exact merge commits, original estimates and observed wall intervals are
in the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-212--2026-09-24).
The #212 merge `ba24016d209be6e49171be52332887558db16ab2` has **558 tracked
Markdown pages**. The recorded full-page acceptance count is **71 distinct
existing pages**; **487 remain**. The pending inventory reconciles as 308
skill pages, 59 previously corrected primary pages, 58 dated notes or tracking
pages, 18 other reader pages and 44 synthetic fixtures. Four new dated review
notes entered the inventory after #207. They were not accepted as existing
pages by the batches they document.

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-212)
changes the documentation residual estimate from **55–200** to **50–175
active hours**, and the selected backlog from **150–394** to **145–369 active
hours**. This checkpoint work item previously and currently estimates **1–2
active hours**. Acceptance remains **IN PROGRESS**. The next page batch needs
its own page-level evidence and independent review; this accounting does not
accept any of the 487 pending pages.

## Ledger update for the batch after pull request #213 — 2026-09-24

The candidate starts from the exact #213 merge
`620f0268edcab0259153958a3174884b75d8a178`. One new review note raises
the Markdown inventory from 558 to **559**. Twenty distinct existing pages
gain full-page acceptance, raising the accepted count from 71 to **91**.
Thus **468** remain: 298 skill, 49 corrected primary, 59 notes/tracking,
18 other reader and 44 synthetic fixture pages. The new note is pending,
not counted as accepted merely because it documents acceptance of other pages.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-213)
changes documentation from **50–175** to **45–170 active hours** and selected
backlog from **145–369** to **140–364 active hours**. Acceptance remains
**IN PROGRESS**; the unreviewed pages retain their pending status.

## Ledger update for the batch after pull request #234 — 2026-09-24

The candidate starts from the exact #234 merge
`5c46c7b3e61712674051eb734fa7d099a10aae4f`. One new review note
raises the tracked Markdown inventory from 575 to **576**. Eighteen
distinct existing skill pages gain full-page acceptance after six independent
corrected-candidate reviews, raising accepted existing pages from 431 to
**449**. Thus **127 remain**: zero skill entrypoints/references, 48
previously corrected primary pages, 17 dated notes/tracking pages, 18 other
reader pages and 44 synthetic fixtures. The new review note is pending rather
than counted as accepted existing work. Linked eval/reference/asset alignment
does not add accepted pages.

The previous repository-wide documentation estimate is **25–110 active
hours**, and this batch estimate is **3–6 active hours**. The unchanged
[residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-234)
narrows raw documentation work from 27.4–105.2667 to **26.25–101.8333 active
hours**. Outward five-hour planning bounds change documentation to **25–105**
and selected backlog from **120–304** to **120–299 active hours** on merge.
Acceptance remains **IN PROGRESS** until exact-head Actions and merge.

## Ledger update for the batch after pull request #233 — 2026-09-24

The candidate starts from the exact #233 merge
`b545d07591f1508b197d708b33cfd2991d50db58`. One new review note
raises the tracked Markdown inventory from 574 to **575**. Forty distinct
existing skill references gain full-page acceptance after two independent
corrected-candidate reviews, raising accepted existing pages from 391 to
**431**. Thus **144 remain**: 18 skill pages, 48 previously corrected
primary pages, 16 dated notes/tracking pages, 18 other reader pages and
44 synthetic fixtures. The new review note is pending rather than counted
as accepted existing work. Three owning skill entrypoints were aligned
with corrected references, but they are not additional accepted pages.

The original and current batch ETA are **6–12 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-233)
changes from 30.0167–113.1 to **27.4–105.2667 raw active hours**.
Outward five-hour planning bounds narrow documentation from **30–115**
to **25–110 active hours**, and the selected backlog from **125–309**
to **120–304 active hours**. Acceptance of the 40 pages is contingent
on exact-head Actions and merge. The next full per-item forecast is due
five subsequent merges after the #233 forecast checkpoint.

## Ledger update for the batch after pull request #231 — 2026-09-24

The candidate starts from the exact #231 merge
`65384f04696c699881b2ff0294b6ce63711c85cf`. One new review note
raises the Markdown inventory from 573 to **574**. Twenty distinct existing
skill references gain full-page acceptance, raising the accepted count from
371 to **391**. Thus **183** remain: 58 skill, 48 previously corrected
primary, 15 dated notes/tracking, 18 other reader and 44 synthetic fixture
pages. Twenty selected references leave the skill bucket; the new note
enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-231)
changes from 31.3–116.9333 to **30.0167–113.1 raw active hours**.
Outward five-hour rounding narrows documentation from **30–120** to
**30–115 active hours** and selected backlog from **125–314** to
**125–309 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows this fifth merge if the candidate merges.

## Ledger update for the batch after pull request #230 — 2026-09-24

The candidate starts from the exact #230 merge
`275678c96f934aecb85c0b9e3c9fbce2b1490c23`. One new review note
raises the Markdown inventory from 572 to **573**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 351
to **371**. Thus **202** remain: 78 skill, 48 previously corrected primary,
14 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Seven selected entrypoints and thirteen selected references leave the skill
bucket; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-230)
changes from 32.5833–120.7667 to **31.3–116.9333 raw active hours**.
Outward five-hour rounding narrows documentation from **30–125** to
**30–120 active hours** and selected backlog from **125–319** to
**125–314 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows one more merge after this batch if it
becomes the fourth completed merge after #227.

## Ledger update for the batch after pull request #229 — 2026-09-24

The candidate starts from the exact #229 merge
`b949422c1c4aca65ecf809cc48ff2d9c78aeede6`. One new review note
raises the Markdown inventory from 571 to **572**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 331
to **351**. Thus **221** remain: 98 skill, 48 previously corrected primary,
13 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-229)
changes from 33.8667–124.6 to **32.5833–120.7667 raw active hours**.
Outward five-hour rounding keeps documentation at **30–125 active hours**
and selected backlog at **125–319 active hours**. Acceptance remains
**IN PROGRESS**; the next full per-item checkpoint follows two more merges
after this batch if it becomes the third completed merge after #227.

## Ledger update for the batch after pull request #228 — 2026-09-24

The candidate starts from the exact #228 merge
`0bc4a8fcae32ccaab009ae9e0e23390ce4342f6a`. One new review note
raises the Markdown inventory from 570 to **571**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 311
to **331**. Thus **240** remain: 118 skill, 48 previously corrected primary,
12 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-228)
changes from 35.15–128.4333 to **33.8667–124.6 raw active hours**.
Outward five-hour rounding narrows documentation from **35–130** to
**30–125 active hours** and selected backlog from **130–324** to
**125–319 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows three more merges after this batch if it
becomes the second completed merge after #227.

## Ledger checkpoint through pull request #232 — 2026-09-24

The five merges since the #227 forecast are #228, #229, #230, #231 and #232.
Their exact merge commits, original estimates and available wall intervals
are in the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-232--2026-09-24).
The #232 merge `970aad27524bccc8a3f342bc990215904253be53` has **574
tracked Markdown pages**. The recorded full-page acceptance count is **391
distinct existing pages**; **183 remain**. The pending inventory reconciles
as 58 skill pages, 48 previously corrected primary pages, 15 dated notes
or tracking pages, 18 other reader pages and 44 synthetic fixtures. Four
new dated review notes entered the inventory after #227. They were not
accepted as existing pages by the batches they document.

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-232)
changes the documentation residual estimate from **35–130** at #227 to
**30–115 active hours**, and the selected backlog from **130–324** to
**125–309 active hours**. This checkpoint work item previously and currently
estimates **1–2 active hours**. Acceptance remains **IN PROGRESS**; the next
page batch needs its own page-level evidence and independent review. This
accounting does not accept any of the 183 pending pages. The next five-merge
counter starts after #232. The next acceptance batch targets 40 pages, with
two read-only reviewers auditing 20 pages each and individual page outcomes
retained; the per-page estimate remains unchanged.

## Ledger checkpoint through pull request #227 — 2026-09-24

The five merges since the #222 forecast are #223, #224, #225, #226 and #227.
Their exact merge commits, original estimates and available wall intervals are
in the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-227--2026-09-24).
The #227 merge `88cc83fc547495b4f4d10eb5af76a4879c05af15` has **570
tracked Markdown pages**. The recorded full-page acceptance count is **311
distinct existing pages**; **259 remain**. The pending inventory reconciles
as 138 skill pages, 48 previously corrected primary pages, 11 dated notes
or tracking pages, 18 other reader pages and 44 synthetic fixtures. Four
new dated review notes entered the inventory after #222. They were not
accepted as existing pages by the batches they document.

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-227)
changes the documentation residual estimate from **40–145** at #222 to
**35–130 active hours**, and the selected backlog from **135–339** to
**130–324 active hours**. This checkpoint work item previously and currently
estimates **1–2 active hours**. Acceptance remains **IN PROGRESS**; the next
page batch needs its own page-level evidence and independent review. This
accounting does not accept any of the 259 pending pages.

## Ledger update for the batch after pull request #226 — 2026-09-24

The candidate starts from the exact #226 merge
`777f439327f6d9e3e602f1b42f25cd8a2cb7e7ac`. One new review note
raises the Markdown inventory from 569 to **570**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 291
to **311**. Thus **259** remain: 138 skill, 48 previously corrected primary,
11 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-226)
changes from 36.4333–132.2667 to **35.15–128.4333 raw active hours**.
Outward five-hour rounding narrows documentation from **35–135** to
**35–130 active hours** and selected backlog from **130–329** to
**130–324 active hours**. Acceptance remains **IN PROGRESS**; the required
full per-item checkpoint follows this batch's exact merge tree if it merges
as the fifth completed merge after #222.

## Ledger update for the batch after pull request #225 — 2026-09-24

The candidate starts from the exact #225 merge
`bc9e48b070fe99085757ce1d9cb0b791640e0d42`. One new review note
raises the Markdown inventory from 568 to **569**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 271
to **291**. Thus **278** remain: 158 skill, 48 previously corrected primary,
10 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-225)
changes from 37.7167–136.1 to **36.4333–132.2667 raw active hours**.
Outward five-hour rounding narrows documentation from **35–140** to
**35–135 active hours** and selected backlog from **130–334** to
**130–329 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows one more merge after this batch if it
becomes the fourth completed merge after #222.

## Ledger update for the batch after pull request #224 — 2026-09-24

The candidate starts from the exact #224 merge
`cf19639335158ffa09c02247d5d7b400f14fb522`. One new review note
raises the Markdown inventory from 567 to **568**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 251
to **271**. Thus **297** remain: 178 skill, 48 previously corrected primary,
9 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending. One already accepted
entrypoint was replaced before the final twenty-page selection.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-224)
changes from 39–139.9333 to **37.7167–136.1 raw active hours**. Outward
five-hour rounding leaves documentation at **35–140 active hours** and
selected backlog at **130–334 active hours**. Acceptance remains **IN
PROGRESS**; the next full per-item checkpoint follows three more merges
after this batch if it becomes the second completed merge after #222.

## Ledger update for the batch after pull request #223 — 2026-09-24

The candidate starts from the exact #223 merge
`6ccf20a8d5cbcd355d27b4ebf38980d6724959ba`. One new review note
raises the Markdown inventory from 566 to **567**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 231
to **251**. Thus **316** remain: 198 skill, 48 previously corrected primary,
8 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending. Two already accepted
references were excluded before the final twenty-page selection.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-223)
changes from 40.2833–143.7667 to **39–139.9333 raw active hours**.
Outward five-hour rounding changes documentation from **40–145** to
**35–140 active hours** and selected backlog from **135–339** to
**130–334 active hours**. Acceptance remains **IN PROGRESS**; the next
full per-item checkpoint follows three more merges after this batch if it
becomes the second completed merge after #222.

## Five-merge ledger checkpoint after pull request #222 — 2026-09-24

The exact #222 merge `7a913818c49bd0d5ee4a07faee6cb75bc0b524de`
contains **566 tracked Markdown pages**. Since the #217 checkpoint,
four 20-page batches accepted **80 distinct existing pages** and four
new review notes entered the inventory. Acceptance rose from 151 to
**231**; pending pages fell from 411 to **335**. Disjoint pending buckets
are **218 skill, 48 previously corrected primary, 7 dated notes/tracking,
18 other reader and 44 synthetic fixture pages**. The four batch notes
record disjoint accepted paths; the hash-pinned Scenario A fixtures remain
pending and unchanged.

The [full five-merge forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-222)
rechecked all 14 selected and seven optional rows. The unchanged per-page
assumptions yield **40.2833–143.7667 raw documentation hours**, rounded
outward to **40–145**. Other selected work remains **95–194**, so the
selected total changes from the #217 checkpoint's **135–354** to
**135–339 active hours**. The previous and current checkpoint ETA are
both **1–2 active hours**. Acceptance remains **IN PROGRESS**; the
next five-merge counter starts after #222. PR #139 and #197 guard
dispositions and the separate Behavioral Eval Runner holdout-executor
implementation grant remain pending.

## Ledger update for the batch after pull request #221 — 2026-09-24

The candidate starts from the exact #221 merge
`c0a3d1d4de64ce9f7307c22d2dbddaaf149c6239`. One new review note
raises the Markdown inventory from 565 to **566**. Twenty distinct existing
skill pages gain full-page acceptance, raising the accepted count from 211
to **231**. Thus **335** remain: 218 skill, 48 previously corrected primary,
7 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected entrypoints and ten selected references leave the skill bucket;
the new note enters the dated bucket as pending. The ten hash-pinned Scenario
A fixture pages screened preliminarily remain pending and unchanged.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-221)
narrows from 41.5667–147.6 to 40.2833–143.7667 raw hours. Outward
five-hour rounding changes documentation from **40–150** to **40–145
active hours** and selected backlog from **135–344** to **135–339 active
hours**. Acceptance remains **IN PROGRESS**. The fifth completed merge
after #217 triggers the next full per-item checkpoint.

## Ledger update for the batch after pull request #220 — 2026-09-24

The candidate starts from the exact #220 merge
`afe5f456ccf20cba8a8cf3e168fdfd547dd1b80c`. One new review note
raises the Markdown inventory from 564 to **565**. Twenty distinct existing
pages gain full-page acceptance, raising the accepted count from 191 to
**211**. Thus **354** remain: 238 skill, 48 previously corrected primary,
6 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected skill pages and ten selected dated evidence notes leave those
respective buckets; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-220)
narrows from 42.6833–151.1 to 41.5667–147.6 raw hours. Outward five-hour
rounding changes documentation from **40–155** to **40–150 active hours**
and selected backlog from **135–349** to **135–344 active hours**.
Acceptance remains **IN PROGRESS**.

## Ledger update for the batch after pull request #219 — 2026-09-24

The candidate starts from the exact #219 merge
`dbad6c25c11179489c6c8f78aca387a3b768995c`. One new review note
raises the Markdown inventory from 563 to **564**. Twenty distinct existing
pages gain full-page acceptance, raising the accepted count from 171 to
**191**. Thus **373** remain: 248 skill, 48 previously corrected primary,
15 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected skill pages and ten selected dated evidence notes leave those
respective buckets; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-219)
narrows from 43.8–154.6 to 42.6833–151.1 raw hours. Outward five-hour
rounding leaves documentation at **40–155 active hours** and selected
backlog at **135–349 active hours**. Acceptance remains **IN PROGRESS**.

## Ledger update for the batch after pull request #218 — 2026-09-24

The candidate starts from the exact #218 merge
`694333c0b7ebc697272b03705700c845fcc6462a`. One new review
note raises the Markdown inventory from 562 to **563**. Twenty distinct
existing pages gain full-page acceptance, raising the accepted count
from 151 to **171**. Thus **392** remain: 258 skill, 48 previously
corrected primary, 24 dated notes/tracking, 18 other reader and 44
synthetic fixture pages. Ten selected skill pages and ten selected
dated evidence notes leave those respective buckets; the new note
enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-218)
narrows from 44.92–158.1 to 43.8–154.6 raw hours. Outward five-hour
rounding changes documentation from **40–160** to **40–155 active
hours** and selected backlog from **135–354** to **135–349 active
hours**. Acceptance remains **IN PROGRESS**.

## Five-merge ledger checkpoint after pull request #217 — 2026-09-24

The exact #217 merge `f6a05e97b68108a9de0c81f37ce48b8ffe55d78c`
contains **562 tracked Markdown pages**. Since the #212 checkpoint,
four 20-page batches accepted **80 distinct existing pages** and four
new review notes entered the inventory. Acceptance rose from 71 to
**151**; pending pages fell from 487 to **411**. The disjoint pending
buckets are 268 skill, 48 previously corrected primary, 33 dated
notes/tracking, 18 other reader and 44 synthetic fixture pages.

The [full five-merge forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-217)
rechecked every selected and optional row. Its unchanged per-page
assumptions produce **44.92–158.1 raw documentation hours**, outwardly
rounded to **40–160**. Other selected work remains **95–194**; the
selected total changes from the #212 checkpoint's **145–369** to
**135–354 active hours**. Acceptance remains **IN PROGRESS**. The
previous and current checkpoint ETA are both **1–2 active hours**.

## Ledger update for the batch after pull request #216 — 2026-09-24

The candidate starts from the exact #216 merge
`d759f26527017574154a23c0748e659a75ef8b71`. One new review note
raises the Markdown inventory from 561 to **562**. Twenty distinct
existing pages gain full-page acceptance, raising the accepted count from
131 to **151**. Thus **411** remain: 268 skill, 48 previously corrected
primary, 33 dated notes/tracking, 18 other reader and 44 synthetic fixture
pages. Ten selected skill pages and ten selected dated evidence notes leave
those respective buckets; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-216)
narrows from 46.03–161.6 to 44.92–158.1 raw hours. Outward five-hour
rounding changes documentation from **45–165** to **40–160 active hours**
and selected backlog from **140–359** to **135–354 active hours**.
Acceptance remains **IN PROGRESS**. The fifth merge after #212 triggers
the next full forecast checkpoint.

## Ledger update for the batch after pull request #215 — 2026-09-24

The candidate starts from the exact #215 merge
`4e09c54b511a43672c282bc75c41061ec4f2f878`. One new review note
raises the Markdown inventory from 560 to **561**. Twenty distinct existing
pages gain full-page acceptance, raising the accepted count from 111 to
**131**. Thus **430** remain: 278 skill, 48 previously corrected primary,
42 dated notes/tracking, 18 other reader and 44 synthetic fixture pages.
Ten selected skill pages and ten selected dated evidence notes leave those
respective buckets; the new note enters the dated bucket as pending.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-215)
narrows from 47.15–165.1 to 46.03–161.6 raw hours. Outward five-hour
rounding changes documentation from **45–170** to **45–165 active hours**
and selected backlog from **140–364** to **140–359 active hours**.
Acceptance remains **IN PROGRESS**.

## Ledger update for the batch after pull request #214 — 2026-09-24

The candidate starts from the exact #214 merge
`cdacb2ff93446144c8aaf6c34cdbbb91c3b48aac`. One new review note raises
the Markdown inventory from 559 to **560**. Twenty distinct existing pages
gain full-page acceptance, raising the accepted count from 91 to **111**.
Thus **449** remain: 288 skill, 48 previously corrected primary, 51 dated
notes/tracking, 18 other reader and 44 synthetic fixture pages. One selected
control-plane evidence page came from the primary bucket; the nine selected
documentation evidence notes came from the dated-note bucket. The new note
is pending, not counted as accepted merely because it documents this batch.

The previous and current batch ETA are both **3–6 active hours**. The
[interim residual model](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-214)
narrows from 48.35–168.85 to 47.15–165.1 raw hours. Outward five-hour
rounding leaves documentation at **45–170 active hours** and selected backlog
at **140–364 active hours**. Acceptance remains **IN PROGRESS**.
