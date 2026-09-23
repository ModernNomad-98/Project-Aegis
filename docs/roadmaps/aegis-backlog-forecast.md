# Project Aegis backlog forecast

## Start here — current reading

This is a rolling **active-work estimate**, not a calendar promise or permission
to start blocked work. At the latest recorded [five-merge checkpoint after pull
request #169](#five-merge-checkpoint--2026-09-23-after-pull-request-169), the
selected remaining work totals **175–394 active hours**, including **80–200
active hours** for the repository-wide documentation readability sweep. That
checkpoint was recorded on 2026-09-23; later work should be checked against
the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-169--2026-09-23)
and [documentation batch ledger](aegis-documentation-readability-backlog.md#documentation-batches)
before treating its totals as current.

For requirements and remaining gates, use the owning [Behavioral Eval Runner
(BER) backlog](behavioral-eval-runner-backlog.md), [control-plane (CP)
backlog](resumable-control-plane-backlog.md), and [issue #101 setup routing
plan](aegis-setup-routing-plan.md). The [execution handoff](aegis-efficient-execution-handoff-2026-09-23.md)
routes work across those records. Optional helpers and unselected host or
product scope are separate from the selected total; the full all-options
backlog has no finite estimate.

The **baseline after pull request #106** and the older cadence paragraphs and
tables below are retained as historical snapshots. Their dated estimates,
pending decisions, and statements about what will happen next describe their
original checkpoints. Follow the latest checkpoint and the owning records for
current status and authorization.

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
present one of the bounded totals as an all-options completion promise. Those
figures belong to the checkpoint before the one below.

## Five-merge checkpoint — 2026-09-23, after PR #104

Here, “PR” means pull request; “work package” means a bounded planned delivery;
“POSIX host” means a Unix-like execution environment; and “owner decision 1”
is the later human ratification of the Behavioral Eval Runner's measured
calibration result. The numbered backlog identifiers link to their detailed
requirements in the Behavioral Eval Runner and control-plane registers above.

This snapshot preserves the earlier tables. The fifth merge after PR #111
was PR #104; pull request numbers do not describe merge order. The owner also
accepted the schema shape, selected the recommended evidence policy and
disposable-POSIX-host direction, approved the bounded control-plane and setup
scopes, and expanded the documentation requirement. These decisions change
gates and scope; they do not establish an available host or approved labels.

| Merged request | Merge commit | Observed wall time from first work checkpoint | Result |
| --- | --- | --- | --- |
| [#112](https://github.com/ModernNomad-98/Project-Aegis/pull/112) | `fa79092f1c0fb1984b75245d8bce6a41982e5419` | 9m13s | Previous five-merge forecast |
| [#113](https://github.com/ModernNomad-98/Project-Aegis/pull/113) | `5a2452a0e0a6cec974d142e14a66641cd51f2c5d` | 11m21s | Issue #101 setup scope proposal |
| [#114](https://github.com/ModernNomad-98/Project-Aegis/pull/114) | `d187849287e5047fc821f7a1070b0c59cc5b32b9` | 8m35s | Control-plane exact-file scope |
| [#115](https://github.com/ModernNomad-98/Project-Aegis/pull/115) | `f3d3e07cd623a1cd69413d0d28e15b75df4c5a49` | 7m15s | Issue #101 offline advisory-contract scope |
| [#104](https://github.com/ModernNomad-98/Project-Aegis/pull/104) | `c83a0601d9b7945ad407b6fa81bd2563ab501475` | 4h42m26s, including owner/main-drift wait | Version-integrity code and compatibility policy; owner accepted shapes |

The five intervals overlap in calendar time: PR #104 waited while #112–#115
were prepared and merged. Their sum is **not** an elapsed project duration or
active-work measurement. Active-only, review and owner-wait durations were
not fully instrumented. The short document PRs provide no reliable coding
speed multiplier. PR #104's final local suite passed 997 tests with 14
expected skips; its Linux and Windows jobs passed. Its protected-file guard
failed only on the documented manual-review condition under the owner's
PR-specific exception. No other failed check is treated as green.

| Work item | Previous remaining active hours | New remaining active hours | Change or current gate |
| --- | ---: | ---: | --- |
| Behavioral Eval Runner backlog item 007 / work package 2B-1A | 1–2 | **0** | PR #104 merged after owner shape acceptance; delivered scope closed |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Private 160-case candidate remains pending semantic and label review |
| Behavioral Eval Runner backlog item 009 evidence policy enforcement | 8–16 | 8–16 | Owner chose the 30-day complete-bundle policy; implementation and host-specific encryption proof remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Development driver lacks reviewed holdout support; offline scope proposal PR #116 is open |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Historical allowance, exact source, private labels, development result and later holdout freeze remain gates |
| Selected-host capability proof (R4 tool-path isolation and R5 execution-profile isolation) | 12–24 | 12–24 | Disposable POSIX direction accepted; no named/provisioned host or selected-host proof exists |
| Work package 2B-4 | 12–24 | 12–24 | Live Scenario A still follows calibration and host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus phase remains dependent on 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain later-phase work |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain later-phase work |
| Control-plane work package 003 | 12–24 | 12–24 | Owner approved the synthetic first-increment scope; separate merged exact grant is still required; real source and host proofs remain |
| Control-plane work package 004 | 8–16 | 8–16 | No real delivery target selected and package 003 prerequisites remain |
| Issue #101 package 2 | 6–12 | 6–12 | Owner approved Aegis-only setup scope; exact grant and implementation remain |
| Issue #101 package 3 | 6–12 | 6–12 | Owner approved offline advisory contract scope; exact grant and implementation remain |
| Issue #101 package 4 | 8–16 | 8–16 | Comparative evaluation still needs host, inputs and separate execution authority |
| Issue #101 package 7 | 6–12 | 6–12 | End-to-end release review remains after selected integration outcomes |
| Repository-wide documentation readability | Not counted | **80–200** | New owner requirement; 491 tracked Markdown files inventoried; component guides and navigation first, then recorded full sweep |
| **Selected remaining total** | **112–228** | **191–426** | Each open item counted once; active work only |

The earlier cross-stream decision packet and issue #101 package 1 remain
closed as planning work. The new documentation estimate is deliberately wide:
491 tracked Markdown files require a recorded review, and actual rewrite volume is
unknown. Its earlier narrow 4–8-hour component estimate and interim 24–60-hour
repository estimate are superseded by **80–200 hours** until the first audited
documentation batches provide a better basis. The new total subtracts the
closed 1–2-hour schema row and adds this 80–200-hour item. It does not count
the still-open PR #116 proposal as completed implementation.

The optional issue #101 local and online helpers remain **8–20 hours each**.
If both are selected, the bounded selected-plus-both total becomes
**207–466 active hours**. Signing and immutable storage, additional hosts or
products, multi-judge arbitration, future control-plane architecture and
other unselected adoption remain outside both totals. The full all-options
backlog has no finite estimate. Owner waits, GitHub queue, provider run time
and host provisioning are excluded from active-hour estimates. Re-estimate
all open rows after the next five merged requests or sooner if a decision
materially changes scope.

## Five-merge checkpoint — 2026-09-23, after pull request #121

This snapshot keeps the previous estimate visible above. Five pull requests
merged after #104, in merge order. Times are observed wall intervals from the
first recorded work checkpoint; they are lower bounds when work began earlier.
They overlap and cannot be added to estimate active labor or project duration.

| Merged pull request | Merge commit | Observed wall interval | Delivered |
| --- | --- | ---: | --- |
| [#117](https://github.com/ModernNomad-98/Project-Aegis/pull/117) | `a7c0724c86cce3f59b4dacfe0db7502ac148b49a` | 12m43s | Documentation inventory and forecast checkpoint |
| [#116](https://github.com/ModernNomad-98/Project-Aegis/pull/116) | `2755fb6b59c64290a4cef2e4f9bcac204699fe76` | 39m21s | Offline holdout executor proposal only; implementation still needs a grant |
| [#118](https://github.com/ModernNomad-98/Project-Aegis/pull/118) | `1af342712d27d5e6ea482b3f451106b4dccaf125` | 10m42s | Exact grants for the control-plane synthetic proof and issue #101 packages 2 and 3; evidence-policy choice only |
| [#120](https://github.com/ModernNomad-98/Project-Aegis/pull/120) | `2c119b22d6a6da437bcb17e513438cde8f4b5f13` | 6m59s | Root guide first screen and contribution writing standard |
| [#121](https://github.com/ModernNomad-98/Project-Aegis/pull/121) | `34241baf5fd1911f3d7d07915adc3bacd272d4b2` | At least 10m39s | Issue #101 package-3 offline advisory contract; no host hook or provider call |

The observed intervals are short mainly because three packages were
documentation/governance changes. Active-only time was not instrumented.
Pull request #121's first checkpoint came after implementation began. Local
checks, independent review and all three GitHub Actions passed for its exact
head. Pull requests #119 and #122 and the in-progress control-plane and setup
package-2 candidates are not merged at this checkpoint; their work is not
counted as delivered. The component-guide guard exception for #119 awaits a
separate owner disposition.

| Open work item | Previous remaining active hours | New remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Private 160-case candidate still needs semantic and label review; no verified completion |
| Behavioral Eval Runner backlog item 009 evidence policy enforcement | 8–16 | 8–16 | #118 recorded the 30-day complete-bundle choice, but implementation authority and host storage proof remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | #116 prepared an offline holdout design; implementation grant and tests remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Private labels, source/allowance, development evidence and a later holdout freeze remain |
| Selected-host capability proof (R4 tool-path and R5 execution-profile isolation) | 12–24 | 12–24 | A disposable Portable Operating System Interface host direction is chosen; a named host and its proof are not |
| Work package 2B-4 | 12–24 | 12–24 | Limited live suite depends on calibration and host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 12–24 | 12–24 | The synthetic first increment is under independent review; real authority, evidence and host proofs remain |
| Control-plane work package 004 | 8–16 | 8–16 | No selected delivery target; package 003 is a prerequisite |
| Issue #101 package 2 | 6–12 | 6–12 | Conversational setup candidate is under independent review, not merged |
| Issue #101 package 3 | 6–12 | **0** | #121 merged its approved offline advisory scope; a real host remains package 4 scope |
| Issue #101 package 4 | 8–16 | 8–16 | Comparative evaluation needs a selected host, inputs and separate authority |
| Issue #101 package 7 | 6–12 | 6–12 | End-to-end release review remains after integration selection |
| Repository-wide documentation readability | 80–200 | 80–200 | #120 improved the entry point; #119 and #122 are open. The 491-file review is still broad, so the range is unchanged pending audited batches |
| **Selected remaining total** | **191–426** | **185–414** | Package 3's 6–12 hours closed; each other open row was reconsidered and retains its range |

The conditional local and online issue #101 helpers remain **8–20 active
hours each**. If both are selected, the bounded selected-plus-both total is
**201–454 active hours**. The all-options backlog still has no finite total:
extra hosts/products and later architecture choices have no selected quantity.
These are active-work estimates, not calendar promises. Owner decisions,
GitHub queues, provider runs and host provisioning are excluded. The next
five-merge review starts after #121; update sooner if an owner decision changes
scope or a completed audited batch provides meaningful new timing evidence.

## Five-merge checkpoint — 2026-09-23, after pull request #126

This snapshot follows the #121 checkpoint above. Five pull requests merged
after #121, in merge order. The observed intervals are wall time from each
first recorded checkpoint; they include review, GitHub queue or parallel work
where present. They are not measured active labor or an additive project
duration.

| Merged pull request | Merge commit | Observed wall interval | Delivered |
| --- | --- | ---: | --- |
| [#123](https://github.com/ModernNomad-98/Project-Aegis/pull/123) | `c965595c3c388c94f15174d45fc3d2fa8fd073b4` | 19m29s | Control-plane work package 003A: synthetic negative proofs only |
| [#122](https://github.com/ModernNomad-98/Project-Aegis/pull/122) | `b2c6db2fdf90eee20aa4de52d184076b7e447f4e` | At least 11m25s | Three active maintainer guides; editing began before timing started |
| [#124](https://github.com/ModernNomad-98/Project-Aegis/pull/124) | `d598390f4b7bb367ce79dd1276157f91ae36556b` | About 19m59s | Issue #101 package 2: manual Aegis-only Windows setup |
| [#125](https://github.com/ModernNomad-98/Project-Aegis/pull/125) | `ad8c1cef62527464aff2e698b58b094a790b058f` | 13m27s | Previous every-item forecast; its interval overlaps other PR work |
| [#126](https://github.com/ModernNomad-98/Project-Aegis/pull/126) | `709668594d43cb5cad8ce3dff14c574866228b07` | 14m46s | Two active technical guides and a dated review record |

PRs #123 and #124 passed independent audits and all three exact-head GitHub
Actions after correcting review findings. The documentation PRs also passed
independent audits and exact-head Actions. Active-only time was not
instrumented; none of these short intervals is a measured implementation
rate. Pull requests #119, #127 and #128 are open at this checkpoint, so their
changes are not counted as delivered. The protected-file guard on #119 is
failed and awaits a PR-specific owner disposition, even though its Linux and
Windows execution jobs passed on the earlier head; the rebased head is being
checked separately.

| Selected open work item | Previous remaining active hours | New remaining active hours | Re-estimation evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Private candidate still needs semantic and label review; no completed freeze |
| Behavioral Eval Runner backlog item 009 evidence policy enforcement | 8–16 | 8–16 | Thirty-day complete-bundle choice exists; implementation grant and host storage proof do not |
| Work package 2B-3 execution support | 8–16 | 8–16 | Offline design proposal merged earlier; executor implementation still awaits authority |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Private labels, source/allowance, development result and later holdout freeze remain |
| Selected-host capability proof (R4 tool-path and R5 execution-profile isolation) | 12–24 | 12–24 | Disposable-host direction exists, but no named/provisioned host proof |
| Work package 2B-4 | 12–24 | 12–24 | Limited live suite follows calibration and host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 12–24 | **8–16** | #123 delivered the bounded synthetic falsifiers; real source, freshness, host, evidence and billing proofs still need separate authority. This is a scope-based residual estimate, not extrapolation from its short wall interval |
| Control-plane work package 004 | 8–16 | 8–16 | No selected delivery target; package 003 remains prerequisite |
| Issue #101 package 2 | 6–12 | **0** | #124 merged its approved manual Aegis-only Windows scope; helper and other-host work remains separate |
| Issue #101 package 4 | 8–16 | 8–16 | Comparative evaluation needs selected host, inputs and execution authority |
| Issue #101 package 7 | 6–12 | 6–12 | End-to-end release review follows integration selection |
| Repository-wide documentation readability | 80–200 | 80–200 | #122 and #126 improved five guides. The original #117 inventory had 491 tracked Markdown files; this #126 tree has 501. #119, #127 and #128 are unmerged. Broad range retained pending larger audited coverage |
| **Selected remaining total** | **185–414** | **175–394** | Closed package 2's 6–12 hours and reduced package 003 by 4–8 hours; all other rows reconsidered |

The following optional rows were also reconsidered. Their ranges do not enter
the selected total until the owner chooses their scope and quantity.

| Optional open work item | Previous active hours if selected | New active hours if selected | Current gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner backlog item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision pending |
| Behavioral Eval Runner backlog item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count unselected |
| Behavioral Eval Runner backlog item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count unselected |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Separate architecture and adoption decisions |

If both issue #101 helpers are selected, the bounded selected-plus-both total
is **191–434 active hours**, down from **201–454**. The all-options backlog
still has **no finite total ETA** because optional host/product counts and
architecture choices remain open. These are active-work ranges; owner waits,
GitHub queues, provider runs and host provisioning are excluded. Start the
next five-merge counter after #126. Update earlier if a decision or audited
completion materially changes scope.

## Five-merge checkpoint — 2026-09-23, after pull request #130

Five requests merged after #126, in merge order. The intervals below are wall
time from the first recorded checkpoint, include overlapping review and queue
time, and are not measured active labor. Four requests had all exact-head
GitHub Actions green. PR #119 had Linux and Windows green; its protected-file
guard remained failed under the owner's explicit, PR-only exception, now
recorded as consumed in [APR-010 and APR-011](../approvals/APPROVAL_REGISTER.md).

| Merged request | Merge commit | Observed wall interval | Delivered |
| --- | --- | ---: | --- |
| [#127](https://github.com/ModernNomad-98/Project-Aegis/pull/127) | `fe7d1f247ffef0301b225e0c899d7678d4c0e040` | About 14m35s | Skill-generation standard guide |
| [#128](https://github.com/ModernNomad-98/Project-Aegis/pull/128) | `ecfa4114545e7b719eece88134c6fbc9aea7e1f2` | At least 13m23s | Skills-catalog navigation and representative entries |
| [#119](https://github.com/ModernNomad-98/Project-Aegis/pull/119) | `d2053b61fa80738d9dd2c669980652914bb5c872` | About 1h6m03s | Behavioral Eval Runner and control-plane component guides |
| [#129](https://github.com/ModernNomad-98/Project-Aegis/pull/129) | `ddbe7b02fdf5e93c2133296d22acf875f1762a4b` | 14m41s | Previous every-item forecast |
| [#130](https://github.com/ModernNomad-98/Project-Aegis/pull/130) | `2badb39a76e2445e666ca320bef43591b5b6fad2` | 5m38s | Consumed #119 exception record |

Each open row was reviewed against those delivered scopes and the observed
durations. The documentation inventory is 503 tracked Markdown files at this
checkpoint, compared with 491 at the original inventory and 501 after #126.
The catalog batch reviewed navigation and representative entries; it did not
review every skill entry. PR #131's later evidence-policy proposal is a scope
proposal within the existing policy row, not another implementation row.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Semantic and owner label review remain |
| Behavioral Eval Runner backlog item 009 evidence policy enforcement | 8–16 | 8–16 | The selected policy still needs an implementation grant and evidence |
| Work package 2B-3 execution support | 8–16 | 8–16 | Executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, source, allowance, results and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | No named host or completed isolation proof |
| Work package 2B-4 | 12–24 | 12–24 | Calibration and host prerequisites remain |
| Work package 2B-5 | 8–16 | 8–16 | Corpus execution remains |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and prerequisite proof remain |
| Issue #101 package 4 | 8–16 | 8–16 | Host integration and comparative evaluation remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release review remains |
| Repository-wide documentation readability | 80–200 | 80–200 | More guides are readable, but most of the 503-page inventory still needs review |
| **Selected remaining total** | **175–394** | **175–394** | No additional implementation row closed; non-documentation subtotal is 95–194 |

The optional rows were also re-estimated. Their ranges do not enter the
selected total until the owner chooses their scope and quantity.

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

Selecting both issue #101 helpers would make the bounded selected-plus-both
total **191–434 active hours**. The all-options backlog has
**no finite total ETA** until optional quantities and architecture are chosen.
These are active-work estimates; owner decisions, GitHub queues, provider runs
and host provisioning are excluded. Start the next five-merge counter after
#130 and revise sooner if an audited completion changes scope.

## Five-merge checkpoint — 2026-09-23, after pull request #135

Five requests merged after #130, in merge order. All three exact-head GitHub
Actions passed for each, and each had an independent read-only audit. Their
intervals overlap and include review and queue time; active-only effort was
not separately measured. PR #131 proposed a bounded policy proof; #134
recorded the owner's grant, effective on its merge. Neither delivers the
implementation. The source tree at this checkpoint tracks **506 Markdown
files**, compared with 503 after #130 and 491 in the original inventory.

| Merged request | Merge commit | Observed wall interval | Delivered |
| --- | --- | ---: | --- |
| [#131](https://github.com/ModernNomad-98/Project-Aegis/pull/131) | `e783f0f772700d30e203390b31e56c25187a1bc6` | 12m24s | Bounded Behavioral Eval Runner evidence-policy proposal |
| [#132](https://github.com/ModernNomad-98/Project-Aegis/pull/132) | `f259fc9e0c3b9717a477c9208183d8c0aaefcc09` | 7m16s | Previous five-merge forecast |
| [#133](https://github.com/ModernNomad-98/Project-Aegis/pull/133) | `524e82e809f7f03f3f170bf28d713ddf59d93ef3` | 10m00s | Scenario A runbook and navigation |
| [#134](https://github.com/ModernNomad-98/Project-Aegis/pull/134) | `7e8f0c1067ee0a2e963520bf735a4b7b907a991f` | 10m03s | Owner-approved offline evidence-policy work package 2B-1B |
| [#135](https://github.com/ModernNomad-98/Project-Aegis/pull/135) | `1c2d1a647b5a9e937467396a8aea831cb296ea0e` | 11m25s | Root README routing and documentation batch ledger |

Every selected row was reconsidered. PR #133 and #135 make bounded pages
readable, but they do not close the remaining repository-wide sweep. The
policy work package starts at #134's merge commit and remains in progress;
its eight-hour first-increment cap belongs within the existing 8–16-hour
evidence-policy row. GitHub issue #101 was reopened after package 3 had
closed the whole issue prematurely; packages 4 and 7 remain open in both the
issue and this estimate.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Semantic and owner label review remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | Offline proof is authorized but not delivered; real-host and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, source, allowance, results and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | No named host or completed isolation proof |
| Work package 2B-4 | 12–24 | 12–24 | Calibration and host prerequisites remain |
| Work package 2B-5 | 8–16 | 8–16 | Corpus execution remains |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and prerequisite proof remain |
| Issue #101 package 4 | 8–16 | 8–16 | Selected-host integration and comparative evaluation remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release review remains |
| Repository-wide documentation readability | 80–200 | 80–200 | More pages are reviewed, but the full 506-page inventory remains open |
| **Selected remaining total** | **175–394** | **175–394** | No selected implementation row closed; non-documentation subtotal remains 95–194 |

Optional work was also reconsidered. [Strategic skill expansion and framework
coverage](product-agnostic-skill-and-agent-roadmap.md) is now visible as an
optional backlog row. The [current catalog](../skills-catalog.md) and demand
evidence must define a bounded candidate batch before it receives an ETA;
subtracting the present skill count from an aspirational roadmap target would
invent work that has not been selected.

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Previously unlisted | Unbounded until a candidate batch is selected | Demand, coverage and explicit package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

The selected total remains **175–394 active hours**; selecting both optional
issue #101 helpers would make the bounded total **191–434 active hours**. The
all-options backlog still has **no finite ETA** because optional host and
product quantities, strategic expansion and later architecture are undecided.
Owner waits, GitHub queues, provider runs and host provisioning are excluded.
Start the next five-merge counter after #135 and revise sooner if a completed
audited implementation materially changes scope.

## Five-merge checkpoint — 2026-09-23, after pull request #141

Five requests merged after #135, in the order below. Each received an
independent review and passed all three GitHub Actions on its final revision.
The [execution measurement record](aegis-execution-metrics.md#checkpoint-after-pull-request-141--2026-09-23)
compares each package's estimate with its observed interval. Times in this
snapshot use Coordinated Universal Time (UTC). The source tree reviewed and
merged for #141 contains **509 tracked Markdown files**, compared with 506
after #135 and 491 in the original inventory. This checkpoint edits two
existing records and adds no new Markdown file.

| Merged pull request | Merge commit | GitHub merge event (`mergedAt`, UTC) | Observed wall interval | Delivered |
| --- | --- | --- | ---: | --- |
| [#136](https://github.com/ModernNomad-98/Project-Aegis/pull/136) | `50ac170dad99aa826fc8707431ab21403dfce858` | 17:51:29 | About 6m29s | Issue #101's agreed local evaluation shortlist recorded in its roadmap |
| [#137](https://github.com/ModernNomad-98/Project-Aegis/pull/137) | `df64f776312cf2ae8f980ef1e5c81d74eb8a7cb9` | 17:56:56 | About 7m56s | Previous five-merge forecast |
| [#138](https://github.com/ModernNomad-98/Project-Aegis/pull/138) | `41058f6f4f8a767da4495c42559472f7fa868ed9` | 18:11:25 | 13m06s | Offline setup routing guide, example and navigation |
| [#140](https://github.com/ModernNomad-98/Project-Aegis/pull/140) | `1a2469ec6ec0e318c656102bec1c3fe513375cd2` | 18:24:35 | 13m38s | Three user guides corrected against their skill contracts |
| [#141](https://github.com/ModernNomad-98/Project-Aegis/pull/141) | `9427bf57f7ef3e9fe585fa8cf108e601d6633335` | 18:36:31 | 10m55s | Setup routing plan reconciled with delivered packages 2 and 3 |

The merge times above are GitHub pull-request `mergedAt` events, which can
differ by one second from the merge commit object's timestamp. The starts for
#136 and #137 were recorded only to the minute, so their
intervals are approximate. These intervals overlap, include review and
continuous integration, and do not measure active labor. Pull request #138
needed a Developer Certificate of Origin (DCO) sign-off correction before
its final green checks; that rework is included in its interval. Review,
queue and rework time cannot be separated reliably from the captured data.
Short documentation intervals do not establish implementation throughput or
the time needed to review every remaining page.

At this checkpoint, [pull request #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
is still open at `8928383f0838e2d99ee3a89c44b98b7aba7f1c9b`.
Its offline evidence-policy candidate has passed local checks, independent
adversarial review, and Linux and Windows Actions. The protected-file
`gate-guard` check failed and a request-specific owner disposition remains
pending. Its implementation is therefore not counted as merged delivery.
The separate [approved offline grant](../approvals/APPROVAL_REGISTER.md#aegis-apr-012-offline-behavioral-eval-runner-evidence-policy-proof)
does not grant that exception or real-host operation. Its eight-hour cap
remains inside the existing evidence-policy estimate, not an additional row.

Every selected row was reconsidered against the five merged requests and the
remaining gates. No implementation row closed in this window. The
[documentation batch ledger](aegis-documentation-readability-backlog.md#documentation-batches)
records bounded page progress; it does not establish full inventory coverage.
Issue #101 packages 2 and 3 remain delivered within their approved offline
scopes; the new plan explanation does not deliver packages 4 through 7.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | No new semantic or owner label approval is evidenced by these merges |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | Offline candidate #139 remains open; real-host storage proof and operator controls also remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | The offline executor proposal still needs its implementation grant and code |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed execution source and allowance, development results and a later holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | A named host and measured tool-path and execution-profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution still depends on calibration and host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | The synthetic increment already shipped; real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | A delivery target and package-003 prerequisite proof remain |
| Issue #101 package 4 | 8–16 | 8–16 | #136 records the agreed shortlist and #141 clarifies the plan; pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | End-to-end release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Three further readability batches improved bounded pages; most of the 509-file inventory still needs recorded review |
| **Selected remaining total** | **175–394** | **175–394** | The non-documentation subtotal remains 95–194; the documentation estimate remains 80–200 |

Every optional row was also reconsidered. No merge in this window selected
either helper, additional hosts or products, a strategic skill batch, or a
later architecture. The [strategic roadmap](product-agnostic-skill-and-agent-roadmap.md)
and [skills catalog](../skills-catalog.md) remain inputs to selecting a bounded
expansion package; an aspirational target does not define its effort.

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and explicit package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

The selected total remains **175–394 active hours**. Selecting both optional
issue #101 helpers adds **16–40 hours**, for a bounded conditional total of
**191–434 active hours**. The full all-options backlog has **no finite
estimate** while optional quantities and strategic or architecture choices
remain unbounded. Owner waits, GitHub queues, provider runs and host
provisioning remain excluded. Start the next five-merge counter after #141;
revisit sooner if an audited implementation or owner decision changes the
remaining scope materially.

## Five-merge checkpoint — 2026-09-23, after pull request #146

This is the fifth merge after #141. The five requests below passed independent
review and all three exact-head GitHub Actions before merge. Pull request (PR)
numbers are not merge order. Times are GitHub `mergedAt` events in Coordinated
Universal Time (UTC); durations start at the first recorded work checkpoint.
They overlap and include review, queue time, and rework. Active-only labor was
not instrumented, so the intervals are not an implementation rate.

| Merge order and delivered scope | Original bounded estimate | Merge event (UTC) | Observed start-to-merge wall | Merge commit |
| --- | ---: | --- | ---: | --- |
| [#142](https://github.com/ModernNomad-98/Project-Aegis/pull/142): historical skill category maps 08–09 | 1–3 active hours | 18:44:39 | 15m47s | `4ed081818f6456b4d2763a3f1cc1c6bd45c0e740` |
| [#143](https://github.com/ModernNomad-98/Project-Aegis/pull/143): prior five-merge forecast | 1–2 active hours | 18:52:10 | 24m50s from first preparation; 14m41s from editing start | `7e5a429b6e4cd3e96a694be0342bab81f9442c13` |
| [#144](https://github.com/ModernNomad-98/Project-Aegis/pull/144): historical skill category maps 01–07 | 2–4 active hours, revised from 1–3 | 18:55:43 | 16m44s | `adcef2b97a34c018da76c6b7cae673e62a2365cd` |
| [#145](https://github.com/ModernNomad-98/Project-Aegis/pull/145): current control-plane backlog guide | 2–4 active hours | 19:04:34 | About 8m34s; start recorded only as about 18:56 | `cf63696527400d5119ff39e37b2c5e35f0006c68` |
| [#146](https://github.com/ModernNomad-98/Project-Aegis/pull/146): current owner-decision index | 1–3 active hours | 19:11:10 | 14m16s | `831dd75a5f43463b032e162160b0348299d3c6c1` |

Nine historical category maps now explain that their 300 numbered entries are
planning candidates. The control-plane register and owner-decision index now
show current delivery and remaining gates first. These are bounded page fixes;
they close no selected implementation row or the repository-wide documentation
sweep. The merged tree contains **513 tracked Markdown files**, versus 509 at
the #141 checkpoint. The individual PR bodies and timing comments record
their prior estimates, checks, audit findings and corrections.

[PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139) remains
open at this checkpoint with its protected-file guard failure. Its offline
evidence-policy implementation is not counted as merged delivery. The
30-day policy choice and synthetic grant do not establish real-host controls.
No new label approval, selected host, provider authority, or optional product
scope was established by this five-merge interval.

Every selected row was re-estimated from delivered scope and remaining gates.
The short, overlapping documentation intervals do not support a reduction to
the broad 80–200-hour sweep or to runtime work. The full inventory still needs
recorded review.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Semantic review and owner-approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 is open; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, source, allowance, results and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path and execution-profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Calibration and selected-host proof remain prerequisites |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus work follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Selected target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Host, cases, budget, authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows chosen integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Bounded pages improved; most of the 513-file inventory remains unreviewed |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation: **95–194**; documentation: **80–200** |

Every optional row was also re-estimated. No optional quantity or product was
selected. The two helper ranges are additive only if both are later selected.

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

The selected total stays **175–394 active hours**. Selecting both issue #101
helpers would add **16–40 hours**, for **191–434 active hours**. The full
all-options backlog has no finite estimate while optional quantities and
strategic choices are unset. Owner waits, GitHub queues, provider execution
and host provisioning are outside the active-hour ranges. Restart the
five-merge counter after #146; revise sooner if verified scope changes.

## Five-merge checkpoint — 2026-09-23, after pull request #151

Five requests merged after #146, in the order below. Each passed independent
review and all three GitHub Actions on its final revision. Merge times use
the GitHub pull-request event field, `mergedAt`, in Coordinated Universal
Time (UTC). Pull request numbers do not determine merge order.

| Merged pull request and delivered scope | Bounded estimate | Merge event (UTC) | Observed wall interval | Merge commit |
| --- | ---: | --- | ---: | --- |
| [#148](https://github.com/ModernNomad-98/Project-Aegis/pull/148): previous five-merge forecast | 1–2 active hours | 19:21:11 | 15m12s from first preparation | `bc8993f6ea0d4aeb764cef70ca674b0a0eb373d4` |
| [#147](https://github.com/ModernNomad-98/Project-Aegis/pull/147): current Behavioral Eval Runner backlog guide | 2–4 active hours | 19:21:59 | 16m32s | `4b083b4b36d9d6cb7ad993baec9bc84e0a5f4891` |
| [#149](https://github.com/ModernNomad-98/Project-Aegis/pull/149): current reading route for the historical handoff | 1–3 active hours | 19:29:36 | 11m03s | `70ca4eef13521d27c11754979b2bfb90ce3981c5` |
| [#150](https://github.com/ModernNomad-98/Project-Aegis/pull/150): current control-plane design entry point | 2–4 active hours | 19:36:02 | About 18m02s | `8ba005fcade464f350facc5ec3544e636fad248d` |
| [#151](https://github.com/ModernNomad-98/Project-Aegis/pull/151): current forecast navigation | 1–3 active hours | 19:42:13 | 16m09s | `3ba17903033ffd1cefc30f4b61857cc36ef1f0e6` |

The intervals overlap and include review, integration and checks. The #148
interval begins with preparation that ran alongside other work; #150's start
was recorded only as about 19:18 UTC. Active effort and waiting were not
separately measured. The [measurement record](aegis-execution-metrics.md#checkpoint-after-pull-request-151--2026-09-23)
preserves the starts, previous estimates and measurement limits.

Four bounded readability batches now direct readers to current status while
preserving historical contracts and evidence. The source tree merged for
#151 contains **517 tracked Markdown files**, compared with 513 after #146
and 491 in the original inventory. The four added files are dated batch
records; the inventory count is not a count of defects or completed reviews.
The full [documentation sweep](aegis-documentation-readability-backlog.md)
remains open, including individual skill contracts and other unreconciled
pages. The short intervals for these entry-point changes do not establish a
review rate for that broader work.

[Pull request #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
remains open at this checkpoint, at
`8928383f0838e2d99ee3a89c44b98b7aba7f1c9b`. Its Linux and Windows
Actions passed, but the protected-file guard failed and its separate owner
disposition remains pending. The offline evidence-policy candidate is not
counted as merged delivery. The five merged documentation requests grant no
new label approval, execution source, provider allowance, host authority or
optional adoption.

Every selected row was reconsidered against the delivered scope and its
remaining gates. No selected implementation row closed in this window.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Semantic review and owner-approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 remains open; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed source and allowance, development results and later holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path and execution-profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution still depends on calibration and selected-host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | #150 clarifies the delivered synthetic increment; real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | A selected delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Four bounded pages improved; most of the 517-file inventory still needs recorded review |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation remains **95–194**; documentation remains **80–200** |

All seven optional rows were also reconsidered. No optional package or
quantity was selected by these requests. [Strategic expansion](product-agnostic-skill-and-agent-roadmap.md)
still requires a bounded candidate batch informed by the
[current skills catalog](../skills-catalog.md).

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

The selected total remains **175–394 active hours**. Selecting both optional
issue #101 helpers adds **16–40 hours**, giving **191–434 active hours**.
The full all-options backlog has no finite estimate while optional quantities
and strategic or architecture choices remain unbounded. Owner waits, GitHub
queues, provider execution and host provisioning are outside the active-hour
ranges. Restart the five-merge counter after #151, and revise sooner if
verified delivery or an owner decision materially changes the remaining scope.

## Five-merge checkpoint — 2026-09-23, after pull request #156

Five requests merged after #151, in the order below. All five final revisions
passed the Linux, Windows and protected-file GitHub Actions checks. The merge
clock is GitHub's pull-request `mergedAt` event in Coordinated Universal
Time (UTC). Duration notation uses **m** for minutes and **s** for seconds.

| Merged pull request and delivered scope | Bounded estimate | Merge event (UTC) | Observed wall interval | Merge commit |
| --- | ---: | --- | ---: | --- |
| [#152](https://github.com/ModernNomad-98/Project-Aegis/pull/152): first 20-page skill screen, two corrected guides | 2–4 active hours | 19:49:02 | 17m38s | `4343d8c6322f974b2eb62c1d5b1529d85d6a9c7d` |
| [#153](https://github.com/ModernNomad-98/Project-Aegis/pull/153): previous five-merge forecast | 1–2 active hours | 19:53:58 | 15m01s from first preparation | `4aed9750cee00897eb3d989345dce4d910b1bb17` |
| [#154](https://github.com/ModernNomad-98/Project-Aegis/pull/154): second 20-page skill screen, two corrected cloud guides | 2–4 active hours | 19:57:41 | 23m16s | `e900a0455c5ee3bb138b9292a6bcb71cbdfe7be8` |
| [#155](https://github.com/ModernNomad-98/Project-Aegis/pull/155): third 20-page skill screen, three corrected guides | 2–4 active hours | 20:07:31 | 22m53s | `89dbc757d6a257c917b099f402e5c2c2f062e939` |
| [#156](https://github.com/ModernNomad-98/Project-Aegis/pull/156): fifth 20-page skill screen, four corrected guides | 2–4 active hours | 20:09:10 | 11m40s | `75cd7c5d628c11fc6ab8eb72674e25bebbfa68a2` |

The intervals overlap and include review, integration and checks. Active
effort, waiting and rework were not separately instrumented. The
[measurement record](aegis-execution-metrics.md#checkpoint-after-pull-request-156--2026-09-23)
records the starts, previous estimates and source limitations. These wall
intervals cannot be added as active labor or used as an implementation rate.

The four merged skill batches screened **80 entrypoints** for terminology and
output clarity and corrected **11 skill pages**. Their coverage is batches
1, 2, 3 and 5. Batch 4 is outside this checkpoint; the fifth batch's name
does not establish completion of the first 100 pages. The
[first](../evidence/documentation/skill-docs-first-20-readability-2026-09-23.md),
[second](../evidence/documentation/cloud-skill-readability-2026-09-23.md),
[third](../evidence/documentation/skill-docs-third-20-readability-2026-09-23.md)
and [fifth](../evidence/documentation/skill-docs-fifth-20-readability-2026-09-23.md)
batch records bound these claims. The fifth batch's shared documentation
ledger row remains a separate integration task at this checkpoint.

The exact #156 merge tree contains **521 tracked Markdown files**, compared
with 517 after #151 and 491 in the original inventory. The four additional
files are dated batch records. These entrypoint screens do not complete the
supporting references or every acceptance criterion in the
[documentation sweep](aegis-documentation-readability-backlog.md).
The remaining review depth and rewrite volume are still uncertain, so the
documentation range stays broad at **80–200 active hours**.

[Pull request #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
remains open at `8928383f0838e2d99ee3a89c44b98b7aba7f1c9b`:
Linux and Windows checks passed, but the protected-file guard failed and the
separate owner disposition remains pending. No unmerged policy work is
counted as delivered. These five merges changed no runtime, implementation
grant, private-label decision, selected host or provider authority.

Every selected row was reconsidered. Documentation screening advanced, but
no selected implementation row closed and the wider sweep remains open.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Semantic review and owner-approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 remains open; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed source and allowance, development results and later holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path and execution-profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution still depends on calibration and selected-host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | A selected delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Four bounded skill screens advanced; supporting references and full acceptance coverage remain open |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation remains **95–194**; documentation remains **80–200** |

All seven optional rows were also reconsidered. No optional package or
quantity was selected. [Strategic expansion](product-agnostic-skill-and-agent-roadmap.md)
still needs a bounded candidate batch informed by the
[current skills catalog](../skills-catalog.md).

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

The selected total remains **175–394 active hours**. Selecting both optional
issue #101 helpers adds **16–40 hours**, giving **191–434 active hours**.
The full all-options backlog has no finite estimate while optional quantities
and strategic or architecture choices remain unbounded. Owner waits, GitHub
queues, provider execution and host provisioning are outside the active-hour
ranges. Restart the five-merge counter after #156, and revise sooner if
verified delivery or an owner decision materially changes remaining scope.

## Five-merge checkpoint — 2026-09-23, after pull request #160

Five requests merged after #156, in the order below. All five final revisions
passed the Linux, Windows and protected-file GitHub Actions checks. The merge
clock is GitHub's pull-request `mergedAt` event in Coordinated Universal
Time (UTC). Duration notation uses **m** for minutes and **s** for seconds.

| Merged pull request and delivered scope | Bounded estimate | Merge event (UTC) | Observed wall interval | Merge commit |
| --- | ---: | --- | ---: | --- |
| [#162](https://github.com/ModernNomad-98/Project-Aegis/pull/162): previous five-merge forecast | 1–2 active hours | 20:23:21 | 13m10s from first preparation | `1182041071feb39dc2be8cff40dd6a9ee6571cf6` |
| [#157](https://github.com/ModernNomad-98/Project-Aegis/pull/157): fourth 20-page skill screen, three corrected guides | 2–4 active hours | 20:25:05 | 33m02s | `e2a2e73bb03c231fdf1d20f63ef9e54ee9fdc985` |
| [#158](https://github.com/ModernNomad-98/Project-Aegis/pull/158): sixth 20-page skill screen, three corrected guides | 2–4 active hours | 20:26:31 | 25m55s | `f5373fa47b73f9aeb8de34670140202aac22e8aa` |
| [#159](https://github.com/ModernNomad-98/Project-Aegis/pull/159): seventh 20-page skill screen, four corrected guides | 2–4 active hours | 20:32:16 | 28m48s | `6c820732def6743a0d45a935641f53db07cf2db2` |
| [#160](https://github.com/ModernNomad-98/Project-Aegis/pull/160): eighth 20-page skill screen, four corrected guides | 2–4 active hours | 20:33:17 | 26m20s | `770c49ef875dfbcac63c3f3bb596bc694f5d536e` |

The [measurement record](aegis-execution-metrics.md#checkpoint-after-pull-request-160--2026-09-23)
records the starts and previous estimates. These overlapping wall intervals
include review, integration and checks; active effort, waiting and rework
were not separately instrumented. They cannot be added as active labor or
used as a full-documentation review rate.

This interval delivered **four 20-page entrypoint screens and 14 corrected
skill pages**: batches 4, 6, 7 and 8. Their
[fourth](../evidence/documentation/skill-docs-fourth-20-readability-2026-09-23.md),
[sixth](../evidence/documentation/skill-docs-sixth-20-readability-2026-09-23.md),
[seventh](../evidence/documentation/skill-docs-seventh-20-readability-2026-09-23.md)
and [eighth](../evidence/documentation/skill-docs-eighth-20-readability-2026-09-23.md)
batch records describe the bounded findings and preserved contracts. Together
with the previous checkpoint, batches 1–8 screened **160 entrypoints** and
corrected **25 skill pages**. Screening for terminology and output clarity
does not establish every page's full acceptance. Shared documentation-ledger
rows for batches 5–8 remain to be integrated at this checkpoint.

The exact #160 merge tree contains **525 tracked Markdown files**, compared
with 521 after #156 and 491 in the original inventory. The four new files
are dated batch records. Supporting references, remaining entrypoints and
the broader [documentation acceptance criteria](aegis-documentation-readability-backlog.md#acceptance-for-each-page)
remain open. The remaining review depth and rewrite volume are uncertain;
the documentation range therefore stays **80–200 active hours**.

[Pull request #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
remained open at `8928383f0838e2d99ee3a89c44b98b7aba7f1c9b` when checked at
20:37:49 UTC: Linux and Windows passed, while the protected-file guard failed
and the separate owner disposition remained pending. Pull requests #161,
#163, #164 and #165 were also unmerged at that observation and are excluded
from this checkpoint's delivery claims. These five merges changed no runtime,
implementation grant, private-label decision, selected host or provider
authority.

Every selected row was reconsidered. No selected implementation row closed,
and the bounded documentation progress does not close the wider sweep.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Semantic review and owner-approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 remains open; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed source and allowance, development results and later holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path and execution-profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution still depends on calibration and selected-host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | A selected delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Four more bounded screens advanced; supporting references, ledger integration and full acceptance remain open |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation remains **95–194**; documentation remains **80–200** |

All seven optional rows were reconsidered. No optional package or quantity
was selected by these merges. [Strategic expansion](product-agnostic-skill-and-agent-roadmap.md)
still needs a bounded candidate batch informed by the
[current skills catalog](../skills-catalog.md).

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

The selected total remains **175–394 active hours**. Selecting both optional
issue #101 helpers adds **16–40 hours**, giving **191–434 active hours**.
The full all-options backlog has no finite estimate while optional quantities
and strategic or architecture choices remain unbounded. Owner waits, GitHub
queues, provider execution and host provisioning are outside the active-hour
ranges. Restart the five-merge counter after #160, and revise sooner if
verified delivery or an owner decision materially changes remaining scope.

## Five-merge checkpoint — 2026-09-23, after pull request #164

Five requests merged after #160, in the order below. All five final revisions
passed the Linux, Windows and protected-file GitHub Actions checks. The merge
clock is GitHub's pull-request `mergedAt` event in Coordinated Universal
Time (UTC). Duration notation uses **m** for minutes and **s** for seconds.

| Merged pull request and delivered scope | Bounded estimate | Merge event (UTC) | Observed wall interval | Merge commit |
| --- | ---: | --- | ---: | --- |
| [#170](https://github.com/ModernNomad-98/Project-Aegis/pull/170): previous five-merge forecast | 1–2 active hours | 20:46:46 | 9m50s from first preparation | `00ff28110b73eec149810566a2c23319df5fc079` |
| [#165](https://github.com/ModernNomad-98/Project-Aegis/pull/165): revert and live-incident routing correction | 1–3 active hours | 20:47:57 | 19m31s | `cf2240417c24a07b90cd59e7c4f27614f9541c47` |
| [#161](https://github.com/ModernNomad-98/Project-Aegis/pull/161): final 26-path skill screen, three corrected guides | 2–4 active hours | 20:48:39 | 41m18s | `206850cadab3119dce0fd0a0add094a947e3d9d3` |
| [#163](https://github.com/ModernNomad-98/Project-Aegis/pull/163): first reference batch, three corrected pages | 2–4 active hours | 20:49:42 | 35m18s | `ce24fb174d4a25095e4821b8f670e4b2ce510d4f` |
| [#164](https://github.com/ModernNomad-98/Project-Aegis/pull/164): second reference batch, four corrected pages | 2–4 active hours | 20:50:33 | 36m06s | `2ad75c6d1dcef92fa03c793934354a83463aa114` |

The [measurement record](aegis-execution-metrics.md#checkpoint-after-pull-request-164--2026-09-23)
records the starts and previous estimates. These overlapping wall intervals
include review, integration and checks; active effort, waiting and rework
were not separately instrumented. They cannot be added as active labor or
used as a full-documentation review rate.

The [final entrypoint screen](../evidence/documentation/skill-docs-final-screen-readability-2026-09-23.md)
adds **26 paths and three corrected guides**. Together with the eight earlier
batches, the sorted pass covered **186 `SKILL.md` paths and corrected 28
entrypoint pages**. The path count comprises **185 shipped skills plus the
authoring template**, `.claude/skills/_template/SKILL.md`; the validator
excludes that template. These are bounded terminology and output screens,
not evidence that every page meets the full readability acceptance criteria.

Separately, the [owning-skill correction](../evidence/documentation/governance-poisoning-routing-correction-2026-09-23.md)
updates two skill instructions and one behavior-evaluation assertion. It
corrects misleading revert mechanics and live-incident routing without
performing either operation. The
[first](../evidence/documentation/skill-references-first-20-readability-2026-09-23.md)
and [second](../evidence/documentation/skill-references-second-20-readability-2026-09-23.md)
reference batches correct **seven reference pages**. Supporting references
and full page acceptance still require work. Shared documentation-ledger
integration for entrypoint batches 5 through the final screen, the reference
batches and the owning-skill correction remains pending at this checkpoint.

The exact #164 merge tree contains **529 tracked Markdown files**, compared
with 525 after #160 and 491 in the original inventory. Four new dated
evidence records account for this interval's increase. The broader
[documentation acceptance criteria](aegis-documentation-readability-backlog.md#acceptance-for-each-page)
remain open, and the remaining review depth and rewrite volume are uncertain.
The documentation range therefore stays **80–200 active hours**.

[Pull request #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
remained open at `8928383f0838e2d99ee3a89c44b98b7aba7f1c9b` during this
checkpoint's read-only verification: Linux and Windows passed, while the
protected-file guard failed and the separate owner disposition remained
pending. No unmerged policy work or later pull request is counted as delivered
here. These five merges changed no runtime, implementation grant, private-label
decision, selected host or provider authority.

Every selected row was reconsidered. No selected implementation row closed,
and the bounded documentation progress does not close the wider sweep.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Semantic review and owner-approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 remains open; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed source and allowance, development results and later holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path and execution-profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution still depends on calibration and selected-host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | A selected delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Final entrypoint screen, seven reference corrections and two owning-skill corrections advanced; full acceptance and ledger integration remain open |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation remains **95–194**; documentation remains **80–200** |

All seven optional rows were reconsidered. No optional package or quantity
was selected by these merges. [Strategic expansion](product-agnostic-skill-and-agent-roadmap.md)
still needs a bounded candidate batch informed by the
[current skills catalog](../skills-catalog.md).

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

The selected total remains **175–394 active hours**. Selecting both optional
issue #101 helpers adds **16–40 hours**, giving **191–434 active hours**.
The full all-options backlog has no finite estimate while optional quantities
and strategic or architecture choices remain unbounded. Owner waits, GitHub
queues, provider execution and host provisioning are outside the active-hour
ranges. Restart the five-merge counter after #164, and revise sooner if
verified delivery or an owner decision materially changes remaining scope.

## Five-merge checkpoint — 2026-09-23, after pull request #169

Five requests merged after #164, in the order below. All five final revisions
passed the Linux, Windows and protected-file GitHub Actions checks. The merge
clock is GitHub's pull-request `mergedAt` event in Coordinated Universal
Time (UTC). Duration notation uses **m** for minutes and **s** for seconds.

| Merged pull request and delivered scope | Bounded estimate | Merge event (UTC) | Observed wall interval | Merge commit |
| --- | ---: | --- | ---: | --- |
| [#174](https://github.com/ModernNomad-98/Project-Aegis/pull/174): previous five-merge forecast | 1–2 active hours | 21:01:09 | 9m41s from first preparation | `29a44b2b7e1599f41873971e14eacd15f169d258` |
| [#166](https://github.com/ModernNomad-98/Project-Aegis/pull/166): third reference batch, three corrected pages | 2–4 active hours | 21:02:08 | 40m27s | `c3e520941856b5c7d0789d155192db154491c64e` |
| [#167](https://github.com/ModernNomad-98/Project-Aegis/pull/167): fourth reference batch, four corrected pages | 2–4 active hours | 21:03:14 | 41m20s | `8f0383b6bdaaac7b284e6b3909971dc58d6840b1` |
| [#168](https://github.com/ModernNomad-98/Project-Aegis/pull/168): fifth reference screen, first ten-page half | 1–3 active hours for this half | 21:04:15 | 36m20s | `d40da6eccc94330350eb9ea3271863959ceb1d19` |
| [#169](https://github.com/ModernNomad-98/Project-Aegis/pull/169): fifth reference screen, second ten-page half | 1–3 active hours for this half | 21:05:02 | 37m01s | `37c018d166f0647703b4a0f7009ae0ca4c5e32b0` |

The [measurement record](aegis-execution-metrics.md#checkpoint-after-pull-request-169--2026-09-23)
records the starts and previous estimates. For #168 and #169, the previous
**2–4 active hours** applied to the whole screen; each half received its own
**1–3 active-hour** estimate. These scopes must remain distinct. The
overlapping wall intervals include review, integration and checks; active
effort, waiting and rework were not separately instrumented. They cannot be
added as active labor or used as a full-documentation review rate.

This interval corrects **27 reference pages**: three in the
[third batch](../evidence/documentation/skill-references-third-20-readability-2026-09-23.md),
four in the [fourth batch](../evidence/documentation/skill-references-fourth-20-readability-2026-09-23.md),
and ten in each [first half](../evidence/documentation/skill-references-fifth-a-readability-2026-09-23.md)
and [second half](../evidence/documentation/skill-references-fifth-b-readability-2026-09-23.md)
of the fifth screen. Cumulative delivered reference corrections total **34
pages**. The bounded reference screens now reach sorted positions **1–100
of 156**; this does not establish every screened page's full acceptance.
The changes explain terms and navigation and correct misleading abort labels,
incident routing, revert guidance and a percentile sample-size example.
They do not perform the operations described by those reference pages.

The exact #169 merge tree contains **533 tracked Markdown files**, compared
with 529 after #164 and 491 in the original inventory. Four new dated
evidence records account for the increase. The earlier entrypoint pass still
comprises **186 `SKILL.md` paths: 185 shipped skills and one authoring
template**, with 28 entrypoint pages corrected in those screen batches.
The separate owning-skill correction remains recorded in the prior checkpoint.
Shared documentation-ledger integration remains pending. The broader
[documentation acceptance criteria](aegis-documentation-readability-backlog.md#acceptance-for-each-page)
remain open, and the remaining review depth and rewrite volume are uncertain.
The documentation range therefore stays **80–200 active hours**.

At the **21:06:39 UTC** preparation checkpoint, requests #171, #172 and #173
remained open. Their remaining 56-reference screen scope is excluded from
delivered coverage here. Request #175 was also open and is excluded.
[Pull request #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
remained open at `8928383f0838e2d99ee3a89c44b98b7aba7f1c9b`; its documented
protected-file guard failure and separate owner disposition remained pending.
No unmerged policy work or later request is counted as delivered. These five
merges changed no runtime, implementation grant, private-label decision,
selected host or provider authority.

Every selected row was reconsidered. No selected implementation row closed,
and the bounded documentation progress does not close the wider sweep.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Evidence and remaining gate |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Semantic review and owner-approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 remains open; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed source and allowance, development results and later holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path and execution-profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution still depends on calibration and selected-host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | A selected delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | 27 more reference pages corrected; remaining references, ledger integration and full acceptance remain open |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation remains **95–194**; documentation remains **80–200** |

All seven optional rows were reconsidered. No optional package or quantity
was selected by these merges. [Strategic expansion](product-agnostic-skill-and-agent-roadmap.md)
still needs a bounded candidate batch informed by the
[current skills catalog](../skills-catalog.md).

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

The selected total remains **175–394 active hours**. Selecting both optional
issue #101 helpers adds **16–40 hours**, giving **191–434 active hours**.
The full all-options backlog has no finite estimate while optional quantities
and strategic or architecture choices remain unbounded. Owner waits, GitHub
queues, provider execution and host provisioning are outside the active-hour
ranges. Restart the five-merge counter after #169, and revise sooner if
verified delivery or an owner decision materially changes remaining scope.

**Historical baseline — recorded after pull request #106 on September 23,
2026.** The paragraph and baseline tables below preserve estimates and pending
decisions recorded then. They are not current work status or authorization.
Use the checkpoint above for current remaining work. Pull request #104 has
since merged, and issue #101 packages 2 and 3 delivered their approved scopes.

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
