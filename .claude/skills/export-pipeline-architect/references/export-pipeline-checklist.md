# Export pipeline authorization, redaction and audit checklist

Reference for the export-pipeline-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Requester authority and tenant scope are explicit and deny-by-default.
- Job lifecycle covers status, notification, expiry and cleanup.
- Every redacted/excluded field has a classification basis.
- Delivery is bounded, single-use and expiring.
- Audit evidence records request, scope, redaction and delivery.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- A customer or tenant needs their data exported from the system.
- An existing export path has unclear authorization, scope or redaction rules.
- Export delivery, expiry, retention or audit evidence needs to be designed.
- A compliance or support request requires a safe, auditable export workflow.

## 3. Output and evidence rules

1. Requester/authority and tenant-scope rules.
2. Export job lifecycle and state/status model.
3. Redaction/exclusion map with classification basis.
4. Storage, delivery, expiry and cleanup controls.
5. Audit evidence and failure/partial-export handling.

- Delivery: short-lived single-use token, explicit reissue, access/download audit and cleanup evidence.
- Notification boundary: delivery/notification UX routes to notification-webhook-ux-designer.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Route per-store tenant scoping and context propagation to `multi-tenant-data-architect`; this skill does not perform that owner's work.
- Route audit event taxonomy, record schema and integrity to `audit-log-architect`; this skill does not perform that owner's work.
- Route external API/event contracts and delivery semantics to `api-event-architect`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `multi-tenant-data-architect`, `audit-log-architect`, `api-event-architect`, `tenant-isolation-reviewer`, `data-partitioning-sharding-strategist`, `sensitive-disclosure-guard`, `secure-migration-reviewer`, `authorization-matrix-designer`, `admin-console-architect`, `background-job-orchestration-architect`, `notification-webhook-ux-designer`, `data-quality-monitor-designer`, `static-analysis-reviewer`, `security-pr-reviewer` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Requester authority and tenant scope are explicit and deny-by-default.
- Job lifecycle covers status, notification, expiry and cleanup.
- Every redacted/excluded field has a classification basis.
- Delivery is bounded, single-use and expiring.
- Audit evidence records request, scope, redaction and delivery.
- Failure and partial exports are defined, not silently reported as complete.
- Delivery is short-lived and single-use with an explicit reissue path.
- Audit covers request, scope, redaction, delivery, access/download and cleanup proof.
