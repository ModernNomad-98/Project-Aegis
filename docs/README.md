# Project Aegis documentation

Start here for current guidance. Dated evidence and design proposals preserve
their original context; use the active registers below to determine current work.

Project Aegis ships a skills library for artificial intelligence-assisted
engineering. Two
maintainer tools accompany it:

- The [Behavioral Eval Runner (BER)](../tools/behavioral_eval_runner/README.md)
  inventories test cases and grades recorded behavior so maintainers can
  measure whether the skills work. Its general commands are offline; measured
  model calibration remains gated.
- The [delivery control plane](../tools/aegis_delivery_control/README.md)
  records authority, budget, intent and receipts so an interrupted delivery
  operation can resume safely. Its current kernel runs synthetic targets only.

Each component guide explains normal use, commands, files and current limits.
The backlog links below show what remains proposed or blocked.

Shorthand: BER is the Behavioral Eval Runner; WP (work package) is the governing
delivery unit of the
[durable backlog](roadmaps/behavioral-eval-runner-backlog.md); and OD-1 (owner
decision 1) is the owner's ratification of a measured judge-calibration result.
Under the [control-plane register](roadmaps/resumable-control-plane-backlog.md),
CP-WP is a control-plane work package, T a state transition, C a crash boundary
and F a finding-specific negative acceptance family. R1–R5 name the five
capability-evidence gates recorded in the
[BER durable backlog](roadmaps/behavioral-eval-runner-backlog.md).

## Use the skills

- [Project README](../README.md): setup, skill picker, shipped skills and agents.
- [Consumer starter package](consumer-starter-package.md): the fixed, dependency-checked file set for a first product slice — 39 skill files for 18 skills plus 2 startup files. It covers the owner record and commit identity it requires, its recording-authority and screenshot-policy handoffs, and lists the remaining UNRUNs in its [evidence record](evidence/consumer-readiness/local-starter-v2.md); the [v1 record](evidence/consumer-readiness/local-starter-v1.md) remains the historical 39-file record.
- [Skills catalog](skills-catalog.md): implemented capabilities and their boundaries.
- [Engineering discipline](ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md): principles and workflow.
- [Skill generation standard](skill-generation-standard.md): current authoring contracts.

## Maintain the source library

- [Contributing](../CONTRIBUTING.md): verification, review and sign-off requirements.
- [Offline continuous integration (CI)](offline-ci.md): local reproduction, Linux/Windows checks and known gaps.
- [Security policy](../SECURITY.md): supported surfaces and private reporting.
- [Changelog](../CHANGELOG.md), [construction history](HISTORY.md), and
  [reconciliation and decision log](reconciliation/step-0-reconciliation-v4.md):
  delivered changes, historical context and recorded decisions.

**Read these before acting.** They hold the current authority, boundaries and
status; the dated proposals and evidence pages further down are history.

- [Owner approval register](approvals/APPROVAL_REGISTER.md): all current
  Project Aegis grants, limits and lifecycle events; read the complete register
  before acting.
- [Merge policy](reconciliation/auto-merge-policy.md): current authority and historical decisions.
- [Audit evidence registers](audits/README.md): dated row-level audit and coverage
  registers (read-only reference, not build authorization).
- [Delivery workflow](delivery-workflow.md): the seven-stage delivery rule, each
  stage's evidence, and the exact-head invalidation rule.
- [Aegis SCIF naming and the necessity/reuse check](aegis-scif-naming-and-necessity.md):
  the framework's name and its forms, the five questions Stage A owes and Stage B
  tests, and the residual-occurrence inventory.
- [Evidence reading guide](evidence/README.md): routes to 18 dated decision and
  delivery records, with current-status boundaries.
- [Documentation readability backlog](roadmaps/aegis-documentation-readability-backlog.md):
  the plan to explain each component in plain language, define project shorthand,
  and review all repository documentation for human and agent readers.

**Run and read the current workflows.**

- [Scenario A acceptance runbook](acceptance/scenario-a-runbook.md): run and read
  synthetic evidence for the beginner product-state workflow; behavioral
  acceptance remains a separate gate.
- [Approval lifecycle grading](approval-lifecycle-grading.md): normal use,
  the evidence contract and current limits for the BER approval grader.
- [BER schema compatibility](behavioral-eval-runner-schema-compatibility.md):
  normal use, records and current limits for versioned BER records.
- [Skill-eval behavioral test procedure](skill-eval-behavioral-test-procedure.md):
  normal use, method and current limits for repeatable skill-eval runs.

**Review the dated proposals and plans.** Each one states its own scope and
limit; listing it here does not authorize the work it proposes.

- [Efficient execution plan and new-chat handoff](roadmaps/aegis-efficient-execution-handoff-2026-09-23.md):
  September 23 backlog sequence, model policy, verified state and continuation task.
- [Conversational setup and routing plan](roadmaps/aegis-setup-routing-plan.md):
  issue #101 decisions, candidate screen and proposed evaluation protocol.
- [Offline setup routing contract](../tools/aegis_setup/README.md):
  maintainer guide to the implemented synthetic advisory checks; there is no
  host integration, provider connection or dispatch authority.
- [Issue #101 package-2 scope proposal](roadmaps/aegis-setup-package-2-authorization-proposal.md):
  reviewable Aegis-only conversation and saved-state implementation boundary.
- [Feature-flag system skill proposal](roadmaps/feature-flag-architect-skill-proposal.md):
  accepted scope for the new `feature-flag-architect` skill, its boundary with
  the existing rollout strategist, and a provisional estimate. The proposal now
  carries a **delivered** status banner (added 2026-10-11 by PR #734); the scope
  description above is unchanged by it, and the banner adds no authorization.
- [CI baseline and bottleneck observations](roadmaps/aegis-ci-baseline-2026-10-11.md)
  (2026-10-11): the observed six jobs, branch protection and ranked bottlenecks,
  with the method to re-derive every figure. Observation only — it authorizes no
  CI change.
- [P0-B FAST SAVE directive record](roadmaps/p0b-fast-save-directive-2026-10-11.md)
  (2026-10-11): the owner's directive transcribed on `main`, with its prohibited
  actions, acceptance tests and open grouping questions; it closes and grants nothing.
- [FAST SAVE handoff protocol v1](design/fast-save-handoff-protocol-v1.md): the
  DRAFT operator-facing procedure for "save progress and pause" — documented
  policy with no mechanical enforcement.
- [Skill-eval harness execution-path decision](roadmaps/skill-eval-harness-execution-path-decision.md)
  (PR #735): the owner's decision on the harness execution path. A decision
  record, not an authorization to run.
- [CP-WP-003 / CP-WP-004 owner decision packet](roadmaps/cp-wp-003-004-owner-decision-packet.md)
  (PR #733): the two open control-plane decisions prepared for the owner; it
  selects no option and grants nothing.
- [BER WP-2B-3 owner decision chain](roadmaps/ber-wp2b3-owner-decision-chain.md)
  (PR #732): the order of the WP-2B-3/4/5/6/7, R2 and OD-1 decisions and the
  evidence each needs; it changes no work-package status.
- [SCIF eval-assets and pilot census](evidence/scif/scif-eval-assets-and-pilot-census-2026-10-11.md)
  (PR #739): the fitted eval cases and the bounded read-only census, with assets,
  static results, actual runs and unrun checks kept apart.
- [Strategic skills roadmap](300-repeatable-software-saas-skills-roadmap.md):
  the product-agnostic 300-skill backlog that replaced the
  [superseded 150-skill draft](150-claude-skills-roadmap.md).

## Resume Behavioral Eval Runner work

Use a current `main` checkout and the [development setup](offline-ci.md).
No old computer or recovery ZIP is required to obtain the committed project.
The [runner README](../tools/behavioral_eval_runner/README.md) describes the
implemented controls and offline commands. The
[durable backlog](roadmaps/behavioral-eval-runner-backlog.md) is the authority
for remaining work and BER execution gates.

As recorded on 2026-09-12:

| Delivery | Current disposition | Evidence |
| --- | --- | --- |
| PR #88 calibration engineering | Merged; scoped engineering complete | [Closeout](evidence/ber-pr88-closeout-2026-09-12/README.md) |
| PR #90 shared contracts | Merged; confirmed review issues resolved | [Closeout](evidence/shared-contracts-closeout-2026-09-12/README.md) |
| PR #91 offline CI | Merged; Linux and Windows checks passed on `main` | [Delivery](evidence/offline-ci-2026-09-12/DELIVERY.md) |
| PR #93 owner grants and CI closeout | Merged; grants recoverable from GitHub | [Register](approvals/APPROVAL_REGISTER.md) |

**Measured WP-2B-3 calibration is unfinished.** Four original calibration
inputs remain unavailable. Continue with the
[replacement preparation plan](evidence/ber-recovery-2026-09-11/replacement-plan.md),
then the required source review, input approvals and execution preflight.
OD-1 remains open, WP-2B-4 remains blocked, and WP-2B-7's behavioral advisory
integration is future work. Green offline CI does not close those gates.

The [new-computer handoff](evidence/ber-recovery-2026-09-11/README.md) separates
current setup from historical reproduction and records exactly what is missing.
The [selected-host capability proposal](roadmaps/ber-selected-host-capability-decision.md)
defines the next R4/R5 host choice and staged evidence gate.
Original roadmap proposals and dated evidence remain useful history, rather
than instructions to reopen completed PRs or reproduce the lost computer.

## Resume delivery control-plane work

Use a current `main` checkout. CP-WP-001 was a documentation-only contract and
merged in [PR #95](https://github.com/ModernNomad-98/Project-Aegis/pull/95) as
`32cbb2dff8265b2c2aaff38f2ace198417ef1646`; it did not implement a controller
or runtime. Read the [design](design/resumable-control-plane-v1.md), the
[work-package register](roadmaps/resumable-control-plane-backlog.md) and the
[review evidence](evidence/control-plane/cp-wp-001-review.md) together.

CP-WP-002 is DONE under [AEGIS-APR-004](approvals/APPROVAL_REGISTER.md):
[PR #99](https://github.com/ModernNomad-98/Project-Aegis/pull/99) merged on 2026-09-23
at `be552fb778ec50fd0cbe82eff9f1022235ec11d8` after its final exact-head reviews and
all three hosted checks passed.

The exact package suite passed 543 tests on Windows and 543 on Linux (three expected
platform skips); all three stop findings, the aggregate stop gate, T13 authority
lifecycle intake, T15 binding-mismatch handling, the T14 PLANNED/BLOCKED resume slice,
T05 local-execution pause and T06 contacted external-mutation uncertainty pause
received independent `APPROVE`.

The narrow T07 local-nonexecution settlement and its BLOCKED-only T14 recovery route,
plus the narrow T08 validation-pause checkpoint and its clean VALIDATING T14 resume
route, T09's exact-head reconciliation pause fence, and the narrow T17
validator-result/T14 exact-T09-resume slice also received independent `APPROVE`.

The T17 operation-uncertainty foundation, including typed source/control evidence,
conditional uncertainty categories, atomic semantic migration and exact-set recovery,
also received independent `APPROVE`.

The T17 verified-receipt route now also has independent `APPROVE`: it binds a typed
query/time/source/response lookup, exact receipt/plan/slot/head facts and complete
settlement ancestry, then clears its exact uncertainty set atomically with typed
PAUSED/BLOCKED/VALIDATING routing and strict recovery.

The T17 authoritative-nonexecution and authenticated safe-retry slice also has
independent `APPROVE`, including all-path seal binding, generation-bound retry,
stacked-pause replay and proof-prefix-safe migration. F02 is now independently
accepted: proof-free owner dispositions remain non-dispatching, and the only reviewed
same-key successor retains outcome/activity uncertainty plus the exact T06 pause until
distinct T14 RESUME authority clears it.

T22 terminal-restart reporting is independently accepted with strictly read-only
main/auxiliary verification and typed stale/unverified status. F03 source-atomic
one-use authority is independently accepted: host/manual races, lifecycle timing,
correction ownership, clock rollback and lost-receipt replay are now directly asserted.

F04a reservation-boundary accounting is also independently accepted, including exact
known usage, durable overrun fences, unknown-liability retention, pre-contact bound
denial and strict semantic-v10 migration. All 22 acceptance-family rows now have tested,
independently accepted coverage.

All 28 transition, 9 crash-boundary and 22 acceptance-family rows are independently
accepted; the final exact-head architecture/security/QA and hosted gates also passed.
The independently accepted selected-check foundation binds explicit v2 per-check
dependencies and launch gates, derives a deterministic topological order and
reconstructs projections strictly.

The current increment adds signed monotonic gate facts and complete launch snapshots,
universal no-preclaim T27, atomic T11 next-check routing, exact T16 route recovery and
contact-time stale launch disablement with T25/T16 continuation. T11, T27, F11 and F17
are included in the independently accepted 28/9/22 canonical inventory. The [Codex
handoff](evidence/control-plane/cp-wp-002-codex-handoff.md) is the final CP-WP-002
evidence record.

No deployment, provider call, production data, real authority or real execution adapter
is authorized.

The [control-plane work package 003A offline proof proposal](roadmaps/cp-wp-003-offline-proof-proposal.md)
defined the synthetic increment delivered in PR #123. It tests failures of
source, freshness, containment, evidence and accounting claims. Work package
003 still needs real-source and selected-host proof before any live route;
the [current backlog](roadmaps/resumable-control-plane-backlog.md) tracks those
gates.
