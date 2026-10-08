# OPT1-AUDIT lane L2: governance, process rules and approvals

- **Lane:** L2, read-only. Base: detached `origin/main` = `7d1d05e8170254ae60e8deb175c74e244a284a80` (`git rev-parse HEAD`). Clean tree before and after (`git status --porcelain | wc -l` printed 0 both times).
- **Workspace role:** Role A. All four landmarks are present: `README.md` starts `# Project Aegis`; `docs/skills-catalog.md`, `scripts/validate-skills.py` and `artifacts/audits/skill-contract-audit-baseline.json` all exist (checked with `ls`).
- **Start:** 2026-10-07T20:34:45Z (`date -u`). No ETA was announced to the owner at the start. This lane was dispatched as a subagent, so that gap is recorded here and no figure is made up.
- **Skills used (Role A dogfood rule)**

  | Skill | How it was applied | Result |
  | --- | --- | --- |
  | `source-of-truth-reconciler` | Quoted each conflicting claim with its anchor. Labelled each one IS (what the repo does) or SHOULD (what is intended). Applied the precedence rule. Did not pick a winner where only the owner can decide. | The SHOULD-question "which artifact gives the official pending count" has no winner in the repository. It is held for the owner (C1 of the reconciliation below). |
  | `scoped-approval-register` | Worked out effective authority from the register's full history. Checked whether each grant's wording actually covers the action, and treated any widening as needing a new grant. | No active entry authorizes Option 1. AEGIS-APR-101 explicitly withholds it. Widening the keeper's scope to the index would need a new GRANT. |
  | `change-classification-gate` | Reference only: the class-to-validation table. | Regenerating the index needs no human approval by class. Adopting Option 1 is a governance-text change, which delivery-workflow Proportionality routes to a deeper audit. |

  No MANUAL-ONLY skill was used.

## Bottom line

Option 1 does not break any written process, provided it is adopted through the owner decisions it needs. As written, though, C1–C5 are not enough. Five points:

1. **No register entry authorizes it, and one says so outright.** AEGIS-APR-101 Scope FORBIDDEN reads: *"No approval of the charter's proposed canonical index, its precedence, or changed counting rules."* (`docs/approvals/APPROVAL_REGISTER.md:3150`). That does not prohibit Option 1. It means Option 1 needs a **new owner POLICY DECISION**, plus a decision-log D-entry under `CONTRIBUTING.md` rule 4. C1–C5 do not include that decision.
2. **The tool does not produce a single pending count, by design.** `check_index.py` hard-codes `"exact_pending_count": "NOT DERIVABLE from this procedure"` (`tools/readability_acceptance/check_index.py:230`). At `7d1d05e` it splits the 602 indexed pages into four buckets: 212 provably pending, 159 with no recorded acceptance, 224 within 10 lines (undecided), and 7 it cannot decide. Two ledger rules it cannot see decide the two undecided buckets: "accepted unless listed" versus "pending by definition", and "a small edit must be reviewed". Choosing how to count those buckets is exactly the "changed counting rules" that APR-101 withheld.
3. **Nobody is named to regenerate the index.** The keeper's grant covers writing in the ledger file only. The coordinator is barred from the work. No rule names any other holder.
4. **The index goes stale on most documentation merges.** As built, it goes stale whenever a page is added, or the ledger or the evidence records change. That happened on 22 of the 53 first-parent commits since the index was built. The index has never been regenerated.
5. **The CI extension, as sketched, would collide with three standing rules:** gate-guard protection of the workflow file, gate isolation, and `MG1`'s all-green rule.

Rated against today's manual reconciliation, Option 1 is **neutral to helpful** on cost per cycle. It is **slower** if each trigger needs its own 7-stage regeneration PR, and **faster** once conditions C7 and C8 below remove that coupling.

## (a) Process steps, roles and approvals that Option 1 changes, contradicts or leaves without an owner

**Reconciliation report** (`source-of-truth-reconciler` format)

| # | Claim A | Claim B | Type | Verdict |
| --- | --- | --- | --- | --- |
| C1 | The ledger is the current record: *"until then the ledger's own counts govern"* and *"the readability ledger's own pending set is the current record"* (`docs/roadmaps/aegis-open-decisions-2026-09-23.md:148`); the banner says *"the approval register and the readability ledger are the current records"* (`:3`). | Option 1 makes the index the official count. | SHOULD | **Blocked for the owner.** No repository precedence rule decides it, and APR-101 withholds index precedence. Both claims stay recorded. |
| C2 | The tool *"decides nothing"* (`tools/readability_acceptance/README.md:12`) and prints *"a bound plus an unknown remainder, never one exact pending figure"* (`:40-41`). | Option 1 treats the index as "the official pending count". | SHOULD | **Blocked for the owner.** The owner must define which tool output is "the count" before either claim can be corrected. |
| C3 | *"One coordinator owns edits, shared terms, the page ledger, conflict resolution and the final pull request"* (ledger `:2828-2829`; added 2026-09-23 in `2642763b`). | The coordinator *"does not author, edit, commit, push or merge the change itself"* (`AGENTS.md:61-64`; added 2026-10-01 in `29817f50`). The keeper role excludes the coordinator (APR-101 `:3148`). | SHOULD | **AGENTS.md wins.** It is the canonical, current startup rule (precedence rule 3), and the ledger sentence predates it. Option 1 must not name the coordinator as the regenerating role. Stale source to fix forward: ledger `:2828-2829`. |
| C4 | The index's own `rules` map cites ledger line ranges, and the builder comment says *"check_index.py re-reads these lines so a tracker edit cannot silently invalidate the citations"* (`build_index.py:93-94`). | `check_index.py` never reads `rules`: `grep -n 'rules\|RULE_LINES' check_index.py` finds no match. The ledger says *"0 of the 11 ranges still resolves"* (ledger `:164-165`). | IS | **The code wins (precedence rule 2).** The builder comment is false. Under Option 1 those references go stale on every ledger edit. |

**Assumptions surfaced**

- I assumed C3's "named role" means an agent acting at Stage C (implementation) of a normal 7-stage PR. If the owner meant the keeper instead, a new grant is needed (row G3 below).
- I assumed the "CI drift check" extension would fail on drift. If it would only print a warning, rows F17 and F18 mostly fall away.

**Process elements Option 1 touches**

| Element (source) | Effect of Option 1 | Rating | Mitigation |
| --- | --- | --- | --- |
| Precedence of the ledger as the current record (open-decisions `:3`, `:148`; `CONTRIBUTING.md:148-150` *"tracks the full repository sweep"*) | Contradicted. Needs dated forward corrections, not rewrites (`CONTRIBUTING.md` rule 4). | SLOWS (one-time docs PR) | New **C13** |
| Ledger statements *"Do not add, subtract or merge the two figures"* and *"no exact count is asserted"* (ledger `:115-118`), and the owner question held at `:120-123` | Option 1 answers the held question. It needs a forward note naming the new authority and method (PROC-04: a published figure names its method). | SLOWS (one-time) | **C6**, **C13** |
| Who may regenerate the index | **No rule names anyone.** The ledger and the 2026-10-07 note only say regeneration *"writes under `tools/` and needs its own plan and review"* (ledger `:125-126`). The keeper's scope is *"recording … in `docs/roadmaps/aegis-documentation-readability-backlog.md`"* (APR-101 `:3148`), so writing the index JSON is outside it. The coordinator is excluded (`AGENTS.md:61-64`; APR-101). | RISK (no owner) | C3 + new **C8** |
| Keeper procedure (APR-101; charter `docs/evidence/documentation/acceptance-conversion-process-2026-10-02.md` (a)–(b)) | Still works unchanged under C2. However, the keeper's rows are not harvested today. A builder run at `HEAD` (no `--write`) produced no `e6fc8d24` candidate for either setup page; the feasibility page still binds to `8ed59cd761d1`, and the offline-review page has no candidate. APR-101 and the charter fix no row format, so a future keeper's wording could silently stop harvesting. | RISK | C1, plus a pinned keeper-row format (part of **C10**) |
| A second recording channel: `stated-acceptances.json` (hand-curated, 19 rows: 10 `tracker-row`, 9 `tracker-audit-table`) | The builder checks only that each row's revision resolves and its path exists (`build_index.py:469-504`). It does not check that the row's `quote` appears in the ledger. Under Option 1, editing this file would change the official count without a keeper act, bypassing the keeper's independence rules (APR-101: not the author, not the reviewer, not the coordinator). | RISK | New **C10** (the builder verifies each quote exists in the ledger) |
| Every ledger edit must be safe for the harvester | Today that is a per-PR choice: PR #677's acceptance criteria AC-5 and AC-6 required that *"no added sentence or table cell reads as an acceptance to the harvester's own functions"*. Under Option 1 it becomes a standing duty on every ledger writer. Keeper rows must harvest; everything else must not. No written rule or owner covers this. | SLOWS + RISK | **C10** |
| Five-merge re-estimation (`docs/roadmaps/aegis-execution-metrics.md:65-69`) | Not broken; only the source of the forecast's readability input changes. Adopting Option 1 is a *"material owner decision"*, which *"triggers an earlier forecast update"* (`:68-69`). The five-merge windows are unreliable as a regeneration schedule: *"twelve complete five-merge windows"* were caught up after the fact (`aegis-backlog-forecast.md:15`). | SLOWS (one-time) / RISK if regeneration rides on checkpoints | **C13**; do not tie C3 to the five-merge checkpoint |
| `CONTRIBUTING.md` rule 6 (`:134-137`): *"name … any pages still waiting for the repository-wide readability sweep"* | No rule requires the ledger's figure. Under Option 1, `check_index.py --path <p>` answers this per page with one command, as long as the index is fresh. | HELPS | C7 |
| Decision banking (`CONTRIBUTING.md` rule 4; highest D-entry is D72 by grep of `docs/reconciliation/step-0-reconciliation-v4.md`; the 10-line rule *"carries no decision number"*, ledger `:424-428`) | Switching the authority is a material decision, so it owes the next free D-entry. | SLOWS (one-time) | **C6** |

## (b) Owner grants and register entries Option 1 needs, and whether any existing entry forbids it

**No existing entry forbids Option 1.** Several decline to authorize it, and some bound how it can be delivered:

- **AEGIS-APR-101 Scope FORBIDDEN** (`:3150`): *"No approval of the charter's proposed canonical index, its precedence, or changed counting rules."* This is repeated in the ledger (`:120-123`, `:3350`) and in the charter (`:434`: *"Items 2 and 3 of Ratification owed are therefore still owed"*). Option 1 is exactly charter items 2 and 3: the index's path and precedence, and the count consequence.
- **AEGIS-APR-105** (`:3380-3448`): the seven-stage policy applies to every change. It has no fast lane for generated artifacts, and *"any replacement requires a later recorded owner choice"*.
- **AEGIS-APR-100** (`:3070-3141`): commit, push and merge are pre-approved, but the Scope FORBIDDEN says *"does not start or enlarge a work package … waive a protected `gate-guard` … A separate applicable work grant is still needed."*
- **AEGIS-APR-047**: the only standing `gate-guard` exception. It covers four BER files and nothing under `.github/workflows/` or `tools/readability_acceptance/` (`CONTRIBUTING.md:52-56`; APR-100 restates it).

**Grants and decisions needed**

| ID | What is needed | Why | Kind |
| --- | --- | --- | --- |
| G1 | Owner **POLICY DECISION**: the index is authoritative for the pending count; the ledger stays authoritative for the acceptance records and their narrative; a disagreement between them is a defect, fixed forward in the ledger or in the harvester and never by hand-editing the index. | APR-101 withholds precedence; open-decisions `:148` currently says the ledger governs. | Register entry, plus the next free D-entry |
| G2 | Owner **counting-rule decision** for each bucket the tool reports: no recorded acceptance (159 at `7d1d05e`; 172 in a rebuild at `HEAD`); within 10 lines but unreviewed (224); cannot decide (7); and pages missing from the index (7). | APR-101 withholds *"changed counting rules"*. The charter (`:350-355`) calls the count change an *"owner-visible consequence"*. | The same entry as G1, or a separate one |
| G3 | Either a **new GRANT widening the keeper's scope** to running `build_index.py --write` in its own recording PR, or a named non-coordinator role. | APR-101 scope is the ledger file only. Under `scoped-approval-register`, widening is a new grant, not a supersession. | Register GRANT |
| G4 | A **standing work authorization** for recurring regenerations. | APR-100 needs *"a separate applicable work grant"*. Without one, each regeneration needs the owner to select it. | Register GRANT |
| G5 | C4's preservation method. **No tags exist today**: `git tag -l` and `git ls-remote --tags origin` both count 0. Adopting tags is a new repository convention, and no grant names a tag push. | `e6fc8d24` is reachable only from `origin/docs/readability-batch-b` (`git merge-base --is-ancestor` exit 1; `for-each-ref --contains` lists that one ref). `65bacc7d6b85` and `d3dcb62a335d` are already lost (`git cat-file -e` exit 128). `delete_branch_on_merge: false` (`gh api repos/...`), yet objects were still lost. | Owner decision |
| G6 | Only for the CI extension: a one-time, exact-head `gate-guard` exception for editing `.github/workflows/validate-skills.yml`, plus a placement decision (see F17). | The workflow path is protected (gate pattern at `validate-skills.yml:528`). APR-100 forbids waiving it. | One-time register GRANT, then a CONSUMED event |
| G7 | Owner classification of `tools/readability_acceptance/` under *"approval/evidence tooling under `tools/`"* (`CONTRIBUTING.md:243-245`). | Every PR must answer the Security-relevant surface question correctly, and `SD-F` gates on that answer. Making the tool official strengthens the reading that it is evidence tooling. | Owner decision (open-decisions row) |

## (c) Delivery-stage cycles per index regeneration, compared with today's manual reconciliation

**Today: PR #677, measured with REST calls (`gh api .../pulls/677`, `.../issues/677/comments`)**

- **Timeline:** 1 commit `ccf3fc22` at 18:31:35Z; PR opened 18:35:11Z; Codex usage-limit notice 18:35:18Z; `SD-D: ACCEPT` 18:50:10Z; `SD-E: INCOMPLETE — UNRUN LISTED` 18:56:28Z; `SD-F: REVISE` 19:07:14Z; `SD-F: ACCEPT` 19:12:12Z; merged 19:14:33Z; `SD-G` receipt 19:15:20Z.
- **Wall time from commit to merge:** 42m58s. The PR was open for 39m22s.
- **REVISE rounds:** 1 is verifiable on the PR (`SD-F` round 1). Its cause was a missing Stage E row in the skills table, a bound-field problem, not a content defect. The body's *"`PLAN-rev2.md` … received `SD-B: ACCEPT`"* implies an earlier plan revision, so a Stage B REVISE is likely but **unverified**: the plan files are *"session artifacts held by the coordinator"*.
- **The brief's "~1h40m wall":** **unverified.** The start of Stage A cannot be seen in the repository or the PR.
- **Agents:** 7 distinct stage holders (`docs/delivery-workflow.md`: *"A full seven-stage change needs seven distinct holders"*).

**Option 1: each regeneration**

| Item | Value | Basis |
| --- | --- | --- |
| Stages and agents | 7 stages, 7 distinct agents, at least one Codex wait (`MG3`) | APR-105 covers every change. Proportionality *"bounds the audit's length, never its existence"*. No exemption exists for generated artifacts. |
| Owner exception | None needed | `tools/readability_acceptance/**` and the ledger match the gate pattern in 0 of 14 files (pattern loop over `git ls-tree`). |
| CI | `tools-tests-linux` and `tools-tests-windows` run, because the path filter matches `^tools/`. Neither tests `readability_acceptance` (`grep readability .github/ scripts/` finds 0). PR #677's Windows job was skipped. | `validate-skills.yml:57-99`, `:355-460` |
| Review effort | Probably lighter than #677. Stages D and E can rebuild deterministically and compare bytes, **but only if the build is reproducible** (F9). | **Unmeasured:** no regeneration has ever run. `git log -- tools/readability_acceptance` shows 1 commit, #629. |
| Time | **Unknown.** No sample exists, and PROC-12 marks coordinator estimates as the least reliable input. | n/a |

**How often regeneration triggers**

- **Option 1 as specified (C1–C5), with `check_index.py` reading only the rows already in the index:** any merge that adds a page, records an acceptance, or changes an evidence record makes the index stale. That happened on **22 of 53** first-parent commits from `d6e48418` to `7d1d05e` (per-commit `git diff --diff-filter=A '*.md'` plus touches to the ledger or to `docs/evidence/documentation`). That is an upper-bound proxy. Run as separate PRs, that is up to 22 extra 7-stage cycles in about 5 days. **SLOWS.**
- **With C7** (pages missing from the index are counted by rule at `--ref`): only acceptance-recording events trigger a regeneration. Measured: 1 keeper recording since APR-101 (PR #635; the ledger has one `First ledger-keeper recording` heading). Each recording costs 14 stage-holds (keeper PR plus regeneration PR), or **7** if G3 lets the keeper regenerate in the same PR.
- **One-time adoption:** a harvester-repair PR, the independent review (C5), the owner-decision register and D-entry PR (G1–G4), and a PR correcting surfaces forward (C13). That is about 4 PRs × 7 stages = about 28 stage-holds. This is an **agent estimate, not measured**.
- **Review rounds:** no cap applies. The owner's *"CAP REVIEW ROUNDS … DECLINED AND TABLED … Until then the policy remains run-until-clean"* (2026-10-04, re-raise due 2026-10-11) is recorded **only** on `origin/coord/idle-check-2026-10-04:.coord/coordinator-cadence.jsonl` (line 72). `git grep 'run-until-clean' origin/main` finds 0.

## (d) Ledger rules the index does not or cannot encode (checked against `tools/readability_acceptance` code)

| Ledger rule (anchor) | Code behaviour (anchor and evidence) | Rating |
| --- | --- | --- |
| A small edit keeps acceptance only if an independent reviewer checked it (2026-09-28; ledger `:2784-2791`) | Not encodable. Git cannot see review, so 224 pages stay "within 10 lines, undecided" (`check_index.py:28-33`, `:233-239`). | BREAKS exactness unless G2 rules on it |
| Accepted unless listed (ledger `:112`, `:392-394`) versus pending by definition (charter (c), ledger `:3212-3214`) | Pages with no recorded acceptance are reported as unknown, never counted (`check_index.py:170-178`). | BREAKS exactness unless G2 rules on it |
| The net-difference baseline is the **last full-page acceptance**; a retained targeted edit does not reset it (ledger `:2773-2799`) | `RETENTION_RE` and `ACCEPT_RE` turn any "keeps acceptance" or "accepted" in a cell into an acceptance at the cell's last revision (`build_index.py:114-123`, `:420-445`). At ledger `:2612` (as of `d6e48418`), both `CONTRIBUTING.md` (*"keeps acceptance after a targeted review"*) and `project-orchestrator/SKILL.md` (*"becomes **pending**"*) were recorded as `accepted` at `7b3fbca`. The real acceptance `469d6cb` (PR #452) was missed. No count effect today: drift is 61 and 37 lines, so both pages are pending either way. | RISK (latent under-count). Neither mis-binding is among the four blind spots PR #677 named. |
| Corrections forward revoke an earlier recorded acceptance (for example ledger `:330-336`, `:409-412`) | The harvester has no concept of revocation. `newest_first` picks the candidate with the newest revision date (`build_index.py:459-466`). | RISK |
| A renamed or renumbered heading is not a new section (ledger `:2781-2782`) | `HEADING_RE = ^\+#{1,6} ` counts any added heading line (`check_index.py:56`, `:95-100`). At `7d1d05e`, 17 pages are pending only through the new-section test, and all 17 genuinely add `## Current reading` (0 removed headings), so there is no false positive today. | RISK (latent over-count) |
| A new page starts pending (ledger `:99`, `:269-271`) | Pages added after the index was built are missing from `reader_pages`, so `check_index` never sees them. PR #677 had to add 7 by hand. | SLOWS (forces regeneration) → **C7** |
| Hand-written text in a generated report needs independent review (ledger `:2808-2810`) | Generated reports are excluded wholesale (`build_index.py:65`, `:149-155`). | NEUTRAL (1 file) |
| Acceptances recorded only in pull-request comments ("named as accepted on GitHub", ledger `:2879`) | Not visible to git (`README.md:60-61`). | RISK |
| The rule text's own line references | They rot with every ledger edit (0 of 11 resolve). The builder only checks `end > len(lines)` (`build_index.py:507-516`). | RISK → **C10** |
| Reproducibility of an "official" figure (PROC-04: *"a published figure names its method"*) | The builder reads the ledger and the evidence files from the **working tree**, not from `--ref` (`build_index.py:356-358`, `:411`, `:478`). A rebuild at `HEAD` in this clone drops the 6 `65bacc7` rows from `stated-acceptances.json` (*"STATED DROPPED (revision unresolved)"*), so those pages move from cannot-decide to no-record, and the result depends on which clone built it. | RISK → **C9**, C4 |
| Things that are encoded correctly | Net difference measured as `numstat` added plus deleted from the acceptance revision (`check_index.py:69-92`). Edits made before the 2026-09-27 rule are counted automatically. Fixture and generated-report classes. Unreachable revisions are not decided (PROC-01). | HELPS |

## Findings table

| # | Finding | Rating | Mitigated by |
| --- | --- | --- | --- |
| F1 | No authority for the precedence switch; APR-101 withholds it | BREAKS if adopted without it | new C6 (G1, G2) |
| F2 | Open-decisions `:3` and `:148` name the ledger as the current record | SLOWS (one-time) | new C13 |
| F3 | The tool emits no single count (by design); G2 has to define one | BREAKS without G2 | C6 |
| F4 | No role is named to regenerate; keeper scope is the ledger only; coordinator excluded; ledger `:2828-2829` is stale | RISK | C3 + new C8 (G3) |
| F5 | Index goes stale on new pages and recordings (22 of 53 merges); never regenerated | SLOWS | new C7 |
| F6 | Keeper rows not harvested; keeper row format not pinned | RISK | C1 + C10 |
| F7 | Every ledger edit must stay safe for the harvester (as PR #677 AC-5/AC-6 required) | SLOWS / RISK | C10 |
| F8 | Rule-line references rot; the builder comment's claim is false | RISK | C10 |
| F9 | Build reads the working tree; results depend on the clone | RISK | new C9, C4 |
| F10 | Retention or "becomes pending" text harvested as acceptance (`7b3fbca`) | RISK (latent) | C5 must include these as regression cases |
| F11 | "Unreviewed small edits" (224) and "accepted unless listed" (159/172) cannot be encoded | BREAKS exactness | C6 |
| F12 | Rename-is-not-a-new-section not encoded (0 cases today) | RISK | C5 regression case |
| F13 | Each regeneration is a full 7-stage, 7-agent cycle; no fast lane (APR-105); no round cap (tabled) | SLOWS per trigger | C7 + C8 (bundle into the keeper PR) |
| F14 | Regeneration needs no `gate-guard` exception (0 of 14 paths protected) | HELPS | n/a |
| F15 | The CI extension edits a protected workflow, so a one-time owner exception is needed | SLOWS | new C11 (G6) |
| F16 | Gate isolation: the index check cannot run in a gate job unless `tools/readability_acceptance/` is protected, and then every regeneration trips `gate-guard` and needs an owner exception | BREAKS the cheap regeneration path | C11: run it advisory only |
| F17 | Advisory jobs are path-scoped to `^tools/` (owner right-sizing, 2026-10-05), so they skip the docs PRs that cause drift. `MG1` treats any red applicable check as merge-blocking. | RISK / SLOWS | C11: informational, non-failing output |
| F18 | Security-surface classification of the tool is ambiguous | RISK | new C12 (G7) |
| F19 | The repository has no tag convention; one acceptance revision is reachable from one side branch only; two are lost | RISK | C4 + G5 |
| F20 | Needs a D-entry and an early forecast update | SLOWS (one-time) | C6, C13 |
| F21 | Replaces judgement-heavy reconciliations (#677) with a command, encodes net difference and pre-rule edits natively, and removes the "accepted unless listed" under-count (if G2 chooses so) | HELPS | n/a |

## What Option 2 (the ledger stays official) costs

- Manual reconciliation in the style of #677 continues. Each one is a 7-stage cycle with judgement-heavy figures.
- The ledger's floor is admittedly stale: *"a re-run could only raise the floor"* (ledger `:107`). The two bases cannot be combined (`:115-118`).
- The "accepted unless listed" under-count pattern stays.
- The harvester repair is owed under **both** options (ledger `:125-130`).
- The ledger's self-cost does not change under either option: any edit of more than 10 lines returns the ledger to pending. Five ledger edits since the keeper's recording (first-parent `git log`) each returned it to pending, and each one also moved the index's line references.

## Proposed new conditions (in addition to C1–C5)

- **C6.** One owner POLICY DECISION covering G1 and G2: precedence, plus a counting rule for every tool bucket. Recorded in the register and as the next free D-entry.
- **C7.** `check_index` counts every tracked reader page at `--ref`, and pages missing from the index are classified by C6's rule. Then only acceptance recordings trigger a regeneration.
- **C8.** Name the regenerating holder, never the coordinator. Either widen the keeper's scope by a new grant (G3) so it can regenerate in the same PR, or name a separate Stage C holder. Add a standing work grant (G4).
- **C9.** Reproducible build: `--ref` pinned, a clean worktree at that revision, and a recorded rule for lost or side-branch-only revisions. Stages D and E verify by rebuilding and comparing bytes.
- **C10.** Harvester discipline:
  - every curated `stated-acceptances.json` row must quote ledger text that the builder can find;
  - the keeper row format is pinned;
  - retention and negated or "becomes pending" text never binds as an acceptance;
  - rule-line references are validated against their text, or removed.
- **C11.** CI drift output is informational and non-failing. Any workflow edit takes a one-time exact-head exception and an owner placement decision.
- **C12.** The owner classifies the tool for the Security-relevant surface answer.
- **C13.** One docs PR adds dated forward notes on: open-decisions `:3` and `:148`, `CONTRIBUTING.md:148-150`, the tool README `:12` and `:40-41`, ledger `:115-123` and `:2828-2829`, and the forecast note `:17-30`. The early forecast update follows from `aegis-execution-metrics.md:68-69`.

## Evidence commands (key outputs quoted above)

- `git rev-parse HEAD` → `7d1d05e8…`. `git status --porcelain | wc -l` → 0, before and after.
- `grep -n` / `sed -n` over the files and lines cited.
- `git show d6e48418:<ledger> | sed -n 2612p`.
- Gate pattern loop over `git ls-tree -r --name-only HEAD -- tools/readability_acceptance <ledger>` → `files=14 matched=0`.
- `python3 -I -B tools/readability_acceptance/check_index.py --json --ref 7d1d05e8…` → 602 / 436 / 212 / 159 / 224 / 7.
- `TMPDIR=<scratch> python3 -I -B tools/readability_acceptance/build_index.py --ref HEAD --candidates` (no `--write`) → 675 / 609 / recorded 437 / unknown 172 / 6 rows dropped as `STATED DROPPED`.
- `python3 -B -m unittest discover -s tools/readability_acceptance/tests` → 7 tests OK, and no `__pycache__` left behind.
- `git merge-base --is-ancestor e6fc8d24 origin/main` → exit 1. `git cat-file -e 65bacc7d6b85^{commit}` → exit 128.
- `git tag -l | wc -l` → 0. `gh api repos/ModernNomad-98/Project-Aegis` → `delete_branch_on_merge: false`.
- `gh api .../pulls/677`, `.../pulls/677/commits`, `.../issues/677/comments`.
- `git show origin/coord/idle-check-2026-10-04:.coord/coordinator-cadence.jsonl`.

## Not checked

- The full text of the 3,282-line `process-issues-and-prevention-2026-10-02.md` beyond PROC-01, PROC-04 and PROC-05.
- Most ledger dated history (lines 433–2626).
- The full register, beyond searches and the entries APR-047 (by citation), APR-100, APR-101, APR-102 (skim) and APR-105.
- Session-checkpoint pages: matched by `grep` only. None mentions the index or the keeper.
- PR #677's Stage A and B artifacts (held off-repository) and its true start time.
- Whether PR #629 (the index tool) was independently reviewed (PROC-05).
- Correctness of the tool beyond rule encoding. That is assumed to be another lane's scope.
- Branch-protection settings beyond `delete_branch_on_merge`.
- Codex review behaviour.
- Nothing in the reserved scope was touched.

- **Finish:** 2026-10-07T20:46:32Z (`date -u`). Measured wall time: 11m47s from 20:34:45Z. Active time was not measured separately. No ETA was given at the start, so there is nothing to compare against.
