# Forty skill-reference pages after pull request #233

This batch starts from the exact pull request (PR) #233 merge
`b545d07591f1508b197d708b33cfd2991d50db58`. The original and current
batch estimates are **6–12 active hours**. The selected backlog at start is
**125–309 active hours**, including **30–115 documentation hours**. The
[acceptance checklist](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page)
requires a full-page reading, local links, an owning-skill contract check,
independent corrected-candidate review, and exact-head Actions. Two
read-only reviewers checked disjoint 20-page halves in full against the
owning skills and local links. Each rechecked the findings after correction;
both halves were accepted. Exact-head Actions and merge remain required.

The 40 pages are the next sorted skill references after
`qa-strategy-architect/references/risk-and-layer-catalog.md`. Two existing
pages needed no change; the others received the corrections recorded below.

| Existing reference (`.claude/skills/` prefix) | Full-page disposition and reason |
| --- | --- |
| `query-plan-reader/references/plan-reading-guide.md` | Corrected: analysis can execute writes; rollback does not undo external or nontransactional effects; plan terms and parent route clarified. |
| `rag-security-architect/references/rag-retrieval-authz.md` | Corrected: filtered search claims require evidence of authorized returned hits and metadata. |
| `readme-craftsman/references/readme-sheet.md` | Corrected: parent route and first-use terms. |
| `regression-suite-curator/references/curation-rules.md` | Corrected: historical roadmap label distinguished from current rule; demotion needs demonstrated equivalent protection. |
| `release-readiness-reviewer/references/readiness-evidence.md` | Corrected: first-use terms for check and approval evidence. |
| `requirements-gathering-facilitator/references/elicitation-sheet.md` | Corrected: parent route and local meaning of the first discovery stage. |
| `risk-tiered-validation-selector/references/classifier-rules.md` | Corrected: instruction paths force full validation. |
| `rls-policy-auditor/references/rls-audit-checklist.md` | Corrected: effective restricted-role tests and isolated failed-write examples. |
| `roadmap-to-commitments-translator/references/commitments-sheet.md` | Corrected: capacity arithmetic and human commitment boundary. |
| `roadmap-under-uncertainty-planner/references/roadmap-uncertainty-sheet.md` | Corrected: horizon labels, parent route, and nonbinding medium-confidence language. |
| `rollback-runbook-author/references/rollback-runbook-template.md` | Corrected: destructive repair checks effective existing grant before asking for missing scope. |
| `saas-platform-architect/references/platform-deployment-models.md` | Corrected: control-plane deployment is a per-capability decision; tenant enforcement fails closed before a second tenant. |
| `schema-evolution-planner/references/evolution-stage-playbook.md` | Corrected: compatibility follows the actual overlap and rollback window; contraction needs zero-reader and rollback-close evidence. |
| `scoped-approval-register/references/register-format.md` | Accepted unchanged: effective-grant and lifecycle examples already provide a clear parent-owned reference. |
| `screenshot-evidence-planner/references/evidence-rules.md` | Corrected: synthetic data still needs whole-frame sensitive-content inspection. |
| `secrets-identity-hardener/references/secret-classification-and-rotation.md` | Corrected: intended class and observed exposure are separate; rotation and purge check applicable grants. |
| `secure-migration-reviewer/references/migration-safety-checklist.md` | Corrected: old-shape removal needs all-reader, rollback and passing negative-test evidence. |
| `security-logging-alerting-architect/references/security-event-coverage-sheet.md` | Corrected: Internet Protocol address defined at first use. |
| `security-pr-reviewer/references/security-review-passes.md` | Corrected: parent route and first-use security terms. |
| `sensitive-disclosure-guard/references/disclosure-controls.md` | Corrected: minimization alone cannot authorize sending remaining sensitive fields to a training-on-inputs provider. |
| `sharded-validation-with-resume/references/shard-runner-design.md` | Corrected: parent route and runner terms. |
| `skill-deprecation-planner/references/deprecation-stage-playbook.md` | Corrected: applicable standing grants can cover a stage without a fresh approval. |
| `skill-quality-reviewer/references/quality-review-checklist.md` | Corrected: parent route and review terms. |
| `skill-usage-instrumenter/references/usage-signal-catalog.md` | Corrected: zero-use windows account for ship date and actual exposure. |
| `slo-reliability-architect/references/slo-derivation.md` | Corrected: an owning incident policy may page on urgent resource exhaustion. |
| `soc2-trust-criteria-mapper/references/tsc-scoping-map.md` | Accepted unchanged: scoping, source limits, and owning-skill route are clear. |
| `source-currency-auditor/references/currency-audit-sheet.md` | Corrected: parent route and first-use terms. |
| `source-of-truth-reconciler/references/conflict-resolution-examples.md` | Corrected: code in an examined tree does not alone prove deployed runtime behavior. |
| `staff-scope-selector/references/staff-scope-sheet.md` | Corrected: local meaning of staff and parent route. |
| `standing-approval-and-auto-advance/references/standing-approval-policy.md` | Corrected: template restatement does not extinguish an independent owner grant; disarming auto-merge checks authority. |
| `static-analysis-reviewer/references/triage-rubric.md` | Corrected: parent route and first-use terms. |
| `streaming-event-architect/references/backbone-decision-sheet.md` | Corrected: queue replay varies by transport; at-least-once delivery and idempotent effects separated. |
| `structured-output-validator/references/output-validation-patterns.md` | Corrected: parent route and first-use terms. |
| `sunset-deprecation-communicator/references/sunset-comms-sheet.md` | Corrected: deprecation and sunset field formats and owner-approved revised dates. |
| `superadmin-observability-console-designer/references/panel-taxonomy-and-read-security.md` | Corrected: thresholds require calibration; stale green results are visibly stale; live response has a human and runbook. |
| `supply-chain-security-reviewer/references/supply-chain-checklist.md` | Corrected: compare lockfile with installed graph; material consequences extend beyond execution and secret theft. |
| `systematic-debugger/references/isolation-tactics.md` | Corrected: lockfile experiments preserve unrelated work; parent route and diagnostic terms. |
| `system-prompt-leakage-reviewer/references/prompt-leakage-checks.md` | Corrected: parent route. |
| `tech-spec-writer/references/tech-spec-sheet.md` | Corrected: parent route and spec terms. |
| `tenant-isolation-reviewer/references/isolation-surface-checklist.md` | Corrected: parent route and isolation terms. |

The independent reviewers found and verified fixes for NULL semantics in
query plans, effective grants in secret rotation, an owning-skill severity
contract, queue replay wording, usage-window eligibility, and the sample
sunset date. The owning entrypoints for `secrets-identity-hardener`,
`skill-usage-instrumenter`, and `supply-chain-security-reviewer` were
aligned with their references; these previously accepted pages do not add
to this batch's 40 new acceptances. Local skill validation passed: 185
valid, zero warnings. Exact-head Actions and merge remain outstanding.
No provider call, private input, production operation, or host change is
part of this documentation batch. The new note itself enters the pending
dated-note bucket; it is not counted as an accepted existing page.
