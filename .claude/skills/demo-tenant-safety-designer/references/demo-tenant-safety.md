# Demo tenant safety, seeding and reset rules

Reference for the demo-tenant-safety-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Demo and production are separated in identity, data, secrets and infrastructure.
- Seed data is synthetic; no real customer data path exists.
- Mutations are bounded and resettable; guardrails are stated.
- Demo roles/access are limited and audited.
- Reset/expiry is reliable and evidenced; conversion-to-real needs explicit approval.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- Sales or product demos need tenant-like environments.
- A demo environment might contain or leak real customer data.
- Demo tenants need reset, expiry or mutation guardrails.
- A demo tenant could be mistaken for production or be converted accidentally.

## 3. Output and evidence rules

1. Demo vs production separation model (identity, data, secrets, infrastructure).
2. Synthetic seed policy and generation rules.
3. Mutation guardrails and sandbox boundaries.
4. Access/role limits and reset/expiry plan.
5. Monitoring signals and conversion-to-real rules.

- Misuse signals: production DB/secret access, outbound email/payment/webhook attempts, data-volume anomalies, role escalation, export attempts; each with an alert owner and escalation path.
- Residual realism limits: state what the demo cannot mirror and the approval path if a closer mirror is needed.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Route cross-tenant leakage review of a real system to `tenant-isolation-reviewer`; this skill does not perform that owner's work.
- Route tenant-creation workflow and seeding to `tenant-provisioning-designer`; this skill does not perform that owner's work.
- Route executing non-production test-tenant creation to `test-tenant-provisioner`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `tenant-isolation-reviewer`, `tenant-provisioning-designer`, `test-tenant-provisioner`, `multi-tenant-security-tester`, `tenant-modeler`, `secrets-identity-hardener`, `authorization-matrix-designer`, `audit-log-architect`, `saas-platform-architect`, `membership-invitation-designer`, `admin-console-architect`, `observability-operator`, `release-readiness-reviewer`, `secure-migration-reviewer` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Demo and production are separated in identity, data, secrets and infrastructure.
- Seed data is synthetic; no real customer data path exists.
- Mutations are bounded and resettable; guardrails are stated.
- Demo roles/access are limited and audited.
- Reset/expiry is reliable and evidenced; conversion-to-real needs explicit approval.
- No provisioning or live environment mutation is performed by the design.
- Concrete misuse signals and their alert owner/escalation path are defined.
