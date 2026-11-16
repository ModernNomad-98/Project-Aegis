# OWNER AUTHORITY PACKET — C1.1b protected required-context wiring (T23; exact lines, 2026-11-10)

Basis: C11B-REQUIRED-CONTEXT-DESIGN-OUTLINE-2026-11-10.md — 46323 B / 5eb20f392812ff06271f92ab05464d5be646422d7bde0877cac9a9303632d370 (task-26; design only, no edits).

## Findings that condition the authority
- gate-guard protects .github/workflows/ and scripts/; C1.1b therefore needs a one-time gate-guard exception.
- APR-140 is NOT applicable to C1.1b (its condition (c) forbids any .github change; its FORBIDDEN includes .github/ and guard/approval/CI/settings). A SEPARATE one-time owner authority line is required.
- Recommended placement D-1A: move the production checker under scripts/ (single source), rather than extending gate-guard's pattern.
- Required context proposed: aegis-verdict-gate, POST_F_READINESS only, exact-PR-head binding, base-only checkout, fail-closed; staged rollout: ship non-required -> independent verify -> owner registers required.
- Anti-spoof depends on T4 custody; otherwise auditable-only.

## Candidate authority line A (NOT GRANTED; owner may edit)

Line: "I authorize the bounded C1.1b protected required-context wiring change for ModernNomad-98/Project-Aegis: (1) a one-time gate-guard exception for exactly the C1.1b changed paths at the exact Stage-F-accepted head; (2) implementation of the moved read-only verdict/readiness checker and its workflow job; (3) the repository-settings change to register aegis-verdict-gate as required on main with enforce_admins=true, up-to-date/strict (or merge queue if available), dismiss stale approvals, non-admin automation identity, distinct approving identity, R1 routing, no bypass except recorded break-glass; (4) recording measured before/after settings. Conditions: no check removed or weakened; gate-guard and other failed checks at the exact head recorded as failed with authorized disposition, never green; Stage F re-derives the protected-path pattern and required-check list; bypasses recorded only; ENFORCED only after independent re-read plus negative controls; mounted host coverage UNKNOWN and no host-containment claim; rollback plan; no plan revision. Scope FORBIDDEN: other protected paths/settings; gate-pattern/approval-mechanism changes; auto-merge; APR-140 cited for .github/; policy-of-record changes beyond the documented required-check update; provider/host/install/publication/spend; plan revision 3."

## Staged variant (recommended for lower risk)
B1 line: "I authorize only the protected-path implementation and one-time gate-guard exception for C1.1b at the exact Stage-F-accepted head; no settings change yet."
B2 line (after independent verification): "I authorize registering aegis-verdict-gate as a required context on main under the settings/identity conditions recorded in the C1.1b outline."

## Prerequisites/route
Requires T2/T3, T4 settings/identity, T6 auth method, T7 exception/unavailable authority, an independent Stage B of a captured C1.1b Stage A plan, and applicable implementation authority. No implementation/CI/settings/merge/enforcement is authorized by this packet.

Recorded by: Lead (DeepSeek Harness; route deepseek-flash). Local record only.