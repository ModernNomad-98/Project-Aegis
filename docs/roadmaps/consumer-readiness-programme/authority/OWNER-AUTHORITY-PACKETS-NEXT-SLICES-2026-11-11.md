# OWNER AUTHORITY PACKETS — NEXT SLICES C2 and C1.1b (2026-11-11)

Tabled decisions for the next C&C slices. Nothing granted. C1.1a is merged (701ebc7c); C2 and C1.1b plans are captured but not authorized.

## C2 (governance/evidence reuse) — implementation authority
State: plan captured (C2-STAGE-A-PLAN-DRAFT 56,715/f44a6e2f); Stage B audit in flight. Prerequisites T1/T2/T3/T6 satisfied via T9; T4 declined; T10 recorded; T22 conditional; T24 remains UNVERIFIED.
Line: "I authorize C2.1-C2.4 implementation under the accepted C2 Stage A plan <captured hash>, in one bounded PR with the closed 38-path scope (36 new files + the two bounded docs edits), including the docs/delivery-workflow.md policy amendment with its rule-preservation inventory, on one-time authorisation for that policy edit; no settings, required contexts, CI wiring or protected-path change; B/D/E/F evidence at the exact head, 3-head budget, no 4th head without a scoped exception; T22 condition (i) is not attached; the store remains UNVERIFIED and no verified-provenance/readiness claim is made; independent reviewers <names>. No plan revision, no provider spend, no host change."

## C1.1b (protected required-context wiring) — staged authority
State: plan captured 76,919/6e1d44d7; Stage B in flight. Critical finding: required-context registration is not viable today because readiness is structurally blocked (store UNVERIFIED T24; auth UNVERIFIED T6). Stage 1/2 can be prepared/verified non-required under one-time gate-guard exception; Stage 3 (owner registers required) must wait.
Line (staged): "I authorize C1.1b Stage 1 and Stage 2 ONLY, under a one-time gate-guard exception for exactly the C1.1b changed paths at the Stage-F-accepted head: move the checker/tests/fixtures under scripts/aegis_verdict_gate/ as the protected single source, add the dedicated non-required variable-gated workflow/job aegis-verdict-gate and the read-only fetch adapter, with base-only checkout and POST_F_READINESS fail-closed behavior; no repository-settings change and no required-context registration; after independent verification, Stage 3 remains blocked until I supply a supported authentication method (T6) and a VERIFIED store provenance (T24 option A/B). No plan revision, no provider spend, no host change; reviewers <names>."

## Supporting decisions needed for C1.1b Stage 3
- T6: "I select <method> as the supported authentication method for independent verdicts; T6 UNVERIFIED+BLOCKED is superseded for this slice."
- T24/AUTH-STORE: "I authorize <register entry by holder | owner-line authority record> for the C1.1 record store; provenance may be VERIFIED for C1.1b Stage 3 once the entry exists and checks."
- T4: "I <authorize the exact settings set S1-S9 | decline> for required-context registration; if declined, C1.1b stays non-required/auditable only."
- T7: "I define <holder/bounds> for unavailable-review disposition and any further scoped head exception; the C1.1a one-time T7-equivalent exception is consumed."

## Experience (unchanged, still owner-held)
T8/T8a-c/T21 item-5 export/deliverable/retrieval/source link; T14 item-8 hosted schema-only proof; T15-T20 E3 item-2 outcome/CP dispositions; T12-T13 historical Stage-B/closure; T11 R8 adoption. Exact lines are in OWNER-AUTHORITY-PACKETS-2026-11-10.md, its addendum, ITEM8, and the item-5 packet.

## Non-claims
No implementation, repo/settings/host/CI/provider/spend action; no design acceptance; no plan revision. C1.1a remains the only merged slice.

Recorded by: Lead (DeepSeek Harness; route deepseek-flash). Local record only.