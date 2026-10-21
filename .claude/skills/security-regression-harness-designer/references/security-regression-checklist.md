# Security regression harness checklist and evidence rules

Reference for the security-regression-harness-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Per fixed vuln: vulnerable path, violated invariant, forbidden outcome, expected denial.
- Case matrix: authorized positive control + one denial case per forbidden action + boundary/tenant variants.
- Fixtures: two-tenant/two-role synthetic data, deterministic ids, no real secrets/PII.
- Layer choice: cheapest reliable layer; API/service tests for authz, unit for policy, E2E only where necessary.
- CI: deterministic runs, bounded retries, failure artifacts, no assertion weakening.
- Evidence: red-before/green-after, expected denial output, honest not-covered list.

## 2. When this applies

- A security or authorization bug has been fixed and must never return.
- The existing tests pass even though the vulnerability existed.
- You need fixtures that reproduce the vulnerable access path without real secrets or production data.
- You must place the regression in the right CI layer with deterministic evidence.

## 3. Output and evidence rules

1. Vulnerable-path and invariant statement.
2. Positive/negative case matrix with fixtures and expected outcomes.
3. Layer/CI placement and flake policy.
4. Evidence and retest plan.
5. Coverage limitations and residual risk.

Every claim in the returned record is backed by inspected evidence or explicitly labeled **assumption**, **UNKNOWN** or **UNRUN**. An empty or unrun check is never a PASS. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Stop and route out when the request matches another owner; see Stop Conditions.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Pre-fix vulnerable path and invariant stated.
- At least one expected-denial negative case per forbidden action; positive control included.
- Fixtures are safe, synthetic and deterministic; no real secrets/production data.
- CI placement and bounded retry policy defined; no weakened assertions.
- Red-before/green-after or equivalent retest evidence required.
- Coverage limitations and residual risk stated honestly.
