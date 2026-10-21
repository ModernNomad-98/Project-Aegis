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

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Cross-tenant leakage review of a real system routes to `tenant-isolation-reviewer`; this skill does not perform that owner's work.
- Tenant-creation workflow and seeding routes to `tenant-provisioning-designer`; this skill does not perform that owner's work.
- Executing non-production test-tenant creation routes to `test-tenant-provisioner`; this skill does not perform that owner's work.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Demo and production are separated in identity, data, secrets and infrastructure.
- Seed data is synthetic; no real customer data path exists.
- Mutations are bounded and resettable; guardrails are stated.
- Demo roles/access are limited and audited.
- Reset/expiry is reliable and evidenced; conversion-to-real needs explicit approval.
- No provisioning or live environment mutation is performed by the design.
