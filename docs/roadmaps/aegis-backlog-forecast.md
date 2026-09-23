# Project Aegis backlog forecast

Baseline: 2026-09-23, after PR #106. This is an active-work forecast for the
remaining scope in the [execution handoff](aegis-efficient-execution-handoff-2026-09-23.md),
the [BER backlog](behavioral-eval-runner-backlog.md), the
[CP backlog](resumable-control-plane-backlog.md), and [issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101).
It is not authorization to start a blocked package. Ranges include implementation,
local checks, independent audit and PR preparation; they exclude owner wait,
GitHub queue time, provider execution wait and new scope. Dependencies make a
calendar completion date unsupported at present.

## Re-estimation rule

Count merged PRs after PR #106, regardless of their issue number. After each
five merges, re-read every PR's estimate, observed active time (or explicitly
unavailable measurement), CI/review time, owner wait, scope change and progress
checkpoints in the [measurement log](aegis-execution-metrics.md) and PR body/
comments. Re-estimate **every open row below** and both total ranges; add a
dated snapshot with the five merge commits and reasons for changed estimates.
Keep the prior snapshot. Record newly opened/closed work, decision delays,
rework and critical-path changes separately. Do not convert wall time to
active time or treat a short governance PR as a coding throughput rate.
The next cadence checkpoint is the fifth PR merged *after* #106. Also update
the forecast earlier when an owner decision materially changes scope.

The available timed PRs are sparse: #103 has only a late 10:52 UTC checkpoint
and at least 5m14s to merge; #105 took 12m50s observed wall time from its first
checkpoint to merge; #106 took 8m21s. PRs #100/#102 have no comparable active
measurement in this log. The ranges below are scope estimates, **not** a
statistical extrapolation from those short governance PRs. PR #104 has local
tests and two execution jobs green but awaits the owner's schema-shape decision.

## Remaining selected work — baseline estimate

| Work item | Scope counted once | Remaining active hours | Gate / confidence |
| --- | --- | ---: | --- |
| BER-BKL-007 / WP-2B-1A | Finish PR #104 after the owner shape decision; close its lifecycle | 1–2 | Owner decision pending; medium |
| WP-2B-3 candidate inputs | New 160-item packet, guide, private versioned inputs, semantic review and hashes | 4–8 | Started; owner labels later; low |
| Cross-stream owner-decision packet | BKL-009 handling, replacement source/accounting, host/CP and issue #101 decisions | 3–6 | Decisions may add scope; low |
| WP-2B-3 execution support | Approved pins, missing holdout execution path, offline tests and readiness | 8–16 | Requires label/source/allowance decisions; low |
| WP-2B-3 measurement / OD-1 packet | Development evidence, holdout freeze and one holdout, result review | 4–10 | Provider and owner gates; low |
| R4/R5 selected-host proof | Isolation/profile capability evidence; includes BKL-003 live claim scope | 8–16 | Host selection pending; low |
| WP-2B-4 | Limited Scenario A live suite after separate authorization | 12–24 | WP-2B-3 and host gates; low |
| WP-2B-5 | Generic corpus execution | 8–16 | WP-2B-4 gate; low |
| WP-2B-6 | Scheduling, cost, quarantine and cadence; includes BKL-011 operations and BKL-012 | 8–16 | Prior phase; low |
| WP-2B-7 | Advisory CI/operator workflow; includes BKL-013 | 4–8 | Protected workflow review; low |
| CP-WP-003 | Authority, evidence and execution capability proofs | 8–16 | Separate authorization; low |
| CP-WP-004 | One selected delivery integration | 8–16 | CP-WP-003 and selected target; low |
| Issue #101 package 1 | Design, candidate screening and durable planning | 4–8 | Planning/authority first; low |
| Issue #101 package 2 | Conversational setup and Aegis-only completion | 6–12 | Design; low |
| Issue #101 package 3 | Compatibility checks and offline adapter contract | 6–12 | Design; low |
| Issue #101 package 4 | Bounded comparative evaluation and selection gate | 8–16 | Separate evaluation authority; low |
| Issue #101 package 7 | End-to-end evaluation and release readiness | 6–12 | Selected integration outcome; low |
| **Total selected remaining work** | **Each package counted once** | **106–214** | **Active hours; owner/CI/provider waits excluded** |

BER-BKL-001/002/004/006/008 and WP-2B-0/1/2 are delivered within their
recorded scopes. Remaining real-host R3/R4/R5 proof is counted at the live
gate. BKL-005 and the calibration half of BKL-011 are counted in WP-2B-3;
BKL-011's ongoing operations half is counted in WP-2B-6; BKL-009 is counted
in the decision packet and later operator work; R1/2/3 in their owning phase. This mapping
prevents a supporting backlog record from being estimated as a second build.
The current BER-BKL-007 row is a *remaining* estimate; its earlier 3–5-hour
initial estimate and partial execution remain in the PR history.

## Conditional and unselected scope

| Work item | Active hours if selected | Current disposition |
| --- | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | Conditional on package 4 selection |
| Issue #101 package 6, online helper | 8–20 | Conditional on package 4 selection and provider authority |
| BER-BKL-010 signing/immutable storage | 4–12 | Adoption decision pending |
| BER-BKL-014 additional host adapters | 8–20 per host | Host selection pending |
| BER-BKL-015 optional operations products | 8–24 per product | Product selection pending |
| Multi-judge arbitration and CP-FUT-001 | Not bounded | Separate architecture/adoption decisions |

If **both** #101 helpers are selected, the currently bounded active total
becomes **122–254 hours**. The optional BER/CP rows are not included in either
total because their quantity or adoption is undecided. A fixed “all backlog”
calendar ETA would hide those decisions and owner/provider waits; the next
five-merge review must revisit them explicitly.
