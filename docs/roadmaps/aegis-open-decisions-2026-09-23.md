# Project Aegis — next owner decisions

> **Current reading, checked 2026-09-26 after pull request #370:** The table and
> sequence under [Original decision packet](#original-decision-packet-after-pr-107)
> preserve the proposal prepared after #107. They are not today's queue. Use
> the index below with the [approval register](../approvals/APPROVAL_REGISTER.md),
> [current forecast](aegis-backlog-forecast.md#start-here--current-reading),
> and owning backlogs before
> acting. This page grants no implementation, host or provider authority.

## Current disposition

For this page, Behavioral Eval Runner (BER) names the evaluation tool and
control plane (CP) names the delivery kernel. A backlog item (BKL), work
package (WP), and recorded decision (DEC) have separate lifecycles. An APR
is an entry in the owner approval register. A pull request (PR) is a proposed
or merged repository change. Owner decision 1
(OD-1) is the later ratification of BER's measured judge result. R4 and R5
are BER's host confinement and execution-profile evidence gates. POSIX means
a Unix-like operating-system interface; continuous integration (CI) runs
repository checks, not a selected-host proof. A source SHA is a commit hash;
`NON_BASELINE` means the result cannot qualify for the measured baseline.
`SYSTEM` is the Windows operating-system service account.

| Topic | Current status and next gate |
| --- | --- |
| BER evidence policy (BKL-009) | [APR-009](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection) selected the 30-day complete-bundle policy. The synthetic proof merged in [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139), and the bounded synthetic integration merged in [PR #257](https://github.com/ModernNomad-98/Project-Aegis/pull/257); APR-012 and APR-023 are consumed in APR-022 and APR-027. Real-host access, encryption, privacy and operator cleanup remain unscoped. Follow the [BER backlog](behavioral-eval-runner-backlog.md); these offline deliveries do not approve deletion or a live run. |
| Replacement candidate labels | The public [sanitized candidate checkpoint](../evidence/ber-replacement-candidate-1-summary.md) records 160 pending candidates. Owner semantic review and exact-byte label approval remain open; this index does not inspect or approve private inputs. |
| BER WP-2B-3 source, allowance and OD-1 | [PR #249](https://github.com/ModernNomad-98/Project-Aegis/pull/249) delivered bounded synthetic offline holdout support. The [live execution proposal](ber-wp2b3-holdout-execution-scope.md) is still a proposal, not a renewed provider allowance. Historical accounting, exact reviewed live execution source, private label approval, host proof and an explicit call/token/dollar cap remain prerequisites. No measured result or OD-1 ratification exists. |
| BER host and R4/R5 | The owner selected a new disposable Linux VM on VirtualBox; [PR #260](https://github.com/ModernNomad-98/Project-Aegis/pull/260) merged its setup proposal. Agent-assisted setup was approved in APR-028, then paused after repeated login stalls. The VM was last verified powered off with networking disabled and an empty virtual DVD drive. The [host decision proposal](ber-selected-host-capability-decision.md) distinguishes generic Linux CI from host evidence. No Stage A probe is authorized or recorded. |
| CP-WP-003 | [APR-006](../approvals/APPROVAL_REGISTER.md#aegis-apr-006-control-plane-offline-capability-proofs-first-increment) and [PR #123](https://github.com/ModernNomad-98/Project-Aegis/pull/123) delivered the synthetic CP-WP-003A proof. The [CP backlog](resumable-control-plane-backlog.md) still blocks real source authority, independent freshness, containment, evidence and billing claims. The delivered proof grants no real dispatch. |
| CP-WP-004 | No delivery target is selected. The [CP backlog](resumable-control-plane-backlog.md) requires CP-WP-003 prerequisites and a separately approved integration with exact receipt, rollback and budget terms. |
| Issue #101 setup and routing | Packages 1–3 shipped in [PR #109](https://github.com/ModernNomad-98/Project-Aegis/pull/109), [PR #124](https://github.com/ModernNomad-98/Project-Aegis/pull/124), and [PR #121](https://github.com/ModernNomad-98/Project-Aegis/pull/121). The bounded synthetic Stage 4A bridge shipped in [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281); [APR-036](../approvals/APPROVAL_REGISTER.md#aegis-apr-036-stage-4a-offline-bridge-package-completed) records consumption of APR-031. [PR #319](https://github.com/ModernNomad-98/Project-Aegis/pull/319) shipped the version-2 offline request binding at reviewed head `550151dcf286f8ec64480bc91f47e390454417d2`, merged as `a59c015c01b4035ab1a438533736134f96deac13` on 2026-09-26 at 02:24:21 UTC with Linux, Windows and `gate-guard` green. This remains synthetic-only. Stage 4B real host proof and the later helper comparison need separate scope and approval; packages 5/6 remain conditional, package 7 pending, and no helper is selected. Follow the [setup plan](aegis-setup-routing-plan.md). |
| Confidential conduct-reporting intake | The [Code of Conduct](../../CODE_OF_CONDUCT.md#enforcement) now states that no confidential route or independent recipient has been published. The original [D59 finding](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions) remains an owner decision: provide a usable private contact and alternate recipient before claiming confidential intake. Do not put sensitive incident details in a public issue. |

### Decided on 2026-09-26

These items were open owner decisions after the #344 checkpoint, and the
owner decided all three on 2026-09-26. [PR #365](https://github.com/ModernNomad-98/Project-Aegis/pull/365)
recorded the first two in the [approval register](../approvals/APPROVAL_REGISTER.md)
and merged on 2026-09-26 at 21:17:29 UTC as `2aed8dd3`; the S5 verdicts were
accepted in chat and have no register entry. For the first two, the register
entry, not this summary, is the authority. The same record added the standing merge
conditions [AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green),
[AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
and [AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review),
the eval-maintenance ruling [AEGIS-APR-051](../approvals/APPROVAL_REGISTER.md#aegis-apr-051-eval-file-maintenance-of-delivered-skills-is-backlog-delivery)
and the package-2 consumption record [AEGIS-APR-052](../approvals/APPROVAL_REGISTER.md#aegis-apr-052-consumption-of-the-package-2-implementation-grant).

| Topic | Decision and what it does not cover |
| --- | --- |
| BER selected-precheck aggregate correction ([PR #331](https://github.com/ModernNomad-98/Project-Aegis/pull/331) proposal) | Approved as [BER-DEC-014](behavioral-eval-runner-backlog.md#ber-dec-014-bounded-synthetic-selected-precheck-aggregate-correction--owner-approved) and [AEGIS-APR-046](../approvals/APPROVAL_REGISTER.md#aegis-apr-046-ber-selected-precheck-aggregate-correction): one bounded synthetic correction to two BER reporting paths, at most 8 active hours and 300 added lines, $0 spend, synthetic local fixtures only. It became active when #365 merged. Implemented; [PR #374](https://github.com/ModernNomad-98/Project-Aegis/pull/374) merged at 23:24:51 UTC as `7390ae0a` under AEGIS-APR-047; APR-046 consumed; [PR #381](https://github.com/ModernNomad-98/Project-Aegis/pull/381) recorded that consumption as AEGIS-APR-053, merged on 2026-09-27 at 03:31:29 UTC as `032e0302`. It does not change the private-label, selected-host, provider-budget or OD-1 gates. |
| Protected-file guard options ([PR #333](https://github.com/ModernNomad-98/Project-Aegis/pull/333) packet) | Option A approved as [AEGIS-APR-047](../approvals/APPROVAL_REGISTER.md#aegis-apr-047-standing-gate-guard-exception-for-four-ber-files): a standing, conditional owner exception for four named BER reporting/aggregation files. The `gate-guard` check still fails and each use needs a receipt, independent review and exact-head checks. Options B and C were not selected; every other protected path keeps a one-time owner decision. |
| Six UNSURE owner-choice skills (group S5) | **Resolved 2026-09-26:** the owner accepted all six verdicts. `feature-flag-rollout-strategist` NEEDS an owner-choice step and eval case, `edge-owner-deadline-ramp-pace-choice`: when a launch date conflicts with the evidence-backed ramp, compare moving the date, compressing the ramp or launching to a limited cohort. It was queued as a small batch and delivered by #377. The other five do not need one: `data-quality-monitor-designer` (actions follow the blast-radius ranking, the service-level agreement is a consumer fact, and promise gaps belong to `slo-reliability-architect`); `cross-team-dependency-negotiator` (prioritization is escalated to shared management); `admin-console-architect` (consent and scope are policy input owned by `authorization-matrix-designer`); `funnel-definition-designer` (attribution follows the stated decision); and `agent-instruction-consolidator` (a rule plus simple approval). The owner-choice backlog is now 23 skills; S1, S2 and S3 merged in #366, #368, #370 and #373, and S4 (#376) and the new step (#377) merged on 2026-09-27 at 01:44:03 and 01:44:07 UTC, so all 23 are delivered. |

Later on 2026-09-26 the owner also settled the items below. They come from
the owner's chat instructions and have no register entry yet; where a row
requires a record, that record is still to be written.

| Topic | Decision and what it does not cover |
| --- | --- |
| `scripts/audit-skill-contracts.py` dirty-path defect | **Resolved, no owner choice remains.** The contract-audit script's handling of dirty (uncommitted) paths was fixed in [PR #373](https://github.com/ModernNomad-98/Project-Aegis/pull/373), merged at 23:32:15 UTC as `4ca04c1e` with the owner-approved protected-path PR; `gate-guard` failed on its protected paths, as the one-time owner exception anticipated. |
| `project-orchestrator` feature-flag route | **Yes:** route from Stage 9 ("Decide to release") to the rollout strategist as an owner choice ("ship directly or behind a release flag?"). The routing change was not started at this reading; [PR #384](https://github.com/ModernNomad-98/Project-Aegis/pull/384) delivered it, with the accepted Stage 3 route, on 2026-09-27 at 04:25:58 UTC (`0f46808d`). |
| D64 decision-log row | **Required:** a D64 row must be added to the [recorded decisions](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions). No D64 row existed at this reading; [PR #383](https://github.com/ModernNomad-98/Project-Aegis/pull/383) added it on 2026-09-27 at 03:43:01 UTC (`6844ab9f`). |
| Caching seam | **Kept** as currently written. |
| Four one-way ROUTE-002 hub findings | **Stay census data:** these four routing-reciprocity findings are recorded, not fixed. Other ROUTE-002 findings stay in the open row below. #383 as merged records a fifth one-way finding, toward `tenant-isolation-reviewer`, which the owner also confirmed on 2026-09-26 stays census data (decision log D64). |

[PR #382](https://github.com/ModernNomad-98/Project-Aegis/pull/382) removed the two `scripts/__pycache__`
bytecode files that #372 committed by mistake and ignores bytecode caches.
`gate-guard` flagged its protected `scripts/` paths; it merged on 2026-09-27
at 01:29:38 UTC as `0d05a838`, so no owner choice remains.

### Still open for the owner

Each item below needs an owner choice or read before work that depends on it
can start. Listing an item here grants nothing.

| Open item | What the owner needs to decide |
| --- | --- |
| Security-surface rule in [CONTRIBUTING](../../CONTRIBUTING.md#external-contributions) for maintainer PRs | The guide requires an additional explicit security review when an external PR touches a security-relevant surface. The owner needs to decide whether, and in what form, that rule also applies to the maintainer's and agents' own PRs. |
| Pull request template | Whether completing the repository's PR template is mandatory for every PR or advisory. |
| Confidential conduct-reporting intake | Provide a usable private contact and an alternate recipient before the project claims confidential intake ([D59 finding](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions)). The [Code of Conduct](../../CODE_OF_CONDUCT.md#enforcement) still says neither has been published. |
| ROUTE-002 routing reciprocity backlog | Whether and in what order to fix the remaining skill-contract audit findings where one skill excludes another without a matching exclusion back. #362 closed the ai-closeout-reporter case, and the owner kept four one-way hub findings, and a fifth from #383, as census data (see above). Later on 2026-09-26 the owner decided to reciprocate 23 high-value seams (including five hub exceptions) and record the rest as census data; that work is in progress. |
| Issue #101 Stage 4B host proof | The exact host profile, permissions, telemetry, provider and cost limits, and a separate grant for any real host session. All eight synthetic Stage 4B cases are still NOT RUN. |
| CP-WP-003 and CP-WP-004 | Real source authority and capability proof for CP-WP-003, then selection of one bounded real integration for CP-WP-004; both need separate reviewed scope and grants. |
| Private BER candidate labels | Semantic review and exact-byte approval of the 160 pending private candidates; this index does not inspect them. |
| Disposable Linux VM | Whether and when to resume the paused VirtualBox setup; a Stage A host probe needs its own grant. |

### Owner-requested backlog items

These items are in the backlog at the owner's request. Listing one here does
not authorize its implementation.

- **New skill: feature-flag architecture.** The in-app half of feature flags
  that the shipped `feature-flag-rollout-strategist` (rollout strategy only)
  does not cover: flag store versus vendor choice, SDK and configuration
  placement, fail-safe defaults when the flag service is down,
  tenant/plan/cohort targeting, kill-switch wiring and flag-debt removal
  hooks; plus routing from `project-orchestrator`'s release/QA stage to the
  rollout strategist as an owner choice ("ship directly or behind a release
  flag?"). Source: owner request on 2026-09-26. The skills roadmap already
  lists it as planned:
  [#27 "Feature Flag Architecture" (P1)](../skills/01-software-architecture-engineering.md)
  and [#65 "Feature Flag Rollout by Tenant" (P1)](../skills/02-saas-platform-architecture.md).
  Delivery path: the [skill-generation standard](../skill-generation-standard.md)
  (new SKILL.md, evals, trigger evals and catalog row), a skill-quality review,
  then the orchestrator routing change. Provisional estimate: 2–4 active hours
  for the new skill plus 0.5–1 for the routing, outside the bounded selected
  subtotal. **Owner decision needed first (made on 2026-09-26; see the next item):** accept a scope
  proposal covering the new-skill posture, its name, and its boundaries with
  `feature-flag-rollout-strategist`, `plan-entitlement-architect`,
  `authorization-matrix-designer` and `ab-test-designer`.
- **2026-09-26, about 15:20 PDT:** the owner accepted the feature-flag skill
  scope proposal (one new auto-invocable skill `feature-flag-architect`, a
  reciprocal description edit to `feature-flag-rollout-strategist`, and a
  separate `project-orchestrator` Stage-3 route) and said to build now. The
  proposal page merged as [PR #378](https://github.com/ModernNomad-98/Project-Aegis/pull/378)
  on 2026-09-27 at 01:40:32 UTC (`a2d2b831`); the skill was then in progress and merged as [PR #383](https://github.com/ModernNomad-98/Project-Aegis/pull/383) on 2026-09-27 at 03:43:01 UTC (`6844ab9f`). Later
  on 2026-09-26 the owner
  approved the orchestrator route at Stage 9 ("Decide to release"); see
  [Decided on 2026-09-26](#decided-on-2026-09-26). Both routes merged as
  [PR #384](https://github.com/ModernNomad-98/Project-Aegis/pull/384) on 2026-09-27 at 04:25:58 UTC (`0f46808d`).

The [current forecast](aegis-backlog-forecast.md#start-here--current-reading)
places the bounded selected subtotal at **71–146 active hours**: the ten
selected rows. The 4–8-hour #331 correction made it 75–154 while undelivered;
#374 delivered it. Beyond that subtotal are the
unestimated issue #101 Stage 4B and the BER-BKL-009 host, runtime, privacy
and cleanup residual. The selected total therefore has no finite estimate. It is a scope
estimate, not
permission to start a gated package. The independent gates in the original
packet below still apply where the current index marks them open.

## Original decision packet after PR #107

Prepared 2026-09-23 after public PR #107. This is a review packet, not a
phase authorization or a claim that a blocked gate is complete. The
[execution handoff](aegis-efficient-execution-handoff-2026-09-23.md) groups
these decisions for efficient review; BER, CP and setup retain separate
authority records and implementation branches.

| Decision | Current evidence | Recommendation | Decision boundary |
| --- | --- | --- | --- |
| BER-BKL-009 final evidence policy | Scoped BER-DEC-006/008 handling and writer metadata exist, but no complete production policy/enforcement | Select the [30-day whole-bundle policy proposal](ber-bkl-009-evidence-policy-decision.md), owner+SYSTEM WP-2B-3 readers and verified host encryption; separately authorize implementation | Owner sets exact periods, readers and mechanism; BKL-009 stays PARTIAL until policy, writer and runbook are reviewed |
| Replacement candidate labels | Private input PR #1 contains 160 PENDING candidates; public [sanitized checkpoint](../evidence/ber-replacement-candidate-1-summary.md) records hashes and checks | Review the full private packet; approve exact bytes only after semantic/risk review or request a new version | A candidate commit and structural PASS do not create human gold labels |
| WP-2B-3 source and allowance | BER-DEC-008 pins its original authorization merge; the replacement packet and any holdout executor are later revisions; old input/usage bytes are missing | Operationally assume **zero available residual allowance** until independently reconciled, without changing the historical grant; after label approval and reviewed execution source, record an exact revised source SHA/tree and a new explicit call/token/dollar cap in a merged amendment | No provider metadata or judgment request, dependency install or new source pin follows from this proposal |
| BER selected host / R4–R5 | On the current Windows host, mid-write reparse prevention is unavailable in the evidence writer and post-leader descendant cleanup is unproven; POSIX writer tests run in generic Linux CI, but no selected-host capability proof exists. Profile isolation is unproven. | Select a host under the [capability decision proposal](ber-selected-host-capability-decision.md), then authorize its bounded offline probe; report unsupported paths as NON_BASELINE and stop before live dispatch | Do not choose a live host by documentation alone; any provisioned host, credentials or live probe needs its own authority |
| CP-WP-003 | CP-WP-002's 543-test offline kernel is DONE; source-atomic real approval, monotonic reconciliation, containment/fencing, and bounded liability remain blocked | Prepare a zero-provider, synthetic capability-proof authorization with negative authority/race/rollback/path/process/receipt/billing probes | Separate reviewed CP scope and owner approval; no real adapter, deployment or provider call |
| CP-WP-004 | No delivery target selected; CP-WP-003 gates are unproven | Decide the single integration only after CP-WP-003 evidence; a draft GitHub PR is a candidate reversible target for comparison with local artifact export | Selection needs exact idempotency, receipt, rollback, source/evidence/budget pins and explicit owner authority |
| Issue #101 setup/routing | [Issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101) records seven numbered packages, current Aegis-only/local/online/help choices and no selected helper | Start package 1 as design and candidate screening; keep Aegis-only as a complete baseline, then compare optional helpers on paired tasks before selecting one | No installation, credentials, paid evaluation, provider call or helper default is authorized by the issue |

## Proposed near-term sequence

1. Review private calibration PR #1 for candidate defects without moving
   labels out of the private repository. Preserve each rejected version.
2. Decide the BKL-009 policy parameters in the linked proposal. A subsequent
   governance entry must authorize code/runbook enforcement; no retroactive
   rewrite of BER-DEC-008/010 or WP-2B-0 spike evidence.
3. Prepare offline host and CP-WP-003 scope/evidence proposals. Probe only
   after their own reviewed authorizations; current capability reports are
   limitations, not verified live guarantees.
4. Prepare issue #101 package-1 design separately. Screen alternatives and
   define the paired evaluation before any local install or online use.
5. Only after labels, exact source review, historical-accounting disposition,
   host proof and explicit renewed allowance may a WP-2B-3 provider preflight
   be considered. Development, owner wait, holdout freeze and OD-1 result
   ratification remain sequential gates.

These choices are independent. Accepting the evidence policy, for example,
does not approve the 160 labels, renew a provider budget, authorize CP-WP-003,
or select an issue #101 helper.

The live issue #101 body was read on 2026-09-23 and lists packages 1–7.
The earlier execution handoff's "six packages" wording is stale after the
issue's forward correction; the current issue controls this count. Neither
source itself grants runtime implementation authority.
