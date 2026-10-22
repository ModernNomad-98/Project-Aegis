# QA scenario extensions: roadmap #231/#232/#233/#234

Reference for the `test-plan-designer` skill (extension-only bundle; no coverage-map status change in this batch). It supplies scenario shapes for the adjacent QA backlog rows and names the owners whose mechanisms the planner cites; it never edits test code or claims a rerun.

## Row #231 - timezone and DST-sensitive journeys (PARTIAL; `saas-timezone-architect` mechanism)

- Plan cases around UTC instant vs local-intent storage: a user near midnight, a DST spring-forward gap and a fall-back overlap, and a tenant zone override.
- Ask for the expected observable per case (stored instant, rendered local time, scheduled-job fire time) before the run.
- Owner boundary: timezone CONTRACT design is `saas-timezone-architect`; this planner consumes it.

## Row #232 - tenant-data export journeys (PARTIAL; `export-pipeline-architect` mechanism)

- Plan: request -> async status -> download, an expired artifact, a re-request after expiry, and a cross-tenant request that must be denied.
- Assert on job status transitions and on artifact scope, never on internal rows alone.
- Owner boundary: export pipeline design is `export-pipeline-architect`.

## Row #233 - tenant-data import journeys (GAP; `import-pipeline-architect` mechanism)

- Plan: preview -> review -> confirm, a partial import with per-row failures, a duplicate upload (idempotent re-run), and an unauthorized confirm.
- Every case states the recovery/reversal expectation and the audit event that proves it.
- Owner boundary: import pipeline design is `import-pipeline-architect`.

## Row #234 - membership-invitation journeys (GAP; `membership-invitation-designer` mechanism)

- Plan: invite -> accept, expired single-use token, seat-limit rejection, wrong-recipient identity binding, and revoke-before-accept.
- Assert on one-time token semantics and role/seat outcome, not just on UI text.
- Owner boundary: invitation design is `membership-invitation-designer`.

## Use rules

- Scenarios are starting points: trace each one to a risk and a layer, and keep them out of the coverage claim until an assertion exists.
- Do not re-grade #231-#234 in the coverage map from this reference; that is a planning-gate decision.
