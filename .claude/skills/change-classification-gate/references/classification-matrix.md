# Change Classification Matrix

Supporting detail for `change-classification-gate`. Read on demand.

## Per-class definitions and validation detail

| Class | Counts as | Validation detail beyond the floor |
| --- | --- | --- |
| docs-only | Markdown/prose, comments, diagrams. NOT agent-instruction files. | Verify links resolve and any referenced files/paths exist. |
| ui-style | CSS, layout, copy, assets; no logic branches change. | Build passes; visual check of affected surfaces; note viewport assumptions. |
| frontend-logic | Component/state/routing behavior. | Unit tests for the changed behavior; build; note browser assumptions. |
| backend-api | Handlers, services, jobs, contracts; no schema change. | Unit/integration tests over the changed path; contract compatibility noted. |
| schema-migration | DDL, migration files, seed/backfill scripts. | Forward migration plan; explicit rollback; data-loss statement (even "none"); order-of-deploy notes. |
| rls-security | RLS policies, authz rules, session/trust handling, secrets paths. | Negative tests (what must now FAIL); reviewer named; tenant-scope reasoning written down. |
| cloud-iac | Terraform/Bicep/CloudFormation, CI/CD workflows, infra config. | Plan/diff output reviewed BEFORE apply; blast-radius statement; drift check. |
| ai-agentic | Prompts, skills, agent instructions, tool grants, model config. | Eval cases updated/added; guardrail review (tool permissions, autonomy, injection surface). |
| qa-test-only | Tests, fixtures, harnesses; production code untouched. | Run the suite; confirm snapshot/fixture changes are intended, not masking. |
| refactor | Structure changes with behavior preserved. | Tests green before AND after on the same suite; no public contract change, or reclassify. |
| bug-fix | Restoring intended behavior. | Reproduce the failure first; prove the fix flips it; regression test added. |
| release-deploy | Version cuts, deploys, feature-flag flips in shared envs. | Full gate: CI green, evidence bundle, rollback rehearsed or at least written. |

## Classification rules of thumb

- **Highest class governs approval.** A task that is 90% docs and 10% RLS is an
  RLS task for approval purposes; the docs part still only needs the docs floor.
- **When two classes could apply, take the riskier one.** The cost asymmetry is
  extreme: over-classifying wastes minutes, under-classifying ships unreviewed
  risk.
- **Class follows effect, not file extension.** A `.md` file that a tool
  executes or obeys (agent instructions, runbooks wired to automation) is not
  docs-only. A SQL file that only documents an example is not schema-migration.
- **Generated files inherit the class of their generator input**, not their own
  extension.

## Common misclassifications seen in practice

| Looks like | Actually is | Why |
| --- | --- | --- |
| docs-only edit to CLAUDE.md | ai-agentic | Steers every future agent run. |
| "add a column" backend task | schema-migration | DDL present; needs rollback + approval. |
| snapshot test update | qa-test-only OR a masked regression | Confirm the behavior change was intended before updating snapshots. |
| dependency bump | backend-api or release-deploy | Behavior and supply-chain surface change; check changelogs, run the suite. |
| "rename for clarity" sweep | refactor (broad) | Multi-module renames need behavior-preservation proof and approval. |
| workflow YAML tweak | cloud-iac | CI is infrastructure; a bad edit can bypass merge gates. |
