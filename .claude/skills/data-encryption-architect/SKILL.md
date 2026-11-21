---
name: data-encryption-architect
description: 'Use when encryption in transit and at rest must be designed across data classes, stores and trust boundaries: classify data, inventory stores and flows, design TLS/mTLS termination and certificate ownership, choose per-store encryption and customer-managed keys, define the KMS key hierarchy, custody, rotation and revocation, crypto-shredding and evidence. Design-only: no key, credential, console or rotation is executed; stored-credential execution routes to secrets-identity-hardener (manual), cloud config review to cloud-security-baseline-reviewer, IaC review to iac-reviewer and PII lifecycle to pii-lifecycle-designer. NOT for stored-credential hashing, envelopes or rotation versions (secrets-identity-hardener), backup-encryption verification (database-backup-verifier), appsec implementation (appsec-implementer) or compliance certification (compliance family).'
---

# Data Encryption Architect

Terms: **family 26** - Data protection (README roster family 26; docs/skills-catalog.md Data protection family, EVG-12); **design-only** means this skill produces a design and its evidence record and never touches a key, credential, console, rotation or provider API.

## Purpose

Design encryption in transit and at rest across every store and trust boundary a system uses, and record the decision with its evidence. The deliverable is an ENCRYPTION DESIGN: data classes, a transit design (TLS/mTLS, termination points, internal hops, certificate ownership and lifecycle), a per-store at-rest design (provider default versus customer-managed key, envelope encryption), a KMS key hierarchy with custody, rotation and revocation, deletion and crypto-shredding semantics, inherited protection for backups, replicas and DR copies, the evidence each claim rests on, residual risk and handoffs. Encryption choices are architecture, not configuration: this skill decides them and hands execution to the named owners.

The skill is **auto-invocable and design-only**. It reads supplied facts, states every provider-specific detail as a verification item, and never claims a control is configured, rotated or verified. Execution, cloud configuration changes and provider verification are delegated host/user actions under the named owners.

## Use When

- A concrete request like: Design encryption in transit and at rest for our SaaS stores and trust boundaries.
- A new store, region, integration, backup path or key-management model is being added and its encryption design must be decided before build.
- A design review, security questionnaire or architecture decision needs the recorded encryption design, its key hierarchy and its evidence pointers.
- An audit question exposes that nobody owns the encryption design, the certificate lifecycle or the rotation policy.

**Do not use when:** the request belongs to a named neighbouring owner (the complete routing list is in Stop Conditions), or when the only ask is to execute a rotation, verify a backup or certify compliance.

## Inputs to Inspect

- Data classes: the classification scheme and each class's sensitivity, retention and deletion rules; classification is agreed with `pii-lifecycle-designer`, whose lifecycle record this skill consumes rather than re-derives.
- Stores and flows: every database, object store, cache, search index, queue, log sink, backup target, analytics store and third-party processor, plus what data each holds and which flows cross which boundary.
- Trust boundaries: browser to edge, edge to application, service to service, application to store, region to region, cloud account to cloud account, and third-party processor boundaries, mapped by the caller or `threat-modeler`.
- Residency, contractual and regulatory constraints by store and region, stated as constraints - not as a compliance conclusion.
- Threat model or risk register entries that name interception, store compromise, backup theft or key compromise as a concern.
- Provider facts: the caller's provider, service tier and feature availability. Every provider-specific statement is a verification item to confirm against current provider documentation; nothing is asserted from memory.

## Workflow

1. Classify the data: for each flow and store name the data class, sensitivity, retention and deletion requirement, and cite the classification source. Where no classification exists, mark it an open input, not a guess.
2. Inventory stores and flows: one row per store and per flow, with the boundary it crosses and the owner who can change it.
3. Design transit: choose TLS versus mTLS per hop, name every termination point, separate external from internal hops, and define certificate ownership, issuance, renewal, revocation and trust-anchor lifecycle. State where encryption ends and where a hop is plaintext.
4. Design at rest per store: for each store decide provider-default encryption versus a customer-managed key, and where envelope encryption is required, define the data key and wrapping key roles. Record the decision and the rejected alternative.
5. Define the key hierarchy: KMS root and key hierarchy, per-store and per-tenant keys, custody (who can use, who can administer, who can delete), separation of duties, rotation policy and triggers, revocation and compromise response, and deletion authority.
6. Design deletion and crypto-shredding: which data is destroyed by key destruction versus by record deletion, when key destruction is irreversible, what remains readable in backups, logs and caches, and the evidence that proves each deletion path.
7. Propagate to backups, replicas and DR copies: state that every copy inherits the at-rest design, or name the exception and its compensating control.
8. Record the decision and evidence: decision record, owner, date, alternatives rejected, and the evidence each claim needs - without claiming it was collected.
9. Hand off: execution of keys, credentials and rotations to `secrets-identity-hardener` (manual); cloud configuration review to `cloud-security-baseline-reviewer`; IaC review to `iac-reviewer`; PII lifecycle design to `pii-lifecycle-designer`; implementation to the authorized implementer.

## Output Format

Return an **ENCRYPTION DESIGN** with these parts, in order:

1. Scope: systems, stores, flows, regions and accounts covered; what is explicitly out of scope.
2. Data classes: class, sensitivity, retention/deletion rule, classification source, stores and flows it appears in.
3. Transit table: hop, boundary, TLS or mTLS, termination point, certificate owner, renewal and revocation, residual plaintext.
4. At-rest table: store, data class, provider default or customer-managed key, envelope encryption, key reference, custody, evidence.
5. Key hierarchy: root, wrapping and data keys, per-tenant scoping, custody and separation of duties, rotation triggers, revocation path.
6. Rotation: what rotates, on which trigger, who executes it, how the old key is retired, and the compatibility window.
7. Deletion: record deletion versus crypto-shredding, reversibility, backup/replica coverage, evidence of completion.
8. Evidence: per claim, what artifact would prove it and where it lives; uncollected items marked UNVERIFIED.
9. Residual risk: what remains exposed in transit or at rest, and the accepted owner decision if any.
10. Handoffs: exact owner and deliverable for each execution or review item.

## Validation Checklist

- [ ] Every store in the inventory appears in the at-rest table, including caches, queues, logs, backups and analytics.
- [ ] Every trust boundary is covered by a transit decision, and plaintext hops are stated, not implied.
- [ ] Certificate ownership and lifecycle (issue, renew, revoke, trust anchor) are assigned to a named role.
- [ ] Each at-rest choice states provider default versus customer-managed key, with the rejected alternative and reason.
- [ ] The key hierarchy names custody, separation of duties, rotation triggers and revocation, and accepts that a destroyed key is unrecoverable.
- [ ] Crypto-shredding is distinguished from record deletion and its limits in backups, replicas and logs are stated.
- [ ] Backups, replicas and DR copies either inherit the design or carry a named exception.
- [ ] Every provider-specific fact is marked "verify against current provider documentation".
- [ ] No claim says a control is configured, rotated, tested or compliant; uncollected evidence is UNVERIFIED.
- [ ] Handoffs name the owning skill and deliverable, with `secrets-identity-hardener` marked manual-only.

## Gotchas

- Treating "encryption at rest is enabled" as the design: it says nothing about key custody, rotation, deletion or backups.
- Designing TLS only at the edge while internal hops, queue consumers or replicas stay plaintext or default-encrypted.
- Forgetting certificate lifecycle: expiry, renewal ownership and revocation are part of the transit design.
- Assuming crypto-shredding erases copies in backups, caches, search indexes and logs when the key was copied elsewhere.
- Letting a customer-managed key design omit custody and separation of duties, so the same role can use, rotate and delete the key.
- Stating a provider capability, default, limit or tier from memory instead of marking it a verification item.
- Sliding from "designed" into "configured" in the write-up, which turns a design into an unverified compliance claim.

## Stop Conditions

- The caller wants keys created, rotated, revoked, exported or deleted, a console or API exercised, or a certificate issued: refuse; this skill is design-only. Hand execution to `secrets-identity-hardener` (manual-only) for stored credentials and key material, and to the owning platform operator for provider console actions.
- The ask is stored-credential hashing, secret envelopes or rotation versions: `secrets-identity-hardener` owns it, manual-only; this skill designs storage encryption, not credential storage.
- The ask is to review configured cloud accounts, baseline controls or live settings: `cloud-security-baseline-reviewer`; this skill designs, it does not inspect an account.
- The ask is a review of infrastructure-as-code changes: `iac-reviewer`; this skill produces the design that review checks against.
- The ask is PII lifecycle, retention scheduling or data-subject deletion mechanics: `pii-lifecycle-designer`; this skill consumes that record and designs the encryption that supports it.
- The ask is to verify backups exist, restore or are encrypted in practice: `database-backup-verifier`; this skill designs what backups must inherit.
- The ask is to implement or test an application control: `appsec-implementer` (manual-only); this skill stops at the design.
- The ask is to certify, attest or opine on ISO 27001, SOC 2, GDPR or any legal obligation: refuse the claim and route to the compliance family (`compliance-control-foundation`, `iso-27001-isms-architect`, `soc2-trust-criteria-mapper`); this skill records encryption decisions, not compliance status.
- A provider-specific fact is unavailable and cannot be verified: do not assert it from memory; mark it a verification item and name who must confirm it against current provider documentation.
- Required inputs (data classes, store inventory, threat model, residency constraints) are missing: state what is missing and mark the affected design areas UNVERIFIED instead of inventing them.

## Supporting Files

- [encryption-decision-matrix](references/encryption-decision-matrix.md) - store-type matrix, transit options, key custody options, rotation triggers, crypto-shred semantics and the evidence list.
- [evals/evals.json](evals/evals.json) - the 5 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 8 trigger-discrimination cases (1 positive / 7 negative) against the nearest manifest owners.

**Source:** docs/skills-catalog.md - Data protection family (EVG-12 encryption design gap, family 26). The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
