# Readability Phase 4 re-read lane A — Stage C batch record, batch 3, 2026-10-15

- **Lane:** PHASE 4 RE-READ LANE A — the alphabetically first quarter of the sorted pending set
  of the documentation readability backlog. **Stage:** C (IMPLEMENT — for this batch the evidence
  record only; no keeper row is authored here). **Base:**
  `e2a3e20b7c20ef8385b219b39c6405237163406f` (`origin/main` at branch creation — the merge of PR #769
  "tools: rebuild the readability acceptance index at e6ed06a3 (101 keeper rows)"; re-measured this
  session: `git ls-remote origin refs/heads/main` still resolves to `e2a3e20b7c20ef8385b219b39c6405237163406f`,
  so the batch-1, batch-2 and batch-3 bases are the same revision).
- **Agent / model attribution (the 2026-10-13 rule):** this record and every text this lane
  publishes are drafted by **DeepSeek (deepseek-v4-pro)**, an AI agent operating under the owner
  account; the lane's agent identity is `readability-lane-a-implementer-c` (this batch-3 session).
- **What this page is.** The lane's tracked batch record. It is the **evidence source** every
  row a separate keeper appends to the ledger's consolidated keeper table cites, so the ledger's
  `Quote` column can hold a verbatim fragment of a tracked page (the column contract), and it
  **names every row's full 40-character acceptance revision verbatim** in its own bytes.
- **This batch authors NO keeper rows and appends NOTHING to the ledger.** The diff against the
  base adds exactly this record file. The rows for these eight pages are recorded later by a
  separate eligible keeper under AEGIS-APR-101 (the ledger-keeper recording role) from this
  evidence; the earlier same-agent rows of batches 1 and 2 follow the owner's AEGIS-APR-117 route
  (withdrawal and fresh re-record by a different agent from the same evidence), so **no page needs
  re-reading**.
- **Acceptance revision bound by all eight reads of this batch:**
  `e2a3e20b7c20ef8385b219b39c6405237163406f`
  That revision resolves to itself and is contained in `refs/remotes/origin/main`
  (`git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main` exits 0,
  observed 2026-10-15 in this lane's fresh clone).
- **The lane changed none of the eight read pages.** So the bytes each reader read are the bytes
  the merge receives, and the acceptance is not voided by the merge. The lane's diff against the
  base touches only this new record.

## 1. Lane derivation — the command, not a handed-down list

The pending set is the `no_recorded_acceptance` (pages with no acceptance row in the index) and
`provably_pending` (pages whose recorded acceptance has drifted past the 10-line/new-section
rule) buckets of the instrument, taken at the pinned base, sorted by repository path, split into
four quarters; lane A is the first quarter. Commands and observed output (2026-10-15, this lane's
fresh clone at the base):

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref e2a3e20b7c20ef8385b219b39c6405237163406f
```

```json
{ "compared_ref": "e2a3e20b7c20ef8385b219b39c6405237163406f", "reader_pages_in_tree": 653,
  "accepted_on_recorded_review": 57, "provably_pending": 4, "no_recorded_acceptance": 586,
  "recorded_acceptance_within_10_lines": 0, "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6, "official_pending_count": 596 }
```

The `no_recorded_acceptance` bucket's 586 paths are derived with the instrument's own tree
classification: `git ls-tree -r --name-only e2a3e20b7c20ef8385b219b39c6405237163406f` (719 Markdown paths), minus the
fixture prefixes and the one generated report, gives 653 reader pages; the 586 are those with no
row in `tools/readability_acceptance/acceptance-index.json`'s `reader_pages` (68 rows at the
base) and no `events` row. Union with the 4 `provably_pending` paths = **590** paths; sorted,
the first `ceil(590 / 4) = 148` paths are lane A:

- **Lane A count: 148.** **First path:** `.claude/agents/ai-security-red-team-reviewer.md`.
  **Last path:** `.claude/skills/feature-flag-rollout-strategist/references/flag-rollout-sheet.md`.
- **This batch** is **paths 17-24 of that range** (sorted indices 16-23), i.e. the next eight after
  batch 1's paths 1-8 and batch 2's paths 9-16. No page outside the range is read or recorded here,
  and each of the eight is re-verified to have no acceptance row and no event row in the index at
  the base (checked per path against the index JSON; all eight absent from both arrays).
- **Briefing reconciliation (source-of-truth-reconciler).** The brief's phrase "Lane A is quarter
  index 16 (0-based start), approximately paths 17 to 23 of the sorted pending list" conflicts with
  the lane's own batch-1 artifact (`wt-laneA-b1/_laneA_paths.json`: `{"quarter": 148, "total":
  590}`, whose `mine` list begins at sorted index 0) and with the batch-1/batch-2 records (both
  state lane A is the first `ceil(590/4)=148` paths). Resolution: the artifact and the two prior
  batch records win — lane A's quarter is sorted indices 0-147 (148 paths), and "quarter index 16"
  names this batch's starting sorted index (16), which is 1-based path 17, matching "approximately
  paths 17 to 23" as 1-based paths 17-24. All four lanes' quarters remain contiguous and disjoint
  (lane B's shared artifact `laneB-pages.json` begins at sorted index 148).
  **Provenance of the two named artifacts — stated because neither is repository-checkable.**
  `wt-laneA-b1/_laneA_paths.json` and `laneB-pages.json` are **session artifacts, not repository
  artifacts**: re-measured 2026-10-16, neither appears in the tree of any ref (all refs under
  `refs/heads` and `refs/remotes` scanned with `git ls-tree -r`), and both exist only as files in
  the working copy outside the repository. **The reconciliation therefore rests on a session
  artifact that is not retrievable from the repository.** What *is* repository-checkable is the
  instrument's own derivation of section 1 (the 590-path union and the `ceil(590/4) = 148` split)
  and the batch-1 and batch-2 records' own page lists; the artifact corroboration is recorded as
  session-local and is offered as corroboration only, never as repository evidence.
- **The six `cannot_decide` pages are in NO lane.** They are excluded from every lane's
  two-bucket pending list and this batch does not pick them up. The six (each a lost-commit event —
  an acceptance whose commit was recorded, never bound and never dropped — per the checker's
  `undecided` array): `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md`,
  `.../azure-baseline.md`, `.../gcp-baseline.md`, `.../supabase-baseline.md`,
  `.../vercel-baseline.md` and `.claude/skills/database-backup-verifier/SKILL.md`. Stated here so
  the exclusion is recorded rather than accidental.

## 2. The roster, the concurrency, and the role separation (stated, not hidden)

| Batch | Theme | Pages | Read at | Reader |
| --- | --- | ---: | --- | --- |
| B3 | eight `.claude/skills/` pages of the range: the `adr-writer` ADR template, the `aegis-setup` skill and its state contract, the `agent-authorization-matrix` skill and its template, the `agent-containment-reviewer` skill and its pattern sheet, and the `agent-failure-recovery` skill | 8 | base `e2a3e20b7c20…` | `readability-lane-a-implementer-c` |

**Concurrency: one reader.** This lane's brief directs a single agent to perform the batch; the
three-reader ceiling (ledger L3000-3006) is satisfied by construction and is recorded here rather
than presented as multiple agents.

**Role separation — satisfied by construction.** The ledger-keeper role (AEGIS-APR-101 — the
standing rule that the keeper who records an acceptance row must be a different agent from the
page's author **and** from the accepting reviewer) is exercised by a **different agent** for this
lane's rows: this batch's agent is the accepting reader and the writer of this evidence record
only. It authors **no keeper rows** and appends nothing to the ledger, so no row here is "green"
or "not green" — there is no row here. Both APR-101 conditions are satisfied for the rows a
separate keeper will record from this evidence: the keeper differs from this accepting reviewer
(a different agent, the owner's AEGIS-APR-117 route — same-agent rows withdrawn and re-recorded
by a different agent from the same evidence) and from the page authors — the lane wrote none of
the eight read pages: this lane's agent authored no commit in the repository before this batch,
and the last commit touching each page names other authors (`git log -1 --format="%h %an %s" --
<page>`):

| Page | Last-touching commit / author |
| --- | --- |
| P1 | `b4751d58` Peter Nguyen ("feat: apply D15 enrichment deltas to four shipped skills") |
| P2 | `78a9822b` Project Aegis Agent ("Clarify Aegis setup choice guidance") |
| P3 | `6ba6e1ad` Peter Nguyen ("docs: apply readability sweep batch 6 required fixes") |
| P4 | `67f577e2` Peter Nguyen ("docs: apply readability sweep batch 2 required edits") |
| P5 | `1c2f026c` Peter Nguyen ("docs: accept twenty full-page skill reviews after 221") |
| P6 | `ed5f8ae6` Peter Nguyen ("docs(skills): gloss internal jargon at first use in seven skill pages (#601)") |
| P7 | `1c2f026c` Peter Nguyen ("docs: accept twenty full-page skill reviews after 221") |
| P8 | `3d01e1c5` Peter Nguyen ("docs: accept twenty reader pages after PR 208") |

**Keeper IDs — none allocated here.** This batch records evidence only and consumes no keeper-row
identifier. Lane A's allocated band **K-082–K-180** (the lane's reserved range of keeper-row IDs)
is as recorded in the batch-2 record, which cites `KEEPER-ID-ALLOCATION.md`; that allocation
file is not present **at the bound base revision** (`git ls-tree -r --name-only e2a3e20b7c20ef8385b219b39c6405237163406f`
lists no such path, and `git grep -l KEEPER-ID-ALLOCATION e2a3e20b7c20ef8385b219b39c6405237163406f`
matches nothing — exit 1), so this record does not re-derive the band from it. **This claim is
scoped to the named revision and is not a live claim about main:** re-measured 2026-10-16, the same
grep against `3b0d6cd54222442e2e0b1598829bd078c03a22d4` matches **2 files**, so the allocation file
has since arrived on main. The scope is stated because the unscoped form of this sentence ("matches
nothing") went stale with main rather than being wrong when written. The separate keeper assigns the
batch-3 rows' IDs when recording from this evidence. This lane records under AEGIS-APR-101
(recording role, keeper separation) and delivers under AEGIS-APR-039 (the standing backlog
delivery grant: commits, pushes, pull requests and merges for authorized Project Aegis backlog
work — this batch uses the commit/push/PR part only and does not merge).

## 3. Per-page dispositions — eight full-page re-reads, seven accepted and one partial, zero edits

Every page was read **whole, line by line, as prose**, at the bound revision
`e2a3e20b7c20ef8385b219b39c6405237163406f`, in this session; each page's full text was displayed in one read with no
display elision. The six acceptance bullets of the ledger's
[Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page)
were judged per page; the disposition table:

| # | Page | Lines / bytes at the bound revision | Verdict | Edits |
| --- | --- | ---: | --- | ---: |
| P1 | `.claude/skills/adr-writer/assets/adr-template.md` | 65 / 2,565 | **accepted** | 0 |
| P2 | `.claude/skills/aegis-setup/SKILL.md` | 134 / 8,260 | **accepted** | 0 |
| P3 | `.claude/skills/aegis-setup/references/state-contract.md` | 37 / 2,500 | **accepted** | 0 |
| P4 | `.claude/skills/agent-authorization-matrix/SKILL.md` | 177 / 11,115 | **accepted** | 0 |
| P5 | `.claude/skills/agent-authorization-matrix/references/matrix-template.md` | 84 / 4,513 | **accepted** | 0 |
| P6 | `.claude/skills/agent-containment-reviewer/SKILL.md` | 218 / 13,049 | **accepted** | 0 |
| P7 | `.claude/skills/agent-containment-reviewer/references/containment-patterns.md` | 104 / 5,686 | **partial** | 0 |
| P8 | `.claude/skills/agent-failure-recovery/SKILL.md` | 122 / 6,309 | **accepted** | 0 |

Line and byte counts are `git show e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` measured in this session, not
transcribed. No page needed a fix, so no "corrected" row exists and no page's net line change is
anything other than 0.

**Counts: seven accepted, one partial.** P7 is the partial page. Its failing bullet is B2, and the
defect is named in section 4 with its page line: **ACLs** is used bare at page L88 with no
on-page or companion-page gloss, against a library norm that glosses it. A page that carries a
recorded defect is **not** a full-page acceptance, so it is not counted as one here.

**Eligibility for keeper rows — stated so a partial page cannot be laundered into an acceptance.**
**Only P1, P2, P3, P4, P5, P6 and P8 are eligible to receive an acceptance row of any kind from
this evidence. P7 is PARTIAL: it gets NO acceptance row of any kind — no full-page-acceptance row
and no targeted-review row — and it stays pending.** *Acceptance row* is one row of the ledger's
consolidated table recording that a named reader accepted the page at a named revision, in either
its full-page or its targeted-review form; *stays pending* means the page continues to count in
the official pending total until a later eligible re-read clears it.

**The rule this record states, for every reader of it: a page marked PARTIAL is never given an
acceptance row of any kind — no full-page-acceptance row and no targeted-review row — and never
leaves the pending set. Only a page whose verdict is full is eligible for a row.** The mechanism
that makes the rule necessary is named here rather than left implicit: the ledger's fixed-format
event vocabulary has no partial kind, and `tools/readability_acceptance/check_index.py` L181-184
buckets a reachable row whose page has **zero** drift as `accepted` — so a row offered for a
partial page would silently un-pend it, which is the outcome this record must not produce. The
same rule is stated the same way in lane A's batch-5 record
(`docs/evidence/documentation/readability-lane-a-batch-5-2026-10-15.md`, "Eligibility for keeper
rows" and "The corrected PARTIAL ruling"), which is the sibling this record aligns with.

**Full 40-character blob IDs at the bound revision (section 3 verification, computed by command,
not transcribed).** `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` × 8, run in this
session; each ID below is 40 hex characters and each section 7 prefix is its first eight:

| # | Page | Full blob ID (40 hex) |
| --- | --- | --- |
| P1 | `.claude/skills/adr-writer/assets/adr-template.md` | `b0337e23a06d47b759c9e7263ed6050026ae752e` |
| P2 | `.claude/skills/aegis-setup/SKILL.md` | `8b45f8a2b3de6f54abd5a2c5c673f1e38bf4080b` |
| P3 | `.claude/skills/aegis-setup/references/state-contract.md` | `d2c483b69a327a9ad36112b6a3b35595ad0e9d1a` |
| P4 | `.claude/skills/agent-authorization-matrix/SKILL.md` | `bc6351cfd3daac2d0f8a0bfd008a53e240d86073` |
| P5 | `.claude/skills/agent-authorization-matrix/references/matrix-template.md` | `d3b2df8fe8a868ba5e455774ea4994c47feb337a` |
| P6 | `.claude/skills/agent-containment-reviewer/SKILL.md` | `f8d3ad11f1dac6764aaffe8866698c33e4facb0e` |
| P7 | `.claude/skills/agent-containment-reviewer/references/containment-patterns.md` | `3d79aaf520a6cefb5da81b410ca52aa015bab9c4` |
| P8 | `.claude/skills/agent-failure-recovery/SKILL.md` | `27fd46658f83c90aa9bfffb3e1ce89622e5d5ad0` |

## 4. Per-page read detail — ranges, bullets, purpose restatements, verification

**How the quotations in this section read (stated once, then applied).** A quoted span is
**byte-verbatim** in its page at the bound revision except for these stated allowances: whitespace
runs are collapsed to single spaces and a line break is joined with a space; Markdown **de-markup**
is removed (backticks, bold/italic markers, link targets and brackets, a blockquote `>` marker, a
list bullet); and a **`…` marks text omitted** from the middle or end of the page's sentence. A
quotation that **joins two non-adjacent page lines** is not covered by those allowances, so each
one is **marked "normalized, not byte-verbatim" in place** — there are three (§4 P3, P5 and P7,
each a heading joined to the first clause of page L3). This convention was re-derived by sweeping
every double-quoted span in this section against its own page at the bound revision (2026-10-16);
after the three marked joins, no span in this section falls outside the allowances above.

**P1 — `.claude/skills/adr-writer/assets/adr-template.md`** — read whole, L1-65.
Purpose and normal use (restated from the page alone): a fill-in template for a decision author
writing an architecture decision record (ADR) — copy it, number it, answer the Context / Decision
/ Alternatives Considered / Consequences / Operational Impact / Rollback sections, and remove the
guidance comments before publishing; the Rollback section is mandatory and must cover trigger
conditions, back-out steps, hard parts and the point of no return.
Bullets: B1 purpose+audience — satisfied (opens "Template for decision authors: …"). B2
abbreviations — satisfied: ADR expanded at first use ("an architecture decision record (ADR)"),
the `NNNN`/`MMMM` placeholders explained in the opening note, the status vocabulary and its
certainty labels (`(confirmed)` / `(inferred)` / `(unknown)`) stated. B3 structure/example —
satisfied: fixed section headings with per-section guidance comments, placeholder examples
("Use Postgres row-level security for tenant isolation"), and each section states what it must
accept (Rollback: all four parts; "N/A" is not a plan). B4 shipped vs proposed — not applicable: a
decision-record template makes no shipped-state claim about a system; its Status field vocabulary
(proposed | accepted | rejected | deprecated | superseded) is the mechanism that keeps proposed
separate from decided. B5 links/commands — satisfied: one link (`../SKILL.md`, resolves to
`.claude/skills/adr-writer/SKILL.md`, present at the bound revision); zero commands. B6
independent read — this record; the page's author is another agent/human (see section 2).
**Verdict: accepted, no edit.**

**P2 — `.claude/skills/aegis-setup/SKILL.md`** — read whole, L1-134.
Purpose and normal use: a MANUAL-ONLY (never auto-invoke) skill that guides one person through
four plain-language setup choices (Aegis only / Aegis plus a local helper / Aegis plus an online
helper / help me choose) and, on tested single-user Windows PowerShell, saves an Aegis-only
preference for this checkout; it never authorizes a tool, provider, model or agent, never saves a
helper choice as completed, and never asks for a credential.
Bullets: B1 satisfied (frontmatter description + Purpose state the invocation rule and the job).
B2 satisfied — "MANUAL-ONLY; never auto-invoke" is glossed at first use; BER expanded at first use
("Behavioral Eval Runner (BER)"), OS ("Operating system (OS)"), JSON ("JavaScript Object Notation
(JSON)"); Aegis, helper, local, online and tokens each defined at first use in the Workflow.
B3 satisfied — the canonical sections in order, a four-row choice table with per-choice
benefit/cost, one concrete PowerShell command with the path-variable gotcha explained, an Output
Format stating exactly what completion and non-completion say, and Stop Conditions that refuse
credential requests, provider calls, installs and silent record overwrites. B4 satisfied — the
page separates what is shipped ("Only completable choice today" for Aegis only) from what is
proposed/unavailable (both helper paths marked "Unavailable today; do not request a credential"),
and "`selected` means preference only. `verified` requires separate host proof" (verbatim, page
L112-113, the page's line break joined with a space; the page's sentence continues "and is not
emitted here"). B5 satisfied — one
link (`references/state-contract.md`, present); one PowerShell command whose script
`scripts/selection.ps1` exists; the named `scripts/test-selection.ps1`, `evals/evals.json`
and `evals/trigger-evals.json` exist for the skill directory. B6 this record (author: Project
Aegis Agent, another agent — section 2 table).
**Verdict: accepted, no edit.**

**P3 — `.claude/skills/aegis-setup/references/state-contract.md`** — read whole, L1-37.
Purpose and normal use: the exact local-state format and fail-closed rules of the aegis-setup
selection writer — the state directory derivation, the allowed absolute-path spellings, the
project-key computation, the fixed record fields, the no-secrets storage rule, the
unselected/configured/verified/unavailable state vocabulary, and the atomic write/replace
sequence.
Bullets: B1 satisfied (opens "Aegis setup state contract, version 1" — page L1 heading, verbatim).
The longer opening quoted in earlier drafts of this line is **normalized, not byte-verbatim**: it
joins that heading to the first clause of page L3 ("Use this with the Aegis Setup skill") and
flattens that clause's link markup — the words and their order are the page's, the punctuation and
markup are not. B2 satisfied — the opening reading line defines SHA-256, UTF-8, JSON and UTC at
first use; UNC expanded at first use ("Universal Naming Convention (UNC)"); the record fields are
the definition of themselves. B3 satisfied — short purpose-led paragraphs; concrete examples of
accepted and rejected path spellings (`C:\...` / `C:/` accepted; UNC, device-namespace,
drive-relative, rooted-relative rejected); the page's subject IS the accept/produce/refuse
contract (what is stored, what is never stored, what fails closed, what repair cannot do).
B4 satisfied — "configured, verified and unavailable remain distinct future states; this writer
cannot produce them" and "Other operating systems may show the conversation but cannot claim
saved selection until tested" separate shipped capability from proposed. B5 satisfied — one link
(`../SKILL.md`, present); zero commands; the named `selection.ps1` exists. B6 this record
(author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P4 — `.claude/skills/agent-authorization-matrix/SKILL.md`** — read whole, L1-177.
Purpose and normal use: a MANUAL-ONLY skill that produces a standing, deny-by-default
authorization matrix of what an AI agent may do on its own authority, what requires a named human
decision and what is forbidden, per action class and execution context; it holds the
non-negotiable floor (protected-branch merge and deploy/production/secrets/history-rewrite cells
approval-required, auto-merge arming forbidden to agents) and stops after proposing until a human
approves.
Bullets: B1 satisfied (description + Reading key + Purpose). B2 satisfied — "MANUAL-ONLY; never
auto-invoke" glossed at first use; the Reading key defines AI, PR, CI and CLI at first use.
B3 satisfied — the canonical sections in order, a numbered workflow, the concrete auto-merge
incident as the motivating example, an Output Format template whose Status field separates
AWAITING APPROVAL from APPLIED, and Stop Conditions that halt before any unapproved application.
B4 satisfied — proposal-first is enforced throughout ("Propose the artifact … STOP for
approval", "Apply after approval", "No governance file edited before explicit approval"), which
is exactly the shipped-vs-proposed separation. B5 satisfied — one link
(`references/matrix-template.md`, present); the two named `gh` commands use the real GitHub
CLI; `evals/evals.json` and `evals/trigger-evals.json` exist. B6 this record (author: Peter
Nguyen).
**Verdict: accepted, no edit.**

**P5 — `.claude/skills/agent-authorization-matrix/references/matrix-template.md`** — read
whole, L1-84.
Purpose and normal use: the taxonomy and copyable template for the agent-authorization-matrix
skill — the action taxonomy (classify by what the action TRIGGERS), the context axis, the default
floor table, the approval-semantics definitions (one-time vs durable), and the auto-merge case
study that motivates the floor.
Bullets: B1 satisfied (opens "Agent Authorization Matrix — taxonomy and template" — page L1 heading,
verbatim; the longer opening quoted in earlier drafts of this line is **normalized, not
byte-verbatim**: it joins that heading to the first clause of page L3 and flattens that clause's
two link targets — words and order are the page's, the punctuation and markup are not). B2 satisfied — PR, CI and APR
defined in the opening lines ("APR identifies an approval-register record"); "durable grant"
explained at first use; the A/R/F legend (AUTONOMOUS / APPROVAL-REQUIRED / FORBIDDEN) stated
before the table; AEGIS-APR-002 explained where cited. B3 satisfied — tables for taxonomy,
contexts and the pre-filled floor, a concrete case-study narrative with the `mergedBy` detail,
and the deny-by-default rule ("Unlisted action = R by definition"). B4 satisfied — the page
separates the default floor from deviations ("every deviation from this floor carries the
approving human's name and date inside the artifact"), names the real recorded AEGIS-APR-002
grant as a source example, and states that example is not a grant elsewhere. B5 satisfied — two
links (`../SKILL.md` and `../../../../docs/approvals/APPROVAL_REGISTER.md`, both present);
the two named `gh` commands use the real GitHub CLI; the named `agent-governance-audit` skill
exists. B6 this record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P6 — `.claude/skills/agent-containment-reviewer/SKILL.md`** — read whole, L1-218.
Purpose and normal use: a review skill that checks whether a multi-agent system can contain
failure and drift — the OWASP ASI08 cascading-failure half (blast-radius isolation, bounded
trust, circuit breakers, checkpoints, retry and fan-out limits) and the ASI10 rogue-agent half
(inventory, drift baselines, authority-severing kill switches) — returning severity-ranked
findings with propagation/drift paths and the controls that close them.
Bullets: B1 satisfied (description + Reading key + Purpose). B2 satisfied — OWASP expanded at
first use in the description, ASI08/ASI10 in the Reading key, API and DoS in the Reading key, LLM
and AI at first use in the Use When section; SIGKILL (a Unix signal proper name) and `SEV` (a
placeholder token inside the Output Format template) are judged non-defining — noted here rather
than hidden. B3 satisfied — the canonical sections in order, a numbered workflow that demands a
concrete propagation path for every HIGH-severity finding, an Output Format template with a
mandatory "Not reviewed" field, and Stop Conditions that refuse live execution and
side-effecting kills. B4 satisfied with note — the page separates what it designs from what it
executes ("This skill designs containment controls; the `incident-response-runbook` skill authors
the procedure but does not run an incident." — verbatim, page L50-52; live incidents belong to the
human incident owner following the approved runbook); it makes no
shipped-vs-proposed claim about a system. B5 satisfied — one link
(`references/containment-patterns.md`, present); zero commands; `evals/evals.json` and
`evals/trigger-evals.json` exist; every named skill it routes to exists in the library
(ai-cost-guardrail-designer, incident-response-runbook, agent-goal-hijack-defender,
inter-agent-comms-reviewer, observability-operator, rollback-runbook-author,
structured-output-validator, agent-tool-safety-guard, agent-identity-privilege-reviewer,
human-approval-boundary, llm-output-safety-reviewer). B6 this record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

**P7 — `.claude/skills/agent-containment-reviewer/references/containment-patterns.md`** — read
whole, L1-104.
Purpose and normal use: the agent-containment-reviewer reference sheet — failure-domain mapping,
the propagation-path catalog (bad-output / failure / flood / cost / contamination), the
breaker/bulkhead/backpressure patterns, checkpoint-and-rollback design, the agent inventory
schema, the drift-baseline signals, and the authority-severing kill-switch rubric.
Bullets: B1 satisfied (opens "Agent Containment Patterns (ASI08 + ASI10)" — page L1 heading,
verbatim; the longer opening quoted in earlier drafts of this line is **normalized, not
byte-verbatim**: it joins that heading to the first clause of page L3 and flattens its link target
— words and order are the page's, the punctuation and markup are not. ASI08/ASI10 expanded
immediately). B2 **partial, recorded not repaired** —
OWASP is expanded at first use. Three further terms were then measured against the C-1 norm test
(a term is resolved if the page itself, or the page's own linked companion, defines it; otherwise
the gap stands only if the library's practice is to gloss it). Two of the three are **observations,
not gaps**: **API** is resolved by this page's own linked companion `../SKILL.md`, whose Reading key
at **L10** defines "application programming interface (API)"; and **ASI01** is resolved by this
page's own sentence at **L76**, "drift here without an attacker is ASI10, with one it's ASI01", read
with the L3 expansion of OWASP and its naming of ASI08/ASI10. **One term stands as the gap: ACLs,
used bare at page L88** — "broker/topology ACLs closed — not merely process termination" — with no
expansion of *access-control list* anywhere on the page and none in `../SKILL.md`. The norm
measurement supports the gap rather than an assumption about it: at the bound revision **32 of the
653 reader pages use the token `ACL`/`ACLs`; 18 of those 32 gloss it on the page; only 14 use it
bare — 2.1% of the 653 — and this page is one of those 14.** The library's practice is therefore to
gloss it, and the sibling skill in the same family does exactly that:
`.claude/skills/inter-agent-comms-reviewer/SKILL.md` **L13-14** — "**ACL** means access-control list"
(the gloss begins at L13 and completes at L14).
Recorded
as a property of the page's text at the bound revision, not repaired, because editing an
instruction file under `.claude/skills/` would reclassify this change beyond docs-only (the
change-classification-gate's agent-instruction-file rule). B3 satisfied — numbered sections,
propagation-catalog and inventory tables, concrete patterns with the rationale named, and the
kill-switch rubric states the seven conditions that must ALL hold. B4 satisfied with note — the
opening states the live-containment boundary ("Live containment follows the authorized human
incident owner and current approved runbook"); a pattern catalog makes no shipped-state claim
about a system. B5 satisfied — one link (`../SKILL.md`, present); zero commands; every named
skill exists in the library (structured-output-validator, ai-cost-guardrail-designer,
memory-context-poisoning-reviewer, observability-operator, rollback-runbook-author,
agent-identity-privilege-reviewer, inter-agent-comms-reviewer, agent-goal-hijack-defender,
agent-governance-audit, incident-response-runbook). B6 this record (author: Peter Nguyen).
**Verdict: PARTIAL, no edit.** The named defect is the **ACLs** gap at page L88 set out in
the B2 bullet above; the two other terms measured there are observations that resolve, not gaps. A
partial page carries **no acceptance row of any kind and stays pending** (the rule stated in full
in section 3): the earlier form of this line recorded a full-page acceptance beside an
acknowledged unmet bullet, which is the defect this repair corrects.

**P8 — `.claude/skills/agent-failure-recovery/SKILL.md`** — read whole, L1-122.
Purpose and normal use: a MANUAL-ONLY skill that returns a damaged working state (failed runs,
dirty or conflicted trees, partial commits, broken branches, blocked permissions) to a
known-good, verified condition in the fixed order diagnose (read-only) → preserve → recover →
verify → report, with a rescue ref or verified copy covering every valuable path before any
destructive command, and the destructive set gated on fresh explicit human approval.
Bullets: B1 satisfied (description + Purpose state the manual-only posture and the fixed order).
B2 satisfied — "MANUAL-ONLY; never auto-invoke" glossed at first use; the `-u` option's ignored
-file caveat explained at first use; the remaining terms are git command names. B3 satisfied —
the canonical sections in order, a numbered workflow with the preserve-before-touch rule, an
Output Format template, a checklist, and Stop Conditions that enumerate the destructive set
command by command. B4 satisfied with note — the skill states its own operative contract ("The
order is fixed…"; "clean slate" is a human decision, never an agent convenience); it makes no
shipped-vs-proposed claim about a system. B5 satisfied — one link
(`references/recovery-playbooks.md`, present); the named git commands are real; the
"no trigger-evals file" claim is verified (no `evals/trigger-evals.json` for the skill
directory); `evals/evals.json` exists. B6 this record (author: Peter Nguyen).
**Verdict: accepted, no edit.**

## 5. The verbatim quote lines the keeper rows cite (seven lines — one per full page; none for the partial page)

P1 accepted: .claude/skills/adr-writer/assets/adr-template.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P2 accepted: .claude/skills/aegis-setup/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P3 accepted: .claude/skills/aegis-setup/references/state-contract.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P4 accepted: .claude/skills/agent-authorization-matrix/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P5 accepted: .claude/skills/agent-authorization-matrix/references/matrix-template.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P6 accepted: .claude/skills/agent-containment-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
P8 accepted: .claude/skills/agent-failure-recovery/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f

**This list is seven lines, for seven full pages. P7 is deliberately absent, and the absence is
the point.** P7 is PARTIAL (section 3, section 4), so **no row-quote line of any kind is offered
for it** — a line in the shape above is exactly the string a keeper transcribes into an acceptance
row, and `tools/readability_acceptance/check_index.py` L181-184 buckets a reachable row with zero
drift as `accepted`, which would silently un-pend a page this record itself marks partial. An
earlier form of this section offered eight lines, including a P7 line; that eighth line is removed
and must not be reinstated. Seven full pages, seven lines; the partial page has none.

## 6. Count honesty, the machine-visibility note, and the self-cost

- **Both insertion scopes, stated separately — the insert-only claim covers the first commit only.**
  *Against the derivation base* the change is insert-only: the base does not contain this path, so
  `git diff --numstat e2a3e20b..<this repair's commit>` is **549 added / 0 deleted** over one added
  path — and equally `385 0` at the audited head `27ee6291`. That claim is true and it is also
  **insufficient**, because it says nothing about the branch's own history, where the commits are
  not insert-only:
  - `d3eba65b..27ee6291` (the first repair) is **20 added / 3 deleted**;
  - `27ee6291..<this repair's commit>` (this repair) is **184 added / 20 deleted**.

  **The deleted lines, counted by enumerating every `-` line of each diff rather than by a regex.**
  For `d3eba65b..27ee6291` the three deleted lines are the two lines of the old spliced P6
  quotation, plus one line whose *content* begins with a single `-` —
  `- **This lane publishes no readability count of its own** (the D84 official-count switch). The` —
  which the unified diff therefore renders as `-- **This lane…`. For this repair the twenty
  deleted lines were enumerated one by one, and **one of them is again a content line beginning with
  `-`** (`- **Next batch selection rule:** the next 8 paths…`), rendering as `-- **Next batch…`.
  **A parser that reads a leading `--` as anything other than a deletion undercounts both commits**
  — 2 instead of 3, and 19 instead of 20. The two-dash case is not hypothetical here; it is this
  branch. Nothing in this record claims the branch's history is insert-only, and no reader should
  read the base-relative figure as covering the repair commits.
- **This lane publishes no readability count of its own** (the D84 official-count switch — D84 is
  the 2026-10-10 index-repair decision that made `check_index.py` the official pending count). The
  instrument's figures at the base are quoted in section 1 as the instrument's.
- **This batch appends no keeper rows, so there is nothing for the builder to pick up.**
  `build_index.py --report` is run in-lane at this batch's committed head as a regression check
  and exits 0 with `table_rows 101, events 101, full_page_acceptances 81, lost_commit_events 10,
  reader_pages_with_rows 68` — identical to the base state, so the evidence-only diff perturbs
  nothing (command in section 7); no
  `build_index.py --write` is run, the index JSON is not edited, and the machine-visible count
  still comes from the routine index-rebuild PR. The rows the separate keeper later records become
  machine-visible at that rebuild, not here.
- **Self-cost.** This batch record itself is a new reader page with no acceptance row, so it is
  pending and not counted among accepted pages — the self-cost every prior update states.
- **No footer self-digest, and none is required (Stage D ruling, applied).** This record carries no
  `## Footer` and no `sha256:` line at either of its commits, and **none was added to satisfy the
  convention**. The ruling this record applies: a footer self-digest is **not required** for this
  record family and is **not retroactive** — its purpose is detecting silent edits, and git already
  binds these bytes more strongly than a hash stored inside the file can, so a record carrying one
  is not better and a record lacking one is not defective. Where a sibling does carry one it is a
  **convenience, not a requirement**: lane A batch 5
  `6342e38b3cf2adfddf72b51d4bee4311afd990d2a730445f331771ce6c739727` over 53,301 bytes / lines
  1-650, and lane C batch 3
  `db9796c63ac8ab53022d8c4c237e62484cb4786ce19a261b81bbe36d9f58e2f8` over 66,134 bytes / lines
  1-721 — both 64 hex, both reproduced byte-for-byte by this lane's own recomputation on 2026-10-16
  (the trailing newline included in the byte count). They are quoted as calibration of the
  convention, not as a standard this record fails.
- **Next batch selection rule — pages named by path, no index pinned.** The next batch takes **the
  next 8 UNREAD pages of lane A's unread sequence, re-measured at its own implementation base.** It
  is never given as an index range or by index arithmetic, because the pending set moves: the
  quarter length and its last path both changed between the bound base and current main (below), so
  an index pinned here would address different pages there. At the bound base, re-derived in this
  session, those eight are (named by path, **a measurement at that base and not an instruction** —
  the next batch must re-derive them and skip anything an earlier batch has read by then):
  `.claude/skills/agent-failure-recovery/references/recovery-playbooks.md`,
  `.claude/skills/agent-goal-hijack-defender/SKILL.md`,
  `.claude/skills/agent-goal-hijack-defender/references/goal-integrity-controls.md`,
  `.claude/skills/agent-governance-audit/SKILL.md`,
  `.claude/skills/agent-governance-audit/references/audit-control-checklist.md`,
  `.claude/skills/agent-harness-architect/SKILL.md`,
  `.claude/skills/agent-identity-privilege-reviewer/SKILL.md` and
  `.claude/skills/agent-identity-privilege-reviewer/references/agent-identity-patterns.md`.
  An earlier form of this bullet pinned them as "paths 25-32 of 148"; the paths are unchanged and
  the pin is removed.
- **The frontier, measured both ways (not a formality).** *Behind the frontier, at the bound base:*
  lane A's read frontier after batches 1-3 is `.claude/skills/agent-failure-recovery/SKILL.md`
  (1-based path 24 of the 148, sorted index 23), and the 24 paths sorting before it are exactly the
  pages batches 1-3 read — so **no unread page sits behind this lane's frontier at this base, and
  none is orphaned by it.** Measured from each record's own committed bytes on 2026-10-16: batch 1
  (PR #771, head `f6a4e4189ecfbe874f97ec9b6b09bf8fe14f49ad`) reads sorted indices 0-7; batch 2
  (PR #777, head `05ad76072d12070164aaf9135223e49e28a296ae`) reads 8-15; this record reads 16-23;
  and lane A batch 4 (PR #789, head `de2bfe7237d6e853fa81925faa9f68a82881bba7`) reads exactly the
  eight paths named in the bullet above — the rule selecting the same pages the index range named,
  which is the check that makes the rule safe to state instead of a number. *Re-measured at current
  main (`3b0d6cd54222442e2e0b1598829bd078c03a22d4`), which is why the numbers in this bullet are
  dated:* reader pages **657** (was 653), pending union **595** (was 590), `ceil(595/4) = 149` (was
  148), and lane A's last path has moved from
  `.claude/skills/feature-flag-rollout-strategist/references/flag-rollout-sheet.md` to
  `.claude/skills/file-upload-storage-architect/SKILL.md`. **Every one of lane A's first 24 paths
  is still `no_recorded_acceptance` at main** — no keeper has recorded a row from batches 1-3 yet —
  so the instrument's pending set alone cannot tell a read-but-unrecorded page from an unread one,
  and the walk frontier is only visible in the lanes' own batch records. That is the measurement the
  sibling audit's "two unread pages behind a lane's frontier" finding warns about, taken here rather
  than assumed.

## 7. Validation actually run (commands and their real results)

| # | Command | Result |
| --- | --- | --- |
| 1 | `git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main` | exit 0 (acceptance revision contained) |
| 2 | `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` × 8 | blob IDs: P1 `b0337e23…`, P2 `8b45f8a2…`, P3 `d2c483b6…`, P4 `bc6351cf…`, P5 `d3b2df8f…`, P6 `f8d3ad11…`, P7 `3d79aaf5…`, P8 `27fd4665…` (full IDs in section 3 verification and available to the keeper, computed by command, not transcribed) |
| 3 | `git show e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` × 8 | line/byte counts in section 3 reproduced |
| 4 | `python -B scripts/ci/check-markdown-links.py` over the 8 pages | exit 0: `files: 8   links checked: 13   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0` |
| 5 | `python -P scripts/validate-skills.py` | exit 0: `OK: 205 skill(s) valid, 0 warning(s)` |
| 6 | `python scripts/tests/test_validator.py` | exit 0: `OK: 181 gate self-test assertion(s) passed.` |
| 7 | per-path check against `tools/readability_acceptance/acceptance-index.json` `reader_pages` AND `events` | all 8 paths absent from both arrays (pending, as derived) |
| 8 | `git log -1 --format="%h %an %s" -- <page>` × 8 | other authors only (section 2 table) |
| 9 | `python -P -B tools/readability_acceptance/check_index.py --json --ref e2a3e20b7c20ef8385b219b39c6405237163406f` | section 1 summary, exit 0 |
| 10 | `git ls-tree -r --name-only e2a3e20b7c20ef8385b219b39c6405237163406f` | 719 Markdown paths; 65 fixtures; 1 generated report; 653 reader pages; all 13 link occurrences of the 8 pages resolve to present targets |
| 11 | `git ls-remote origin refs/heads/main` | still `e2a3e20b7c20ef8385b219b39c6405237163406f` (base unchanged at branch creation) |
| 12 | per-page named-file and named-skill existence checks (section 4) | all present; the P8 "no trigger-evals file" claim verified true |
| 13 | `python -B tools/readability_acceptance/build_index.py --report --ref <this batch's committed head>` | exit 0; counts in section 6 (identical to the base state), run after the `refs/pull/*/head` fetch |

**Rows 14-20 are the repair round's re-runs (2026-10-16), added because rows 1-13 describe the
audited head `27ee6291` and this repair changed the record's bytes.** Nothing in rows 1-13 is
withdrawn; where a re-run reproduced the same figure, the figure still stands.

| # | Command | Result |
| --- | --- | --- |
| 14 | `python -B tools/readability_acceptance/build_index.py --report --ref 27ee6291` and `--ref e2a3e20b` | exit 0 at both: `table_rows 101, events 101, full_page_acceptances 81, lost_commit_events 10, reader_pages_with_rows 68` — re-asserted after the edits and identical to section 6 |
| 15 | 101 data rows asserted by arithmetic first, then read by the tool | 101 data rows counted by hand, exactly 1 separator row, 0 malformed rows, the table running to end of file with no interior blank line; an `[KL]-digits` id regex would miss the 10 `T-001..T-010` rows, so the assertion is by hand and not by regex |
| 16 | `python -B scripts/ci/check-markdown-links.py` over the 8 pages, and over this record | exit 0: 8 pages `links checked: 13   broken: 0   dead: 0` (matching row 4); this record 1 link / 1 anchor / 0 broken / 0 dead |
| 17 | `python -P scripts/validate-skills.py` and `python scripts/tests/test_validator.py` re-run after the edits | exit 0: `OK: 205 skill(s) valid, 0 warning(s)`; `OK: 181 gate self-test assertion(s) passed.` |
| 18 | `git diff --check e2a3e20b` after the edits | exit 0, no output |
| 19 | quotation re-sweep: every double-quoted span in section 4 against its own page at the bound revision | 41 spans checked; after the three marked line-joins (P3, P5, P7) **no span falls outside the allowances stated at the head of section 4**; the only cross-page quotes are P7's `API` (companion `../SKILL.md` L10) and P7's `ACL` gloss (sibling `inter-agent-comms-reviewer/SKILL.md` L13-14), each attributed in place |
| 20 | `git diff --numstat` for the base and for each pair of the branch's commits | base→`27ee6291` `385 0`; base→this repair's commit `549 0`; `d3eba65b..27ee6291` `20 3`; `27ee6291..this repair's commit` `184 20` (the scopes and the two-dash enumerations are in section 6) |
