# Common Control Set — domain scaffold and mechanism map

Starter structure for the framework-agnostic catalog. Every control follows
the same row shape (ID, objective, owner, mechanism, evidence hook, status).
The right-hand column lists shipped skills and candidate artifacts to inspect.
It is a design/review route, not proof that a control operates. Mark a control
implemented only after checking its running mechanism, owner and dated
operating evidence; otherwise record partial or missing status.

## Domain 1 — Access control

| Starter control | Design/review route or candidate artifact to verify |
| --- | --- |
| Role/permission model, deny-by-default | `authorization-matrix-designer` matrix + enforcement-point map |
| Object-level / tenant-scoped authorization | `rls-policy-auditor` audit + `multi-tenant-security-tester` negative suite |
| Tenant isolation across all surfaces | `tenant-isolation-reviewer` review + isolation test matrix |
| Access reviews (periodic recertification) | often MISSING — net-new process; evidence = review records |
| Support/admin brokered access | `authorization-matrix-designer` support-access rules |

## Domain 2 — Cryptography

| Starter control | Design/review route or candidate artifact to verify |
| --- | --- |
| Secret/key custody, rotation, exposure | `secrets-identity-hardener` |
| Session/token security flags | `secrets-identity-hardener` |
| Encryption in transit / at rest design | PARTIAL by design (reconciliation D8/A04 residue) — carry as partial; design review is unowned |

## Domain 3 — Change management

| Starter control | Design/review route or candidate artifact to verify |
| --- | --- |
| Change classification + validation floor | `change-classification-gate` |
| Human approval at risk boundaries | `human-approval-boundary` |
| Reviewed, scoped diffs | `reviewable-diff-discipline`, `code-reviewer`, `security-pr-reviewer` |
| Migration/deploy safety | `secure-migration-reviewer` |
| Release gate + rollback | `release-readiness-reviewer`, `rollback-runbook-author` |

## Domain 4 — Logging & monitoring

| Starter control | Design/review route or candidate artifact to verify |
| --- | --- |
| Tenant-scoped audit trail (taxonomy, schema, integrity, retention) | `audit-log-architect` |
| Operational telemetry, alerts, health | `observability-operator`, `slo-reliability-architect` |
| Security-event detection/alerting | GAP by design (D8/A09 backlog: `security-logging-alerting-architect`) — carry as missing |

## Domain 5 — Incident response

| Starter control | Design/review route or candidate artifact to verify |
| --- | --- |
| Severity ladder, roles, comms, postmortem | `incident-response-runbook` |
| Containment/rollback execution path | `rollback-runbook-author` artifact invoked by reference |

## Domain 6 — Vendor management

| Starter control | Design/review route or candidate artifact to verify |
| --- | --- |
| Dependency/CI/artifact supply chain (incl. AI/ML + agentic surface) | `supply-chain-security-reviewer` (D6/D7 extensions included) |
| Provider data-use/retention terms for AI vendors | `ai-governance-risk-reviewer` data-governance step |
| Vendor risk assessment & review cadence | often MISSING — net-new process; evidence = assessments |

## Domain 7 — Risk assessment

| Starter control | Design/review route or candidate artifact to verify |
| --- | --- |
| Technical threat modeling (input to risk register) | `threat-modeler`, `ai-threat-modeler` |
| Risk register with owners, treatment decisions | often MISSING as a maintained artifact — net-new; the ISO projections require it (6.1) |
| Risk acceptance by a named human | `human-approval-boundary` |

## Domain 8 — AI governance (include when ISO 42001 / AI RMF in scope)

| Starter control | Design/review route or candidate artifact to verify |
| --- | --- |
| AI-SDLC stage/authority contract | `ai-sdlc-operating-model` |
| Standing agent authority (merge/deploy/auto-merge) | `agent-authorization-matrix` |
| Agent memory write/trust/hygiene | `agent-memory-governance` |
| Per-change process compliance audit | `agent-governance-audit` |
| Per-feature AI risk tiering + oversight | `ai-governance-risk-reviewer` |
| AI lifecycle risk program (GOVERN/MAP/MEASURE/MANAGE) | `ai-lifecycle-risk-manager` |

## Status vocabulary

- `implemented` — mechanism exists, runs, and has an evidence hook.
- `partial (<residue>)` — mechanism covers a slice; the named residue does
  not. Example: crypto custody implemented, encryption design review not.
- `missing` — no mechanism. Never dress a policy sentence as a control.

## Row template

```
[CC-<domain>-<nn>] <control name>
Objective:      <the risk this treats, one line>
Owner:          <named human or role>
Mechanism:      <verified running system or maintained process — or MISSING>
Design route:   <named skill if relevant; not evidence of operation>
Evidence hook:  <artifact + where it accrues> (→ compliance-evidence-collector)
Status:         implemented | partial (<residue>) | missing
```
