# Project Aegis — next owner decisions

> **Current reading, checked 2026-09-23 after pull request #144:** The table and
> sequence under [Original decision packet](#original-decision-packet-after-pr-107)
> preserve the proposal prepared after #107. They are not today's queue. Use
> the index below with the [approval register](../approvals/APPROVAL_REGISTER.md),
> [current forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-141),
> and owning backlogs before
> acting. This page grants no implementation, host or provider authority.

## Current disposition

For this page, Behavioral Eval Runner (BER) names the evaluation tool and
control plane (CP) names the delivery kernel. A backlog item (BKL), work
package (WP), and recorded decision (DEC) have separate lifecycles. An APR
is an entry in the owner approval register. A pull request (PR) is a proposed
or merged repository change. Owner decision 1
(OD-1) is the later ratification of BER's measured judge result. R4 and R5
are BER's host confinement and execution-profile evidence gates. POSIX means
a Unix-like operating-system interface; continuous integration (CI) runs
repository checks, not a selected-host proof. A source SHA is a commit hash;
`NON_BASELINE` means the result cannot qualify for the measured baseline.
`SYSTEM` is the Windows operating-system service account.

| Topic | Current status and next gate |
| --- | --- |
| BER evidence policy (BKL-009) | [APR-009](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection) selected the 30-day complete-bundle policy. [APR-012](../approvals/APPROVAL_REGISTER.md#aegis-apr-012-offline-behavioral-eval-runner-evidence-policy-proof) authorized one synthetic offline proof; [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139) was open at this checkpoint. Real-host storage, access, redaction and operator cleanup controls remain incomplete. Follow the [BER backlog](behavioral-eval-runner-backlog.md); policy selection does not approve deletion or a live run. |
| Replacement candidate labels | The public [sanitized candidate checkpoint](../evidence/ber-replacement-candidate-1-summary.md) records 160 pending candidates. Owner semantic review and exact-byte label approval remain open; this index does not inspect or approve private inputs. |
| BER WP-2B-3 source, allowance and OD-1 | The [offline holdout execution proposal](ber-wp2b3-holdout-execution-scope.md) is a proposal, not an implementation grant or a renewed provider allowance. Historical accounting, exact reviewed execution source, labels, host proof and an explicit call/token/dollar cap remain prerequisites. No measured result or OD-1 ratification exists. |
| BER host and R4/R5 | The owner selected a disposable POSIX **direction**, but no named host or selected-host capability proof is recorded. The [host decision proposal](ber-selected-host-capability-decision.md) distinguishes generic Linux CI from host evidence; any offline probe needs its own bounded authority. |
| CP-WP-003 | [APR-006](../approvals/APPROVAL_REGISTER.md#aegis-apr-006-control-plane-offline-capability-proofs-first-increment) and [PR #123](https://github.com/ModernNomad-98/Project-Aegis/pull/123) delivered the synthetic CP-WP-003A proof. The [CP backlog](resumable-control-plane-backlog.md) still blocks real source authority, independent freshness, containment, evidence and billing claims. The delivered proof grants no real dispatch. |
| CP-WP-004 | No delivery target is selected. The [CP backlog](resumable-control-plane-backlog.md) requires CP-WP-003 prerequisites and a separately approved integration with exact receipt, rollback and budget terms. |
| Issue #101 setup and routing | Package 1 planning ([PR #109](https://github.com/ModernNomad-98/Project-Aegis/pull/109)), package 2 Windows Aegis-only setup ([PR #124](https://github.com/ModernNomad-98/Project-Aegis/pull/124)), and package 3 offline advisory contract ([PR #121](https://github.com/ModernNomad-98/Project-Aegis/pull/121)) shipped within bounded scopes. The [setup plan](aegis-setup-routing-plan.md) keeps package 4 host proof and comparison pending separate authority, packages 5/6 conditional, and package 7 pending. No optional helper is selected. |

The [latest five-merge forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-141)
keeps the selected
remaining work at **175–394 active hours**. It is a scope estimate, not
permission to start a gated package. The independent gates in the original
packet below still apply where the current index marks them open.

## Original decision packet after PR #107

Prepared 2026-09-23 after public PR #107. This is a review packet, not a
phase authorization or a claim that a blocked gate is complete. The
[execution handoff](aegis-efficient-execution-handoff-2026-09-23.md) groups
these decisions for efficient review; BER, CP and setup retain separate
authority records and implementation branches.

| Decision | Current evidence | Recommendation | Decision boundary |
| --- | --- | --- | --- |
| BER-BKL-009 final evidence policy | Scoped BER-DEC-006/008 handling and writer metadata exist, but no complete production policy/enforcement | Select the [30-day whole-bundle policy proposal](ber-bkl-009-evidence-policy-decision.md), owner+SYSTEM WP-2B-3 readers and verified host encryption; separately authorize implementation | Owner sets exact periods, readers and mechanism; BKL-009 stays PARTIAL until policy, writer and runbook are reviewed |
| Replacement candidate labels | Private input PR #1 contains 160 PENDING candidates; public [sanitized checkpoint](../evidence/ber-replacement-candidate-1-summary.md) records hashes and checks | Review the full private packet; approve exact bytes only after semantic/risk review or request a new version | A candidate commit and structural PASS do not create human gold labels |
| WP-2B-3 source and allowance | BER-DEC-008 pins its original authorization merge; the replacement packet and any holdout executor are later revisions; old input/usage bytes are missing | Operationally assume **zero available residual allowance** until independently reconciled, without changing the historical grant; after label approval and reviewed execution source, record an exact revised source SHA/tree and a new explicit call/token/dollar cap in a merged amendment | No provider metadata or judgment request, dependency install or new source pin follows from this proposal |
| BER selected host / R4–R5 | On the current Windows host, mid-write reparse prevention is unavailable in the evidence writer and post-leader descendant cleanup is unproven; POSIX writer tests run in generic Linux CI, but no selected-host capability proof exists. Profile isolation is unproven. | Select a host under the [capability decision proposal](ber-selected-host-capability-decision.md), then authorize its bounded offline probe; report unsupported paths as NON_BASELINE and stop before live dispatch | Do not choose a live host by documentation alone; any provisioned host, credentials or live probe needs its own authority |
| CP-WP-003 | CP-WP-002's 543-test offline kernel is DONE; source-atomic real approval, monotonic reconciliation, containment/fencing, and bounded liability remain blocked | Prepare a zero-provider, synthetic capability-proof authorization with negative authority/race/rollback/path/process/receipt/billing probes | Separate reviewed CP scope and owner approval; no real adapter, deployment or provider call |
| CP-WP-004 | No delivery target selected; CP-WP-003 gates are unproven | Decide the single integration only after CP-WP-003 evidence; a draft GitHub PR is a candidate reversible target for comparison with local artifact export | Selection needs exact idempotency, receipt, rollback, source/evidence/budget pins and explicit owner authority |
| Issue #101 setup/routing | [Issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101) records seven numbered packages, current Aegis-only/local/online/help choices and no selected helper | Start package 1 as design and candidate screening; keep Aegis-only as a complete baseline, then compare optional helpers on paired tasks before selecting one | No installation, credentials, paid evaluation, provider call or helper default is authorized by the issue |

## Proposed near-term sequence

1. Review private calibration PR #1 for candidate defects without moving
   labels out of the private repository. Preserve each rejected version.
2. Decide the BKL-009 policy parameters in the linked proposal. A subsequent
   governance entry must authorize code/runbook enforcement; no retroactive
   rewrite of BER-DEC-008/010 or WP-2B-0 spike evidence.
3. Prepare offline host and CP-WP-003 scope/evidence proposals. Probe only
   after their own reviewed authorizations; current capability reports are
   limitations, not verified live guarantees.
4. Prepare issue #101 package-1 design separately. Screen alternatives and
   define the paired evaluation before any local install or online use.
5. Only after labels, exact source review, historical-accounting disposition,
   host proof and explicit renewed allowance may a WP-2B-3 provider preflight
   be considered. Development, owner wait, holdout freeze and OD-1 result
   ratification remain sequential gates.

These choices are independent. Accepting the evidence policy, for example,
does not approve the 160 labels, renew a provider budget, authorize CP-WP-003,
or select an issue #101 helper.

The live issue #101 body was read on 2026-09-23 and lists packages 1–7.
The earlier execution handoff's "six packages" wording is stale after the
issue's forward correction; the current issue controls this count. Neither
source itself grants runtime implementation authority.
