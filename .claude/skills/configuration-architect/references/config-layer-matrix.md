# Config Layer Matrix - configuration layer matrix with precedence and validation rules

Concrete artifact guide for the `configuration-architect` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Layers: build, runtime, tenant, user**
- **Precedence/override rules and conflict handling**
- **Validation per layer and on load**
- **Secret references vs literal values**
- **Ownership and change process per layer**
- **Drift detection and audit trail**
- **Migration path when a setting moves layer**

## 2. Worked table (configuration layer matrix with precedence and validation rules)

| Layer | Source | Precedence | Validation | Owner |
| --- | --- | --- | --- | --- |
| build | env at build | base | schema + required keys | platform team |
| tenant | tenant settings store | overrides runtime | per-tenant schema | tenant ops |

## 3. Construction steps

1. Inventory the config surface and hardcoded values.
2. Assign each setting to exactly one layer.
3. Define precedence and conflict resolution.
4. Specify validation and fail-fast behaviour.
5. Design secret references and precedence.
6. Plan ownership, audit and drift detection.
7. Define migration and rollback for layer moves.

## 4. Quality checks before returning

- Every setting has one owning layer
- Precedence is total and documented
- Secrets are references not literals
- Invalid config fails at startup with a safe message
- Drift is detectable and auditable

## 5. Failure/gotcha handling

- Two sources of truth for one setting cause silent tenant bugs
- Validation that happens after use is decoration
- Moving a setting between layers without migration breaks environments

## 6. Boundaries

- environment parity reviewer requests route to `environment-parity-reviewer`; this skill does not perform that owner work.
- secrets identity hardener requests route to `secrets-identity-hardener`; this skill does not perform that owner work.
- vite build qa engineer requests route to `vite-build-qa-engineer`; this skill does not perform that owner work.
- user preference architect requests route to `user-preference-architect`; this skill does not perform that owner work.
- tenant modeler requests route to `tenant-modeler`; this skill does not perform that owner work.
- feature flag architect requests route to `feature-flag-architect`; this skill does not perform that owner work.
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `code-reviewer`, `design-review-facilitator`, `environment-parity-reviewer`, `feature-flag-architect`, `human-approval-boundary`, `observability-by-design`, `plan-entitlement-architect`, `secrets-identity-hardener`, `tech-spec-writer`, `tenant-modeler`, `user-preference-architect`, `vite-build-qa-engineer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
