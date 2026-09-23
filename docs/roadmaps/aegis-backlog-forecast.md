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
The first cadence checkpoint is PR #111, the fifth PR merged *after* #106.
The next checkpoint is the fifth merge after #111 (PR #116 if no other PR
numbers intervene). Also update the forecast earlier when an owner decision
materially changes scope.

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

## Five-merge checkpoint — 2026-09-23, after PR #111

This snapshot preserves the baseline above. Five PRs merged after #106:

| PR | Merge commit | Observed wall time from first work checkpoint to merge | Delivered |
| --- | --- | ---: | --- |
| [#107](https://github.com/ModernNomad-98/Project-Aegis/pull/107) | `911fe25f7a5297113890512aaecc38694bda3e8a` | 33m20s | Private candidate public checkpoint and baseline forecast; private inputs remain PENDING |
| [#108](https://github.com/ModernNomad-98/Project-Aegis/pull/108) | `2b13be9fac1169bf8f6cd0cfcbe4da0c5b8bf926` | 13m38s | BKL-009 policy proposal and cross-stream owner decision index |
| [#109](https://github.com/ModernNomad-98/Project-Aegis/pull/109) | `32144083bc86412e30d70873f877d4e7c051b6e0` | 9m40s | Issue #101 package-1 design and candidate screen |
| [#110](https://github.com/ModernNomad-98/Project-Aegis/pull/110) | `75d1e6e662ed48f0ec9f6b04c4c52e6f39ead319` | 8m58s | CP-WP-003A synthetic proof scope proposal |
| [#111](https://github.com/ModernNomad-98/Project-Aegis/pull/111) | `8e6971d806e257097c76159ac0875b4fef8baf0b` | 8m19s | BER selected-host R4/R5 decision packet |

These intervals total **1h13m55s observed wall time** across five sequential
packages, including review/CI within each start-to-merge interval. Gaps
between packages are excluded. Active-only time was not instrumented. CI wall time and owner wait
are not separable for every PR; known owner waits remain open for PR #104's
schema shape, private input PR #1's semantic/label approval, BKL-009 policy,
CP-WP-003A authorization and host selection. No inference that a coding
package takes ten minutes follows from governance/documentation PRs.

| Work item | Baseline remaining active h | Revised remaining active h | Evidence and reason |
| --- | ---: | ---: | --- |
| BER-BKL-007 / WP-2B-1A | 1–2 | 1–2 | PR #104 remains open at `5a1c7ace`; schema-shape answer and final main reconciliation pending; no completed change to this gate |
| WP-2B-3 candidate inputs | 4–8 | 1–4 | 160 PENDING cases, guide, split/hash packet and private PR #1 exist; remaining agent work is review-response/revision, with owner semantic approval time excluded |
| Cross-stream owner-decision packet | 3–6 | **0, closed as preparation** | PR #108 merged the policy/index; #110/#111 expanded the CP/host proposals. Actual decision and implementation gates remain separate |
| BER-BKL-009 policy enforcement | Not separately counted | **8–16, new row** | #108 exposed missing ACL/encryption verification, real sensitivity assignment, bundle-first deadline, redaction and marker-gated cleanup. The old decision-packet estimate did not cover this runtime/runbook work; owner parameters pending |
| WP-2B-3 execution support | 8–16 | 8–16 | No holdout executor or reviewed replacement source/allowance yet; #107 prepared inputs only |
| WP-2B-3 measurement / OD-1 packet | 4–10 | 4–10 | Provider, owner label/freeze and result-ratification gates unchanged; no measured run |
| R4/R5 selected-host proof | 8–16 | **12–24** | #111 separated generic Linux CI from selected-host proof and documented Stage A plus eleven effective tool paths and full R5 profile; host/authority still unselected |
| WP-2B-4 | 12–24 | 12–24 | Limited Scenario A live suite still depends on calibration and host evidence |
| WP-2B-5 | 8–16 | 8–16 | Generic corpus phase unchanged; WP-2B-4 gate |
| WP-2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine, BKL-011 operations and BKL-012 remain later-phase work; BKL-009 enforcement is counted separately above |
| WP-2B-7 | 4–8 | 4–8 | Advisory CI/operator workflow and BKL-013 unchanged |
| CP-WP-003 | 8–16 | **12–24** | #110 made synthetic proof plus later real source/freshness/host/evidence/billing verification explicit; no implementation approval yet |
| CP-WP-004 | 8–16 | 8–16 | No delivery target selected; CP-WP-003 gate unchanged |
| Issue #101 package 1 | 4–8 | **0, closed as planning** | #109 merged design, candidate screen and comparison protocol; no runtime work conflated with this row |
| Issue #101 package 2 | 6–12 | 6–12 | Conversational Aegis-only implementation still needed |
| Issue #101 package 3 | 6–12 | 6–12 | Offline adapter/check contract still needed |
| Issue #101 package 4 | 8–16 | 8–16 | Comparative evaluation needs separate authority and measured host behavior |
| Issue #101 package 7 | 6–12 | 6–12 | End-to-end release evaluation remains after selection |
| **Selected remaining total** | **106–214** | **112–228** | Sum of open rows, each counted once; active work only |

The revised total rises slightly despite two completed planning rows because
BER-BKL-009 implementation was missing as a separately executable package,
and the R4/R5 and CP-WP-003 proof surfaces are wider than the baseline table
made explicit. The candidate-input row shrinks because a versioned private
packet now exists. These are scope/progress changes, not a speed multiplier
derived from short PRs. Owner waiting, GitHub queue, provider execution,
provisioning and future unselected scope remain outside active-hour ranges.

The conditional issue #101 package-5 local and package-6 online helper estimates
remain **8–20 active hours each** because no comparison selected either one.
If both are selected, the currently bounded selected-plus-both total is
**128–268 active hours**. The earlier **122–254** conditional total remains
the historical baseline. The other conditional item estimates remain
**4–12 hours** for BER-BKL-010 signing/immutable storage,
**8–20 hours per host** for BER-BKL-014 and **8–24 hours per product** for
BER-BKL-015; no adoption decision or measurement changed them. Multi-judge
work and CP-FUT-001 remain unbounded architecture decisions. No finite all-options total
or calendar date is supportable until those decisions and host/provider waits
are bounded. Revisit every open row after the next five merged PRs, or sooner
after a material owner choice.

For each new work package, communicate its **prior published item ETA** (or
none), its **new item ETA**, and the **current backlog total** at start and in
the PR. The current bounded selected total is **112–228 active hours**;
selecting both issue #101 helpers would make it **128–268**. The full optional
adoption backlog has **no finite total ETA** yet because the number of extra
hosts/products and the multi-judge/distributed decisions are unset. Never
present one of the bounded totals as an all-options completion promise.
