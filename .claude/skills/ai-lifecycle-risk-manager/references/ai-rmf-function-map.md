# AI RMF Function Map

Verified on NIST/AIRC pages: AI RMF 1.0 released 2023-01-26, voluntary;
Core = four functions (govern, map, measure, manage); GOVERN is
"a cross-cutting function that is infused throughout AI risk management";
Generative AI Profile NIST-AI-600-1 (2024-07-26); NIST notes 1.0 is under
revision — **check the current version and cite categories only from the
text in hand.**

## Function × lifecycle-stage practice matrix (starter)

| Stage | MAP | MEASURE | MANAGE | GOVERN thread |
| --- | --- | --- | --- | --- |
| Design | intake via `ai-governance-risk-reviewer` (tier, affected parties); `ai-threat-modeler` for the technical surface; provider/model provenance via `supply-chain-security-reviewer` | eval plan + thresholds designed (`ai-evaluation-harness`) | treatment decisions into the design; no-go escalation path | named owner assigned; appetite check |
| Development | context updates on scope change | evals run pre-merge; red-team cases | gaps fixed or accepted (named human, `human-approval-boundary`) | `ai-sdlc-operating-model` stage gates; `agent-authorization-matrix` authority |
| Deployment | final categorization; disclosure posture | regression gate on release (`release-readiness-reviewer` evidence) | rollback/kill-switch wiring (`agent-containment-reviewer`, `rollback-runbook-author`) | deploy authority per matrix |
| Operation | drift in context (new users, new data) re-maps | behavior/drift monitoring (`observability-operator`), eval re-runs on model/provider change | incidents via `incident-response-runbook`; containment authority severs credentials | periodic program review; register review cadence |
| Decommission | dependent-system map | final-state verification | model retirement; data/memory disposition (`agent-memory-governance`); credential revocation | sign-off by system owner |

## Owning-skill map (compose, never restate)

| Program need | Owning skill |
| --- | --- |
| Per-feature tier/oversight/disclosure | `ai-governance-risk-reviewer` |
| Feature threat enumeration | `ai-threat-modeler` |
| Eval datasets, graders, thresholds, CI gate | `ai-evaluation-harness` |
| Stage/authority SDLC contract | `ai-sdlc-operating-model` |
| Standing agent authority | `agent-authorization-matrix` |
| Memory hygiene/disposition | `agent-memory-governance` |
| Incident response | `incident-response-runbook` |
| Containment/kill switches | `agent-containment-reviewer` |
| Model/data supply chain | `supply-chain-security-reviewer` |
| Cost/consumption bounds | `ai-cost-guardrail-designer` |
| Certifiable wrapper | `iso-42001-aims-architect` |

## AI risk register row (shared with AIMS 6.1.2 where both run)

```
[AIR-<nn>] <risk> — system: <id> | stage: <lifecycle>
Mapped by: <practice/source> | Affected: <parties>
Measure: <metric/eval/monitor + threshold + cadence — or UNMEASURED (review date)>
Manage: <avoid|mitigate(<mechanism>)|transfer|accept(named human, date)>
Owner: <named human> | Next review: <date>
```

## Trigger table

| Trigger | Re-run |
| --- | --- |
| New AI system | full MAP; MEASURE plan; GOVERN owner assignment |
| Model/provider swap | MAP provenance; MEASURE re-baseline; MANAGE rollback check |
| Autonomy increase / new tool access | MAP + tier re-check (`ai-governance-risk-reviewer`); authority re-check |
| New affected population / geography | MAP + impact re-assessment (AIMS 6.1.4 where present) |
| Incident/postmortem | MANAGE routing; register update; MEASURE gap check |
| Scheduled program review | register sweep; RMF current-version check |
| Decommission decision | decommission row of the matrix |
