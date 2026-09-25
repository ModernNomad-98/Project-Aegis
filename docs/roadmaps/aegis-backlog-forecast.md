# Project Aegis backlog forecast

## Start here — current reading

This is a rolling **active-work estimate**, not a calendar promise or permission
to start blocked work. The [owner's issue #101 host-path choice](#material-owner-decision--2026-09-25-issue-101-host-path)
and the subsequent bounded Stage 4A grant are the latest scope changes. The
[five-merge checkpoint after #278](#five-merge-checkpoint--2026-09-25-after-pull-request-278)
is the latest full reassessment. Pull request (PR) #249 delivered the
synthetic offline holdout-support item; PR #250 closed the bounded
documentation residual. PR #253 added one reviewed reader page; PR #257 added
two more. PR #260 added one reviewed setup page and #269 added a reviewed
Behavioral Eval Runner (BER) source inventory, making **589 pages**: 545
accepted readers and 44
classified fixtures, with zero known pending pages. PR #257 delivered the
bounded offline integration and consumed APR-023. The owner's 2026-09-24
approval of the [bounded BER-BKL-009 synthetic integration](#material-owner-decision--2026-09-24-ber-bkl-009),
made effective by merged PR #255,
supersedes the old 8–16-hour whole-item estimate and therefore the old
87–178-hour selected total. After removing the superseded issue #101 package-4
8–16-hour combined row, current selected work has **71–146 active hours for
ten unaffected rows**, plus unestimated issue #101 Stages 4A and 4B and
BER-BKL-009 host, runtime, privacy and cleanup work. The BER offline package
is delivered. The owner chose
a new disposable Linux virtual machine (VM) with VirtualBox as the R4/R5 Stage A
candidate. Setup began under APR-028 and reached an Ubuntu login, but repeated
graphical stalls led the owner to pause it. The VM was last verified powered
off, with networking disabled and its virtual DVD empty; guest completion
checks and a Stage A host probe remain undone. R4/R5 are the runner's
selected-host capability and full-profile requirements. No finite new selected
or all-options
total is defensible until the unestimated residuals are scoped.
Confidential conduct intake remains a separate owner decision. Also check
the [documentation estimate audit after #205](#documentation-estimate-audit--2026-09-23-after-pull-request-205),
the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-278--2026-09-25)
and [documentation batch ledger](aegis-documentation-readability-backlog.md#documentation-batches)
before treating its totals as current.

## Material owner decision — 2026-09-25, issue #101 host path

The owner selected the [recommended separate software development kit
(SDK) managed Windows
session](aegis-setup-package-4a-host-preparation-proposal.md#selected-candidate-and-package-review-2026-09-25-utc)
for an **offline prototype planning direction**. The question expressly said
that selection did not authorize SDK installation, code, a host session or a
provider call. The owner separately approved bounded offline Stage 4A
implementation on 2026-09-25 under the linked proposal: eleven paths, at most
12 active hours and 1,200 handwritten code/test lines, and $0 external spend.
Stage 4A is a synthetic callback implementation in progress;
Stage 4B is the later actual SDK host proof and comparison. The earlier
8–16-hour whole-package row cannot cover both. Subtracting corresponding
low and high estimates from the #265 eleven-row subtotal leaves ten unchanged
rows: `79 − 8 = 71` and `162 − 16 = 146` active hours. This is a scope split, not completed
work credit. The approved 12-hour Stage 4A implementation limit is a ceiling,
not a remaining-work estimate. Separate estimates require a reviewed lockfile,
Stage 4A design and Stage 4B host execution scope.

| Current selected component | Active-work estimate | Remaining boundary |
| --- | ---: | --- |
| Ten unaffected selected rows from the #265 checkpoint | 71–146 h | Existing dependencies and provisional host uncertainty remain. |
| Issue #101 Stage 4A: offline callback prototype | TBD; approved implementation ceiling 12 h | The bounded offline grant is active; exact lock and package-body review precede any scripts-disabled install. No SDK query, CLI process or real host proof is authorized. |
| Issue #101 Stage 4B: actual host proof and comparison | TBD | Pinned execution scope, callback-consumption proof, telemetry and a separate grant remain. |
| BER-BKL-009 host, runtime, privacy and cleanup residual | TBD | Its separate scope and authority gates remain. |
| **Selected total** | **No finite estimate** | Both issue #101 stages and BER residual remain unestimated. |

Optional issue #101 helpers retain their conditional **16–40 active-hour**
combined range after a successful Stage 4B comparison and separate grants.
The seven optional rows were last fully reassessed in the dated #278
checkpoint below. The paused VirtualBox VM remains outside this SDK route.

## Five-merge checkpoint — 2026-09-25, after pull request #278

The five merges after #270 were #271, #272, #273, #274 and #278. Their
[GitHub merge receipts](aegis-execution-metrics.md#checkpoint-after-pull-request-278--2026-09-25)
span 04:03:07–04:45:08 Coordinated Universal Time (UTC) on 2026-09-25:
**42m01s observed wall time**. Review, continuous integration (CI), owner
waiting and concurrent work are included. Active work was not separately
instrumented, so the interval is not a delivery rate. #271 reviewed static
software development kit (SDK) archives; #272 and #273 improved skill choice
guidance; #274 repaired offline receipt prevalidation; #278 recorded the
consumed #274 protected-guard exception and the owner's bounded Stage 4A grant
as APR-031. None completed a selected implementation row or real-host proof.

The #278 tree has **589 tracked Markdown files**: **545 accepted reader pages**
and **44 classified fixtures**, with zero known pending pages at that merge.
The ten estimated selected rows retain **71–146 active hours** after rechecking
their prerequisites. These five merges supplied no measured duration or evidence
closing their gates. The Stage 4A approval is a **12 active-hour ceiling**, not
its remaining-work estimate. Stage 4B and the BER-BKL-009 host, runtime, privacy
and cleanup residual lack executable scope and estimates. The selected and
all-options totals have no finite estimate. In the table, WP means work package,
OD-1 means owner decision 1, CP means control plane, and BKL means backlog item.
R1/R4/R5 are runner evidence requirements; the [runner backlog](behavioral-eval-runner-backlog.md)
and [control-plane backlog](resumable-control-plane-backlog.md) define their gates.

| Selected remaining work item | Active-work planning range | Gate after #278 |
| --- | ---: | --- |
| WP-2B-3 candidate inputs | 1–4 h | Owner inspection of private 160-case labels, guide and exact hashes. |
| WP-2B-3 measurement and OD-1 | 4–10 h | Label approval, reviewed live source and allowance, host proof, measured result and ratification. |
| Selected-host R4/R5 capability proof | 12–24 h, provisional | VirtualBox VM setup paused; guest checks and separate Stage A grant remain. |
| WP-2B-4 | 12–24 h | Calibration, OD-1, R1/R4/R5 evidence and separate live grant. |
| WP-2B-5 | 8–16 h | WP-2B-4 and separate generic-corpus phase grant. |
| WP-2B-6 | 8–16 h | WP-2B-5 plus scheduling, cost, quarantine and dataset authority. |
| WP-2B-7 | 4–8 h | WP-2B-6 and separate advisory CI/operator grant. |
| CP-WP-003 | 8–16 h, provisional | Real atomic authority, independent freshness, containment, evidence and billing proof. |
| CP-WP-004 | 8–16 h | CP-WP-003 real proof, selected operation and separate grant. |
| Issue #101 package 7 | 6–12 h | Release review depends on package-4 host proof and selected helper integration. |
| **Ten-row planning subtotal** | **71–146 h** | Provisional host uncertainty remains; not a delivery promise. |
| Issue #101 Stage 4A offline bridge | TBD; approved ceiling 12 h | APR-031 permits only bounded synthetic implementation; real SDK/host proof remains outside scope. |
| Issue #101 Stage 4B host proof | TBD | Pinned execution scope and separate grant. |
| BER-BKL-009 host/runtime/privacy/cleanup | TBD | Named host, runtime design and separate authority. |
| Documentation readability | 0 known pending at #278 | Accept newly changed pages after full-page review. |
| **Selected total** | **No finite estimate** | Stage 4A, Stage 4B and BER residual remain unestimated. |

The seven optional rows remain conditional: issue #101 packages 5 and 6 are
**8–20 active hours each** after Stage 4B and separate approvals; BER-BKL-010
is **4–12 hours**; BER-BKL-014 is **8–20 hours per additional host**; and
BER-BKL-015 is **8–24 hours per selected product**. Strategic skill expansion,
multi-judge arbitration and future control-plane architecture remain
unbounded until selected and scoped. The two issue #101 helpers together would
add **16–40 hours** if selected. None makes the all-options total finite.
PRs #279, #280 and #282 subsequently merged choice guidance, the preceding
checkpoint and current decision routes without closing an implementation row.
They start the next five-merge cycle. The VirtualBox VM remains paused.


## Material owner decision — 2026-09-24, BER-BKL-009

The owner answered "Approve this bounded scope" to the exact synthetic-only
[PR #253 proposal](ber-bkl-009-policy-scope-amendment-proposal.md). The
separate BER-DEC-013 and APR-023 governance amendment merged in PR #255 as
`0318b1ecde3ebf5f34bb32f8793efc37b574af39`. The one ten-path
implementation branch started from that exact merge and delivered in PR #257.
Its 16 active-hour, 1,500 added code/test lines and $0 external-spend caps
were ceilings, not an estimate. The earlier 8–16-hour BER-BKL-009 whole-item row cannot be carried
forward as a forecast for the newly split scope.

| Current selected component | Active work after the owner decision |
| --- | ---: |
| Other eleven selected rows from the #250 checkpoint | 79–162 hours |
| Bounded BER-BKL-009 offline integration | Delivered in PR #257; 0 hours remaining in this package |
| BER-BKL-009 real-host, runtime, privacy and cleanup residual | TBD pending a named host and separate scope |
| **Selected total** | **No finite estimate yet** |

This table is the state after the BER decision, before the later issue #101
host-path choice. Both optional Issue #101 helpers would add 16–40 hours if selected; all other
optional and strategic work remains outside this selected view. This owner
decision triggered an early forecast update. The full five-merge reassessment
is recorded below; the dated #250 checkpoint remains historical.

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

## Five-merge checkpoint — 2026-09-25, after pull request #270

The five merges after #265 were #266, #267, #268, #269 and #270. Their
[GitHub receipts](aegis-execution-metrics.md#checkpoint-after-pull-request-270--2026-09-25)
span 02:39:53–04:03:07 Coordinated Universal Time (UTC) on 2026-09-25: **1h23m14s wall time**.
Review, continuous integration (CI), owner waiting and concurrent work are included; their active-work
split is unavailable. No delivery rate can be inferred. These merges recorded
the preceding checkpoint, selected the issue #101 prototype direction,
repaired malformed offline adapter failures, inventoried BER evidence source
sites and improved architecture-choice explanations. None closed a selected
implementation row.

The #270 tree contains **589 tracked Markdown files**: **545 accepted reader
pages** and **44 classified fixtures**, with **zero known pending pages**.
#269 added the reviewed static source inventory. The owner's #101 choice
superseded the combined package-4 estimate; that scope split earns no completed
work credit. The remaining ten ranges are retained after rechecking their
dependencies because these merges supplied neither implementation-duration
measurements nor evidence closing their gates.

| Selected remaining work item | Active-work planning range | Gate or uncertainty after #270 |
| --- | ---: | --- |
| WP-2B-3 candidate inputs | 1–4 h | Owner inspection of the private 160-case label packet, guide and exact hashes remains. |
| WP-2B-3 measurement and OD-1 | 4–10 h | Label approval, execution source/allowance, measured development result and holdout freeze remain. |
| Selected-host R4/R5 capability proof | 12–24 h, provisional | VirtualBox VM setup and login repair remain paused; guest checks and separately authorized Stage A proof remain. |
| WP-2B-4 | 12–24 h | Calibration, OD-1, R1/R4/R5 evidence and a separate live grant precede the limited suite. |
| WP-2B-5 | 8–16 h | WP-2B-4 and a separate generic-corpus phase grant remain. |
| WP-2B-6 | 8–16 h | WP-2B-5 plus scheduling, cost, quarantine and dataset operations authority remain. |
| WP-2B-7 | 4–8 h | WP-2B-6 and a separate advisory CI/operator grant remain. |
| CP-WP-003 | 8–16 h, provisional | Real atomic approval source, independent freshness, containment, evidence and billing proof remain. |
| CP-WP-004 | 8–16 h | CP-WP-003 real proof, one selected operation and a separate grant remain. |
| Issue #101 package 7 | 6–12 h | Release review depends on package-4 host proof and any selected helper integration. |
| **Ten-row planning subtotal** | **71–146 h** | Includes provisional host uncertainty; not a delivery promise. |
| Issue #101 Stage 4A: offline callback prototype | TBD; proposed ceiling 12 h | Committed dependency lockfile, synthetic authority contract, complete design and reviewed implementation grant remain. |
| Issue #101 Stage 4B: actual host proof and comparison | TBD | Pinned execution scope, callback-consumption proof, telemetry and separate authority remain. |
| BER-BKL-009 host, runtime, privacy and cleanup residual | TBD | Static source inventory closes no host or runtime gate; named host and separate scope remain. |
| Documentation readability | 0 known pending | Future new or changed pages require acceptance; confidential conduct intake remains an owner decision. |
| **Selected total** | **No finite estimate** | Two issue #101 stages and BER residual remain unestimated. |

All seven optional rows were reassessed without an adoption decision: issue
#101 package 5 remains **8–20 h** after the Stage 4B comparison; package 6
remains **8–20 h** after host proof and separate provider authority;
BER-BKL-010 remains **4–12 h** after OD-4 and BKL-009; BER-BKL-014 remains
**8–20 h per additional selected host** after the v1 adapter and host proof;
BER-BKL-015 remains **8–24 h per selected product** after stable WP-2B-5/6
and consumer selection. Strategic skill/framework expansion and multi-judge
arbitration or future control-plane architecture remain unbounded until
selected and scoped. The two optional #101 helpers together add **16–40 h**
conditionally, without making selected or all-options totals finite.

PR #271 subsequently merged static SDK archive checks on existing pages.
Those checks reduce dependency uncertainty but provide no runtime compatibility
proof and did not themselves grant implementation; the owner granted bounded
offline Stage 4A work later. There is no new active-work estimate. #271 is the
first
merge after this checkpoint. Start the next five-merge counter after #270;
revise sooner for a material scope or owner decision. The VM remains paused.

## Five-merge checkpoint — 2026-09-25, after pull request #265

The five merges after #260 were #261, #262, #263, #264 and #265. Their
[exact GitHub receipts](aegis-execution-metrics.md#checkpoint-after-pull-request-265--2026-09-25)
span 2026-09-24 22:33:06–2026-09-25 02:39:53 UTC, or **4h06m47s** of
wall time. This includes review, CI, owner waiting and concurrent work; no
active-work rate can be derived. The five PRs taught build choices, reconciled
the previous checkpoint, corrected setup guidance, recorded the approved VM
setup, and prepared a conditional issue #101 SDK scope. None closed a selected
implementation row. The VM setup was performed outside these PRs and paused
after graphical login stalls; it did not run a BER host probe.

The #265 tree still has **588 tracked Markdown files**: **544 accepted reader
pages** and **44 classified fixtures**, with **zero known pending pages** in
the bounded readability sweep. PR #265 changed only two existing pages and
recorded their review. Confidential conduct intake remains a separate owner
decision. The BER-BKL-009 real-host, runtime, privacy and cleanup residual
has no scoped estimate. The following eleven rows retain their prior planning
ranges because these merges supplied no measured implementation duration or
new authority to close them; the paused VM adds uncertainty to host proof.

| Selected remaining work item | Active-work planning range | Gate or uncertainty after #265 |
| --- | ---: | --- |
| WP-2B-3 candidate inputs | 1–4 h | Owner must inspect the private 160-case label packet, guide and exact hashes. |
| WP-2B-3 measurement and OD-1 | 4–10 h | Label approval, execution source/allowance, measured development result and holdout freeze remain. |
| Selected-host R4/R5 capability proof | 12–24 h, provisional | Disposable VM exists but guest checks and login repair are paused; Stage A probe needs a separate grant. |
| WP-2B-4 | 12–24 h | Calibration, OD-1, R1/R4/R5 evidence and a separate live grant precede the limited suite. |
| WP-2B-5 | 8–16 h | WP-2B-4 completion and a separate generic-corpus phase grant remain. |
| WP-2B-6 | 8–16 h | WP-2B-5 plus scheduling, cost, quarantine and dataset operations grant remain. |
| WP-2B-7 | 4–8 h | WP-2B-6 and separate advisory CI/operator grant remain. |
| CP-WP-003 | 8–16 h, provisional | Real atomic approval source, independent freshness, containment, evidence and billing proof remain. |
| CP-WP-004 | 8–16 h | CP-WP-003 real proof, one selected operation and a separate grant remain. |
| Issue #101 package 4 | 8–16 h, provisional | No host path selected or code grant. The #265 Stage 4A 12-hour ceiling is hypothetical, not an estimate; selection requires a separate 4A/4B reforecast. |
| Issue #101 package 7 | 6–12 h | End-to-end release review depends on package 4 proof and any selected helper integration. |
| Documentation readability | 0 known pending | 544 accepted readers; future changes require acceptance. |
| **Eleven-row planning subtotal** | **79–162 h** | Includes provisional host and package-4 ranges; not a delivery promise. |
| BER-BKL-009 host, runtime, privacy and cleanup residual | TBD | Needs named host, separate scope and privacy/runtime/cleanup decisions. |
| **Selected total** | **No finite estimate** | The subtotal excludes the unestimated BER residual. |

All seven optional rows were reconsidered without an adoption decision:
issue #101 package 5 remains **8–20 h** after a package-4 comparison;
package 6 remains **8–20 h** after host proof and separate provider authority;
BER-BKL-010 remains **4–12 h** after OD-4 and BKL-009; BER-BKL-014 remains
**8–20 h per selected additional host**; BER-BKL-015 remains **8–24 h per
selected product**; strategic skill/framework expansion and multi-judge
arbitration or future control-plane architecture remain unbounded until
selected and scoped. Both optional #101 helpers would add **16–40 h** to the
known subtotal if selected, without making the selected or all-options totals
finite. No estimate or owner choice here authorizes private labels, provider
calls, host probing, paid work or deployment. Start the next five-merge
counter after #265; revise sooner for a material owner or scope decision.

## Five-merge checkpoint — 2026-09-24, after pull request #260

The five merges after #255 were #256, #258, #257, #259 and #260. Their
[exact GitHub merge receipts](aegis-execution-metrics.md#checkpoint-after-pull-request-260--2026-09-24)
span 18:59:41–22:33:06 UTC, or **3h33m25s** of elapsed wall time. That span
includes review, CI, owner waiting and overlapping work, so it cannot yield
an active-work delivery rate. #256 reconciled the previous checkpoint; #258
planned source-only BER Stage A proof; #257 delivered the synthetic-only
BER-BKL-009 integration; #259 recorded its approval consumption and closeout;
#260 proposed the disposable VirtualBox Linux setup. Only #257 closed a
selected implementation package. PR #261, which taught user-facing build
choices across Aegis skills, is the first merge in the next five-merge cycle.

The merged tree after #260 has **588 tracked Markdown files**: **544 accepted
reader pages** and **44 classified fixtures**, with **zero known pending
pages** in the bounded readability sweep. The confidential conduct intake
route and independent recipient remain owner decisions. The BER-BKL-009
offline package is delivered; its later host, runtime, privacy and cleanup
work still has no scoped estimate. The chosen VirtualBox platform is a
candidate setup path, not a provisioned host or Stage A probe grant.

| Selected remaining work item | Active-work estimate | Gate or uncertainty after #260 |
| --- | ---: | --- |
| WP-2B-3 candidate inputs | 1–4 h | Owner must inspect private candidate labels, guide and exact hashes. |
| WP-2B-3 measurement and OD-1 | 4–10 h | Private labels, source/allowance, measured development result and holdout freeze remain. |
| Selected-host R4/R5 capability proof | 12–24 h | VirtualBox Linux VM is the candidate; provisioning, identity and separate Stage A probe authority remain. |
| WP-2B-4 | 12–24 h | Calibration, OD-1 and host proof precede a limited live suite and separate grant. |
| WP-2B-5 | 8–16 h | WP-2B-4 and separate generic-corpus phase grant remain. |
| WP-2B-6 | 8–16 h | WP-2B-5 plus scheduling, cost, quarantine and dataset operations grant remain. |
| WP-2B-7 | 4–8 h | WP-2B-6 and separate advisory CI/operator grant remain. |
| CP-WP-003 | 8–16 h | Real source, independent freshness, containment, evidence and billing proof remain. |
| CP-WP-004 | 8–16 h | CP-WP-003 real proof, one selected target/operation and separate grant remain. |
| Issue #101 package 4 | 8–16 h | Exact SDK-managed host, versions and Stage 4A offline then Stage 4B host authority remain. |
| Issue #101 package 7 | 6–12 h | Release evaluation depends on selected integration outcomes and separate proof. |
| Documentation readability | 0 known pending | 544 accepted readers; future new or changed pages require acceptance. |
| **Other eleven selected rows** | **79–162 h** | Ranges retained after dependency review; none of the five merges closed these rows. |
| BER-BKL-009 host, runtime, privacy and cleanup residual | TBD | Requires a named host, scoped proof and separate owner decisions. |
| **Selected total** | **No finite estimate** | The eleven-row subtotal excludes the unestimated BER-BKL-009 residual. |

All seven optional rows remain conditional. Issue #101 package 5 remains
**8–20 h** after the package-4 comparison; package 6 remains **8–20 h**
after host proof and separate provider authority. Together those two helpers
would add **16–40 h** to the known eleven-row subtotal, without making the
selected-plus-both total finite. BER-BKL-010 remains **4–12 h** after OD-4
and BKL-009; BER-BKL-014 remains **8–20 h per additional selected host**
after the v1 Claude Code adapter, host proof and owner adoption/budget;
BER-BKL-015 remains **8–24 h per selected product** after stable WP-2B-5/6
and a consumer choice. Strategic skill/framework expansion and multi-judge
arbitration/future control-plane architecture remain unbounded until scoped.
The full all-options backlog has no finite total.

Start the next five-merge counter after #260; #261 is the first merge.
Re-estimate sooner for a material owner or scope decision. None of these
estimates authorizes private input, host probing, provider use, spend or
deployment.

## Five-merge checkpoint — 2026-09-24, after pull request #255

The five requests after #250 were #251–#255. Their [exact GitHub merge
receipts](aegis-execution-metrics.md#checkpoint-after-pull-request-255--2026-09-24)
span 17:56:33–18:59:41 UTC, or **1h03m08s** of elapsed wall time. This
includes review, CI, owner waiting and overlapping work; it is neither active
labor nor a measured delivery rate. #251 recorded the previous checkpoint
and consumed the #249 guard exception; #252 persisted the owner's Aegis
skill-use preference; #253 merged the BER-BKL-009 scope proposal and corrected
current status; #254 recorded consumption of APR-012 and closed post-#253
reading status; #255 made the bounded offline BER-BKL-009 grant effective
through BER-DEC-013/APR-023. These requests did not deliver the authorized
integration or close another selected implementation row.

The #255 tree has **585 tracked Markdown files**: **541 accepted reader
pages** and **44 classified synthetic fixtures**, with **zero known pending
pages** in the bounded sweep. The owner still needs to supply a working private
Code of Conduct intake route and an independent recipient. The #250 historical
selected total of 87–178 hours included a provisional 8–16 hours for all of
BER-BKL-009. The approved offline package now has a **ceiling of 16 active
implementation hours**, not an estimate; its real-host, runtime, privacy and
cleanup residual has no scoped estimate. No finite selected total follows.

| Selected remaining work item | Current active-work estimate or bound | Gate or uncertainty after #255 |
| --- | ---: | --- |
| WP-2B-3 candidate inputs | 1–4 h | Owner must inspect private candidate labels, guide and exact hashes. |
| BER-BKL-009 offline integration | At most 16 h; estimate pending | BER-DEC-013/APR-023 effective at #255; one synthetic-only implementation from exact merge, ten paths and no real-host or provider access. |
| BER-BKL-009 later policy work | TBD | Named host, runtime binding, actual privacy/redaction review and marker-gated cleanup require separate scopes. |
| WP-2B-3 measurement and OD-1 | 4–10 h | Private labels, source/allowance, measured development result and holdout freeze remain. |
| Selected-host R4/R5 capability proof | 12–24 h | Named host and separate Stage A probe authority remain; later model-driven proof remains gated. |
| WP-2B-4 | 12–24 h | Calibration, OD-1 and host proof precede a limited live suite and separate grant. |
| WP-2B-5 | 8–16 h | WP-2B-4 and separate generic-corpus phase grant remain. |
| WP-2B-6 | 8–16 h | WP-2B-5 plus scheduling, cost, quarantine and dataset operations grant remain. |
| WP-2B-7 | 4–8 h | WP-2B-6 and separate advisory CI/operator grant remain. |
| CP-WP-003 | 8–16 h | Real source, independent freshness, containment, evidence and billing proof remain. |
| CP-WP-004 | 8–16 h | CP-WP-003 real proof, one selected target/operation and separate grant remain. |
| Issue #101 package 4 | 8–16 h | Exact SDK-managed host, versions and Stage 4A offline then Stage 4B host authority remain. |
| Issue #101 package 7 | 6–12 h | Release evaluation depends on selected integration outcomes and separate proof. |
| Documentation readability | 0 known pending | 541 accepted readers; future new or changed pages require acceptance. |
| **Other eleven selected rows** | **79–162 h** | Ranges retained after checking dependencies; no one of these five merges closed a row. |
| **Selected total** | **No finite estimate** | Add the bounded offline package and unestimated later BER-BKL-009 work to the eleven-row subtotal. |

All **seven optional rows** were reconsidered. Issue #101 package 5 remains
**8–20 h** if a local helper is selected after the package-4 comparison;
package 6 remains **8–20 h** after host proof and separate provider authority.
Both would add **16–40 h** to the known eleven-row subtotal, but still yield
no finite selected-plus-both total because BER-BKL-009's later work is TBD.
BER-BKL-010 remains **4–12 h** after OD-4 and BKL-009; BER-BKL-014 remains
**8–20 h per additional selected host** after v1 Claude Code adapter
completion, per-host capability proof, and owner adoption/budget; BER-BKL-015
remains **8–24 h per selected product** after stable WP-2B-5/6 and an actual
consumer choice. Strategic skill/framework expansion and multi-judge
arbitration/future control-plane architecture remain unbounded until their
adoption scope is selected. The full all-options backlog has no finite total.
Start the next five-merge counter after #255; revise sooner for a material
scope or owner decision. None of these estimates grants private-input, host,
provider, spend or deployment authority.

## Five-merge checkpoint — 2026-09-24, after pull request #250

The five requests after #245 were #246, #247, #248, #249 and #250. The
[measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-250--2026-09-24)
records each exact merge commit and GitHub merge receipt. Their combined
**1h39m06s** prior-merge wall interval includes review, CI, owner waiting
and overlapping work, so it is not active labor or a delivery rate. #246 and
#247 corrected delivered setup and control-plane paths; #248 added the
multi-agent release path. #249 delivered synthetic offline holdout support
under BER-DEC-012 and a separately approved, now-consumed protected guard
exception in APR-020–021. #250 accepted the remaining documentation notes
and the two new reader pages, and passed all exact-head Actions. No provider
or real-host execution occurred.

The merged tree contains **584 tracked Markdown files**: **540 accepted
reader pages** and **44 classified fixtures**, with **zero known pending
pages** in the bounded readability sweep. Confidential conduct intake still
needs a private route and a separate recipient decision. The #245 baseline
was 96–197 selected active hours, including 1–3 documentation hours. Note
acceptance in #250 removes that residual, and #249 removes the 8–16-hour
offline support row. These are completed scope deductions, not a throughput
extrapolation.

| Selected remaining work item | Active hours after #250 | Gate or uncertainty |
| --- | ---: | --- |
| WP-2B-3 candidate inputs | 1–4 | Owner must review exact labels, guide and hashes |
| BER-BKL-009 evidence policy | 8–16, provisional | Offline proof delivered in #139; host access, encryption, privacy and cleanup still need a scoped decision. A proposed offline increment would supersede this whole-item estimate if approved. |
| WP-2B-3 measurement and OD-1 | 4–10 | Private labels, selected source, allowance, development result and independent holdout freeze remain |
| Selected-host capability proof | 12–24 | Named host and measured isolation remain |
| WP-2B-4 | 12–24 | Calibration and host proof before limited live suite |
| WP-2B-5 | 8–16 | WP-2B-4 before generic corpus |
| WP-2B-6 | 8–16 | Later scheduling, cost, quarantine and dataset operations |
| WP-2B-7 | 4–8 | Later advisory CI and operator workflow |
| CP-WP-003 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| CP-WP-004 | 8–16 | Selected target and CP-WP-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | Select exact host/versions, offline Stage 4A scope and later host comparison authority |
| Issue #101 package 7 | 6–12 | Release evaluation follows selected integration outcomes |
| **Selected remaining total** | **87–178** | Conditional active-work estimate, excluding owner and external waits |

The seven optional rows were also reconsidered. Issue #101 package 5
remains **8–20** if selected, and package 6 **8–20** with separate online
provider authority. BER-BKL-010 remains **4–12** after an OD-4 decision and
BKL-009 completion; BER-BKL-014 remains **8–20 per selected host**;
BER-BKL-015 remains **8–24 per selected product**. Strategic skill and
framework expansion, and multi-judge arbitration plus future control-plane
architecture, remain unbounded until scoped. Both Issue #101 helpers add
**16–40**, making selected-plus-both **103–218**. The full all-options
backlog has no finite total. Start the next five-merge counter after #250;
re-estimate sooner for a material owner choice.

## Five-merge checkpoint — 2026-09-24, after pull request #245

Five requests merged after #244: #139, #197, #239, #235 and #245. The
[measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-245--2026-09-24)
records their exact merge commits and prior-merge wall intervals. Their
5h51m45s combined interval includes owner wait, CI and unrelated work; no
active-only rate can be inferred. Linux and Windows execution checks passed at
each reviewed head. #139, #197 and #239 merged under separate owner-approved,
now-consumed protected guard exceptions in APR-014–019. #235 and #245 had all
exact-head Actions green. No provider or real-host execution occurred.

The #245 tree had **582 tracked Markdown files**. The #238 pending reader
page was corrected in #239, whose new review note was accepted. The #139 and
#197 evidence notes entered the tree before #239; corrected current-reading
versions passed two independent full-page reviews in this checkpoint PR. The
baseline residual was **1–3 documentation active hours**. This PR's corrected
versions close those two notes; the #245 inventory becomes 538 accepted
readers and 44 classified fixtures. PRs #248 and #249 subsequently added two
reviewed reader pages, bringing the candidate tree to **584 pages**: 540
accepted readers and 44 classified fixtures, with zero known pending pages on
this PR's accepted merge. This is a small bounded follow-up, not a measured
throughput rate. Confidential conduct intake
still needs a private route and separate recipient decision.

| Selected open work item | After #238 active hours | Revised after #245 | Remaining gate or reason |
| --- | ---: | ---: | --- |
| WP-2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and exact-label review remains |
| BER-BKL-009 evidence policy | 8–16 | 8–16, provisional | #139 delivered the synthetic offline proof; real-host access, encryption, privacy and cleanup remain unscoped. Do not subtract an unmeasured increment mechanically |
| WP-2B-3 execution support | 8–16 | 8–16 | BER-DEC-012 became effective on #235 merge; one bounded synthetic implementation is authorized but undelivered |
| WP-2B-3 measurement and OD-1 | 4–10 | 4–10 | Private labels, source, allowance, development result and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation remain |
| WP-2B-4 | 12–24 | 12–24 | Calibration and host proof before limited live suite |
| WP-2B-5 | 8–16 | 8–16 | WP-2B-4 gate before generic corpus |
| WP-2B-6 | 8–16 | 8–16 | Later scheduling, cost, quarantine and dataset operations |
| WP-2B-7 | 4–8 | 4–8 | Later advisory CI and operator workflow |
| CP-WP-003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| CP-WP-004 | 8–16 | 8–16 | Selected target and CP-WP-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | #237 prepared options; host and comparison authority remain unselected |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Documentation readability | 1–3 | **0 on this PR's accepted merge** | #239 closed the protected README; two new notes passed corrected-candidate review |
| **Selected remaining total** | **96–197** | **95–194 at the #245 baseline after note acceptance** | Non-documentation subtotal 95–194 before #249 |

All **14 selected** and **seven optional** rows were reconsidered. The optional
rows remain Issue #101 package 5 **8–20** if selected; package 6 **8–20**
with separate provider authority; BER-BKL-010 **4–12**; BER-BKL-014 **8–20
per selected host**; BER-BKL-015 **8–24 per selected product**; strategic skill
and framework expansion unbounded until scoped; and multi-judge arbitration
plus future control-plane architecture unbounded until adopted. Both optional
Issue #101 helpers would add **16–40**, making selected-plus-both **111–234**
at the #245 baseline after note acceptance. PR #249 subsequently delivered
WP-2B-3 offline execution support, reducing current selected work to
**87–178 active hours** and selected-plus-both to **103–218** on this PR's
accepted merge. The full all-options
backlog has no finite total. Start the next five-merge counter after #245;
re-estimate sooner when a material owner choice changes scope.

After this checkpoint, PRs #246 and #247 merged focused corrections to the
already delivered Issue #101 setup path and synthetic control-plane validator
contact boundary. Their exact-head Actions passed; neither closes an open
selected package or changes the estimates above. They are the first two
merges toward the next cadence checkpoint.

## Five-merge checkpoint — 2026-09-24, after pull request #238

Five requests merged after [#232](#five-merge-checkpoint--2026-09-24-after-pull-request-232):
#233, #234, #236, #237 and #238. The exact #238 merge commit is
`a092f8e07429c75cdc06d46befe084cb84a35d13`. The
[measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-238--2026-09-24)
records each merge and the available wall interval. Exact-head and exact-main
Linux and Windows checks passed for the five merges; active-only, review, CI
and queue time cannot be separated from their merge intervals. None of these
merges closed a non-documentation package or an owner decision.

The #238 tree has **579 tracked Markdown files**: **534 reader pages** with
recorded full-checklist acceptance, **44 synthetic fixtures** with an integrity
and classification disposition, and **one pending reader page**,
`scripts/tests/fixtures/README.md`. Since #232, accepted reader pages rose by
**143**: 40 in #234, 18 in #236, and 84 existing pages plus one new review note
in #238. Five new Markdown files entered the tree. The last README needs the
separate guarded PR #239 and its own owner disposition. The residual model is
**1–3 documentation active hours**, excluding owner wait. The previous full
checkpoint assigned **30–115**; the latest interim #236 estimate was
**25–105**. The large batch is an acceptance count, not a measured active-work
rate or evidence to change the per-page time assumptions.

| Selected open work item | #232 remaining active hours | Revised after #238 | Remaining gate or reason |
| --- | ---: | ---: | --- |
| WP-2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and exact-label review |
| BER-BKL-009 evidence policy | 8–16 | 8–16 | PR #139 protected guard disposition; real-host enforcement later |
| WP-2B-3 execution support | 8–16 | 8–16 | PR #235 remains a proposed offline implementation grant |
| WP-2B-3 measurement and OD-1 | 4–10 | 4–10 | Reviewed inputs, source, allowance, development result and holdout freeze |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation |
| WP-2B-4 | 12–24 | 12–24 | Calibration and host proof before limited live suite |
| WP-2B-5 | 8–16 | 8–16 | WP-2B-4 gate before generic corpus |
| WP-2B-6 | 8–16 | 8–16 | Later scheduling, cost, quarantine and dataset operations |
| WP-2B-7 | 4–8 | 4–8 | Later advisory CI and operator workflow |
| CP-WP-003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof |
| CP-WP-004 | 8–16 | 8–16 | Selected target and CP-WP-003 prerequisites |
| Issue #101 package 4 | 8–16 | 8–16 | #237 is preparation, not a selected host or comparison result |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation after selected integration outcomes |
| Documentation readability | 30–115 | **1–3** | One protected reader page remains in #239 |
| **Selected remaining total** | **125–309** | **96–197** | **95–194 non-documentation** plus **1–3 documentation** |

All **14 selected** and **seven optional** rows were reconsidered. The seven
optional rows remain: Issue #101 package 5 **8–20** if selected; package 6
**8–20** with separate provider authority; BER-BKL-010 **4–12**;
BER-BKL-014 **8–20 per selected host**; BER-BKL-015 **8–24 per selected
product**; strategic skill and framework expansion unbounded until a batch is
selected; and multi-judge arbitration plus future control-plane architecture
unbounded until adoption and scope are chosen. Both optional Issue #101 helpers
would add **16–40**, making selected-plus-both **112–237 active hours**. The
full all-options backlog still has no finite total.

Subsequently, #240–#243 corrected defects in the delivered setup and offline
control-plane boundaries. These four merges do not deliver Issue #101 package
4 or 7, the CP real-capability proof, or any provider or host authority. The
selected estimates above therefore remain the current planning bounds. PR
#239 is still unmerged, so neither zero documentation residual nor the
conditional **95–194 selected** total is an observed closure. The separate
confidential conduct intake decision remains open. Four merges followed #238
through #243; this checkpoint PR is the fifth on accepted merge and adds no
selected implementation scope. Start the next five-merge counter after this
checkpoint merges. Re-estimate sooner if a material owner decision changes scope.

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

## Five-merge checkpoint — 2026-09-23, after pull request #173

Five requests merged after #169, in the order below. All five final revisions
passed the Linux, Windows and protected-file GitHub Actions checks. The merge
clock is GitHub's pull-request `mergedAt` event in Coordinated Universal
Time (UTC). Duration notation uses **m** for minutes and **s** for seconds.

| Merged pull request and delivered scope | Bounded estimate | Merge event (UTC) | Observed wall interval | Merge commit |
| --- | ---: | --- | ---: | --- |
| [#177](https://github.com/ModernNomad-98/Project-Aegis/pull/177): previous five-merge forecast | 1–2 active hours | 21:15:07 | 9m09s from first preparation | `9daf12e3d90d513b6c98812c7aeb4c3fe948d7e8` |
| [#175](https://github.com/ModernNomad-98/Project-Aegis/pull/175): scoped human merge-grant clarification | 1–3 active hours | 21:16:02 | 23m34s from first preparation | `41007d4f1acf177845580c247169919c17958cb2` |
| [#171](https://github.com/ModernNomad-98/Project-Aegis/pull/171): sixth reference screen, four corrected pages | 2–4 active hours | 21:16:49 | 35m27s from first preparation | `b9a08fe1214e9bd4adb6c68a06f171065d697b32` |
| [#172](https://github.com/ModernNomad-98/Project-Aegis/pull/172): seventh reference screen, six corrected pages | 2–4 active hours | 21:17:35 | 34m22s from first preparation | `19a145309f7a01043c18e910255018b6b8e033b7` |
| [#173](https://github.com/ModernNomad-98/Project-Aegis/pull/173): final 16-reference screen, five corrected pages | 1–3 active hours | 21:18:19 | 33m46s from first preparation | `e6148322eefd085eeba9c58ef0c89876b90c9f71` |

The [measurement record](aegis-execution-metrics.md#checkpoint-after-pull-request-173--2026-09-23)
records each prior estimate and distinguishes initial read-only preparation
from later editing. The ranges for successive screen batches describe
different scopes. These overlapping wall intervals include review, integration
and checks; active effort, waiting and rework were not separately instrumented.
They cannot be added as active labor or used as a full-documentation review rate.

The [sixth](../evidence/documentation/skill-references-sixth-20-readability-2026-09-23.md),
[seventh](../evidence/documentation/skill-references-seventh-20-readability-2026-09-23.md)
and [final](../evidence/documentation/skill-references-final-16-readability-2026-09-23.md)
reference screens add **15 corrected pages**: four, six and five respectively.
Cumulative corrections from these screen batches are **34 + 15 = 49 reference
pages**. All **156 sorted reference paths** now have bounded screening
coverage. This completes that screening pass, not the full readability
acceptance of each page or the repository-wide documentation sweep.

Separately, [#175](https://github.com/ModernNomad-98/Project-Aegis/pull/175)
clarifies existing scoped human merge grants in **two skill instructions,
two references and two evaluation files**. Those reference changes are
separate from the 49 screen-batch corrections. The change does not create a
grant or alter repository settings, auto-merge state or the later requirement
for green checks. It therefore closes no implementation or owner-decision gate.

The exact #173 merge tree contains **536 tracked Markdown files**, compared
with 533 after #169 and 491 in the original inventory. The three new files
are reference-screen evidence notes; #175 adds no Markdown file. The earlier
entrypoint pass comprises **186 `SKILL.md` paths: 185 shipped skills and one
authoring template**, with 28 pages corrected in those screen batches.
Shared documentation-ledger integration remains pending. Remaining work
includes full [page acceptance](aegis-documentation-readability-backlog.md#acceptance-for-each-page)
and the wider documentation inventory. Its depth and rewrite volume are
uncertain, so the documentation range stays **80–200 active hours**.

At the **21:20:04 UTC** preparation checkpoint, requests #176, #178 and #179
remained open and are excluded from delivered scope.
[Pull request #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
remained open at `8928383f0838e2d99ee3a89c44b98b7aba7f1c9b`; its documented
protected-file guard failure and separate owner disposition remained pending.
These five merges changed no runtime, implementation grant, private-label
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
| Repository-wide documentation readability | 80–200 | 80–200 | All 156 reference paths received bounded screening; ledger integration and full acceptance remain open |
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
ranges. Restart the five-merge counter after #173, and revise sooner if
verified delivery or an owner decision materially changes remaining scope.

## Five-merge checkpoint — 2026-09-23, after pull request #181

Five requests merged after #173, in order #180, #176, #178, #179 and #181.
The revision under review is the exact #181 merge
`e2145b14cf5629c336b4bbcb624ef7f5fcc92f01`. All five merged only
documentation and related evidence; no implementation, owner-decision or
selected-host gate closed. The observed endpoints below are GitHub
pull-request `mergedAt` events in Coordinated Universal Time (UTC). The
[execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-181--2026-09-23)
record each source and wall interval.

| Merge, commit and delivered scope | Previous estimate | New package estimate | First audit/preparation to merge event |
| --- | ---: | ---: | ---: |
| [#180](https://github.com/ModernNomad-98/Project-Aegis/pull/180), `b26d78e13c9238411df90c354b20273db7acfd98`: prior five-merge forecast | 1–2 h | 1–2 h | 10m34s |
| [#176](https://github.com/ModernNomad-98/Project-Aegis/pull/176), `02ff5f00d5f81dc48c8f82225f10092771a4ebc1`: changelog and startup routing | 2–4 h guide batch | 1–3 h bounded correction | 33m05s |
| [#178](https://github.com/ModernNomad-98/Project-Aegis/pull/178), `fd8ea303e220adb8ebe5025682f8345fcbe03027`: seven operational guides | 2–4 h smaller screen | 4–8 h seven-page correction | 29m55s |
| [#179](https://github.com/ModernNomad-98/Project-Aegis/pull/179), `61b3589ccaac40a7d3448f4cbe6bbfb3534c8dc3`: five authorization proposals | 2–4 h smaller guide batch | 2–4 h bounded correction | 30m35s |
| [#181](https://github.com/ModernNomad-98/Project-Aegis/pull/181), `e2145b14cf5629c336b4bbcb624ef7f5fcc92f01`: seven legacy plan and research pages | 4–8 h 15-page audit | 4–8 h seven-page correction | 15m27s |

The previous estimates for #176–#181 refer to earlier or differently bounded
page sets; they are not earlier measurements of the same edit. These wall
intervals overlap and include preparation, review, checks and waits. Active
effort was not instrumented, so the intervals cannot be summed as labor or
extrapolated into a full-sweep rate. The four documentation deliveries added
four dated evidence pages: this #181 tree has **540 tracked Markdown files**,
compared with 536 after #173. The former 184-skill changelog count and legacy
generation plans are now marked historical. Operational guides and proposals
have dated current-reading pointers, while their original decision records
remain intact. This narrows navigation errors; it does not complete the
repository-wide documentation acceptance criteria.

All five PR-head Linux, Windows and protected-file checks passed, and the
main-branch checks for each merge, including #181, passed. The merge-commit
clock differs by one second
from GitHub's `mergedAt` event for #176 and #178; wall intervals use the
GitHub event consistently.

Across this five-merge cycle, the earliest recorded audit began at 21:00:06
UTC and the last merge event occurred at 21:35:10 UTC: **35m04s observed wall
time**. There was no published single active-work ETA for the combined cycle;
the separate package estimates in the table must not be added as if five
people worked serially.

Every **14 selected** and **seven optional** open row was reconsidered against
these deliveries. The full documentation inventory, evidence pages and
individual page acceptance remain unfinished. No measured active-work rate or
new scope evidence supports narrowing the 80–200-hour documentation range, and
no selected implementation row closed. The previous and revised remaining
selected totals are both **175–394 active hours**, comprising **95–194** for
non-documentation work and **80–200** for documentation.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate after #181 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic review and approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | The offline policy PR has not merged into this tree; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | Offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed source and allowance, development results and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path/profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution awaits calibration and selected-host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Selected delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Entry-point/reference screens and these guides advanced; evidence inventory and full page acceptance remain |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation **95–194** plus documentation **80–200** |

All seven optional rows were reconsidered. No optional package or quantity was
selected in these five merges.

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

Both optional issue #101 helpers add **16–40 active hours** if selected,
giving **191–434 active hours** with the selected work. The full all-options
backlog remains unbounded while optional quantities and architecture choices
remain open. Owner waits, GitHub queues, provider execution and host
provisioning are outside the active-hour estimates. Restart the five-merge
counter after #181, and revise sooner if verified delivery or an owner
decision materially changes remaining scope.

## Five-merge checkpoint — 2026-09-23, after pull request #186

Five requests merged after #181, in order #185, #182, #183, #184 and #186.
The reviewed base is the exact #186 merge
`d5b007b0a3cc2bd43806a16970f19c84be9a86b0`. These requests delivered
the preceding forecast, a documentation ledger update and three groups of
reading improvements. No selected implementation item, owner-decision gate
or selected-host prerequisite closed. The [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-186--2026-09-23)
record the original estimates, start times and GitHub merge events.

| Merge, commit and delivered scope | Previous estimate | New package estimate | First audit/preparation to merge event |
| --- | ---: | ---: | ---: |
| [#185](https://github.com/ModernNomad-98/Project-Aegis/pull/185), `7cb14fd6801031de28d5b11d759005cb089ef877`: prior five-merge forecast | 1–2 h | 1–2 h | 13m38s |
| [#182](https://github.com/ModernNomad-98/Project-Aegis/pull/182), `e43708bfaf7bf134260769d58b17980c59f9aa94`: documentation ledger through the completed skill and reference screens | None recorded for this integration | 1–3 h | 50m36s |
| [#183](https://github.com/ModernNomad-98/Project-Aegis/pull/183), `fabdafa532f9760d558d8bcd3b7237742d480895`: three roadmap and audit reading keys | 4–8 h wider screen | 1–3 h bounded correction | 23m22s |
| [#184](https://github.com/ModernNomad-98/Project-Aegis/pull/184), `8a69909ec8889f40a2822b7d78b0c4ad3eb7d660`: evidence index and seven dated status banners | 2–4 h evidence inventory | 4–8 h bounded correction | 13m53s |
| [#186](https://github.com/ModernNomad-98/Project-Aegis/pull/186), `d5b007b0a3cc2bd43806a16970f19c84be9a86b0`: five candidate and hosted-evidence reading notes | 2–4 h evidence inventory | 2–4 h five-page correction | 9m27s |

Here **h**, **m** and **s** mean hours, minutes and seconds. The earlier
estimates for #183–#186 describe preceding or differently bounded screens.
All package intervals overlap and include preparation, review, integration,
checks and waits. Active effort was not instrumented; these observed wall
intervals cannot be summed as labor or used as a documentation or coding rate.
The cycle runs from #182's first preparation at 20:59:26 to #186's merge event
at 21:57:03 Coordinated Universal Time (UTC): **57m37s observed wall time**.
There was no single published active-work estimate for the combined cycle.

The exact #186 tree contains **543 tracked Markdown files**, compared with
540 after #181. The ledger added no file; #183 added one dated evidence note,
#184 added the evidence index and #186 added one dated evidence note.
The [documentation ledger](aegis-documentation-readability-backlog.md#documentation-batches)
now records the completed screens through #173 and the separate owning-skill
corrections. Those screens covered **186 skill entrypoint paths** (185 shipped
skills and one template), with 28 corrected pages, and **156 reference paths**,
with 49 corrected pages. This cycle records that earlier progress; it does not
claim a second pass or new acceptance of those pages.

The [three-page evidence note](../evidence/documentation/remaining-active-docs-readability-2026-09-23.md),
[evidence index](../evidence/README.md) and
[five-page follow-up note](../evidence/documentation/evidence-followup-current-reading-2026-09-23.md)
describe this cycle's bounded reading corrections. Original audit findings,
candidate identities, platform skips and failed hosted-run records remain
historical evidence. Full page acceptance and the wider documentation sweep
remain unfinished, including pages outside these selected groups.

All five final pull-request revisions passed their Linux, Windows and
protected-file checks, and all five main-branch runs passed. The last main
run, [#186 verification 35925522295](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35925522295),
was confirmed successful at the exact merge before this draft froze.

All **14 selected** and **seven optional** open rows were reconsidered.
Ledger integration and dated reading notes reduce known navigation work,
but no measured active-work rate or remaining-page acceptance inventory
supports narrowing the 80–200-hour documentation estimate. No selected
implementation row closed, and no optional package or quantity was selected.
The previous and revised selected totals remain **175–394 active hours**:
**95–194** for non-documentation work and **80–200** for documentation.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate after #186 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic review and approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | Pull request #139 remains unmerged pending its own guard disposition; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | The exact offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed source and allowance, development results and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path/profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution awaits calibration and selected-host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Selected delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Ledger integration through #173 is delivered; full page acceptance and the wider evidence/documentation inventory remain |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation **95–194** plus documentation **80–200** |

All seven optional rows retain their ranges and gates. [Strategic expansion](product-agnostic-skill-and-agent-roadmap.md)
still requires a bounded candidate batch informed by the [skills catalog](../skills-catalog.md).

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

Selecting both optional issue #101 helpers adds **16–40 active hours**,
giving **191–434 active hours**. The full all-options backlog remains
unbounded. Owner waits, GitHub queues, provider execution and host provisioning
are outside the active-hour estimates. This checkpoint grants no new
implementation or execution authority. Restart the five-merge counter after
#186, and revise sooner if verified delivery or an owner decision materially
changes remaining scope.

## Five-merge checkpoint — 2026-09-23, after pull request #191

Five requests merged after #186, in order #189, #187, #188, #190 and #191.
The exact base is the #191 merge
`761915207f7974b3d4cab7fb099216188ef3e968`. This interval delivered
the preceding forecast, three bounded documentation corrections and a ledger
update for earlier batches. No selected implementation item, owner-decision gate or
selected-host prerequisite closed. The [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-191--2026-09-23)
record the source timestamps and observed intervals.

| Merge, commit and delivered scope | Previous estimate | New package estimate | First audit/preparation to merge event |
| --- | ---: | ---: | ---: |
| [#189](https://github.com/ModernNomad-98/Project-Aegis/pull/189), `754c680aff3dc790d05a70588342c5a42e70ac63`: prior five-merge forecast | 1–2 h | 1–2 h | 12m14s |
| [#187](https://github.com/ModernNomad-98/Project-Aegis/pull/187), `8ea56570f645b64acbb953c217ba586a9ca6b0f4`: root maintainer reading route | 2–4 h inventory | 1–3 h bounded correction | 21m18s |
| [#188](https://github.com/ModernNomad-98/Project-Aegis/pull/188), `0c52c3e7812818b135b449fe5766f39932893c4b`: four historical documentation evidence notes | 2–4 h preceding screen | 1–3 h bounded correction | 10m22s |
| [#190](https://github.com/ModernNomad-98/Project-Aegis/pull/190), `a8b81d49698082ca788d08ed21181e347ab43744`: seven agent and contributor pages | 2–4 h preceding 15-page screen | 2–4 h seven-page correction | 13m21s |
| [#191](https://github.com/ModernNomad-98/Project-Aegis/pull/191), `761915207f7974b3d4cab7fb099216188ef3e968`: ledger through #186 | 1–3 h | 1–3 h | 10m08s |

Here **h**, **m** and **s** mean hours, minutes and seconds. The prior ranges
for #187, #188 and #190 describe preceding or differently bounded screens.
The earliest preparation began at 21:48:24 and the final merge event occurred
at 22:16:49 Coordinated Universal Time (UTC): **28m25s observed wall time**
for the cycle. These package intervals overlap and include preparation,
review, integration, checks and waits. Active effort was not instrumented;
the intervals cannot be summed as labor or converted into a coding or full
documentation-review rate. No single combined active-work estimate was published.

The exact #191 tree contains **544 tracked Markdown files**, compared with
543 after #186. Only #190 added a file: its [dated evidence note](../evidence/documentation/agent-contributor-docs-readability-2026-09-23.md).
The [root guide](../../README.md#maintainer-reading-routes) now separates
current maintainer routes from the historical construction plan and replaces
the dense kernel transition narrative with a bounded delivery summary and
links. Four earlier documentation notes now explain their original pending
review statements and point to later merged deliveries; their original
draft checkpoints remain intact. Four agent prompts, the pull-request
template, construction history and workflow research gained clearer terms.
Agent names, tools, models and permissions are unchanged.

The [ledger checkpoint through #186](aegis-documentation-readability-backlog.md#ledger-checkpoint-through-pull-request-186--2026-09-23)
records seven previously delivered readability batches without recounting
the skill/reference screens or forecast updates. Its 543-file count is
explicitly the earlier #186 snapshot. The completed bounded screens still
cover 186 skill entrypoint paths (185 shipped skills and one template), with
28 corrected pages, and 156 reference paths, with 49 corrected pages.
These are screening and correction counts, not full page-acceptance counts.
The ledger integration and this cycle's corrections leave the wider
documentation acceptance criteria open.

All five final pull-request revisions passed their Linux, Windows and
protected-file checks, and all five main-branch runs passed. The last main
run, [#191 verification 35927442963](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35927442963),
was confirmed successful at the exact merge before this draft froze.

All **14 selected** and **seven optional** open rows were reassessed against
the delivered scopes. No implementation, host, private-label or provider
work was delivered. Documentation advanced through bounded corrections,
but no complete remaining-page acceptance inventory or measured active-work
rate supports narrowing its 80–200-hour range. The previous and revised
selected totals remain **175–394 active hours**, comprising **95–194**
for non-documentation work and **80–200** for documentation.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate after #191 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic review and approved private labels remain |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | Pull request #139 remains unmerged pending its own guard disposition; real-host enforcement and operator controls remain |
| Work package 2B-3 execution support | 8–16 | 8–16 | The exact offline executor implementation grant and code remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Labels, reviewed source and allowance, development results and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path/profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live execution awaits calibration and selected-host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus execution follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Selected delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparative results remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Ledger integration through #186 and these bounded corrections are delivered; full page acceptance and the wider inventory remain |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation **95–194** plus documentation **80–200** |

All seven optional rows retain their ranges and selection gates.
[Strategic expansion](product-agnostic-skill-and-agent-roadmap.md) still
requires a bounded candidate batch informed by the [skills catalog](../skills-catalog.md).

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

Both optional issue #101 helpers add **16–40 active hours** if selected,
giving **191–434 active hours**. The full all-options backlog has no finite
estimate while optional quantities and architecture choices remain open.
Owner waits, GitHub queues, provider execution and host provisioning are
outside the active-hour estimates. Pull request #139 remains outside this
merged tree pending its own protected-file guard disposition; this forecast
grants no exception or implementation authority. Restart the five-merge
counter after #191, and revise sooner if verified scope or owner decisions change.

## Five-merge checkpoint — 2026-09-23, after pull request #196

Five requests merged after #191, in order #194, #192, #193, #195 and #196.
The exact base is the #196 merge
`437e73a7967d908b30fe9d919365ec2cf2ed035b`. All five delivered
documentation or forecast corrections. No selected implementation gate,
private-label review, provider authorization or selected-host prerequisite
closed. The [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-196--2026-09-23)
record the source timestamps, checks and elapsed intervals.

| Merged request and delivered scope | Previous estimate | New package estimate | First work to merge |
| --- | ---: | ---: | ---: |
| [#194](https://github.com/ModernNomad-98/Project-Aegis/pull/194), `d65d359a2ae621d923604bb0b715d7af0aa1255a`: preceding forecast | 1–2 h | 1–2 h | 9m52s |
| [#192](https://github.com/ModernNomad-98/Project-Aegis/pull/192), `fe5b6d76b3d382dd5939d66c3ee3904828c6b784`: category and application-path guidance | 2–4 h screen | 1–3 h correction | 11m36s |
| [#193](https://github.com/ModernNomad-98/Project-Aegis/pull/193), `cb9f1570d3d3144d485b728a19f845e73ba43b8d`: historical runner design and skill roadmap | 2–4 h screen | 1–3 h correction | 12m44s |
| [#195](https://github.com/ModernNomad-98/Project-Aegis/pull/195), `866fbd6d4ddf7033134fb1f42e665a22fcee88df`: stable current-forecast links | 2–4 h screen | 1–2 h correction | 9m40s |
| [#196](https://github.com/ModernNomad-98/Project-Aegis/pull/196), `437e73a7967d908b30fe9d919365ec2cf2ed035b`: control-plane verification-input guide | 2–4 h screen | 1–3 h correction | 11m09s |

Here **h**, **m** and **s** mean hours, minutes and seconds. The first work
checkpoint was 22:16:19 and the fifth merge event was 22:35:54 Coordinated
Universal Time (UTC), an observed **19m35s cycle span**. The package intervals
overlap. They include review, integration and GitHub waits; active effort was
not separately instrumented, so they are not a labor sum or a throughput rate
for the full documentation backlog. The preceding 2–4-hour screens cover
different review scope from these narrower correction PRs.

The exact #196 tree has **547 tracked Markdown files**, three more than the
#191 tree's 544. The added files are dated documentation evidence for #193,
#195 and #196. The 186 skill entrypoint paths and 156 reference paths screened
earlier remain bounded screens, not full-page acceptance. This cycle clarified
three category/path pages, a historical runner design and roadmap, the stable
forecast routes, and the control-plane verification guide. It did not finish
the remaining-page inventory or measured active-effort sample needed to
narrow the documentation estimate.

All five final pull-request heads passed their Linux, Windows and
protected-file checks before merge. The five exact-main runs also succeeded,
as recorded in the [execution measurements](aegis-execution-metrics.md#checkpoint-after-pull-request-196--2026-09-23).

All **14 selected** and **seven optional** rows were reassessed against the
five delivered scopes. The previous and revised selected totals remain
**175–394 active hours**, comprising **95–194** for non-documentation work
and **80–200** for repository-wide documentation. Narrow correction times
do not show how many full-page reviews and revisions remain.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Reason or remaining gate after #196 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Private replacement labels still need owner semantic review |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 remains outside main pending its separate protected-file disposition; real-host enforcement remains |
| Work package 2B-3 execution support | 8–16 | 8–16 | Exact offline holdout executor grant and implementation remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Reviewed labels/source/allowance, development result and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured tool-path/profile isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live suite still follows calibration and host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus still follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Guide clarified inputs; real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparison remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Bounded guide, category and roadmap corrections delivered; full page acceptance remains |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation **95–194** plus documentation **80–200** |

The seven optional rows also retain their ranges and selection gates:

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit helper choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit helper choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

Selecting both issue #101 helpers would add **16–40 active hours**, making
the bounded selected-plus-both total **191–434 active hours**. The full
all-options backlog remains unbounded while extra host/product quantities and
architecture choices are unset. Owner wait, GitHub queue, provider execution
and host provisioning remain outside active-hour estimates. Pull request
#197 is a separate protected-guide correction awaiting its own guard
disposition; it is not delivered by these five merges. Restart the five-merge
counter after #196, and re-estimate sooner if verified scope or an owner
decision materially changes remaining work.

## Five-merge checkpoint — 2026-09-23, after pull request #202

Five requests merged after #196, in order #198, #199, #200, #201 and #202.
The exact base is the #202 merge `867a4225cbeb72a2c06139adf7b1f7a2e19910b6`.
The [measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-202--2026-09-23)
records original estimates, starts, merge events, checks and limits. All five
delivered documentation or a forecast; no selected implementation gate closed.

| Merged request and delivered scope | Original package ETA | Observed first-work-to-merge wall time |
| --- | ---: | ---: |
| [#198](https://github.com/ModernNomad-98/Project-Aegis/pull/198), `24d613ebddd6ff4cd6ce35be772f6a80ad1a85f4`: preceding forecast | 1–2 active hours | 12m24s |
| [#199](https://github.com/ModernNomad-98/Project-Aegis/pull/199), `07459e464fb9d5284579d2a85637ee620b995bd2`: contributor merge guidance | 1–3 active hours | About 12 minutes; start recorded to minute precision |
| [#200](https://github.com/ModernNomad-98/Project-Aegis/pull/200), `cedd732df2ae9a843d2c02f213299a31b245a9c5`: documentation backlog current reading | 1–2 active hours | 10m53s |
| [#201](https://github.com/ModernNomad-98/Project-Aegis/pull/201), `6e163aa8567066819c1a4ba6c67d1cb284d039f8`: roadmap status and terms | 1–3 active hours | About 11 minutes; start recorded to minute precision |
| [#202](https://github.com/ModernNomad-98/Project-Aegis/pull/202), `867a4225cbeb72a2c06139adf7b1f7a2e19910b6`: pinned historical control-plane citations | 2–4 active hours | 12m58s |

Here **ETA** means estimated time to complete a bounded package; **m** and
**s** mean minutes and seconds. These overlapping wall intervals include
preparation, independent review, checks, integration and waiting. Active
effort was not separately measured; they cannot be added as labor or used to
extrapolate the remaining full-page documentation sweep. #199 and #201 have
minute-precision starts, so their durations are approximate. The exact
#202 tree has **551 tracked Markdown files**, four more than #196; these
five PRs added dated evidence notes and clarified current versus historical
reading. The separate protected-path requests #139 and #197 remain outside
main pending their own owner decisions.

All five final PR heads passed Linux, Windows and protected-file checks before
merge. All five exact-main runs also passed, including the
[#202 main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35932500973).

All **14 selected** and **seven optional** open rows were re-estimated. The
selected total remains **175–394 active hours**: **95–194** non-documentation
plus **80–200** repository-wide documentation. Corrections to several pages
did not establish full-page acceptance for the remaining repository inventory
or narrow the unmeasured implementation and host gates.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate after #202 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and label review of private replacement inputs remains |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 is unmerged; real-host enforcement remains |
| Work package 2B-3 execution support | 8–16 | 8–16 | Exact offline holdout executor grant and implementation remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Reviewed inputs, source, allowance, development result and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live suite follows calibration and host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparison remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 80–200 | Bounded guidance corrections landed; remaining full-page acceptance inventory is open |
| **Selected remaining total** | **175–394** | **175–394** | Non-documentation **95–194** plus documentation **80–200** |

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

Selecting both issue #101 helpers would add **16–40 active hours**, making
the bounded selected-plus-both total **191–434 active hours**. The full
all-options backlog remains unbounded while extra host/product quantities and
architecture choices are unset. Owner wait, GitHub queue, provider execution
and host provisioning are outside active-hour estimates. Restart the
five-merge counter after #202, and revise sooner if a verified scope change or
owner decision changes the remaining work.

## Documentation estimate audit — 2026-09-23, after pull request #205

The [documentation progress accounting](aegis-documentation-readability-backlog.md#progress-accounting-after-pull-request-205)
reconciles **553 tracked Markdown files** at the exact #205 merge. It
distinguishes 342 sorted skill screens, 83 corrected primary pages outside
those skill paths, 55 dated notes/tracking pages, 29 other reader-facing
pages and 44 synthetic fixtures. Those are disjoint file sets, not 553
completed full-page reviews. The repository had 491 tracked Markdown files
when the original 80–200-hour documentation estimate was made.

The selected remaining estimate stays **175–394 active hours**, including
**80–200 documentation hours**, pending a timed full-page sample across page
types. This is a conservative provisional range, not a conclusion that no
documentation work was done: 61 readability/correction requests changed 221
distinct Markdown paths, while 62 more Markdown files entered the inventory.
The shorter candidate residual model assumed minutes per long roadmap or
backlog page and was rejected as insufficient for full-page acceptance.
Re-estimate after the measured sample; keep the normal five-merge checkpoint.
No implementation or approval gate changes in this interim accounting.

## Documentation-batch estimate — 2026-09-24, after pull request #234

The [18-page skill batch](../evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md)
starts from the exact #234 merge
`5c46c7b3e61712674051eb734fa7d099a10aae4f`. Eighteen distinct
existing skill pages gain full-page acceptance after six independent
corrected-candidate reviews. One new dated review note raises the candidate
inventory from 575 to **576 Markdown pages**; accepted existing pages rise
from 431 to **449**, and **127 remain**: zero skill entrypoints/references,
48 previously corrected primary pages, 17 dated notes/tracking pages, 18
other reader pages and 44 synthetic fixtures. The new note remains pending.

The unchanged residual model calculates **26.25–101.8333 raw active hours**:
`48×8/60 + 17×3/60 + 18×20/60 + 1 + 8 + 4` at the lower end;
`48×25/60 + 17×10/60 + 18×60/60 + 3 + 20 + 8 + 30` at the upper end.
Outward five-hour planning bounds change documentation from **25–110** to
**25–105 active hours**. The other selected rows remain **95–194**, so
selected remaining work changes from **120–304** to **120–299 active
hours**. Both optional issue #101 helpers would make **136–339**; other
optional rows and the unbounded all-options status are unchanged. The
previous documentation estimate was **25–110**, and this batch's separate
estimate is **3–6 active hours**. The next full per-item checkpoint follows
five merges after the #233 forecast checkpoint; #234 is the first.

## Documentation-batch estimate — 2026-09-24, after pull request #233

The [40-page skill-reference batch](../evidence/documentation/full-page-readability-batch-after-233-2026-09-24.md)
starts from the exact #233 merge
`b545d07591f1508b197d708b33cfd2991d50db58`. Forty distinct existing
skill references gain full-page acceptance after independent corrected-candidate
review. One new dated review note raises the candidate inventory from 574 to
**575 Markdown pages**; accepted existing pages rise from 391 to **431**, and
**144 remain**: 18 skill pages, 48 previously corrected primary pages,
16 dated notes/tracking pages, 18 other reader pages and 44 synthetic
fixtures. The new note remains pending.

The unchanged #232 residual model calculates **27.4–105.2667 raw active
hours**: `18×4/60 + 48×8/60 + 16×3/60 + 18×20/60 + 1 + 8 + 4` at the
lower end; `18×12/60 + 48×25/60 + 16×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds narrow documentation
from **30–115** to **25–110 active hours**. The other 13 selected rows remain
**95–194**, so selected remaining work changes from **125–309** to
**120–304 active hours**. Both optional issue #101 helpers would make
**136–344**; other optional rows and the unbounded all-options status are
unchanged. The previous and current batch estimates are **6–12 active
hours**. The next full per-item checkpoint follows five subsequent merges
after the #233 forecast checkpoint.

## Documentation-batch estimate — 2026-09-24, after pull request #231

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-231-2026-09-24.md)
starts from the exact #231 merge
`65384f04696c699881b2ff0294b6ce63711c85cf`. Twenty skill references
gain full-page acceptance. One new review note brings the candidate
inventory to **574 Markdown pages**; **391 existing pages** have full-page
acceptance and **183 remain**. The disjoint pending buckets are **58 skill
pages, 48 previously corrected primary pages, 15 dated notes/tracking
pages, 18 other reader pages and 44 synthetic fixtures**. The new note
remains pending.

The unchanged #227 residual model calculates **30.0167–113.1 active
hours**: `58×4/60 + 48×8/60 + 15×3/60 + 18×20/60 + 1 + 8 + 4` at the
lower end; `58×12/60 + 48×25/60 + 15×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds narrow documentation
from **30–120** to **30–115 active hours**. The other 13 selected rows
remain **95–194**, so the selected total moves from **125–314** to
**125–309 active hours**. Both optional issue #101 helpers would make
**141–349**; other optional rows and the unbounded all-options status are
unchanged. This is the fifth completed merge after #227 if the candidate
merges; a full per-item checkpoint must follow its exact merge tree.

## Documentation-batch estimate — 2026-09-24, after pull request #230

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-230-2026-09-24.md)
starts from the exact #230 merge
`275678c96f934aecb85c0b9e3c9fbce2b1490c23`. Seven skill entrypoints
and thirteen skill references gain full-page acceptance. One new review note
brings the candidate inventory to **573 Markdown pages**; **371 existing
pages** have full-page acceptance and **202 remain**. The disjoint pending
buckets are **78 skill pages, 48 previously corrected primary pages,
14 dated notes/tracking pages, 18 other reader pages and 44 synthetic
fixtures**. The new note remains pending.

The unchanged #227 residual model calculates **31.3–116.9333 active
hours**: `78×4/60 + 48×8/60 + 14×3/60 + 18×20/60 + 1 + 8 + 4` at the
lower end; `78×12/60 + 48×25/60 + 14×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds narrow documentation
from **30–125** to **30–120 active hours**. The other 13 selected rows
remain **95–194**, so the selected total moves from **125–319** to
**125–314 active hours**. Both optional issue #101 helpers would make
**141–354**; other optional rows and the unbounded all-options status are
unchanged. This is the fourth completed merge after #227 if the candidate
merges; the next full per-item checkpoint follows one more merge.

## Documentation-batch estimate — 2026-09-24, after pull request #229

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-229-2026-09-24.md)
starts from the exact #229 merge
`b949422c1c4aca65ecf809cc48ff2d9c78aeede6`. Ten skill entrypoints
and ten skill references gain full-page acceptance. One new review note
brings the candidate inventory to **572 Markdown pages**; **351 existing
pages** have full-page acceptance and **221 remain**. The disjoint pending
buckets are **98 skill pages, 48 previously corrected primary pages,
13 dated notes/tracking pages, 18 other reader pages and 44 synthetic
fixtures**. The new note remains pending.

The unchanged #227 residual model calculates **32.5833–120.7667 active
hours**: `98×4/60 + 48×8/60 + 13×3/60 + 18×20/60 + 1 + 8 + 4` at the
lower end; `98×12/60 + 48×25/60 + 13×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds keep documentation at
**30–125 active hours**. The other 13 selected rows remain **95–194**,
so the selected total remains **125–319 active hours**. Both optional
issue #101 helpers would make **141–359**; other optional rows and the
unbounded all-options status are unchanged. This is the third completed
merge after #227 if the candidate merges; the next full per-item checkpoint
follows two more merges.

## Documentation-batch estimate — 2026-09-24, after pull request #228

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-228-2026-09-24.md)
starts from the exact #228 merge
`0bc4a8fcae32ccaab009ae9e0e23390ce4342f6a`. Ten skill entrypoints
and ten skill references gain full-page acceptance. One new review note
brings the candidate inventory to **571 Markdown pages**; **331 existing
pages** have full-page acceptance and **240 remain**. The disjoint pending
buckets are **118 skill pages, 48 previously corrected primary pages,
12 dated notes/tracking pages, 18 other reader pages and 44 synthetic
fixtures**. The new note remains pending.

The unchanged #227 residual model calculates **33.8667–124.6 active
hours**: `118×4/60 + 48×8/60 + 12×3/60 + 18×20/60 + 1 + 8 + 4` at the
lower end; `118×12/60 + 48×25/60 + 12×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds narrow documentation
from **35–130** to **30–125 active hours**. The other 13 selected rows
remain **95–194**, so the selected total moves from **130–324** to
**125–319 active hours**. Both optional issue #101 helpers would make
**141–359**; other optional rows and the unbounded all-options status are
unchanged. This is the second completed merge after #227 if the candidate
merges; the next full per-item checkpoint follows three more merges.

## Documentation-batch estimate — 2026-09-24, after pull request #226

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-226-2026-09-24.md)
starts from the exact #226 merge
`777f439327f6d9e3e602f1b42f25cd8a2cb7e7ac`. Ten skill entrypoints
and ten skill references gain full-page acceptance. One new review note
brings the candidate inventory to **570 Markdown pages**; **311 existing
pages** have full-page acceptance and **259 remain**. The disjoint pending
buckets are **138 skill pages, 48 previously corrected primary pages,
11 dated notes/tracking pages, 18 other reader pages and 44 synthetic
fixtures**. The new note remains pending.

The unchanged #222 residual model calculates **35.15–128.4333 active
hours**: `138×4/60 + 48×8/60 + 11×3/60 + 18×20/60 + 1 + 8 + 4` at the
lower end; `138×12/60 + 48×25/60 + 11×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds narrow documentation
from **35–135** to **35–130 active hours**. The other 13 selected rows
remain **95–194**, so the selected total moves from **130–329** to
**130–324 active hours**. Both optional issue #101 helpers would make
**146–364**; other optional rows and the unbounded all-options status are
unchanged. This is the fifth completed merge after #222 if the candidate
merges; a full per-item checkpoint must follow that exact merge tree.

## Documentation-batch estimate — 2026-09-24, after pull request #225

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-225-2026-09-24.md)
starts from the exact #225 merge
`bc9e48b070fe99085757ce1d9cb0b791640e0d42`. Ten skill entrypoints
and ten skill references gain full-page acceptance. One new review note
brings the candidate inventory to **569 Markdown pages**; **291 existing
pages** have full-page acceptance and **278 remain**. The disjoint pending
buckets are **158 skill pages, 48 previously corrected primary pages,
10 dated notes/tracking pages, 18 other reader pages and 44 synthetic
fixtures**. The new note remains pending.

The unchanged #222 residual model calculates **36.4333–132.2667 active
hours**: `158×4/60 + 48×8/60 + 10×3/60 + 18×20/60 + 1 + 8 + 4` at the
lower end; `158×12/60 + 48×25/60 + 10×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds narrow documentation
from **35–140** to **35–135 active hours**. The other 13 selected rows
remain **95–194**, so the selected total moves from **130–334** to
**130–329 active hours**. Both optional issue #101 helpers would make
**146–369**; other optional rows and the unbounded all-options status are
unchanged. This is the fourth completed merge after #222 if the candidate
merges; the full per-item checkpoint follows one more merge.

## Documentation-batch estimate — 2026-09-24, after pull request #224

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-224-2026-09-24.md)
starts from the exact #224 merge
`cf19639335158ffa09c02247d5d7b400f14fb522`. Ten skill entrypoints
and ten skill references gain full-page acceptance. One new review note
brings the candidate inventory to **568 Markdown pages**; **271 existing
pages** have full-page acceptance and **297 remain**. The disjoint pending
buckets are **178 skill pages, 48 previously corrected primary pages,
9 dated notes/tracking pages, 18 other reader pages and 44 synthetic
fixtures**. The new note remains pending; one already accepted entrypoint
was replaced before counting.

The unchanged #222 residual model calculates **37.7167–136.1 active
hours**: `178×4/60 + 48×8/60 + 9×3/60 + 18×20/60 + 1 + 8 + 4` at the
lower end; `178×12/60 + 48×25/60 + 9×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds remain **35–140
documentation hours**. The other 13 selected rows remain **95–194**, so
the selected total remains **130–334 active hours**. Both optional issue
#101 helpers would make **146–374**; other optional rows and the
unbounded all-options status are unchanged. This is the second completed
merge after #222 if the candidate merges; the next full per-item checkpoint
follows three more merges unless a material decision changes scope sooner.

## Documentation-batch estimate — 2026-09-24, after pull request #223

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-223-2026-09-24.md)
starts from the exact #223 merge
`6ccf20a8d5cbcd355d27b4ebf38980d6724959ba`. Ten skill entrypoints
and ten skill references gain full-page acceptance. One new review note
brings the candidate inventory to **567 Markdown pages**; **251 existing
pages** have full-page acceptance and **316 remain**. The disjoint pending
buckets are **198 skill pages, 48 previously corrected primary pages,
8 dated notes/tracking pages, 18 other reader pages and 44 synthetic
fixtures**. The new note remains pending; two already accepted references
were excluded before counting.

The unchanged #222 residual model calculates **39–139.9333 active hours**:
`198×4/60 + 48×8/60 + 8×3/60 + 18×20/60 + 1 + 8 + 4` at the lower end;
`198×12/60 + 48×25/60 + 8×10/60 + 18×60/60 + 3 + 20 + 8 + 30` at the
upper end. Outward five-hour planning bounds change documentation from
**40–145** to **35–140 active hours**. The other 13 selected rows remain
**95–194**, so the selected total changes from **135–339** to **130–334
active hours**. Both optional issue #101 helpers would make **146–374**;
other optional rows and the unbounded all-options status are unchanged.
This checkpoint merge #223 is the first completed merge after #222; the
next full per-item checkpoint follows four more merges unless a material
decision changes scope sooner.

## Five-merge checkpoint — 2026-09-24, after pull request #232

Five requests merged after #227, in order #228, #229, #230, #231 and #232.
The exact base is the #232 merge
`970aad27524bccc8a3f342bc990215904253be53`. The
[measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-232--2026-09-24)
records each original estimate beside its observed available wall interval.
All five exact-head Linux, Windows and protected-file checks passed. All
five exact-main runs passed, including [#232](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35966166419).

| Merged request and scope | Merge commit | Original package ETA | Observed available wall interval |
| --- | --- | ---: | ---: |
| [#228](https://github.com/ModernNomad-98/Project-Aegis/pull/228): previous five-merge checkpoint | `0bc4a8fcae32ccaab009ae9e0e23390ce4342f6a` | 1–2 active hours | 8m50s prior merge to merge |
| [#229](https://github.com/ModernNomad-98/Project-Aegis/pull/229): 20-page acceptance batch | `b949422c1c4aca65ecf809cc48ff2d9c78aeede6` | 3–6 active hours | 19m12s prior merge to merge |
| [#230](https://github.com/ModernNomad-98/Project-Aegis/pull/230): 20-page acceptance batch | `275678c96f934aecb85c0b9e3c9fbce2b1490c23` | 3–6 active hours | 18m45s prior merge to merge |
| [#231](https://github.com/ModernNomad-98/Project-Aegis/pull/231): 20-page acceptance batch | `65384f04696c699881b2ff0294b6ce63711c85cf` | 3–6 active hours | 18m36s prior merge to merge |
| [#232](https://github.com/ModernNomad-98/Project-Aegis/pull/232): 20-page acceptance batch | `970aad27524bccc8a3f342bc990215904253be53` | 3–6 active hours | 18m30s prior merge to merge |

GitHub `mergedAt` receipts and the published PR comments give **1h23m53s**
across these five prior-merge-to-merge intervals. First-work timestamps and
active-only, review, CI, queue and owner-wait splits are unavailable. These
wall intervals cannot be used as an active-work throughput rate. No
non-documentation package or owner gate closed in these merges.

The exact merge tree has **574 tracked Markdown pages**. Four distinct
20-page documentation batches accepted **80 existing pages** after the
previous checkpoint's 311, yielding **391 accepted** and **183 pending**.
Four new dated review notes entered the inventory. Disjoint pending buckets
are **58 skill, 48 previously corrected primary, 15 dated note/tracking,
18 other reader and 44 synthetic fixture pages**. Earlier focused screens
remain progress, not full-page acceptance; hash-pinned Scenario A fixtures
remain unchanged and pending.

The unchanged residual model assigns 4–12 minutes per skill page, 8–25
per corrected primary page, 3–10 per dated note and 20–60 per other
reader page; fixtures add 1–3 hours, corrections 8–20, integration 4–8,
and the upper tail 0–30. Exact bucket arithmetic is
`58×4/60 + 48×8/60 + 15×3/60 + 18×20/60 + 1 + 8 + 4` = **30.0167**
at the lower end, and
`58×12/60 + 48×25/60 + 15×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
= **113.1 active hours** at the upper end. Outward five-hour planning
bounds are **30–115 documentation hours**. The four batches evidence page
acceptance; they do not measure active-work rate or justify changing the
per-page assumptions.

The next documentation acceptance package will target **40 pages** to reduce
per-PR and CI overhead. Two read-only reviewers will each audit 20 distinct
pages, with a page-level disposition and independent corrected-candidate
review before merge. This changes packaging, not the per-page residual model
or any authorization gate; the batch ETA will be stated when that work starts.

| Selected open work item | Previous #227 remaining active hours | Revised remaining active hours | Remaining gate after #232 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and label review of private replacement inputs |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | PR #139 guard disposition; real-host enforcement later |
| Work package 2B-3 execution support | 8–16 | 8–16 | Separate exact offline holdout executor grant and implementation |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Reviewed inputs, source, allowance, development result and holdout freeze |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation |
| Work package 2B-4 | 12–24 | 12–24 | Calibration and host proof before limited live suite |
| Work package 2B-5 | 8–16 | 8–16 | Package 2B-4 gate before generic corpus |
| Work package 2B-6 | 8–16 | 8–16 | Later scheduling, cost, quarantine and dataset operations |
| Work package 2B-7 | 4–8 | 4–8 | Later advisory continuous integration and operator workflow |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and package-003 prerequisites |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparison |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation after selected integration outcomes |
| Repository-wide documentation readability | 35–130 | **30–115** | 183 pages lack full-page acceptance; timed stratified review remains |
| **Selected remaining total** | **130–324** | **125–309** | Non-documentation **95–194** plus documentation **30–115** |

The seven optional rows were rechecked separately. Issue #101 package 5
remains **8–20** active hours if selected; package 6 remains **8–20**
and needs provider authority. Behavioral Eval Runner item 010 remains
**4–12**, item 014 **8–20 per selected host**, and item 015 **8–24
per selected product**. Strategic skill expansion and framework coverage
remain unbounded until a candidate batch is selected; multi-judge
arbitration and future control-plane architecture remain unbounded
pending adoption decisions. Both optional issue #101 helpers together
would add **16–40**, making selected-plus-both **141–349 active hours**.
The full all-options backlog has no finite total. PR #139 and #197 remain
open with failed protected-file guards, requiring separate owner
dispositions. The separate Behavioral Eval Runner holdout-executor
implementation grant remains pending; live/provider execution has further
gates. Restart the five-merge counter after #232 and revise sooner if a
verified scope or owner decision materially changes remaining work.

## Five-merge checkpoint — 2026-09-24, after pull request #227

Five requests merged after #222, in order #223, #224, #225, #226 and #227.
The exact base is the #227 merge
`88cc83fc547495b4f4d10eb5af76a4879c05af15`. The
[measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-227--2026-09-24)
records original estimates beside observed available wall intervals. All five
exact-head Linux, Windows and protected-file checks passed. All five
exact-main runs passed, including [#227](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35959689686).
Active labor, review and queue time were not
separately instrumented.

| Merged request and scope | Merge commit | Original package ETA | Observed available wall interval |
| --- | --- | ---: | ---: |
| [#223](https://github.com/ModernNomad-98/Project-Aegis/pull/223): previous five-merge checkpoint | `6ccf20a8d5cbcd355d27b4ebf38980d6724959ba` | 1–2 active hours | About 9m27s first work to merge |
| [#224](https://github.com/ModernNomad-98/Project-Aegis/pull/224): 20-page acceptance batch | `cf19639335158ffa09c02247d5d7b400f14fb522` | 3–6 active hours | About 19m15s first work to merge |
| [#225](https://github.com/ModernNomad-98/Project-Aegis/pull/225): 20-page acceptance batch | `bc9e48b070fe99085757ce1d9cb0b791640e0d42` | 3–6 active hours | About 20m20s first work to merge |
| [#226](https://github.com/ModernNomad-98/Project-Aegis/pull/226): 20-page acceptance batch | `777f439327f6d9e3e602f1b42f25cd8a2cb7e7ac` | 3–6 active hours | 16m44s prior merge to this merge; first-work start unavailable |
| [#227](https://github.com/ModernNomad-98/Project-Aegis/pull/227): 20-page acceptance batch | `88cc83fc547495b4f4d10eb5af76a4879c05af15` | 3–6 active hours | 17m54s prior merge to this merge; first-work start unavailable |

The exact merge tree has **570 tracked Markdown pages**. Four distinct
20-page documentation batches accepted **80 existing pages** after the
previous checkpoint's 231, yielding **311 accepted** and **259 pending**.
Four new dated review notes entered the inventory. Disjoint pending buckets
are **138 skill, 48 previously corrected primary, 11 dated note/tracking,
18 other reader and 44 synthetic fixture pages**. Earlier focused screens
remain progress, not full-page acceptance; hash-pinned Scenario A fixtures
remain unchanged and pending.

The unchanged residual model assigns 4–12 minutes per skill page, 8–25
per corrected primary page, 3–10 per dated note and 20–60 per other
reader page; fixtures add 1–3 hours, corrections 8–20, integration 4–8,
and the upper tail 0–30. Exact bucket arithmetic is
`138×4/60 + 48×8/60 + 11×3/60 + 18×20/60 + 1 + 8 + 4` = **35.15**
at the lower end, and
`138×12/60 + 48×25/60 + 11×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
= **128.4333 active hours** at the upper end. Outward five-hour planning
bounds are **35–130 documentation hours**. The four batches evidence page
acceptance; they do not measure active-work rate or justify changing the
per-page assumptions. No non-documentation package or owner gate closed.

| Selected open work item | Previous #222 remaining active hours | Revised remaining active hours | Remaining gate after #227 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and label review of private replacement inputs |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | PR #139 guard disposition; real-host enforcement later |
| Work package 2B-3 execution support | 8–16 | 8–16 | Separate exact offline holdout executor grant and implementation |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Reviewed inputs, source, allowance, development result and holdout freeze |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation |
| Work package 2B-4 | 12–24 | 12–24 | Calibration and host proof before limited live suite |
| Work package 2B-5 | 8–16 | 8–16 | Package 2B-4 gate before generic corpus |
| Work package 2B-6 | 8–16 | 8–16 | Later scheduling, cost, quarantine and dataset operations |
| Work package 2B-7 | 4–8 | 4–8 | Later advisory continuous integration and operator workflow |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and package-003 prerequisites |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparison |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation after selected integration outcomes |
| Repository-wide documentation readability | 40–145 | **35–130** | 259 pages lack full-page acceptance; timed stratified review remains |
| **Selected remaining total** | **135–339** | **130–324** | Non-documentation **95–194** plus documentation **35–130** |

The seven optional rows were rechecked separately. Issue #101 package 5
remains **8–20** active hours if selected; package 6 remains **8–20**
and needs provider authority. Behavioral Eval Runner item 010 remains
**4–12**, item 014 **8–20 per selected host**, and item 015 **8–24
per selected product**. Strategic skill expansion and framework coverage
remain unbounded until a candidate batch is selected; multi-judge
arbitration and future control-plane architecture remain unbounded
pending adoption decisions. Both optional issue #101 helpers together
would add **16–40**, making selected-plus-both **146–364 active hours**.
The full all-options backlog has no finite total. PR #139 and #197 remain
open with failed protected-file guards, requiring separate owner
dispositions. The separate Behavioral Eval Runner holdout-executor
implementation grant remains pending; live/provider execution has further
gates. Restart the five-merge counter after #227 and revise sooner if a
verified scope or owner decision materially changes remaining work.

## Five-merge checkpoint — 2026-09-24, after pull request #222

Five requests merged after #217, in order #218, #219, #220, #221 and #222.
The exact base is the #222 merge
`7a913818c49bd0d5ee4a07faee6cb75bc0b524de`. The
[measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-222--2026-09-24)
records each original estimate beside its observed wall interval. Exact-head
Linux, Windows and protected-file checks and exact-main runs passed for all
five requests, including the #222 [exact-main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35953714246).
Wall intervals include review and CI wait; active labor was not separately
instrumented.

| Merged request and scope | Merge commit | Original package ETA | Observed first-work-to-merge wall time |
| --- | --- | ---: | ---: |
| [#218](https://github.com/ModernNomad-98/Project-Aegis/pull/218): previous five-merge checkpoint | `694333c0b7ebc697272b03705700c845fcc6462a` | 1–2 active hours | About 6m41s |
| [#219](https://github.com/ModernNomad-98/Project-Aegis/pull/219): 20-page acceptance batch | `dbad6c25c11179489c6c8f78aca387a3b768995c` | 3–6 active hours | About 14m57s |
| [#220](https://github.com/ModernNomad-98/Project-Aegis/pull/220): 20-page acceptance batch | `afe5f456ccf20cba8a8cf3e168fdfd547dd1b80c` | 3–6 active hours | About 15m48s |
| [#221](https://github.com/ModernNomad-98/Project-Aegis/pull/221): 20-page acceptance batch | `c0a3d1d4de64ce9f7307c22d2dbddaaf149c6239` | 3–6 active hours | About 17m27s |
| [#222](https://github.com/ModernNomad-98/Project-Aegis/pull/222): 20-page acceptance batch | `7a913818c49bd0d5ee4a07faee6cb75bc0b524de` | 3–6 active hours | About 17m49s |

The exact merge tree has **566 tracked Markdown pages**. Four distinct
20-page documentation batches accepted **80 existing pages** after the
previous checkpoint's 151, yielding **231 accepted** and **335 pending**.
Four new dated review notes entered the inventory. Disjoint pending buckets
are **218 skill, 48 previously corrected primary, 7 dated note/tracking,
18 other reader and 44 synthetic fixture pages**. Earlier focused screens
remain progress, not full-page acceptance. The hash-pinned Scenario A
fixtures remain unchanged and pending.

The unchanged residual model assigns 4–12 minutes per skill page, 8–25
per corrected primary page, 3–10 per dated note and 20–60 per other
reader page; fixtures add 1–3 hours, corrections 8–20, integration 4–8,
and the upper tail 0–30. The exact bucket arithmetic is
`218×4/60 + 48×8/60 + 7×3/60 + 18×20/60 + 1 + 8 + 4` = **40.2833**
at the lower end, and
`218×12/60 + 48×25/60 + 7×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
= **143.7667 active hours** at the upper end. Outward five-hour planning
bounds are **40–145 documentation hours**. The four batches are evidence of
accepted pages, not a measured active-work rate, so they do not justify
changing the residual per-page assumptions. No non-documentation package or
owner gate closed in these five merges.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate after #222 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and label review of private replacement inputs |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | PR #139 guard disposition; real-host enforcement later |
| Work package 2B-3 execution support | 8–16 | 8–16 | Separate exact offline holdout executor grant and implementation |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Reviewed inputs, source, allowance, development result and holdout freeze |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation |
| Work package 2B-4 | 12–24 | 12–24 | Calibration and host proof before limited live suite |
| Work package 2B-5 | 8–16 | 8–16 | Package 2B-4 gate before generic corpus |
| Work package 2B-6 | 8–16 | 8–16 | Later scheduling, cost, quarantine and dataset operations |
| Work package 2B-7 | 4–8 | 4–8 | Later advisory continuous integration and operator workflow |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and package-003 prerequisites |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparison |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation after selected integration outcomes |
| Repository-wide documentation readability | 40–150 | **40–145** | 335 pages lack full-page acceptance; timed stratified review remains |
| **Selected remaining total** | **135–344** | **135–339** | Non-documentation **95–194** plus documentation **40–145** |

The seven optional rows were rechecked separately. Issue #101 package 5
remains **8–20** active hours if selected; package 6 remains **8–20**
and needs provider authority. Behavioral Eval Runner item 010 remains
**4–12**, item 014 **8–20 per selected host**, and item 015 **8–24
per selected product**. Strategic skill expansion and framework coverage
remain unbounded until a candidate batch is selected; multi-judge
arbitration and future control-plane architecture remain unbounded
pending adoption decisions. Both optional issue #101 helpers together
would add **16–40**, making selected-plus-both **151–379 active hours**.
The full all-options backlog has no finite total. PR #139 and #197 remain
open with failed protected-file guards, requiring separate owner
dispositions. The separate Behavioral Eval Runner holdout-executor
implementation grant remains pending; live/provider execution has further
gates. Start the next five-merge counter after #222 and revise sooner if
verified scope or an owner decision materially changes remaining work.

## Documentation-batch estimate — 2026-09-24, after pull request #221

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-221-2026-09-24.md)
starts from the exact #221 merge
`c0a3d1d4de64ce9f7307c22d2dbddaaf149c6239`. Ten skill entrypoints
and ten skill references gain full-page acceptance. One new review note
brings the candidate inventory to **566 Markdown pages**; **231 existing
pages** have full-page acceptance and **335 remain**. The disjoint pending
buckets are **218 skill pages, 48 previously corrected primary pages, 7
dated notes/tracking pages, 18 other reader pages and 44 synthetic fixtures**.
The new note remains pending. Hash-pinned Scenario A fixtures were examined
but remain pending and unchanged.

The unchanged #217 residual model calculates **40.2833–143.7667 active
hours**: `218×4/60 + 48×8/60 + 7×3/60 + 18×20/60 + 1 + 8 + 4` at the lower
end; `218×12/60 + 48×25/60 + 7×10/60 + 18×60/60 + 3 + 20 + 8 + 30` at the
upper end. Outward five-hour planning bounds change documentation from
**40–150** to **40–145 active hours**. The other 13 selected rows remain
**95–194**, so the selected total changes from **135–344** to **135–339
active hours**. Both optional issue #101 helpers would make **151–379**;
other optional rows and the unbounded all-options status are unchanged.
This is the fifth merge after #217 if the candidate merges; the next PR
must perform the full per-item forecast checkpoint against that exact merge
tree unless a material decision changes scope sooner.

## Documentation-batch estimate — 2026-09-24, after pull request #220

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-220-2026-09-24.md)
starts from the exact #220 merge
`afe5f456ccf20cba8a8cf3e168fdfd547dd1b80c`. Ten skill entrypoints
and ten dated evidence notes gain full-page acceptance. One new review note
brings the candidate inventory to **565 Markdown pages**; **211 existing
pages** have full-page acceptance and **354 remain**. The disjoint pending
buckets are **238 skill pages, 48 previously corrected primary pages, 6
dated notes/tracking pages, 18 other reader pages and 44 synthetic fixtures**.
The new note remains pending.

The unchanged #217 residual model calculates **41.5667–147.6 active hours**:
`238×4/60 + 48×8/60 + 6×3/60 + 18×20/60 + 1 + 8 + 4` at the lower end;
`238×12/60 + 48×25/60 + 6×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds change documentation
from **40–155** to **40–150 active hours**. The other 13 selected rows remain
**95–194**, so the selected total changes from **135–349** to **135–344
active hours**. Both optional issue #101 helpers would make **151–384**;
other optional rows and the unbounded all-options status are unchanged.
This is the third merge after #217; a full per-item checkpoint follows two
more merges unless a material decision changes scope sooner.

## Documentation-batch estimate — 2026-09-24, after pull request #219

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-219-2026-09-24.md)
starts from the exact #219 merge
`dbad6c25c11179489c6c8f78aca387a3b768995c`. Ten skill entrypoints
and ten dated evidence notes gain full-page acceptance. One new review note
brings the candidate inventory to **564 Markdown pages**; **191 existing
pages** have full-page acceptance and **373 remain**. The disjoint pending
buckets are **248 skill pages, 48 previously corrected primary pages, 15
dated notes/tracking pages, 18 other reader pages and 44 synthetic fixtures**.
The new note remains pending.

The unchanged #217 residual model calculates **42.6833–151.1 active hours**:
`248×4/60 + 48×8/60 + 15×3/60 + 18×20/60 + 1 + 8 + 4` at the lower end;
`248×12/60 + 48×25/60 + 15×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds remain **40–155
documentation hours**. The other 13 selected rows remain **95–194**, so
the selected total remains **135–349 active hours**. Both optional issue
#101 helpers would make **151–389**; other optional rows and the unbounded
all-options status are unchanged. This is the second merge after #217;
the next full per-item checkpoint follows three more merges, or a material
decision changing scope.

## Documentation-batch estimate — 2026-09-24, after pull request #218

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-218-2026-09-24.md)
starts from the exact #218 merge
`694333c0b7ebc697272b03705700c845fcc6462a`. Ten existing skill
entrypoints and ten existing evidence pages gain full-page acceptance.
One new review note brings the candidate inventory to **563 Markdown
pages**; **171 existing pages** have full-page acceptance and **392
remain**. The disjoint pending buckets are **258 skill pages, 48
previously corrected primary pages, 24 dated notes/tracking pages, 18
other reader pages and 44 synthetic fixtures**. The new note remains
pending.

The unchanged #217 residual model calculates **43.8–154.6 active hours**:
`258×4/60 + 48×8/60 + 24×3/60 + 18×20/60 + 1 + 8 + 4` at the lower end;
`258×12/60 + 48×25/60 + 24×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds are **40–155
documentation hours**. The other 13 selected rows remain **95–194**,
so the selected total changes from **135–354** to **135–349 active
hours**. Both optional issue #101 helpers would make **151–389**;
other optional rows and the unbounded all-options status are unchanged.
The next full per-item checkpoint is due after five merges following
#217, or sooner if a material decision changes scope.

## Five-merge checkpoint — 2026-09-24, after pull request #217

Five requests merged after #212, in order #213, #214, #215, #216 and #217.
The exact base is the #217 merge
`f6a05e97b68108a9de0c81f37ce48b8ffe55d78c`. The
[measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-217--2026-09-24)
records the estimates and wall intervals. Every exact-head Linux, Windows
and protected-file check passed. All five exact-main runs passed, including
the #217 [exact-main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35948498380).
Wall intervals include review and CI
wait and do not measure active labor.

| Merged request and scope | Merge commit | Original package ETA | Observed first-work-to-merge wall time |
| --- | --- | ---: | ---: |
| [#213](https://github.com/ModernNomad-98/Project-Aegis/pull/213): previous five-merge forecast | `620f0268edcab0259153958a3174884b75d8a178` | 1–2 active hours | About 9m48s |
| [#214](https://github.com/ModernNomad-98/Project-Aegis/pull/214): 20-page acceptance batch | `cdacb2ff93446144c8aaf6c34cdbbb91c3b48aac` | 3–6 active hours | About 17m50s |
| [#215](https://github.com/ModernNomad-98/Project-Aegis/pull/215): 20-page acceptance batch | `4e09c54b511a43672c282bc75c41061ec4f2f878` | 3–6 active hours | About 12m50s |
| [#216](https://github.com/ModernNomad-98/Project-Aegis/pull/216): 20-page acceptance batch | `d759f26527017574154a23c0748e659a75ef8b71` | 3–6 active hours | About 15m04s |
| [#217](https://github.com/ModernNomad-98/Project-Aegis/pull/217): 20-page acceptance batch | `f6a05e97b68108a9de0c81f37ce48b8ffe55d78c` | 3–6 active hours | About 16m07s |

The exact merge tree has **562 tracked Markdown pages**. The four
documentation batches accepted 80 distinct existing pages after the
previous checkpoint's 71, yielding **151 accepted pages** and **411
pending**. Four new dated review notes entered the inventory. The
disjoint pending buckets are **268 skill, 48 previously corrected
primary, 33 dated note/tracking, 18 other reader and 44 synthetic
fixture pages**. Earlier focused screens remain progress, not full-page
acceptance.

The unchanged residual model assigns 4–12 minutes per skill page, 8–25
per corrected primary page, 3–10 per dated note and 20–60 per other
reader page; fixtures add 1–3 hours, corrections 8–20, integration 4–8,
and the upper tail 0–30. The exact bucket arithmetic is
**44.9167–158.1 active hours**, rounded outward to **40–160** for
documentation. This is a planning range, not a measured page rate.
No non-documentation implementation or owner gate closed in these five
merges. PR #139 and #197 remain open with passing Linux/Windows checks
and failed protected-file guards; each needs its own owner disposition.
The separate Behavioral Eval Runner holdout-executor implementation grant
remains pending; live/provider execution has its own further gates.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate after #217 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and label review of private replacement inputs |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | PR #139 guard disposition; real-host enforcement later |
| Work package 2B-3 execution support | 8–16 | 8–16 | Separate exact offline holdout executor grant and implementation |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Reviewed inputs, source, allowance, development result and holdout freeze |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation |
| Work package 2B-4 | 12–24 | 12–24 | Calibration and host proof before limited live suite |
| Work package 2B-5 | 8–16 | 8–16 | Package 2B-4 gate before generic corpus |
| Work package 2B-6 | 8–16 | 8–16 | Later scheduling, cost, quarantine and dataset operations |
| Work package 2B-7 | 4–8 | 4–8 | Later advisory continuous integration and operator workflow |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and package-003 prerequisites |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparison |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation after selected integration outcomes |
| Repository-wide documentation readability | 50–175 | **40–160** | 411 pages lack full-page acceptance; timed stratified review remains |
| **Selected remaining total** | **145–369** | **135–354** | Non-documentation **95–194** plus documentation **40–160** |

The seven optional rows are rechecked separately. Issue #101 package 5
remains **8–20** active hours if selected; package 6 remains **8–20**
and needs provider authority. Behavioral Eval Runner item 010 remains
**4–12**, item 014 **8–20 per selected host**, and item 015 **8–24
per selected product**. Strategic skill expansion and framework coverage
remain unbounded until a candidate batch is selected; multi-judge
arbitration and future control-plane architecture remain unbounded
pending adoption decisions. Both optional issue #101 helpers together
would add **16–40**, making selected-plus-both **151–394 active hours**.
The full all-options backlog has no finite total. Start the next
five-merge counter after #217 and revise sooner if verified scope or an
owner decision materially changes remaining work.

## Documentation-batch estimate — 2026-09-24, after pull request #216

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-216-2026-09-24.md)
starts from the exact #216 merge
`d759f26527017574154a23c0748e659a75ef8b71`. Ten existing skill
entrypoints and ten existing evidence pages gain full-page acceptance. One
new review note brings the candidate inventory to **562 Markdown pages**;
**151 existing pages** have full-page acceptance and **411 remain**. The
disjoint pending buckets are **268 skill pages, 48 previously corrected
primary pages, 33 dated notes/tracking pages, 18 other reader pages and
44 synthetic fixtures**. The new note remains pending.

The unchanged #212 residual model calculates **44.92–158.1 active hours**:
`268×4/60 + 48×8/60 + 33×3/60 + 18×20/60 + 1 + 8 + 4` at the lower end;
`268×12/60 + 48×25/60 + 33×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds are **40–160
documentation hours**. The other 13 selected rows remain **95–194**, so
the selected total changes from **140–359** to **135–354 active hours**.
Both optional issue #101 helpers would make **151–394**; other optional
rows and the unbounded all-options status are unchanged. Because this
batch is the fifth merge candidate since #212, the next work item is the
required full five-merge forecast checkpoint.

## Documentation-batch estimate — 2026-09-24, after pull request #215

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-215-2026-09-24.md)
starts from the exact #215 merge
`4e09c54b511a43672c282bc75c41061ec4f2f878`. Ten existing skill
entrypoints and ten existing evidence pages gain full-page acceptance. One
new review note brings the candidate inventory to **561 Markdown pages**;
**131 existing pages** have full-page acceptance and **430 remain**. The
disjoint pending buckets are **278 skill pages, 48 previously corrected
primary pages, 42 dated notes/tracking pages, 18 other reader pages and
44 synthetic fixtures**. The new note remains pending.

Using the unchanged #212 residual assumptions gives
**46.03–161.6 active hours**:
`278×4/60 + 48×8/60 + 42×3/60 + 18×20/60 + 1 + 8 + 4` at the lower end;
`278×12/60 + 48×25/60 + 42×10/60 + 18×60/60 + 3 + 20 + 8 + 30`
at the upper end. Outward five-hour planning bounds are **45–165
documentation hours**. The other 13 selected rows remain **95–194**, so
the selected total changes from **140–364** to **140–359 active hours**.
Both optional issue #101 helpers would make **156–399**; other optional
rows and the unbounded all-options status are unchanged. A full per-item
re-estimate is next due after five merges following #212, or sooner if a
material decision changes scope.

## Documentation-batch estimate — 2026-09-24, after pull request #214

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-214-2026-09-24.md)
starts from the #214 merge `cdacb2ff93446144c8aaf6c34cdbbb91c3b48aac`.
It accepts ten existing skill entrypoints and ten existing evidence pages.
One new review note brings the candidate inventory to **560 Markdown pages**;
**111 existing pages** have full-page acceptance and **449 remain**. The
disjoint pending buckets are **288 skill pages, 48 previously corrected
primary pages, 51 dated notes/tracking pages, 18 other reader pages and 44
synthetic fixtures**. The new note remains pending.

The unchanged residual model calculates **47.15–165.1 active hours**. Its
outward five-hour planning range remains **45–170 documentation hours**;
progress narrows the raw model but does not justify a new rounded bound.
The other 13 selected rows remain **95–194**, so the selected total remains
**140–364 active hours**. Both optional issue #101 helpers would make
**156–404**; other optional rows and the unbounded all-options status are
unchanged. A full per-item re-estimate is next due after five merges following
#212, or sooner if a material decision changes scope.

## Documentation-batch estimate — 2026-09-24, after pull request #213

The [next 20-page acceptance batch](../evidence/documentation/full-page-readability-batch-after-213-2026-09-24.md)
starts from the #213 merge `620f0268edcab0259153958a3174884b75d8a178`.
Ten skill entrypoints and ten historical evidence pages received full-page
review; two of the evidence pages needed no edit. The candidate tree adds one
review note, bringing the inventory to **559 tracked Markdown pages**. The
recorded accepted-existing count rises from 71 to **91**, leaving **468**.
Disjoint pending buckets become **298 skill pages, 49 previously corrected
primary pages, 59 notes or tracking pages, 18 other reader pages and 44
synthetic fixtures**. The added note remains pending as a newly created page.

The unchanged #212 per-page assumptions and reserves give **48.35–168.85
active hours** for the residual documentation work. Rounding outward to a
five-hour planning range yields **45–170**, from **50–175**. The other 13
selected work items remain **95–194** because no non-documentation gate
closed; the selected total becomes **140–364**, from **145–369**. Both optional
issue #101 helpers would make **156–404**. All other optional rows and the
unbounded all-options status remain unchanged. This is an interim progress
update; the next complete per-item checkpoint remains due after five merges
following #212.

## Five-merge checkpoint — 2026-09-24, after pull request #212

Five requests merged after #207, in order #208, #209, #210, #211 and #212.
The exact base is the #212 merge `ba24016d209be6e49171be52332887558db16ab2`.
The [measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-212--2026-09-24)
records each original estimate and observed wall interval. All three exact-head
checks passed for each request. The #212 [exact-main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35942609209)
passed at the merge commit. These short documentation and correction intervals
do not measure active coding throughput; owner waiting and GitHub queue time
are excluded from the estimates below.

| Merged request and scope | Merge commit | Original package ETA | Observed first-work-to-merge wall time |
| --- | --- | ---: | ---: |
| [#208](https://github.com/ModernNomad-98/Project-Aegis/pull/208): preceding forecast | `754fc7a02f85c1f05dc32b4bbd70c1b616979b50` | 1–2 active hours | About 11m27s |
| [#209](https://github.com/ModernNomad-98/Project-Aegis/pull/209): 21-page acceptance batch | `f1bfaece5b68551f75e910470becd17ed61ccb7e` | 3–6 active hours | About 19m31s |
| [#210](https://github.com/ModernNomad-98/Project-Aegis/pull/210): 20-page acceptance batch | `80fbdbb4b6319dc1e7cafc9a57235a77360f9763` | 3–6 active hours | About 25m24s |
| [#211](https://github.com/ModernNomad-98/Project-Aegis/pull/211): retry semantics correction | `2efae405d555815383abc1d9f713f3e4549eef84` | 1–2 active hours | About 10m29s |
| [#212](https://github.com/ModernNomad-98/Project-Aegis/pull/212): 20-page acceptance batch | `ba24016d209be6e49171be52332887558db16ab2` | 3–6 active hours | About 16m10s |

The exact tree has **558 tracked Markdown pages**. The earlier nine-page
sample, the 21 and 20-page batches, the one-page retry correction and the
latest 20-page batch accepted **71 distinct existing pages**. Four new dated
notes entered the inventory after #207; therefore **487 pages** lack recorded
full-page acceptance. The disjoint pending buckets are **308 skill pages,
59 previously corrected primary pages, 58 dated notes or tracking pages,
18 other reader pages and 44 synthetic fixtures**. Earlier sorted screens
remain progress, not full-page acceptance.

The residual model retains the #207 per-page assumptions: 4–12 minutes for
each skill page, 8–25 for each corrected primary page, 3–10 for each dated
note, and 20–60 for each other reader page. Fixtures add 1–3 active hours,
corrections 8–20, integration 4–8, and the upper tail 0–30. The arithmetic is
**50.3–174.85 active hours**, rounded to **50–175** for documentation. This
is a planning range; a timed stratified review is still needed to calibrate
the per-page rates. No non-documentation implementation or authorization gate
closed in these five merges.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate after #212 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and label review of private replacement inputs |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | PR #139 guard disposition; real-host enforcement later |
| Work package 2B-3 execution support | 8–16 | 8–16 | Separate exact offline holdout executor grant and implementation |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Reviewed inputs, source, allowance, development result and holdout freeze |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation |
| Work package 2B-4 | 12–24 | 12–24 | Calibration and host proof before limited live suite |
| Work package 2B-5 | 8–16 | 8–16 | Package 2B-4 gate before generic corpus |
| Work package 2B-6 | 8–16 | 8–16 | Later scheduling, cost, quarantine and dataset operations |
| Work package 2B-7 | 4–8 | 4–8 | Later advisory continuous integration and operator workflow |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and package-003 prerequisites |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparison |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation after selected integration outcomes |
| Repository-wide documentation readability | 55–200 | **50–175** | 487 pages lack full-page acceptance; timed stratified review remains |
| **Selected remaining total** | **150–394** | **145–369** | Non-documentation **95–194** plus documentation **50–175** |

The seven optional rows from the #207 checkpoint retain their estimates and
selection gates. Both optional issue #101 helpers together add **16–40**
active hours, changing the bounded selected-plus-both total from **166–434**
to **161–409**. Additional host and product quantities, strategic expansion,
multi-judge arbitration and future control-plane architecture remain
unbounded. No finite all-options total or calendar date is supportable. Start
the next five-merge counter after #212, and revise sooner if verified scope or
an owner decision materially changes the remaining work.

## Five-merge checkpoint — 2026-09-23, after pull request #207

Five requests merged after #202, in order #204, #203, #205, #206 and #207.
The exact base is the #207 merge `69c055bdb862f305b511fcef5a0120a1af8918c4`.
The [measurement checkpoint](aegis-execution-metrics.md#checkpoint-after-pull-request-207--2026-09-23)
records their original estimates, overlapping wall intervals and exact-head
checks. Every final pull-request head passed Linux, Windows and protected-file
checks; all five exact-main runs also passed, including the
[#207 main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35936082668).

| Merged request and delivered scope | Original package ETA | Observed first-work-to-merge wall time |
| --- | ---: | ---: |
| [#204](https://github.com/ModernNomad-98/Project-Aegis/pull/204): preceding forecast | 1–2 active hours | About 9½ minutes |
| [#203](https://github.com/ModernNomad-98/Project-Aegis/pull/203): user paths and acceptance runbook | 1–2 active hours | About 18 minutes |
| [#205](https://github.com/ModernNomad-98/Project-Aegis/pull/205): historical evidence reading | 2–4 active hours | About 8½ minutes |
| [#206](https://github.com/ModernNomad-98/Project-Aegis/pull/206): documentation progress and batching | 2–4 combined active hours | About 15 minutes |
| [#207](https://github.com/ModernNomad-98/Project-Aegis/pull/207): nine-page acceptance sample | 2–4 active hours initially; 4–8 before page review | 21m32s |

Here **ETA** means estimated time to complete a bounded package. The wall
intervals overlap, include GitHub and review waits, and are not measurements
of active labor. The #207 sample selected pages with known gaps; all nine
needed corrections. It establishes an acceptance method, not a statistically
representative throughput rate. None of these five requests closed a selected
non-documentation implementation or its remaining owner and host gates.

At the exact #207 tree, **554 tracked Markdown files** exist. Nine corrected
pages have recorded full-checklist acceptance: two skill pages, three primary
pages outside skill paths, one tracking page, one historical note and two
templates. The [progress accounting](aegis-documentation-readability-backlog.md#progress-accounting-after-pull-request-205)
and [nine-page evidence](../evidence/documentation/full-page-readability-sample-2026-09-23.md)
leave **545 pages** without recorded full-page acceptance, in disjoint buckets:
340 skill pages, 80 other corrected primary pages, 54 dated notes or tracking
pages, 27 other reader-facing pages and 44 synthetic fixtures. Earlier sorted
screens and focused corrections still count as progress, but do not by
themselves meet the full-page acceptance checklist.

The provisional documentation residual model assigns **4–12 minutes** per
remaining skill page, **8–25 minutes** per corrected primary page outside
skill paths, **3–10 minutes** per dated note or tracking page, and **20–60
minutes** per other reader-facing page. Synthetic fixtures add **1–3 active
hours**, correction reserve **8–20 hours**, and integration **4–8 hours**.
These assumptions produce about **58–168 active hours** before a further
**0–30-hour** tail reserve for long records, new pages and rework; the planning
range is rounded to **55–200 active hours**. This is a scope model with an
uncertain lower end, not a calibrated measured rate. A four-minute increase
on each of the 340 skill pages would add almost 23 hours, which explains the
larger upper reserve. Record active time across a stratified batch before
narrowing the estimate again.

All **14 selected** and **seven optional** open rows were reconsidered. The
13 non-documentation rows retain **95–194 active hours** because these five
merges did not close their gates. The selected total changes from **175–394**
to **150–394 active hours** after the documentation estimate changes from
**80–200** to **55–200**. The separate #139 and #197 protected-path requests
and the exact offline holdout grant still require their own owner decisions.

| Selected open work item | Previous remaining active hours | Revised remaining active hours | Remaining gate after #207 |
| --- | ---: | ---: | --- |
| Work package 2B-3 candidate inputs | 1–4 | 1–4 | Owner semantic and label review of private replacement inputs remains |
| Behavioral Eval Runner item 009 evidence policy | 8–16 | 8–16 | #139 is unmerged; real-host enforcement remains |
| Work package 2B-3 execution support | 8–16 | 8–16 | Exact offline holdout executor grant and implementation remain |
| Work package 2B-3 measurement and owner decision 1 | 4–10 | 4–10 | Reviewed inputs, source, allowance, development result and holdout freeze remain |
| Selected-host capability proof | 12–24 | 12–24 | Named host and measured isolation remain |
| Work package 2B-4 | 12–24 | 12–24 | Limited live suite follows calibration and host proof |
| Work package 2B-5 | 8–16 | 8–16 | Generic corpus follows package 2B-4 |
| Work package 2B-6 | 8–16 | 8–16 | Scheduling, cost, quarantine and dataset operations remain |
| Work package 2B-7 | 4–8 | 4–8 | Advisory continuous integration and operator workflow remain |
| Control-plane work package 003 | 8–16 | 8–16 | Real source, freshness, containment, evidence and billing proof remain |
| Control-plane work package 004 | 8–16 | 8–16 | Delivery target and package-003 prerequisites remain |
| Issue #101 package 4 | 8–16 | 8–16 | Pinned host, cases, budget, execution authority and comparison remain |
| Issue #101 package 7 | 6–12 | 6–12 | Release evaluation follows selected integration outcomes |
| Repository-wide documentation readability | 80–200 | 55–200 | 545 pages lack recorded full-page acceptance; timed stratified review remains |
| **Selected remaining total** | **175–394** | **150–394** | Non-documentation **95–194** plus documentation **55–200** |

| Optional open work item | Previous active hours if selected | Revised active hours if selected | Remaining gate |
| --- | ---: | ---: | --- |
| Issue #101 package 5, local helper | 8–20 | 8–20 | Package-4 comparison and explicit choice |
| Issue #101 package 6, online helper | 8–20 | 8–20 | Package-4 comparison, provider authority and explicit choice |
| Behavioral Eval Runner item 010, signing and immutable storage | 4–12 | 4–12 | Adoption decision |
| Behavioral Eval Runner item 014, additional host adapters | 8–20 per host | 8–20 per host | Host identity and count |
| Behavioral Eval Runner item 015, optional operations products | 8–24 per product | 8–24 per product | Product identity and count |
| Strategic skill expansion and framework coverage | Unbounded until a candidate batch is selected | Unbounded until a candidate batch is selected | Demand, coverage and package selection |
| Multi-judge arbitration and future control-plane architecture | Unbounded | Unbounded | Architecture and adoption decisions |

Selecting both issue #101 helpers would add **16–40 active hours**, making
the bounded selected-plus-both total **166–434 active hours**. The full
all-options backlog remains unbounded while additional host and product
counts and architecture choices are unset. Owner wait, GitHub queue, provider
execution and host provisioning are outside active-hour estimates. Restart
the five-merge counter after #207, and revise sooner when verified scope,
timed acceptance data or an owner decision changes the remaining work.

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
