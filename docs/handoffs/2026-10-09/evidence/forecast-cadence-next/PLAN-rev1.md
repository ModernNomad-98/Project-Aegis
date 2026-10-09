# FORECAST-CADENCE-NEXT — Stage A plan, revision 1

**SD-A: COMPLETE — planning artifact, awaiting a different agent's hash-bound Stage B audit.** This plan authorizes no source edit or publication by its author.

| Field | Value |
| --- | --- |
| Item | Bounded forecast and measurement checkpoint through PR #688 |
| Stage / holder | A / `/root/backlog_current_inventory` |
| First observed start | 2026-10-09 16:53:30 UTC, clock tool |
| Initial estimate | 15–25 active-work minutes, supplied by coordinator; active time is not separately metered |
| Previous item estimate | None: this is a new continuation checkpoint, not another estimate of the delivered #687 package |
| Entire backlog ETA | Not derivable. The ten-row 71–146 active-hour figure is an unvalidated historical subtotal; unestimated and unselected outcomes remain outside it |
| Immutable assessed cutoff M | `625fc66711eaf7b3ee788cbc2dff98f05f147c1c`, PR #688 integration |
| M tree | `3fb8bf9078cc0150489c294aff273cd0421462b3` |
| Prior assessed cutoff P | `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf`, PR #685 integration |
| Allowed planner writes | This plan and evidence under `C:\src\Codex Projects\Project Aegis\forecast-cadence-next` only |
| Finish / digest | Captured in a separate receipt after read-back; not embedded as a self-referential hash |

## 1. Intent, scope authority and classification

Record the next already-completed five-integration window and the remaining source-backed outcomes without inventing progress, changing a selection, or restarting the cadence. The owner said **"add max agents to work on backlogs"** in this Project Aegis chat. The coordinator selected this bounded Stage A planning task and instructed: **"Define minimal source paths/lines for bounded checkpoint update: window #685,#686,#681,#687,#683 closes at #683; #689/#688 residual; preserve forecast's uncertainty and overlap statements, no invented current ETA or selection."** This is planning authority; later stages need their own assignment and existing delivery authority.

The existing measurement rule at M `docs/roadmaps/aegis-execution-metrics.md:61–76` requires named work estimates, honest time splits and a reassessment after each five integrated PRs. Its later `:3083–3115` reconciliation preserves the #344 anchor and carries #685 rather than restarting at it. This plan applies that rule; it changes no rule.

`change-classification-gate` classification: **docs-only, factual planning/measurement records**. These two pages will report observed integrations and the frozen source's remaining gates. They do not change agent instructions, permissions, work selection, invocation posture, CI or enforcement. If the actual change does any of those things, stop and reclassify at A/B.

The source-library role was locally corroborated in `skillbatch/stage-g-681/validation`: README begins `# Project Aegis`, and the skills catalog, validator and audit baseline landmarks exist. That clone supplies local skills; current policy and source facts here come from GitHub at M, not the clone's old branch. The enclosing scratch directory is not a Git checkout.

The M approval-register preamble permits an action only under an effectively active human grant after lifecycle and scope checks, and recognizes direct current owner instructions. APR-039 covers delivery of authorized backlog work; APR-100 covers delivery mechanics for separately authorized work, not new work selection. No forecast update revives a spent grant, resumes a paused program or changes APR-120/121. A lifecycle/reference scan of the whole saved M register found no later revocation of APR-039/100; their later references preserve or constrain separate scopes. The later C/G holders must perform their own current authority read rather than treating this plan as their grant.

## 2. Why #687 does not already cover this checkpoint

Read-only `gh api repos/ModernNomad-98/Project-Aegis/pulls/687` returned head `e834ea7079060314a2bc4f4275938b1cf01e0f7d`, merge `6650f3af091cb14da7de796848d94af5a0aea72c`, merged at `2026-10-09T15:46:44Z`, and two changed files. Its complete files response contains only the forecast (+135/−0) and execution measurements (+254/−0).

The resulting M forecast `:4730–4856` explicitly assesses only through P/#685. Its metrics companion `:3045–3290` lists the 124 integrations through #685, closes the prior final window at #684 and carries #685. It explicitly says there is no reset at #685. Neither M page contains a subsequent #683-boundary or #688-cutoff assessment. Thus #687 delivered the previous assessment, counts as one later integration, and did not assess its own later integration or close the new window. Do not repeat the 124-PR census or recast #687 as unfinished work.

## 3. Verified integration evidence

`integration-evidence.json` in this scratch directory was read back successfully. SHA-256: `1DCC631F8CF8C7D99B0452572008EBB9BBB951128A62C383AF9F0924FC14F57C`. It records observation at `2026-10-09T16:55:46.8346160Z`, the exact P...M comparison, the six first-parent integrations, exact PR associations, complete per-PR file lists and the comparison's changed paths.

Method: GET `repos/ModernNomad-98/Project-Aegis/compare/P...M`; require all 16 returned commit objects to equal `total_commits`; follow parent zero from M back to P; for each of the six encountered integrations, GET `commits/<sha>/pulls` and require exactly one merged PR with matching `merge_commit_sha` and base `main`; read that PR and its complete file list, checking file count against `changed_files`. This includes single-parent integrations if any exist; it does not assume that all PRs use merge commits. It does not count the ten branch commits as ten more PRs.

| Order after P | PR / result of this source change | GitHub `merged_at` UTC | Integration SHA |
| ---: | --- | --- | --- |
| 1 | #686 — historical CI-job duration evidence; no active-effort calibration | 2026-10-09T14:34:16Z | `2c68df263c99cdb66d6ea4c76cd480f0bf19b5b5` |
| 2 | #681 — unselected expansion proposal; no skill built or selected | 2026-10-09T14:56:02Z | `fc3c68b628a5f2660db0ab490706660b90e30d3f` |
| 3 | #687 — publication of the assessment through #685 | 2026-10-09T15:46:44Z | `6650f3af091cb14da7de796848d94af5a0aea72c` |
| 4 | #683 — records APR-120 and later green-only hold APR-121; does not deliver #682's repair | 2026-10-09T15:53:09Z | `a4fb1445ea92ff6df469627ea9e10f769d69d830` |
| 5 | #689 — stale-checkout evidence-reading corrections; no index-program switch | 2026-10-09T16:03:58Z | `c585afdf737ac021d91cd564dc61ad7e1f6b6053` |
| 6 | #688 — ROUTE-002 textual triage; N12/N13 remain separately selectable proposal candidates | 2026-10-09T16:17:39Z | `625fc66711eaf7b3ee788cbc2dff98f05f147c1c` |

P/#685 merged at `2026-10-09T02:00:04Z`. Combine its one carried membership with the six new integrations: **7 members = one complete window (#685, #686, #681, #687, #683) plus two residuals (#689, #688)**. The next boundary is three additional integrations after M; every later integration, including the PR publishing this checkpoint, counts. No reset or exclusion for documentation/checkpoint PRs is permitted.

GitHub PR `merged_at` is the table's timestamp source throughout. Some Git commit committer timestamps differ by one second; do not mix the two. The optional P-to-M endpoint interval computes to **14h17m35s of wall time**, not active effort, throughput or this package's duration. Omitting that interval is acceptable; inventing active/review/CI/wait splits is not.

The complete P...M changed-path inventory contains ten documentary/evidence paths and no BER, CP, Stage 4B execution or skill implementation. Read actual file contents and the changed register entries before concluding outcome effects; titles and file absence alone are not evidence of live activity outside this fixed source.

## 4. Exact candidate path contract

Only these **two source files** may change. At M both already end with a newline. Preserve all original bytes except for the two permitted insertion locations in each file: a latest-reading insertion after the opening `## Start here` heading, and a new dated section appended at EOF. No existing historical line is replaced or deleted.

| Path | M location / proposed insertion | Content purpose |
| --- | --- | --- |
| `docs/roadmaps/aegis-backlog-forecast.md` | After line 3, before the existing #685 banner; append after line 4856 | A brief newest reading that explicitly dates its #688 cutoff and identifies the #685 banner below as the prior frozen checkpoint; a new `## Cadence reassessment through PR #688 (2026-10-09)` section |
| `docs/roadmaps/aegis-execution-metrics.md` | After line 3, before the existing #685 banner; append after line 3290 | Matching newest reading and `## Cadence measurement checkpoint through PR #688 (2026-10-09)` section, with the reproducible integration table and residual arithmetic |

Line locations are discovery pointers at M, not instructions to edit later line numbers blindly. Unique heading/context and raw-byte checks select the location against implementation base B. The old #685 banners and their entire bodies remain byte-identical. If the insertion leaves two misleading undated claims of present authority, improve the new insertion's explanation rather than rewriting the old dated record.

**Not touched:** coordinator figures and METRICS-1 JSON, approval register, reconciliation log, open-decisions index, readability ledger/index, source audit baselines, skill proposal, skills/evals, code/tests/scripts, CI/workflows/settings, AGENTS/CLAUDE/CONTRIBUTING, protected-policy work and all other agents' artifacts. No new tracked source file or persistent checker is needed. Do not import scratch evidence into the source diff.

The two allowed paths are absent from M CONTRIBUTING's security-surface list (`:238–249`) and from the fetched workflow's `gate_pattern`. The expected PR security answer is **No**, subject to the actual diff and contribution source at F. This does not decide any other PR's security classification.

## 5. Minimum forecast content and evidence boundaries

The new forecast section must:

1. Identify M, P, the measured interval, the separate #683 window boundary and #688 assessed cutoff, and link to the new metrics section. State that #687's publication assessed through #685 only.
2. Give a concise six-PR outcome account; link #681's now-merged proposal and #688's triage without selecting either. Distinguish #683's documented conditions from delivery of #682. Make no historical-green-CI assertion, host assertion or source-merge-to-runtime inference.
3. Reconsider every one of the ten selected outcomes in the #685 table exactly once. A concise table may name each and link its authoritative dependency/status record. At this cutoff, explain why no cited merged source closes a selected outcome; preserve the open/blocked/backlog distinctions and low confidence in effort. This is a source-cutoff statement, not a claim that no work happened outside the repository.
4. Preserve **71–146 as an unvalidated historical subtotal**, not measured remaining work. Preserve **68–140 as an unvalidated historical group sum with the Phase 3/4 #127 overlap**, and no exact deduction. Keep Stage 4B and BER-BKL-009 residuals unestimated, readability index repair/switch paused and outside the subtotal, and the full selected/all-backlog ETA not derivable. Do not turn #686's CI-job sample into active-labor calibration.
5. Reconsider the seven conditional/unselected rows and six unselected expansion groups by linking the #685 tables and recording unchanged selection/dependency status, except for the availability of the new #681 proposal. Do not re-add delivered QA Tier 1, Phase 6, Phase 7 or category-08 batches, or duplicate #127. Preserve the parked UNRUN/conduct-intake dispositions and source-inspection gate; none is activated here.
6. Use bounded non-binding horizons: **now** describes the delivered documentary outcomes and this recording; **next** identifies already-recorded owner/input/evidence gates as unresolved dependencies, with no new pick; **later** retains the dependent and optional outcomes. No precise dates, capacity or workload promise. More agents or more documentary merges alone do not prove a selected outcome complete. Comparative value and active capacity are unknown.
7. State the next cadence trigger from the two residuals, and earlier reassessment on a material owner decision. The updating PR participates normally in the continuing count. Explain terms at first use in the new section or point to a clearly usable nearby reading key; human readers must distinguish PR number, selected outcome and approval ID.

The metrics section owns exact order, count method, links, UTC merge times, full integration SHAs, carry/residuals and timing limitations. The forecast owns outcome interpretation. Cross-link the two; avoid reproducing the 124-row historical census or #686's duration sample.

## 6. Acceptance criteria, all verifiable on the candidate

These are candidate-content criteria. Publication-time CI, automated review, final review, merge and postmerge observations are subsequent delivery obligations, not predeclared omissions from a content criterion. No AC below is declared unverifiable at Stage D. An unexpectedly unrun criterion therefore requires D REVISE or an independently re-audited plan change; it cannot be silently accepted.

| AC | Observable requirement | Required verification |
| --- | --- | --- |
| AC1 — bounded preservation | B...H changes exactly the two listed files through insertion only, in the two allowed locations each. No prior byte or trailing-newline state is lost; historical estimates/records are preserved. | C records `git diff --name-status`, `--numstat`, and raw-byte preservation checks that remove the exact identified inserted spans from H and recover B byte-for-byte. D independently inspects the actual diff and repeats the identity check. |
| AC2 — complete, exact cadence | Six new PR identities and integration SHAs match the complete first-parent P...M chain and API associations. One carried #685 produces window #685/#686/#681/#687/#683, residual #689/#688, and three integrations to the next boundary. #687's cutoff/publication distinction is explicit. | Independent source/API comparison, count arithmetic, exact seven-member sequence assertion and review of all six file inventories plus the prior checkpoint; no PR-number sorting or merge-commit-only counting. |
| AC3 — honest outcome accounting | All ten selected outcomes, seven conditional/unselected outcomes and six unselected expansion groups are reconsidered without duplicate scope, new selection, paused-work resumption or undocumented closure. Each six-PR result matches the actual source. | D uses the owning tables as membership authority, enumerates the unique members, examines changed source/register/proposal/triage, and records any outcome difference. Missing members or an unsupported status are NOT MET. |
| AC4 — estimates and authority preserved | Historical subtotal/group estimates retain their explicit unvalidated labels and #127 overlap; unestimated residuals and no-finite-ETA statement survive. #683 does not become delivery/consumption of #682; CI durations and merge spacing do not become active time or runtime proof. | Read the full new sections and all fresh headline/pointer text against M forecast and current cutoff register. Check references to 71–146, 68–140, #127, Stage 4B, BER-BKL-009, pause, #682 and timing. No numeric active-time deduction or new grant may appear. |
| AC5 — usable and structurally valid docs | New navigation links resolve; headings, tables, counts and UTC times are understandable and agree across both pages. Required validator/self-tests and changed-file link check pass; diff has no whitespace errors. | C and E execute the commands below with exits and tell-tale output. D gives an independent new-reader explanation of page purpose, current cutoff, count and limits; flags/corrects new clarity gaps. No whole-page readability acceptance is self-conferred or recorded by this PR. |
| AC6 — verifiable staged handoff | C supplies immutable H/tree/B, accepted plan hash/B verdict, exact assessed cutoff M, full command receipts, changed/not-touched inventory, current-source refresh and all deviations. Claims not checked are labeled; source snapshots and integration receipt resolve and parse. | D verifies H/tree/B and receipt consumability, reports MET/NOT MET per AC, and distinguishes repository-source proof from unmeasured effectiveness. Later E/F/G preserve their own required records under current workflow. |

## 7. Proportionate validation and later stage routing

For C before publication and independently selected E checks on the exact candidate:

```text
python -B -P scripts/validate-skills.py
python -B -P scripts/tests/test_validator.py
python -B -P scripts/ci/check-markdown-links.py docs/roadmaps/aegis-backlog-forecast.md docs/roadmaps/aegis-execution-metrics.md
git diff --check B H
git diff --name-status B H
git diff --numstat B H
git rev-parse H
git rev-parse H^{tree}
```

Here B/H are actual recorded commits, not literal shell tokens. Run these in the isolated authorized implementation checkout. Preserve byte/newline counts from raw files, not `Measure-Object -Line`. An ephemeral arithmetic/preservation check is appropriate; do not add permanent tests mirroring this prose edit. No provider, VM, deployment, private-input, host-proof or runtime suite is justified by this two-document change. Any unavailable local check must be recorded under the actual E procedure; applicable exact-head checks still need their own verified dispositions.

| Stage | Holder boundary and output |
| --- | --- |
| A | This agent's plan and captured digest; supporting forecast/classification/handoff skills applied. Writing the single-change plan itself is procedural under the current workflow. |
| B | Different agent: ACCEPT/REVISE this exact plan hash, especially scope, completeness of counts, fixed cutoff, estimate honesty and testability. |
| C | Different agent: assigned implementation authority, current-base refresh, two-file candidate, local checks and immutable H/tree/B; no self-audit. |
| D | Different agent: independent per-AC MET/NOT MET/UNRUN audit at H; apply the workflow's actual UNRUN rule. |
| E | Different agent: execute proportional checks at H and issue its own disposition and explicit gaps. |
| F | Different agent: final exact-head review, required PR fields/witness and body binding; author its own skills usage row. |
| G | Different agent: re-read current authority and the canonical MG conditions, verify the required receipts, then merge only if authorized; report postmerge evidence separately. |

Use the canonical `docs/delivery-workflow.md` SD-A–G and MG1–5 as binding IDs; this plan changes none. Each stage carries the accepted plan hash and preceding immutable artifacts, its changed/not-touched list, command/output evidence, timing, deviations and continuation line. Do not invent a new D/approval entry or duplicate MG requirement text in the source checkpoint. PR-body row publication must follow then-current policy/current owner authority; this plan does not publish another agent's rows.

## 8. Entry refresh, concurrency and hard stops

Before C starts and before each later reliance on current state:

- Read live main and all open PRs/holders. Confirm no other lane has already published or is holding this checkpoint or either target file. Do not take over a live holder.
- Retain M as the fixed assessed cutoff. Verify P is an ancestor of M, the source snapshots/SHAs and the full first-parent/PR mapping. Re-read the prior assessment to detect a duplicate.
- Choose implementation base B from current main. If B is later than M, inspect M...B. Unrelated changes may be accommodated while this checkpoint remains explicitly frozen at M; carry later merges forward outside its assessed window and never imply M is current head. Recalculate the live residual status for the handoff separately from the frozen source table.
- If either target acquired a newer checkpoint, if source/outcome/authority changes make the proposed newest-reading misleading, or if a different cutoff/scope is needed, stop and return to A/B. Do not silently retarget all tables or consume a later window under this acceptance.
- If runtime/skills/configuration, register/ledger or a third source file appears necessary, stop and revise scope through A/B. Do not fix unrelated defects in these long pages.
- Stop on unresolved provenance, incomplete API paging/association, missing commits, ambiguous first-parent mapping, duplicate integration membership or unexplained timestamp disagreement. Record unknown instead of selecting the convenient result.
- Red/unresolved applicable checks, missing exact-head review or missing applicable authority remain delivery stops under the canonical workflow. This plan authorizes no exception, settings change or provider rerun.
- Preserve dirty roots and other agents' artifacts. No reset, clean, stash, blanket stage, source rewrite or unauthorized credentials/provider access.

## 9. Provenance, uncertainty and Stage A usage

Saved exact M snapshots carry these repository blob IDs: forecast `0a36c90eefd25848248eecea3b61aef27e8cb1bc`; metrics `c7f27b366b884e01e6b552ff791a079ce6ea92a5`; register `7ee0e822398382101900c79aea9962b540a86c57`; workflow `720a858083f67a4fb91648517a0a918c68cd1d4b`; AGENTS `116450fd754c8040130b73d9816c373bba02d24b`; CONTRIBUTING `dc7fefbd9842167e8225bae2f3f6d50f4dd2acd5`. The content API's base64 bytes were decoded directly into the assigned scratch folder; no Git objects or source files were written.

Independent arithmetic output was `carried=1`, `new=6`, `complete_windows=1`, `window=[685,686,681,687,683]`, `residual=[689,688]`, `needed_after_cutoff=3`, `wall_from_685_to_688=14:17:35`. Live main was re-read during this planning turn as M; it is a point-in-time observation. Production effects, provider execution, global demand, actual active time and full delivery ETA remain unverified/unavailable.

The Stage A skill rows below are this agent's own account. They are available to later authorized metadata publication under the applicable source-row policy; they do not assert later-stage results.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [roadmap-under-uncertainty-planner](https://github.com/ModernNomad-98/Project-Aegis/blob/625fc66711eaf7b3ee788cbc2dff98f05f147c1c/.claude/skills/roadmap-under-uncertainty-planner/SKILL.md) | A / `/root/backlog_current_inventory`, rev1 | Preserved source-cutoff horizons, dependencies, confidence and non-commitment boundaries; derived the next reassessment trigger from the retained cadence. | PLAN-rev1 sections 2–6; no new backlog selection or measured remaining-effort claim; source counts proven in integration-evidence.json. |
| [change-classification-gate](https://github.com/ModernNomad-98/Project-Aegis/blob/625fc66711eaf7b3ee788cbc2dff98f05f147c1c/.claude/skills/change-classification-gate/SKILL.md) | A / `/root/backlog_current_inventory`, rev1 | Inspected the two targets, current instructions, contribution surfaces and guard pattern; locked an insertion-only two-document factual checkpoint and proportional validation. | Docs-only classification; expected security answer No for the bounded diff. Any instruction/authority/runtime change returns to A/B. Candidate validation is UNRUN at planning. |
| [phased-work-handoff-designer](https://github.com/ModernNomad-98/Project-Aegis/blob/625fc66711eaf7b3ee788cbc2dff98f05f147c1c/.claude/skills/phased-work-handoff-designer/SKILL.md) | A / `/root/backlog_current_inventory`, rev1 | Defined immutable plan/head/tree/base evidence, per-AC audit, carried SD/MG IDs, changed/not-touched lists, deviations and current-main refresh for distinct A–G holders. | PLAN-rev1 sections 6–8; all candidate ACs verifiable at D, later publication/check/merge results explicitly pending. |

Deviation: none. Next action: distinct Stage B audit of this captured file; no Stage C source work until that exact revision is accepted and the coordinator assigns the implementation holder.
