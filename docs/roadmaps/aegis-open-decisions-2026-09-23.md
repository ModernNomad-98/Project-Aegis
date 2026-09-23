# Project Aegis — next owner decisions

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
