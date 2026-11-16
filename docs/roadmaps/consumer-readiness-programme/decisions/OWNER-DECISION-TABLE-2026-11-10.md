# OWNER DECISION TABLE — resolved from evidence vs tabled (2026-11-10)

Rule applied: resolve only what the records prove; do not fabricate acceptance/authority; table genuinely owner-held decisions and continue all unaffected work. No repo/settings/host/provider/spend action.

## Resolved from evidence (no owner decision required)
| # | Question | Evidence-based resolution |
| --- | --- | --- |
| R1 | What happened to PR #1014? | MERGED at merge commit f6587e2a (parents 7f86ebb5 + 4fe90e9c), 2026-11-10T21:59:52Z; independent evidence-lineage and design-review records re-verified the git facts. It is historical: do not resume it or reuse the Stage-D ACCEPT at 182d5221 for the merged head without a new R5 rebinding. |
| R2 | What is current main/head point-in-time? | Observed via read-only gh at this pass: main = 7ea22f8c (merge of PR #1015, which is a separate control-plane test-only change, not this programme). This is an OBSERVED point-in-time fact, not a stable claim; no programme action uses it. |
| R3 | Is the integrated plan allowed another revision? | No plan revision 3: plan revision count is 2 (<4); no counted lean reopen exists; APR-139(i) separate. No new plan version is created. |
| R4 | Is the review-head budget consumable by document reviews? | No. Document reviews are not candidate heads; 0 of 3 candidate heads consumed by rev-2 design work. A 4th implementation head would need a scoped exception under applicable authority; none is defined/used. |
| R5 | Is C0.3 structurally sound after review? | Independent review chain: REVISE M1 -> delta REVISE D1-D3 -> errata v2.1 + B1/B2 confirmation -> confirmation ACCEPT (0 mandatory). M1 is closed at corrected-text level; this is review evidence, NOT owner acceptance and NOT B1/B2 acceptance. |
| R6 | Can the programme treat the Aegis Maturity plan as source of remaining work? | No: A is at revision 5 with no reopen, WAITING-ON-OWNER/park-unmerged. It is a separate plan; the integrated programme does not plan A's work. Not a blocker for unaffected C&C/Experience slices. |
| R7 | Is checkpoint live-state (base main/PR/settings) current? | No: historical point-in-time. Branch-protection tuple and mounted coverage remain REPORTED/UNKNOWN; current settings need a fresh owner-authorized observation. |

## Tabled — genuine owner decisions (unresolved; work continues elsewhere)
| # | Decision | What is known | Why it cannot be resolved internally | Recommended option |
| --- | --- | --- | --- | --- |
| T1 | A (Maturity plan-of-record) revision 5 | WAITING-ON-OWNER; no counted reopen; no reset/second reopen | Only actual owner authority can supply a scoped counted lean reopen or confirm hold | Confirm hold/park; do not reopen merely to continue unrelated work |
| T2 | C0.3 design basis acceptance | Independent confirmation ACCEPT (0 mandatory); design still a proposal | Design acceptance/authority is owner-held; review ACCEPT is not owner acceptance | Accept corrected-text v2.1 as design basis for C1/C2 |
| T3 | B1/B2 design acceptance and sequencing | B1 auditable/bypassable with five unmet custody preconditions; B2 advisory/not installable; no overclaim | Cannot self-accept design or settings-dependent enforcement | Accept B1 as auditable-not-enforcing; defer B2; make custody changes before any enforcement claim |
| T4 | Five B1 custody preconditions (admin enforcement, strict/up-to-date, independent approving identity, non-admin automation identity, R1 routing) | Current tuple point-in-time; one-account custody; 4/4 historical admin bypasses | Repository settings/identity authority is owner-side | Approve exact settings/identity plan before C1 implementation |
| T5 | Mounted host-enforcement coverage | UNKNOWN; writable custody; six bypasses not covered | Requires owner-authorized Electron-side read-only composition/config export | Authorize one read-only export so coverage can be proved/disproved |
| T6 | Authentication method for independent verdict provenance | Design defaults to UNVERIFIED/BLOCKED; supported method unknown | No record grants/defines an authentication method or identity custody | Define one minimal independent method (e.g. distinct owner-controlled identity/inbox) or accept BLOCKED |
| T7 | Fourth-head scoped-exception and unavailable-review authority | Not defined in applicable policy; design leaves them UNKNOWN | Policy definition is owner-held | Define holder/duration and bounded unavailable-review disposition before implementation |
| T8 | E0 item-5 preservation export | 77-member manifest 8,105 B/9c2a5089..., single untracked local copy; 05-C/D/E/G NOT MET | A durable export is a write/authority action | Authorize preservation-only export to an owner-named durable location, $0 provider spend |
| T9 | Next implementation slice authorization | Recommended: E0 item-5 export; C&C C1.1/B1-minimal only after design acceptance + A rev-5 + custody decisions | Owner implementation authority | Authorize E0 item-5 export first |
| T10 | Stage-B plan audit of integrated plan rev 2 | Not performed/authorized; must bind aca10d6a if commissioned | Extra review authority | Only if the integrated plan is to become plan-of-record |
| T11 | R8 repo-wide tooling/policy adoption | Scope/effort UNKNOWN; separate governance change required | Owner/governance approval | Defer; scope when C2/C3 near implementation |

## What continues without these decisions
- E1 items 3/4/8 read-only re-derivation at current head (task-11).
- C1.1/B1-minimal Stage A plan draft (task-12), explicitly provisional on T2/T3/T4/T6/T7.
- E0 item-5 export preparation: custody-set verification, manifest checks, chain-of-custody/destination requirements and a separate-reviewer receipt procedure - no export write is performed (preparation task launched alongside this table).
- E3 item-2 open-failure analysis: CP-03/CP-09/CP-19/CP-17 evidence and options, no repair (analysis task launched alongside this table).
- C2/C3/C4 and E2/E4 design/planning work that does not require implementation authority or the tabled decisions.

Recorded by: Lead (DeepSeek Harness; route deepseek-flash; serving model not observable). Local record only. No secrets.