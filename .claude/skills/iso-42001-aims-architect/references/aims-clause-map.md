# AIMS Clause Map — ISO/IEC 42001:2023

Structure verified from the standard's own TOC (preview PDF, first edition
2023-12, ISO/IEC JTC 1/SC 42): harmonized clauses 4–10; AI risk assessment
6.1.2 / 8.2; AI risk treatment 6.1.3 / 8.3; AI system impact assessment
6.1.4 / 8.4; Annex A normative ("Reference control objectives and
controls"); Annex B normative guidance; Annex C/D informative. Finer wording
= verification items against the licensed text. **Annex A counts are never
stated** — public sources conflict.

## The three assessments (the standard's distinctive machinery)

| Assessment | Clause (plan / operate) | Object | Register/artifact |
| --- | --- | --- | --- |
| AI risk assessment | 6.1.2 / 8.2 | risks OF the AI systems to the org and its objectives | AI risk register (inputs: `ai-threat-modeler`, `ai-evaluation-harness` findings) |
| AI risk treatment | 6.1.3 / 8.3 | treatment decisions selecting Annex A objectives/controls | treatment plan → SoA (`statement-of-applicability-author`) |
| AI system impact assessment | 6.1.4 / 8.4 | consequences for INDIVIDUALS and SOCIETIES (fairness, safety, rights, societal effects) | per-system impact assessment with triggers (new system, material change, provider/model swap) and named reviewers |

Keep the three distinct: folding impact into org risk is the most common
design error and an audit finding — the object of assessment differs.

## Clause 4–10 artifact checklist (delta view vs a 27001 ISMS)

| Clause | AIMS-specific additions | Shareable with an existing ISMS |
| --- | --- | --- |
| 4 Context | AI system inventory with org role per system (developer / provider / user); affected individuals/groups as interested parties | issue analysis method, scope discipline |
| 5 Leadership | AI policy; named AI accountability | commitment pattern, role assignment discipline |
| 6 Planning | 6.1.2/6.1.3/6.1.4 machinery above; AI objectives | risk-method scaffolding |
| 7 Support | AI competence (model limits, failure modes); model/feature cards as documented information (`ai-governance-risk-reviewer`) | documented-information control, awareness machinery |
| 8 Operation | 8.2/8.3/8.4 in the AI lifecycle (`ai-sdlc-operating-model` stages; `ai-lifecycle-risk-manager` functions); third-party AI management (`supply-chain-security-reviewer` AI/ML surface) | operational planning discipline |
| 9 Performance evaluation | AIMS-scoped internal audit; management review with AI inputs | audit/review machinery and cadence |
| 10 Improvement | AI nonconformity routing (incl. incident learnings via `incident-response-runbook` postmortems) | corrective-action process |

## Shipped-artifact mechanism map (map, don't rebuild)

| AIMS need | Shipped mechanism |
| --- | --- |
| AI SDLC stage/authority contract | `ai-sdlc-operating-model` |
| Standing agent authority (merge/deploy/auto-merge bans) | `agent-authorization-matrix` |
| Agent memory write/trust/hygiene | `agent-memory-governance` |
| Per-change process compliance evidence | `agent-governance-audit` |
| Per-feature risk tier, oversight, disclosure, model card | `ai-governance-risk-reviewer` |
| AI threat models | `ai-threat-modeler` |
| Eval/red-team practice | `ai-evaluation-harness` |
| Injection/output/tool/memory controls | Phase 7 + 7.5 packs (via `compliance-control-foundation` AI domain) |
| Lifecycle risk program (GOVERN/MAP/MEASURE/MANAGE) | `ai-lifecycle-risk-manager` |

## Impact assessment design pattern (6.1.4 / 8.4)

- Triggers: new AI system; material change (model swap, autonomy increase,
  new affected population); provider/terms change; periodic review.
- Method: affected parties → potential consequences (fairness, safety,
  rights/access, societal) → severity/likelihood → mitigations or
  no-go escalation. Reuse `ai-governance-risk-reviewer` tiering as the
  per-feature input; the AIMS artifact is system-level and retained.
- Reviewers: named humans incl. someone independent of the building team;
  legal review hook for rights-affecting systems.
- Output feeds: risk register (6.1.2), treatment (6.1.3), and disclosure
  decisions.
