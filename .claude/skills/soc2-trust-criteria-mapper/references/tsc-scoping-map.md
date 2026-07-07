# TSC Scoping Map — SOC 2

Verified on AICPA pages: five categories; TSC issued by the Assurance
Services Executive Committee (2017 TSC with revised Points of Focus 2022);
SOC 2 is an examination/attestation. CPA-firm-sourced (verify against the
AICPA guide before citing): Type 1/Type 2 definitions; Security as the
required common-criteria baseline.

## Category selection by commitment

| Category | Include when the org has committed to… | Existing mechanisms to map (via compliance-control-foundation) |
| --- | --- | --- |
| Security (common criteria) | baseline for the engagement | Phase 3/4 packs: authz matrix, RLS audit + negative tests, tenant isolation, secrets custody, change mgmt, audit log, supply chain, incident response |
| Availability | SLAs, uptime/DR commitments | `slo-reliability-architect` targets + error budgets, `incident-response-runbook`, `rollback-runbook-author`, backup posture |
| Processing Integrity | complete/accurate/timely processing (billing, transactions, pipelines) | input validation boundaries, idempotency (`api-event-architect`), job monitoring (`observability-operator`), reconciliation controls (often net-new) |
| Confidentiality | NDA/confidential-data commitments, tenant-data confidentiality | `tenant-isolation-reviewer` surfaces, `secrets-identity-hardener`, retention/disposal rules |
| Privacy | personal-information lifecycle commitments (notice, choice, access, disposal) | `sensitive-disclosure-guard` surface, data-retention posture; substantial net-new likely; legal review hook |

Selection rule: commitment trace or OUT. Record both directions.

## System description skeleton

```
1. Services provided                     <the product customers buy>
2. System components: infrastructure | software | people | procedures | data
3. System boundaries                     <in/out, environments>
4. Commitments and system requirements   <the promises driving categories>
5. Subservice organizations              <carve-out|inclusive + complementary controls>
6. Complementary user-entity controls    <what customers must do>
7. Material changes in the period        <Type 2>
```

## Type decision tree

- Need an artifact fast, controls young → **Type 1** now (design as of a
  date), Type 2 over the following window.
- Controls have operated for a defensible period and buyers want
  assurance → **straight to Type 2** (design + operating effectiveness
  over the period).
- Buyer explicitly requires Type 2 → window feasibility test below.
- All Type decisions and window lengths: confirm with the engaged CPA
  firm; definitions verify against the AICPA guide.

## Window feasibility test

1. For each in-scope control: date it began operating (foundation catalog
   status history, `compliance-evidence-collector` coverage matrix).
2. Candidate window start ≥ latest material-control start date.
3. Evidence tiling: can every control show artifacts across every interval
   of the window? Holes → later start or carried exceptions (human call).

## Subservice organization disposition

| Disposition | Meaning | Description duty |
| --- | --- | --- |
| Carve-out (typical) | subservice org's controls excluded from examination | state relied-upon complementary subservice-org controls + your monitoring of the vendor (vendor-mgmt domain, `supply-chain-security-reviewer`) |
| Inclusive | subservice org's controls examined in your report | requires their cooperation/assertions — rare, coordinate early with the CPA firm |

## Language rules

- Say: attestation, examination, SOC 2 report, "we completed a SOC 2
  Type 2 examination."
- Never: "SOC 2 certified," "SOC 2 certification," "passed SOC 2."
