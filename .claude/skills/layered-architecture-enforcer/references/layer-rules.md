# Layer model, allowed edges and violation checklist

Reference for the layered-architecture-enforcer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Typical layers and what each may not depend on.
- Allowed direction is inward; adapters implement inner-layer ports.
- Violation classes: import inversion, type leak, wrong-layer rule, bypassed port, layer skip, hidden shared state.
- Every accepted exception records rule, location, reason, owner and review date.
- Smallest-change order: narrow signature, move one type, use a port, invert one dependency, split one module.
- Verification: architecture/import rule + focused tests + re-check affected edges.

## 2. When this applies

- A repository or module claims a layered/hexagonal/clean architecture and someone asks whether that still holds.
- A change crosses presentation, application, domain, platform, data-access or infrastructure boundaries.
- A review found domain code importing infrastructure, a controller holding business rules, or an adapter leaking framework types.
- Before a refactor you need the current layer map and the smallest compliant fix rather than a rewrite.

## 3. Output and evidence rules

1. Layer map with evidence for each assignment.
2. Cross-layer edge table with allowed/forbidden status.
3. Violation list with exact location and reasoning.
4. Smallest compliant change per finding, with trade-offs and verification steps.
5. Assumptions, UNKNOWNs and what could not be inspected.

Every claim in the returned record is backed by inspected evidence or explicitly labeled **assumption**, **UNKNOWN** or **UNRUN**. An empty or unrun check is never a PASS. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Stop and route out when the request matches another owner; see Stop Conditions.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Layer model and allowed direction stated before judging violations; unstated rules labeled assumptions.
- Layers mapped from imports/config/annotations, not only directory names.
- Every violation names the exact edge and evidence; exceptions carry a recorded reason.
- Each fix is the smallest compliant change, not a redesign; no code edited.
- Verification includes an architecture/import rule where feasible plus focused tests.
- Uninspected areas and uncertain edges reported, never guessed.
