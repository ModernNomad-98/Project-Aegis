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
