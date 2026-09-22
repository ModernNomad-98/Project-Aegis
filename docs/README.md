# Project Aegis documentation

Start here for current guidance. Dated evidence and design proposals preserve
their original context; use the active registers below to determine current work.

## Use the skills

- [Project README](../README.md): setup, skill picker, shipped skills and agents.
- [Skills catalog](skills-catalog.md): implemented capabilities and their boundaries.
- [Engineering discipline](ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md): principles and workflow.
- [Skill generation standard](skill-generation-standard.md): current authoring contracts.

## Maintain the source library

- [Contributing](../CONTRIBUTING.md): verification, review and sign-off requirements.
- [Offline CI](offline-ci.md): local reproduction, Linux/Windows checks and known gaps.
- [Owner approval register](approvals/APPROVAL_REGISTER.md): all current
  Project Aegis grants, limits and lifecycle events; read the complete register
  before acting.
- [Merge policy](reconciliation/auto-merge-policy.md): current authority and historical decisions.
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
Original roadmap proposals and dated evidence remain useful history, rather
than instructions to reopen completed PRs or reproduce the lost computer.

## Resume delivery control-plane work

Use a current `main` checkout. CP-WP-001 was a documentation-only contract and
merged in [PR #95](https://github.com/ModernNomad-98/Project-Aegis/pull/95) as
`32cbb2dff8265b2c2aaff38f2ace198417ef1646`; it did not implement a controller
or runtime. Read the [design](design/resumable-control-plane-v1.md), the
[work-package register](roadmaps/resumable-control-plane-backlog.md) and the
[review evidence](evidence/control-plane/cp-wp-001-review.md) together.

CP-WP-002 is active under [AEGIS-APR-004](approvals/APPROVAL_REGISTER.md) but is
still an unaccepted draft checkpoint. The full local package suite passed 465
tests on 2026-09-22; all three stop findings, the aggregate stop gate, T13
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
with typed PAUSED/BLOCKED/VALIDATING routing and strict recovery. The remaining
T17 authoritative-nonexecution and authenticated safe-retry slice also has
independent `APPROVE`, including all-path seal binding, generation-bound retry,
stacked-pause replay and proof-prefix-safe migration. T22 terminal-restart
reporting is now independently accepted with strictly read-only main/auxiliary
verification and typed stale/unverified status. T28 with F01 is next in the
documented order.
The independently accepted selected-check foundation binds explicit v2
per-check dependencies and launch gates, derives a deterministic topological
order and reconstructs projections strictly. The current increment adds signed
monotonic gate facts and complete launch snapshots, universal no-preclaim T27,
atomic T11 next-check routing, exact T16 route recovery and contact-time stale
launch disablement with T25/T16 continuation. T11, T27, F11 and F17 remain
`UNVERIFIED` pending committed exact-head trace review even though the corrected
increment received independent `APPROVE`; broader T17 and the
remaining canonical gaps still block merge.
Remaining exact
T/C/F backlog and final review gates still
block merge, so the
passing suite is not a completion or merge claim.
Continue only from the
[Codex handoff](evidence/control-plane/cp-wp-002-codex-handoff.md). No deployment,
provider call, production data, real authority or real execution adapter is
authorized.
