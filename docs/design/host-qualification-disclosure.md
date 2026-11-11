# Host-qualification disclosure (C1.4, disclosure only)

**Status: qualification was NOT performed and is NOT authorised.** This page
is a disclosure of what is unproved, not a qualification report, not a
test record and not a coverage claim. Owner decision T5 (mounted
host-coverage export) is not granted, and no host install, export, settings
change or counter change was made by this slice.

**Authority.** C1.4 of the C1.2-C1.4 Stage A plan REV4 (69,918 B /
`a65fa654...`), captured as
`C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md` (1,081 B / `56939142...`)
and accepted plan-only by Stage B (12,193 B / `3318b957...`), under the
disclosure-only C1.4 authority line. T5-gated qualification is a separate
future captured plan and slice; this page grants nothing and claims nothing.

## What was not done

| Qualification item | State | Missing authority / dependency |
| --- | --- | --- |
| Mounted host-coverage export (which paths the guard actually governs) | **UNRUN** | T5 export not authorised; no host access |
| Denied-tool-call evidence and the retry behaviour after a denial | **UNRUN** | T5 + T9 host authority |
| Monotonicity of the guard across restarts and configuration edits | **UNRUN** | T5 + T4 settings/identity |
| Recovery-message behaviour shown to the user after a denial | **UNRUN** | T5 + T9 host authority |
| Counter/policy custody on the host (who can edit the store) | **UNRUN** | T5 + T7 authority; T24 store custody unresolved |
| Custom executor / ACP / terminal / remote route coverage | **UNRUN** | T5 coverage export + T9 host authority |
| Profile/config custody under the constrained profile | **UNRUN** | T4 settings/identity |
| Independent qualification by a verifier distinct from the implementer | **NOT COMMISSIONED** | named verifier + exact-head evidence; T9 |

None of these rows is a pass, a partial pass or a simulated result. UNRUN is
never converted to PASS, and no row is inferred from the tooling in this
repository.

## What is known, and how

- The guard **facility** exists and is described as monotonic in the C0 intake
  findings (section 6) - **REPORTED**, not re-derived in this pass.
- The desktop composition cannot be dumped, so **mounted coverage is UNKNOWN**.
- The profile patch layer is user-writable under the constrained agent's
  profile, so custody of the configuration route **fails**.
- At least six routes are not governed by the in-process guard: custom
  executor, ACP runtimes, terminal/remote, workflow registration, subagent
  presets, restart re-read.
- Repository-side, `docs/approvals/` is not gate-guard protected, so the
  change-state records have policy + git-history custody only.

The control-by-control matrix and the evidence classes are on
[supported controls and custody](supported-controls-boundary.md). This page
does not repeat or extend them.

## What a reader may conclude

- The repository contains auditable tooling and documented formats; a reader
  can audit a supplied record set after the fact.
- Nothing in this repository prevents, contains or detects a host action. No
  denial, recovery, monotonicity or coverage behaviour has been observed here.
- A record that says a bypass occurred is displayed as a bypass; it is not
  evidence that the bypass was prevented.

## What a reader may not conclude

- That host containment, universal prevention or ENFORCED status holds - the
  assurance claim for every host control is NONE.
- That mounted coverage is known, or that the guard governs a route it was not
  observed to govern.
- That a green readiness result exists: production readiness is BLOCKED while
  T6 is undecided, and the merged checker's own run is blocked by the
  UNVERIFIED store (T24).

## What a real qualification would require

A future T5-gated qualification would need, in one separately captured and
audited slice:

1. an owner-authorised T5 mounted-coverage export and host access authority;
2. T4 settings/identity preconditions, or an explicit scoped exception;
3. a named independent qualifier distinct from author and implementer;
4. exact-head evidence: the commands, the denial events, the recovery
   messages, the counter-store custody probe, and every UNRUN named;
5. a recorded verdict vocabulary that keeps UNKNOWN/UNRUN distinct from PASS;
6. the standing 3-head budget and no head movement after the final verdict.

Until then the honest statement is: **qualification not performed; mounted
coverage UNKNOWN; denial and recovery evidence UNRUN; ENFORCED blocked.**
