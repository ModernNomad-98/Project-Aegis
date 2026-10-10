---
name: role-coverage-test-designer
description: 'Designs role-coverage QA for a SaaS app: which behaviors, screens, data, and journeys each role (anonymous, member, manager, admin, owner, support, platform) may access or perform, the interface-consistency deltas across roles on shared surfaces, and the layer-mapped coverage plan that proves the allowed paths. Produces the coverage design only — designs, executes nothing. Use when asked to design role-based QA coverage, a role-by-surface matrix, persona-to-role test mapping, or cross-role interface-consistency checks. Do NOT use for denial or negative-permission tests (authorization-matrix-designer step 7, multi-tenant-security-tester), designing the authorization matrix itself (authorization-matrix-designer), product-wide QA strategy (qa-strategy-architect), per-change test plans (test-plan-designer), writing E2E specs (playwright-e2e-engineer), or scripted manual cases (manual-test-case-creator).'
---

# Role Coverage Test Designer

**Reading key:** QA is quality assurance; E2E is end-to-end; API is application
programming interface; SaaS is software as a service. A role is a permission
set an account holds (anonymous, member, manager, admin, owner, support,
platform); a persona is an example user who holds a role, not the role itself.
An authorization matrix is the deny-by-default table of who may do what; role
coverage is the QA plan that proves the ALLOWED paths and the interface
differences across roles.

## Purpose

Produce the role-coverage QA design: which behaviors, screens, data, and
journeys each role may access or perform, the interface-consistency deltas
across roles on the same surfaces, and the layer-mapped coverage plan that
proves the allowed paths. It consumes the shipped authorization matrix
(`authorization-matrix-designer` output) as its input — compose, never
restate. It designs and executes nothing.

## Use When

- Use when: asked to design role-based QA coverage for an app's roles.
- Use when: asked for a role × surface matrix, a persona-to-role test mapping, or which allowed paths each role needs covered.
- Use when: asked to check that the same screen or flow behaves consistently across roles (interface-consistency deltas).
- Use when: the authorization matrix exists and the question is which ALLOWED behaviors to verify, at which test layer.
- Do NOT use when: the ask is denial, negative-permission, or cross-tenant tests — the negative-test plan is `authorization-matrix-designer` step 7, executed by `multi-tenant-security-tester` *(manual-only)*.
- Do NOT use when: the ask is designing the authorization matrix itself (roles, grants, deny-by-default policy) — that is `authorization-matrix-designer`.
- Do NOT use when: the ask is the product-wide QA strategy — that is `qa-strategy-architect`.
- Do NOT use when: the ask is a per-change test plan — that is `test-plan-designer`.
- Do NOT use when: the ask is writing or running E2E specs — that is `playwright-e2e-engineer` *(manual-only)*.
- Do NOT use when: the ask is step-by-step scripted manual cases — that is `manual-test-case-creator`.
- Custom-role, grant-ceiling, and role/resource-inheritance coverage is designed by the #59 extension of `authorization-matrix-designer` (built by D78): this skill composes that output — never restates it.

## Inputs to Inspect

1. The authorization matrix design (`authorization-matrix-designer` output): roles, grants, deny-by-default policy, and its step-7 negative-test plan. The matrix is the input; this skill never restates it.
2. The role and persona catalog: which roles exist, which personas exercise them, and which test accounts exist per role.
3. UI surfaces and routes each role can reach, including screens shared across roles.
4. Per-role feature flags, plan/entitlement gates, and tenant configuration that change what a role sees.
5. Existing test coverage across layers, so the design names gaps instead of duplicating.
6. Custom roles, grant ceilings, and inheritance → designed by the #59 extension of `authorization-matrix-designer` (built by D78); compose its output, never restate it.

## Workflow

1. **Gather the matrix and the surfaces.** Read the authorization matrix output and the UI/API surface inventory. No matrix → Stop Conditions.
2. **Enumerate the roles.** List every shipped role the matrix names: anonymous, member, manager, admin, owner, support, platform — no invented roles.
3. **Build the role × surface allowed-path table.** For each role and each surface, the behaviors that role MAY perform (allowed paths only); denials belong to `authorization-matrix-designer` step 7 and `multi-tenant-security-tester`.
4. **Find interface-consistency deltas.** Where the same screen, form, list, or flow appears to two roles with different permitted actions, hidden fields, or menu items, name the delta and the check that would catch a wrong one.
5. **Map layers and persona data.** For each allowed path choose the cheapest reliable layer (unit / API / E2E / manual) and the persona or test account that exercises it.
6. **Name execution handoffs.** State who runs each layer's checks: `playwright-e2e-engineer` *(manual-only)* for permanent specs, `manual-test-case-creator` for scripted cases — handoffs, never executions here.
7. **Emit the design** in the Output Format, stating what was chosen, why, and the main rejected alternative.

## Output Format

Emit the design in the conversation (nothing is written to the repo):

```
ROLE COVERAGE DESIGN — <app>
Role inventory: <every shipped role named, as the matrix names them>
Allowed-path matrix: <role × surface: the behaviors each role MAY do>
Interface-consistency deltas:
  <surface> — <role A> vs <role B> — <differing actions/fields/menus> —
  check <the check that catches a wrong difference>
Per-role journeys: <the journeys each role can complete>
Layer mapping + persona data:
  <allowed path> → unit | API | E2E | manual — persona <who>
Execution handoffs:
  permanent specs → playwright-e2e-engineer (manual-only); scripted cases →
  manual-test-case-creator — named, never executed here
Out of scope:
  denials / negative permissions → authorization-matrix-designer step 7 /
  multi-tenant-security-tester
  custom roles, grant ceilings, inheritance → designed via the #59 extension (built by D78); compose, never restate
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] Every shipped role is named; none invented beyond the matrix.
- [ ] The allowed-path matrix covers each role × surface pair the scope names; no blank cells.
- [ ] Every interface-consistency delta names the two roles, the surface, and the check that catches a wrong difference.
- [ ] Each layer mapping is justified (cheapest reliable layer); persona data is named per role.
- [ ] Denials are stated out of scope and routed to `authorization-matrix-designer` step 7 / `multi-tenant-security-tester`.
- [ ] Custom-role / grant-ceiling / inheritance coverage is composed from the #59 extension (built by D78), never restated.
- [ ] The matrix was composed, never restated; the design claims to execute or drive nothing.

## Gotchas

- Role ≠ persona: a persona is an example user holding a role. A matrix keyed to personas instead of roles breaks the day an account changes; key to roles and name personas as data.
- UI-only coverage misses API-level gaps: the same role can hold a permission the UI never surfaces, or the UI can show an action the API should refuse. Coverage must name the layer per allowed path, not the screen alone.
- Matrix explosion: role × surface × behavior grows fast. Scope to the allowed paths the app ships and say what is skipped; a giant matrix proves nothing if nobody can run it.
- Never restate the matrix: copying `authorization-matrix-designer`'s grants into this design duplicates the source of truth. Reference it and design coverage around it.
- Denials are `authorization-matrix-designer` step 7's and `multi-tenant-security-tester`'s job; absorbing them here duplicates an executed suite and blurs the seam.
- Custom roles, grant ceilings, and inheritance are designed by the #59 extension of `authorization-matrix-designer` (built by D78); compose its output here — do not restate it.

## Stop Conditions

- No authorization matrix or role inventory is supplied or findable → stop and ask for the `authorization-matrix-designer` output; a coverage design cannot start from role names alone.
- The request drifts into designing the matrix itself (roles, grants, policy) → hand off to `authorization-matrix-designer`.
- The request drifts into denial or negative-permission testing → hand off to `authorization-matrix-designer` step 7 and `multi-tenant-security-tester` *(manual-only)*.
- The request becomes executing a pass, writing specs, or driving a browser → hand off to `playwright-e2e-engineer` *(manual-only)* or `manual-test-case-creator`; this skill designs only.
- The request covers custom roles, grant ceilings, or inheritance → stop; that coverage is deferred to the unbuilt #59 extension, not designed here.
- The request involves destructive or live-state action → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `authorization-matrix-designer`, `multi-tenant-security-tester`, `qa-strategy-architect`, `test-plan-designer`, `playwright-e2e-engineer`, and `manual-test-case-creator`.
- `references/` — None: the design is self-contained.
