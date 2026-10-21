---
name: security-regression-harness-designer
description: 'Use when a security or access-control bug is fixed: design a permanent regression harness with fixtures, expected-denial cases and CI placement so the vulnerability cannot silently return. Design-only; it does not perform the security review of the fix diff, replace security-pr-reviewer, curate an existing suite, or implement code.'
---

# Security Regression Harness Designer

Terms: **family 5** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Turn a fixed security/access-control bug into a permanent regression harness: extract the vulnerable path, define positive and negative cases, specify safe fixtures and denial assertions, and place them in CI with flake controls and honest coverage.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A security or authorization bug has been fixed and must never return.
- The existing tests pass even though the vulnerability existed.
- You need fixtures that reproduce the vulnerable access path without real secrets or production data.
- You must place the regression in the right CI layer with deterministic evidence.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- The bug report, fix diff and security review findings, including the exact vulnerable path.
- Existing tests and fixtures near the affected code.
- Tenancy/identity/role model and safe test-account policy.
- CI layers, runtimes and available test doubles.
- Evidence requirements for the security sign-off.

## Workflow

1. Extract the pre-fix path that allowed the bad outcome; state the invariant that was violated.
2. Define positive cases (authorized action succeeds) and negative cases (forbidden action is denied), one assertion each.
3. Specify safe fixtures: two-tenant/two-role data, no real secrets or production records, deterministic identifiers.
4. Choose the cheapest reliable layer(s) and CI placement; specify a flake policy in which expected-denial cases get zero pass-masking retries and a diagnostic rerun keeps the first failure as the job verdict.
5. Define evidence: expected denial assertions, logs/screenshots as applicable, and an honest not-covered list.
6. Require a retest of the fixed vulnerability and a red-before/green-after check where feasible.
7. Return the harness plan; do not weaken or skip existing security tests.

## Output Format

Return, in this order:

1. Vulnerable-path and invariant statement.
2. Positive/negative case matrix with fixtures and expected outcomes.
3. Layer/CI placement and flake policy (zero pass-masking retries for expected-denial cases).
4. Evidence and retest plan.
5. Coverage limitations and residual risk.

## Validation Checklist

- Pre-fix vulnerable path and invariant stated.
- At least one expected-denial negative case per forbidden action; positive control included.
- Fixtures are safe, synthetic and deterministic; no real secrets/production data.
- CI placement and flake policy defined: expected-denial cases get zero pass-masking retries; diagnostic reruns preserve the first failure as the verdict; no weakened assertions.
- Red-before/green-after or equivalent retest evidence required.
- Coverage limitations and residual risk stated honestly.

## Gotchas

- A test that passes before the fix is not a regression test.
- Asserting only the happy path leaves the denial branch unprotected.
- Real production-like fixtures introduce secrets and PII; use synthetic tenants.
- Retries can mask a real security regression: expected-denial failures are never retried into green, and a diagnostic rerun keeps the first failure as the verdict.
- Weakening an existing security assertion to make CI green is a regression, not a fix.

## Stop Conditions

- The request is reviewing the security diff: route to security-pr-reviewer.
- The request is curating an existing suite: route to regression-suite-curator.
- The request is multi-tenant isolation testing: route to multi-tenant-security-tester.
- The request is browser E2E: route to playwright-e2e-engineer.
- The request is writing the implementation: route to tdd-engineer/appsec-implementer.
- The fix or vulnerable path is unknown: ask for it instead of inventing a harness.
- The caller wants CI weakened to pass: refuse and record the risk.

## Supporting Files

- [security-regression-checklist](references/security-regression-checklist.md) - Security regression harness checklist and evidence rules.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 03 #125 (Security Regression Harness); coverage roadmap #125. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
