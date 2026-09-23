# Aegis efficient execution plan and new-chat handoff

> **Current reading, checked 2026-09-23 after pull request #146:** Sections
> 1–9 below preserve the original handoff, including its then-current first
> task and estimates. They are historical instructions, not today's execution
> queue or a new authorization. Read the current routes and dispositions here
> before using them. Existing safety and phase gates still apply.

## Current status and reader routes

This page helps a new maintainer or coding agent find the governing records.
Behavioral Eval Runner (BER), control plane (CP), and issue #101 setup each
have separate work packages (WPs) and approvals. A backlog item (BKL) records
a need; an approval-register entry (APR) or BER decision (BER-DEC) records
specific owner scope. A pull request (PR) can be open or merged. Owner decision
1 (OD-1) is the later human ratification of measured BER calibration. R4/R5
are BER host-confinement and execution-profile evidence gates. Continuous
integration (CI) checks are not selected-host proof.

| Original handoff topic | Current disposition |
| --- | --- |
| First task, BER-BKL-007 in §5 | **DONE** on [PR #104](https://github.com/ModernNomad-98/Project-Aegis/pull/104) merge. The [BER backlog](behavioral-eval-runner-backlog.md) owns its completed status; the old first-task steps remain as historical context. |
| BER evidence policy | [APR-009](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection) selected the 30-day complete-bundle policy. [APR-012](../approvals/APPROVAL_REGISTER.md#aegis-apr-012-offline-behavioral-eval-runner-evidence-policy-proof) granted only one synthetic offline proof; [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139) was open at this check. BKL-009 remains partial; real-host access, encryption and cleanup still need separate proof and scope. |
| CP work | The synthetic CP-WP-003A increment shipped in [PR #123](https://github.com/ModernNomad-98/Project-Aegis/pull/123). The [CP backlog](resumable-control-plane-backlog.md) still blocks broader CP-WP-003 real-source/host claims and CP-WP-004 integration. |
| Issue #101 setup | Package 1 planning ([PR #109](https://github.com/ModernNomad-98/Project-Aegis/pull/109)), package 2 Windows Aegis-only selection ([PR #124](https://github.com/ModernNomad-98/Project-Aegis/pull/124)), and package 3 offline advisory contract ([PR #121](https://github.com/ModernNomad-98/Project-Aegis/pull/121)) shipped in bounded scopes. The [setup plan](aegis-setup-routing-plan.md) keeps package 4 host/comparison work pending, packages 5/6 conditional, and package 7 pending. No helper is selected. |
| BER calibration and host | Replacement labels, reviewed execution source and allowance, a named proven host, measured calibration and OD-1 remain open. No live BER phase is authorized by this handoff. Follow the [BER phase register](behavioral-eval-runner-backlog.md) and [current decision index](aegis-open-decisions-2026-09-23.md). |

Start with the [owner approval register](../approvals/APPROVAL_REGISTER.md)
for authorization and later lifecycle events, then the owning backlog or
setup plan above for exact status. The [latest forecast](aegis-backlog-forecast.md#start-here--current-reading)
estimates **175–394 remaining active hours** of selected work; it does not
grant implementation or provider authority. Review the current branch, head,
checks and open PRs before choosing a task. Do not restart §5 from this dated
handoff.

## Original handoff: sections 1–9 as prepared

Prepared: 2026-09-23. Owner: Peter Nguyen.
Repository: `ModernNomad-98/Project-Aegis` (source-library Role A).
Purpose: carry the revised workload, verified state, model policy and first task
into a new chat without repeating the planning investigation.

This is a durable handoff requested by the owner, not evidence that unfinished
work is complete. No new runtime implementation, provider call or deployment
was performed while preparing it. Existing phase and live-execution gates still
apply; this document does not invent missing owner decisions.

## 1. Owner direction and authority

The continuing objective is to work through the Aegis backlog, resolve defects,
verify changes, and continue with the next ready item. The owner pre-approved
commit, push and merge when local checks, code audit and GitHub Actions are green.
The owner then requested an efficient plan, approval before implementation,
durable storage and a handoff to a new agent. The latest request was:

> ok now provide a handoff to take to a new chat for this new workload & plan

Carry this plan into the new chat. The handoff request authorizes preserving and
delivering this record; do not present it as a new paid-run or later-phase grant.
The new chat's direct instructions govern the next implementation batch.

Read the complete [approval register](../approvals/APPROVAL_REGISTER.md), including
later lifecycle events. Existing grants include read-only agents (AEGIS-APR-001),
recurring administrator merges (002), PR updates (003), and the now-delivered
synthetic CP-WP-002 scope (004). Do not repeatedly request those same grants.

One policy conflict remains explicit: APR-002 covers deliberate administrator
merges with the protected-file guard failure, but the newer conversation required
all Actions to be green. The revised plan proposed the following narrow amendment;
it has not received an unambiguous separate acceptance:

> For approved protected-file changes, permit administrator merge only when the
> sole failed check is the guard's documented manual-review condition, all
> execution/test jobs pass on the candidate revision, and independent audits have
> no unresolved blocking finding. Other failed checks remain blocking.

Do not infer that exception from this handoff. Complete authorized preparation,
fixes, tests and review before presenting a concrete affected PR for that decision.
Do not remove the guard, change branch protection, or report its failure as green.
An ordinary documentation PR whose checks pass does not need this exception.

## 2. Model and agent policy

- Recommended execution lead: `gpt-6-sol`, reasoning `medium`. The owner initially
  requested GPT-5.6 Sol medium, then asked us to choose the most efficient and
  effective model; the revised recommendation is GPT-6 Sol medium.
- Explicit owner permission: "you may use the higher model for reasoning and
  troubleshooting complex issues as needed". Raise reasoning effort or use
  `gpt-6-astra` for a bounded difficult architecture, security, recovery or
  troubleshooting task, then return to the default.
- `gpt-6-luna` is suitable for narrow inventories, routine documentation or
  focused mechanical checks. Do not assign it sole responsibility for accepting
  security or recovery invariants.
- Prefer Standard speed when configurable. Verify the actual runtime setting;
  selecting a model does not prove a service tier or change this chat's model.
- Additional agents require an expected elapsed-time saving greater than 20%,
  including startup, context, review and integration. Estimate before delegation:
  `parallel duration + coordination overhead < 0.8 * serial duration`.
  Check observed results after a batch; speed and total token cost are separate.
- Default to one writer with bounded independent read-only reviews. Multiple
  writers need separate worktrees and disjoint file ownership; one coordinator
  owns shared contracts, backlog records and integration. Avoid nested fan-out.
- Give each agent the relevant task, files, decisions and acceptance checks.
  Avoid copying the entire conversation or repeatedly rereading historical logs.

The model recommendation is based on official documentation checked 2026-09-23:
[Codex agent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents)
and [pricing](https://learn.chatgpt.com/docs/pricing). At that time Standard Codex
rates per million input/output tokens were 50/250 credits for GPT-6 Sol,
100/500 for GPT-5.6 Sol, and 2.5/12.5 for GPT-6 Luna. These compare token rates,
not measured Aegis task cost, subscription savings or completion time.

This coding-agent policy does not change BER's separately pinned calibration
judge (`gpt-5.5-2026-04-23`) or SDK (`openai==3.0.0`).

## 3. Verified starting state

Verification baseline, before this handoff's documentation commit:

| Item | Observed state |
| --- | --- |
| Local workspace | `C:\src\Project Aegis\Project-Aegis` |
| Branch | `docs/ber-schema-compatibility-policy` |
| HEAD / latest merged main | `0a5ce2b229b5550e90ca95bd5d739e816b8ac80f` |
| Open PRs | None at verification |
| Open issues | [#101: conversational setup and optional GLiClass/Jev routing](https://github.com/ModernNomad-98/Project-Aegis/issues/101) |
| Latest main CI | [Run 35848194860](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35848194860), success |

Recheck current branch, main, PRs and issues at startup; this table is dated
evidence. The handoff commit and its delivery PR will be later than this baseline.

Completed work to preserve:

- CP-WP-002 is DONE. [PR #99](https://github.com/ModernNomad-98/Project-Aegis/pull/99)
  merged at `be552fb778ec50fd0cbe82eff9f1022235ec11d8`. It includes strict chained
  denial-event replay and the corrected T09 recovery path. Final reviews accepted
  architecture, security and QA. Windows and Linux each ran the 543-test package
  suite; Linux had three expected skips. Claims remain synthetic/process-crash
  scoped; no real adapter, authority source or deployment was delivered.
- [PR #100](https://github.com/ModernNomad-98/Project-Aegis/pull/100) merged at the
  baseline above. CP status is reconciled; BER-BKL-002 naming cleanup is DONE.
- Dependabot PR #98 was closed: its SDK upgrade conflicted with the approved
  `openai==3.0.0` pin and its checks failed. Do not reopen the upgrade as routine
  cleanup without the applicable changed-version decision.
- BER core, Scenario A offline grading, shared contracts and offline CI are
  delivered. Measured calibration and later live phases are unfinished.

Preserve pre-existing local state. `git status` reported
`docs/design/resumable-control-plane-v1.md` modified and untracked
`artifacts/recovery/`, `artifacts/reviews/`, and Python `__pycache__` directories.
These are not handoff changes. Do not stage, delete, overwrite or reset them.
Inspect any overlap before implementation. No schema-policy draft existed on
the current branch when this handoff was prepared.

## 4. Execution batches

Keep required work visible. Supporting BER backlog entries often refer to the
same work package; do not build or estimate them twice.

| Batch | Concrete result | Sequence / decision boundary |
| --- | --- | --- |
| A. BER schema integrity | BKL-007 strict serialized-version validation, regression tests, compatibility policy and accurate backlog closure | First bounded implementation candidate; protected-file merge condition applies |
| B. Calibration preparation | Reproducible 160 candidate cases, guide, 40/120 split, rationales, quality reports and hashes | Preparation can overlap A with clear ownership; human labels remain PENDING |
| C. Owner decision preparation | BKL-009 retention/access/encryption proposal; replacement storage/source/accounting changes; host and CP authority/integration choices; #101 setup decisions | Prepare concrete recommendations together; keep each work package's authority distinct |
| D. Calibration completion | Missing holdout execution support, approved replacement pins, offline tests, development measurement, holdout freeze, one holdout execution and OD-1 disposition | Reuse existing ledger/gates/provider boundaries; preserve sequential owner/result gates |
| E. BER live delivery | Selected-host proofs and WP-2B-4 Scenario A, then WP-2B-5 corpus, WP-2B-6 operations, WP-2B-7 advisory CI | Each phase follows applicable authorization and evidence gates; BKL-003/005/012/013 follow their owning phases |
| F. Control plane | CP-WP-003 capability proofs, then one selected CP-WP-004 delivery integration | Host/source/operation choices first; separate approval scope; can progress alongside ready BER work |
| G. Setup and routing, #101 | Design, Aegis-only conversation and saved states, offline adapter contracts, separate GLiClass/Jev integrations, then comparative evaluation | Preserve the issue's six packages; design first; actual installation, credentials and calls need their named authority |

Integrate BKL-009 operator handling and BKL-011 dataset/drift procedures where
they are consumed. Share verified host investigation findings between BER and
CP without treating their runtime contracts or approvals as interchangeable.
When one stream waits for a decision, continue another authorized ready task.

Keep BKL-010 signing/immutable storage, BKL-014 additional hosts, BKL-015 optional
products, multi-judge arbitration, CP-FUT-001 and the strategic skill-expansion
backlog visible as later adoption decisions. Do not silently drop them, label
them DONE, or build an unselected product merely to empty the backlog.

## 5. First task: BER-BKL-007

Read the [backlog entry](behavioral-eval-runner-backlog.md#ber-bkl-007--final-production-jsonyaml-schemas-and-schema-migration-policy),
the design's evidence contract and the existing schemas/tests. The prior read-only
audit found these specific gaps; reproduce them against the current revision:

- `AttemptRecord.from_dict`, `AggregateRecord.from_dict` and
  `CaseManifestRecord.from_dict` in `tools/behavioral_eval_runner/models.py` default
  missing serialized `schema_version` fields to the current version.
- CLI record validators use these loaders, so a schema requirement on its own
  does not establish rejection at that boundary.
- `verify_input_evidence` and `verify_final_bundle` in `evidence.py` verify hashes
  and identities without establishing supported versions for every relevant
  manifest/report/marker. Test self-consistent unknown-version bundles.
- Inspect `execution_profile.py` and other external read boundaries for the same
  omission; do not infer that every constructor default is a bug.

Write failing regressions, require an explicit supported version on external
records, and keep legitimate internal creation defaults if appropriate. Version
families are separate; do not force WP-2B-1/2/3 records into a single version.
Document version changes, compatibility, reading older evidence, and reviewed
conversion with original evidence bytes/hashes preserved. No silent upgrade or
rewriting of historical evidence. Close BKL-007 only after implementation,
policy and reviewed acceptance are actually complete.

Use one behavior-focused PR with its tests, policy and backlog update. Do not
create a separate status-only PR for every development checkpoint.

## 6. Calibration facts the next agent must retain

The [replacement plan](../evidence/ber-recovery-2026-09-11/replacement-plan.md)
explicitly calls for agent-prepared candidates. Peter does not need to author
all 160 cases. Use the surviving validator, rubrics and review findings:

- Ten controls A/B/C/D/G/H/I/J/N/O; sixteen cases each.
- Forty development and 120 distinct holdout cases; required label, critical-risk
  and adversarial distributions are specified in the replacement plan.
- All candidate labels start PENDING with rationales. Peter approves final labels
  and exact bytes; AI suggestions are not human-approved gold labels.
- Screen duplicates, cross-split similarity, schema/composition, judge-envelope
  leakage and size bounds. Preserve semantic independence, not just counts.
- Reconcile the owner's GitHub-backup direction with old external-only storage
  terms; disclose public holdout exposure. Preserve approved materials durably.
- The current development driver AND provider are development-only. Freeze
  contracts do not mean a complete reviewed holdout executor already exists.
- Missing original files do not establish unused spending allowance. Resolve
  historical accounting and changed input/source pins before provider requests.
- Owner freeze follows development results; OD-1 ratification follows measured
  holdout results. Neither can be recorded in advance as an accepted result.

The authorization specifies development <=90 minutes, holdout <=4 hours and whole
run <=6 active hours, excluding owner waiting. These are stop ceilings, not a
promise of completion. Preserve concurrency, retry, budget and exposure limits.
The coding-agent multi-agent rule does not authorize parallel calibration calls.

## 7. Verification and efficient delivery

Use the existing [offline CI instructions](../offline-ci.md) and
[contribution rules](../../CONTRIBUTING.md). During development run checks that
address the changed behavior. At a candidate revision, run all applicable final
checks and independent review, fix findings, and verify the final revision before
merge. Retain commands, exit results, revision and meaningful output.

Relevant existing commands include:

```text
python scripts/validate-skills.py
python -m tools.behavioral_eval_runner self-check
python -m unittest discover -s tools/behavioral_eval_runner/tests -p test_*.py -v
python -m unittest discover -s tools/aegis_delivery_control/tests -p test_*.py -v
git diff --check
```

These examples are not a substitute for the current repository-required checks.
For CP changes, keep explicit local Windows and pinned Linux CP verification:
the current Actions workflow does not run the CP suite. Green Actions alone
does not establish CP correctness.

Latest observed Actions runs took about three minutes and already ran Linux and
Windows independently. CI redesign is not an identified high-value accelerator.
Avoid unnecessary repeated full audits of unchanged code, but rerun required
final checks whenever the candidate changes. Never retry a measured evaluation
until green or erase failures to improve a result.

Use existing approved dependencies and fixtures. Keep unrelated local files
unstaged. Update the backlog and continuation record alongside each delivery.
Record deviations explicitly; do not silently change scope, pins or decisions.

## 8. Estimates and progress reporting

The earlier 61-146 engineering-day total and derivative completion ranges are
withdrawn as delivery forecasts. They were not based on measured agent throughput.
Do not carry them forward as commitments or replace them with invented savings.

Measure implementation, tests, review, integration, CI waiting and owner waiting
separately. Use the first two completed batches to forecast the next ready work.
Report token/credit usage when the runtime exposes it; otherwise label it unknown.
Keep a brief current-task checkpoint so a new agent can resume without a fresh
whole-repository investigation. Stop forecasting dates across unresolved host,
authority or dataset decisions as though they were coding tasks of known size.

## 9. New-chat startup

1. Verify Role A landmarks, current branch/head, local changes and current queue.
2. Read this handoff, AGENTS.md, the complete approval register and the applicable
   current backlog/skill. Historical documents retain history; current registers
   and later owner instructions determine current scope.
3. Confirm the execution model/effort actually selected. The coordinator can
   launch a bounded execution agent using `gpt-6-sol` / `medium`; claiming a model
   change without observing or setting it is not a handoff.
4. Carry the proposed protected-file exception as the one unresolved merge-policy
   choice unless a later explicit owner instruction settles it. Do not block
   otherwise authorized local preparation and verification on that merge choice.
5. Check implementation authority for Batch A separately from this handoff's
   publication. If the new chat explicitly approves that bounded implementation,
   make the required scope record durable under the BER authorization protocol
   and begin section 5. Otherwise present the concrete Batch A scope for approval;
   the handoff alone does not authorize its runtime edits. Continue permitted
   preparation while any decision is pending. Do not restart CP-WP-002,
   reconstruct lost approval bytes, or reopen all 35 calibration decisions.

Canonical backlog sources:
[BER](behavioral-eval-runner-backlog.md),
[control plane](resumable-control-plane-backlog.md),
[#101](https://github.com/ModernNomad-98/Project-Aegis/issues/101), and the
[strategic skills roadmap](../300-repeatable-software-saas-skills-roadmap.md).
