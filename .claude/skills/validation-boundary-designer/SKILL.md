---
name: validation-boundary-designer
description: 'Designs where and how input validation lives at each boundary — API, command, form, database, integration — without one-layer reliance: the boundary inventory, per-boundary validation plus type-safe schema choices, the non-negotiable business and security invariants and their enforcement points, and database-level constraint backstops. Produces the design only — writes and reviews no code and no diff. Use when asked to design validation placement across layers, choose shared vs boundary-specific schemas, enumerate invariants and their enforcement points, or plan database constraints as backstops. Do NOT use for reviewing an actual diff for mass-assignment or authorization holes (security-pr-reviewer), permission-denial test plans (multi-tenant-security-tester), external API contracts (api-event-architect), the write-path pipeline (command-gateway-architect), or migration scripts (schema-evolution-planner).'
---

# Validation Boundary Designer

**Reading key:** API is application programming interface; DB is database; UI is
user interface. A boundary is any point where data crosses a trust or
representation edge (client form, API request, command handler, database
write, integration payload). An invariant is a rule that must hold no matter
which layer receives the data first; a backstop is a later, independent
enforcement point that catches what an earlier layer missed or was bypassed.

## Purpose

Produce the boundary-validation design: where and how input validation lives
at each boundary (API, command, form, database, integration) without
one-layer reliance. The deliverable names the boundaries, the per-boundary
validation and type-safe schema choices, the non-negotiable business and
security invariants and their enforcement points, and the database-level
constraint backstops. It is a design document; it writes and reviews no code
and no diff.

## Use When

- Use when: asked to design validation placement across layers.
- Use when: asked to choose shared vs boundary-specific schemas for inputs.
- Use when: asked to enumerate invariants and where each is enforced.
- Use when: asked to plan database constraints as backstops for validated inputs.
- Do NOT use when: the ask is reviewing an ACTUAL diff for mass-assignment or authorization holes — that is `security-pr-reviewer` (its checklist owns mass-assignment).
- Do NOT use when: the ask is a permission-denial test plan — that is `multi-tenant-security-tester` *(manual-only)*.
- Do NOT use when: the ask is an external API contract (wire shapes, versioning, error envelopes) — that is `api-event-architect`.
- Do NOT use when: the ask is the write-path pipeline this design feeds (commands, transactions, side effects) — that is `command-gateway-architect`.
- Do NOT use when: the ask is migration scripts or schema evolution mechanics — that is `schema-evolution-planner`.

## Inputs to Inspect

1. The surface/boundary inventory: routes, commands, forms, jobs, integrations, and where data enters the system.
2. Existing schema and validation code, so the design composes reality instead of assuming a greenfield.
3. Threat-model notes and prior `security-pr-reviewer` findings — mass-assignment and authorization coverage is named by reference, never restated.
4. Business rules and invariants: what must hold regardless of entry point (amounts, states, ownership, referential integrity).
5. Database schema and existing constraints, to plan backstops against what already exists.

## Workflow

1. **Inventory the boundaries.** List every surface where untrusted or cross-layer data enters: API endpoints, command handlers, forms, jobs, integrations.
2. **Assign per-boundary validation and schema choices.** For each boundary: what it validates (shape, type, range, format), which schema it uses (shared vs boundary-specific, type-safe), and what it deliberately does NOT validate.
3. **List the non-negotiable invariants.** Business and security rules that must hold everywhere; name the enforcement point for each (the layer that owns it) and any re-check layers.
4. **Plan database constraint backstops.** Which invariants get a DB-level constraint (unique, check, foreign key, exclusion) so a bypassed or buggy earlier layer still cannot persist bad state.
5. **State what stays with the owners.** Mass-assignment policy → `security-pr-reviewer` / `multi-tenant-security-tester`; wire contracts → `api-event-architect`; pipeline mechanics → `command-gateway-architect`; migrations → `schema-evolution-planner`.
6. **Emit the design** in the Output Format, stating what was chosen, why, and the main rejected alternative.

## Output Format

Emit the design in the conversation (nothing is written to the repo):

```
BOUNDARY-VALIDATION DESIGN — <system / feature>
Boundary inventory: <every data entry point named>
Per-boundary validation:
  <boundary> — validates <shape/type/range/format> — schema <shared | boundary-specific>
  — deliberately not validated: <what a later layer owns>
Invariants & enforcement:
  <invariant> — enforced at <layer/point> — re-checked at <layers> — why non-negotiable
Database constraint backstops:
  <table/column> — <constraint kind> — invariant it backs — failure mode it closes
Out of scope:
  diff review / mass-assignment policy → security-pr-reviewer
  denial test plans → multi-tenant-security-tester
  external wire contracts → api-event-architect
  write-path pipeline → command-gateway-architect
  migrations → schema-evolution-planner
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] Every boundary is named; none assumed away.
- [ ] Each boundary states what it validates, its schema choice, and what it deliberately does not validate.
- [ ] Every non-negotiable invariant has a named enforcement point and the re-check layers.
- [ ] Database constraint backstops are named per invariant, not a vague "add constraints".
- [ ] Mass-assignment and denial policy is referenced, never restated.
- [ ] The design claims to write or review no code and no diff.

## Gotchas

- One-layer reliance is the classic failure: UI-only validation dies the day a client skips the UI; API-only validation dies when a job or migration writes directly. Every invariant needs its enforcement point AND its backstop.
- UI validation is convenience, not security; the design must say which layer owns the rule.
- Restating `security-pr-reviewer`'s mass-assignment checklist or `multi-tenant-security-tester`'s denial plan duplicates their owned coverage — reference them.
- Schema choices that are not type-safe push runtime failures deeper into the system; name the parse point per boundary.
- A backstop constraint that duplicates a business rule silently (different wording, same intent) drifts; keep each invariant's wording stable across layers.

## Stop Conditions

- No boundary or surface inventory is supplied or findable → stop and ask for it; a design cannot start from "add validation".
- The request becomes reviewing a diff for mass-assignment or authorization holes → hand off to `security-pr-reviewer`.
- The request becomes a permission-denial test plan → hand off to `multi-tenant-security-tester` *(manual-only)*.
- The request becomes writing code, migrations, or running anything → stop; this skill designs only.
- The request involves destructive or live-state action → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `security-pr-reviewer`, `multi-tenant-security-tester`, `api-event-architect`, `command-gateway-architect`, and `schema-evolution-planner`.
- `references/` — None: the design is self-contained.
