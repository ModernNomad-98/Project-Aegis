# Plan-of-record package reference

## Package files
- PLAN.md: what/why, scope and non-goals, blast radius, exact file inventory, count/gate deltas, protected-path/authority map, closure matrix, owner decisions, verification/re-base.
- SPECS-ANNEX.md: inventory at the base, supersession/spec details, count coupling, closure staging, acceptance rows, authority.
- A-ROWS.json: one row per acceptance criterion with an executable closure command, base expectation (fail-before) and after expectation (pass-after).
- IMPACT.md: change size, risk, protected paths, authority and residual owner actions.
- plan-binding.json: revision, base, artifacts and captures identities (bytes/LF/sha256), non-circular evidence bindings.
- INDEX.md: what the plan answers, base, evidence, artifact identities, risks, next step.
- final-verification.txt: the executed checks and their results at the captured revision.

## Five questions every plan answers
1. Necessity: what is missing without this change, and what recurring cost justifies it?
2. Reuse: which existing skills, registries and mechanisms are reused instead of new ones?
3. Ownership/authority: who may decide, who executes, and where is the owner decision recorded?
4. Minimum-safe action: what is the smallest change satisfying the directive without weakening gates?
5. Complexity justification: why the selected size is proportionate and alternates are rejected.

## Two-PR split example
PR-1: new content plus registrations and count coupling (mechanical, protected count pins disclosed). PR-2: governance prose supersession plus append-only decision entry. Record per-PR closure expectations; never claim one head passes both PRs' checks.

## Binding rules
- Measure every artifact after its final edit; LF-only bytes; sha256.
- The binding may pin INDEX and final-verification; neither INDEX nor final-verification may embed its own hash or the binding hash.
- Re-freeze all pins after any edit to a bound artifact.
