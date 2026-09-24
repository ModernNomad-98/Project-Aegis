# Project Aegis documentation

Start here for current guidance. Dated evidence and design proposals preserve
their original context; use the active registers below to determine current work.

Project Aegis ships a skills library for artificial intelligence-assisted
engineering. Two
maintainer tools accompany it:

- The [Behavioral Eval Runner](../tools/behavioral_eval_runner/README.md)
  inventories test cases and grades recorded behavior so maintainers can
  measure whether the skills work. Its general commands are offline; measured
  model calibration remains gated.
- The [delivery control plane](../tools/aegis_delivery_control/README.md)
  records authority, budget, intent and receipts so an interrupted delivery
  operation can resume safely. Its current kernel runs synthetic targets only.

Each component guide explains normal use, commands, files and current limits.
The backlog links below show what remains proposed or blocked.

## Use the skills

- [Project README](../README.md): setup, skill picker, shipped skills and agents.
- [Skills catalog](skills-catalog.md): implemented capabilities and their boundaries.
- [Engineering discipline](ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md): principles and workflow.
- [Skill generation standard](skill-generation-standard.md): current authoring contracts.

## Maintain the source library

- [Contributing](../CONTRIBUTING.md): verification, review and sign-off requirements.
- [Offline CI](offline-ci.md): local reproduction, Linux/Windows checks and known gaps.
- [Evidence reading guide](evidence/README.md): routes to 15 dated decision and
  delivery records, with current-status boundaries.
- [Scenario A acceptance runbook](acceptance/scenario-a-runbook.md): run and read
  synthetic evidence for the beginner product-state workflow; behavioral
  acceptance remains a separate gate.
- [Owner approval register](approvals/APPROVAL_REGISTER.md): all current
  Project Aegis grants, limits and lifecycle events; read the complete register
  before acting.
- [Merge policy](reconciliation/auto-merge-policy.md): current authority and historical decisions.
- [Efficient execution plan and new-chat handoff](roadmaps/aegis-efficient-execution-handoff-2026-09-23.md):
  September 23 backlog sequence, model policy, verified state and continuation task.
- [Conversational setup and routing plan](roadmaps/aegis-setup-routing-plan.md):
  issue #101 decisions, candidate screen and proposed evaluation protocol.
- [Offline setup routing contract](../tools/aegis_setup/README.md):
  maintainer guide to the implemented synthetic advisory checks; there is no
  host integration, provider connection or dispatch authority.
- [Issue #101 package-2 scope proposal](roadmaps/aegis-setup-package-2-authorization-proposal.md):
  reviewable Aegis-only conversation and saved-state implementation boundary.
- [Documentation readability backlog](roadmaps/aegis-documentation-readability-backlog.md):
  the plan to explain each component in plain language, define project shorthand,
  and review all repository documentation for human and agent readers.
- [Security policy](../SECURITY.md): supported surfaces and private reporting.
- [Changelog](../CHANGELOG.md), [construction history](HISTORY.md), and
  [reconciliation and decision log](reconciliation/step-0-reconciliation-v4.md):
  delivered changes, historical context and recorded decisions.

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
[PR #99](https://github.com/ModernNomad-98/Project-Aegis/pull/99) merged on
2026-09-23 at `be552fb778ec50fd0cbe82eff9f1022235ec11d8` after its final
exact-head reviews and all three hosted checks passed. The exact package suite
passed 543 tests on Windows and 543 on Linux (three expected platform skips); all
three stop findings, the aggregate stop gate, T13
authority lifecycle intake, T15 binding-mismatch handling, the T14
PLANNED/BLOCKED resume slice, T05 local-execution pause and T06 contacted
external-mutation uncertainty pause received independent `APPROVE`. The narrow
T07 local-nonexecution settlement and its BLOCKED-only T14 recovery route, plus
the narrow T08 validation-pause checkpoint and its clean VALIDATING T14 resume
route, T09's exact-head reconciliation pause fence, and the narrow T17
validator-result/T14 exact-T09-resume slice also received independent
`APPROVE`. The T17 operation-uncertainty foundation, including typed
source/control evidence, conditional uncertainty categories, atomic semantic
migration and exact-set recovery, also received independent `APPROVE`.
The T17 verified-receipt route now also has independent `APPROVE`: it binds a
typed query/time/source/response lookup, exact receipt/plan/slot/head facts and
complete settlement ancestry, then clears its exact uncertainty set atomically
with typed PAUSED/BLOCKED/VALIDATING routing and strict recovery. The
T17 authoritative-nonexecution and authenticated safe-retry slice also has
independent `APPROVE`, including all-path seal binding, generation-bound retry,
stacked-pause replay and proof-prefix-safe migration. F02 is now independently
accepted: proof-free owner dispositions remain non-dispatching, and the only
reviewed same-key successor retains outcome/activity uncertainty plus the exact
T06 pause until distinct T14 RESUME authority clears it. T22 terminal-restart
reporting is independently accepted with strictly read-only main/auxiliary
verification and typed stale/unverified status. F03 source-atomic one-use
authority is independently accepted: host/manual races, lifecycle timing,
correction ownership, clock rollback and lost-receipt replay are now directly
asserted. F04a reservation-boundary accounting is also independently accepted,
including exact known usage, durable overrun fences, unknown-liability retention,
pre-contact bound denial and strict semantic-v10 migration. All 22 acceptance-
family rows now have tested, independently accepted coverage. All 28 transition,
9 crash-boundary and 22 acceptance-family rows are independently accepted; the
final exact-head architecture/security/QA and hosted gates also passed.
The independently accepted selected-check foundation binds explicit v2
per-check dependencies and launch gates, derives a deterministic topological
order and reconstructs projections strictly. The current increment adds signed
monotonic gate facts and complete launch snapshots, universal no-preclaim T27,
atomic T11 next-check routing, exact T16 route recovery and contact-time stale
launch disablement with T25/T16 continuation. T11, T27, F11 and F17 are included
in the independently accepted 28/9/22 canonical inventory. The
[Codex handoff](evidence/control-plane/cp-wp-002-codex-handoff.md) is the final
CP-WP-002 evidence record. No deployment,
provider call, production data, real authority or real execution adapter is
authorized.

The [control-plane work package 003A offline proof proposal](roadmaps/cp-wp-003-offline-proof-proposal.md)
defined the synthetic increment delivered in PR #123. It tests failures of
source, freshness, containment, evidence and accounting claims. Work package
003 still needs real-source and selected-host proof before any live route;
the [current backlog](roadmaps/resumable-control-plane-backlog.md) tracks those
gates.
