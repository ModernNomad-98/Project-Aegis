# QA scenario extensions: roadmap #231/#232/#233/#234

Reference for the `test-plan-designer` skill (extension-only bundle; no coverage-map status change in this batch). It supplies scenario shapes for the four adjacent QA backlog rows and names the owners whose mechanisms the planner cites; it never edits test code or claims a rerun.

## Row #231 - Timezone QA Strategy (PARTIAL; `saas-timezone-architect` mechanism)

- Plan cases around UTC instant vs local-intent storage: a user near midnight, a DST spring-forward gap and a fall-back overlap, and a tenant zone override.
- Ask for the expected observable per case (stored instant, rendered local time, scheduled-job fire time) before the run.
- Owner boundary: timezone CONTRACT design is `saas-timezone-architect`; this planner consumes it.

## Row #232 - Notification QA Strategy (PARTIAL; `notification-webhook-ux-designer` mechanism)

- Plan: notification preference respected, quiet-hours/tenant policy honoured, duplicate suppression, retry after transient failure, and unsubscribe/opt-out taking effect on every channel.
- Assert on the delivered/suppressed record and the user-visible state, not only on a queued event.
- Owner boundary: notification UX/design is `notification-webhook-ux-designer`; delivery mechanics stay with their owners.

## Row #233 - Import QA Strategy (GAP; `import-pipeline-architect` mechanism)

- Plan: preview -> review -> confirm, a partial import with per-row failures, a duplicate upload (idempotent re-run), and an unauthorized confirm.
- Every case states the recovery/reversal expectation and the audit event that proves it.
- Owner boundary: import pipeline design is `import-pipeline-architect`.

## Row #234 - Export QA Strategy (GAP; `export-pipeline-architect` mechanism)

- Plan: request -> async status -> download, an expired artifact, re-request after expiry, a cross-tenant request that must be denied, and field-level redaction in the exported file.
- Assert on job status transitions, artifact scope and redaction, never on internal rows alone.
- Owner boundary: export pipeline design is `export-pipeline-architect`; migration-runbook concerns are `data-migration-runbook-author`.

## Use rules

- Scenarios are starting points: trace each one to a risk and a layer, and keep them out of the coverage claim until an assertion exists.
- Do not re-grade #231-#234 in the coverage map from this reference; that is a planning-gate decision.
