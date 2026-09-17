# Changelog

Dated changes delivered to `main`, using Australia/Sydney dates; these entries
do not imply a tagged release.
For current setup and remaining work, see the [documentation index](docs/README.md).
Earlier construction history is in [HISTORY](docs/HISTORY.md), with immutable
decisions in the [reconciliation log](docs/reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions).

## 2026-09-13

- **Resumable delivery control contract ([PR #95](https://github.com/ModernNomad-98/Project-Aegis/pull/95)):**
  delivered the documentation-only [durable state, authority and recovery design](docs/design/resumable-control-plane-v1.md),
  its [separate work-package register](docs/roadmaps/resumable-control-plane-backlog.md)
  and [review evidence](docs/evidence/control-plane/cp-wp-001-review.md). No
  controller or runtime was implemented. CP-WP-002 remains blocked pending
  separate explicit authorization.

## 2026-09-12

- **Calibration engineering ([PR #88](https://github.com/ModernNomad-98/Project-Aegis/pull/88)):**
  delivered reviewed execution controls, telemetry accounting, request deadlines
  and recovery records. The engineering scope is complete; measured calibration
  and OD-1 ratification remain open. Original calibration inputs are unavailable;
  the [replacement plan](docs/evidence/ber-recovery-2026-09-11/replacement-plan.md)
  records the next preparation steps and approval gates.
- **Shared skill contracts ([PR #90](https://github.com/ModernNomad-98/Project-Aegis/pull/90)):**
  added immutable approval lifecycle rules, bounded recording of approved state
  projections, a clear distinction between planning readiness and human
  commitments, corrected invocation posture, and approval-grader coverage.
  The review resolved 19 confirmed issues and 79 false positives from 98
  candidates, plus three adjacent fixes. The library remains at 184 skills;
  manual-only skills increased from 18 to 27. See the
  [review evidence](docs/evidence/shared-contracts-closeout-2026-09-12/README.md).
- **Offline CI ([PR #91](https://github.com/ModernNomad-98/Project-Aegis/pull/91)):**
  added permanent Linux and Windows checks for the validator, contract audit,
  BER regressions and PowerShell acceptance scripts, with pinned dependencies
  and retained command evidence. Fixed Windows PowerShell execution by using
  its native shell. See [CI reproduction and limits](docs/offline-ci.md) and
  [delivery verification](docs/evidence/offline-ci-2026-09-12/DELIVERY.md).
- **Persistent owner approvals ([PR #93](https://github.com/ModernNomad-98/Project-Aegis/pull/93)):**
  recorded recurring read-only-agent and administrator-merge grants in the
  [source repository approval register](docs/approvals/APPROVAL_REGISTER.md),
  linked it from startup instructions, and recorded the offline-CI closeout.

These deliveries do not establish measured calibration, live skill efficacy,
OD-1 ratification, or completion of the future behavioral advisory CI lane.

## 2026-08-18

- **Audit correction ([PR #89](https://github.com/ModernNomad-98/Project-Aegis/pull/89)):**
  retired AEGIS-060 as a false positive. Typed `(subagent)` annotations remain valid.
