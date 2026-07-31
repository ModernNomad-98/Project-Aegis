# Skill-contract audit — baseline report

- Engine: `audit-skill-contracts` v2.0.0; rule catalog v2.0.0 (27 rules, `scripts/audit-rules.yaml`)
- Repo SHA: `f88b56f12676c3a3ee47a245284c9190e61af5d1` (branch `audit/aegis-corpus-contract-baseline`; working tree dirty: true; dirty scanned surfaces: none)
- Corpus content hash: `754184b16ec473970951f9af9590566c7ef7ef95611d4c6a7b0bc4761fb9d754`
- Skills scanned: **184**
- Findings: **334** (321 mechanical, 13 semantic-review candidates)

A baseline finding is EXPECTED here: this report freezes the state of
the corpus BEFORE remediation. A finding below is not a tool failure,
structural findings are not behavioral proof, and rows marked
SEMANTIC-REVIEW CANDIDATE are queue entries for the named reviewer
skill — never mechanically proven defects.

| Severity | Count |
|---|---:|
| P0 | 1 |
| P1 | 17 |
| P2 | 5 |
| info | 311 |

| Rule | Count |
|---|---:|
| APPR-002 | 1 |
| ARTF-001 | 10 |
| EVAL-004 | 5 |
| ROUTE-002 | 311 |
| ROUTE-003 | 1 |
| STATE-005 | 2 |
| VOCAB-002 | 4 |

## Findings (P0/P1 + all semantic-review candidates)

- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/agent-authorization-matrix/SKILL.md:72` (owner: agent-authorization-matrix; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/agent-containment-reviewer/SKILL.md:76` (owner: agent-containment-reviewer; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/agent-memory-governance/SKILL.md:56` (owner: agent-memory-governance; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/audit-log-architect/SKILL.md:7` (owner: audit-log-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('durably') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/human-approval-boundary/SKILL.md:44` (owner: human-approval-boundary; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/offline-first-sync-architect/SKILL.md:74` (owner: offline-first-sync-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/operational-vs-analytical-splitter/SKILL.md:88` (owner: operational-vs-analytical-splitter; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ROUTE-003** [P1/high/mechanical] `.claude/skills/project-orchestrator/SKILL.md:138` (owner: project-orchestrator; maps: AEGIS-035, AEGIS-045) — Stage 2 route reaches roadmap-to-commitments-translator without roadmap-under-uncertainty-planner, but the commitments skill declares a roadmap as its input and the prioritization skill hands sequencing to the roadmap planner (AEGIS-035)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/project-orchestrator/SKILL.md:262` (owner: project-orchestrator; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **STATE-005** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/project-orchestrator/references/project-state-template.md:71` (owner: project-orchestrator; maps: AEGIS-002, AEGIS-006) — append-only-declared file contains narrative section '## MVP scope (approved)' with no defined supersession mechanics (how is it updated without rewriting bytes?)
- **STATE-005** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/project-orchestrator/references/project-state-template.md:122` (owner: project-orchestrator; maps: AEGIS-002, AEGIS-006) — append-only-declared file contains narrative section '## MVP scope (approved)' with no defined supersession mechanics (how is it updated without rewriting bytes?)
- **APPR-002** [P0/medium/SEMANTIC-REVIEW CANDIDATE → agent-governance-audit] `.claude/skills/project-orchestrator/references/project-state-template.md:140` (owner: project-orchestrator; maps: AEGIS-003, AEGIS-008) — scope grant that authorizes BUILDING from a requirements-stage approval: 'Build the v1 scope' (content approval must not become implementation authority)
- **VOCAB-002** [P1/high/mechanical] `.claude/skills/roadmap-under-uncertainty-planner/SKILL.md:3` (owner: roadmap-under-uncertainty-planner; maps: AEGIS-044, AEGIS-039) — 'committed' used as a roadmap HORIZON label ('committed/planned/exploratory') while roadmap-to-commitments-translator reserves 'committed' for capacity-backed promises (AEGIS-044)
- **VOCAB-002** [P1/high/mechanical] `.claude/skills/roadmap-under-uncertainty-planner/SKILL.md:62` (owner: roadmap-under-uncertainty-planner; maps: AEGIS-044, AEGIS-039) — 'committed' used as a roadmap HORIZON label ('committed/planned/\n   exploratory') while roadmap-to-commitments-translator reserves 'committed' for capacity-backed promises (AEGIS-044)
- **VOCAB-002** [P1/high/mechanical] `.claude/skills/roadmap-under-uncertainty-planner/SKILL.md:100` (owner: roadmap-under-uncertainty-planner; maps: AEGIS-044, AEGIS-039) — 'committed' used as a roadmap HORIZON label ('Now (committed)') while roadmap-to-commitments-translator reserves 'committed' for capacity-backed promises (AEGIS-044)
- **VOCAB-002** [P1/high/mechanical] `.claude/skills/roadmap-under-uncertainty-planner/references/roadmap-uncertainty-sheet.md:10` (owner: roadmap-under-uncertainty-planner; maps: AEGIS-044, AEGIS-039) — 'committed' used as a roadmap HORIZON label ('Committed / Planned / Exploratory') while roadmap-to-commitments-translator reserves 'committed' for capacity-backed promises (AEGIS-044)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/scoped-approval-register/SKILL.md:6` (owner: scoped-approval-register; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE → skill-quality-reviewer] `.claude/skills/streaming-event-architect/SKILL.md:75` (owner: streaming-event-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('Durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)

## P2/info findings (summarized; full detail in the JSON report)

- **EVAL-004** × 5 — e.g. `.claude/skills/agent-goal-hijack-defender/evals/trigger-evals.json`: trigger-evals neighbor 'ai-security-red-team-reviewer (subagent)' is annotated prose, not a resolvable name (target 'ai-
- **ROUTE-002** × 311 — e.g. `.claude/skills/ab-test-designer/SKILL.md`: exclusion toward `event-schema-architect` is not reciprocated (event-schema-architect's description never mentions this

## Vocabulary census (non-zero skills)

- `ab-test-designer`: planned×1
- `accessibility-test-harness`: accepted×1, committed×5, complete×1
- `admin-console-architect`: complete×1
- `adr-sequencer`: accepted×11, proposed×4
- `adr-writer`: accepted×3, complete×1, durable×1, proposed×4
- `agent-authorization-matrix`: accepted×1, complete×1, deployed×1, durable×4
- `agent-containment-reviewer`: durable×3
- `agent-failure-recovery`: committed×1, complete×1, verified×6
- `agent-governance-audit`: accepted×1, complete×1, durable×1, verified×1
- `agent-harness-architect`: complete×1, deployed×1, verified×4
- `agent-identity-privilege-reviewer`: durable×1, verified×2
- `agent-instruction-consolidator`: complete×1, verified×1
- `agent-memory-governance`: complete×1, durable×4, proposed×1, verified×8
- `agent-startup-context-gate`: committed×1, verified×12
- `agentic-loop-designer`: complete×1
- `ai-closeout-reporter`: complete×1
- `ai-cost-guardrail-designer`: estimated×3, verified×1
- `ai-governance-risk-reviewer`: accepted×1
- `ai-lifecycle-risk-manager`: accepted×1, complete×1, released×3, verified×2
- `ai-misinformation-guard`: verified×4
- `ai-router-architect`: estimated×2
- `ai-sdlc-operating-model`: complete×1, durable×1, verified×2
- `ai-threat-modeler`: accepted×4, targeted×1
- `api-contract-test-designer`: accepted×1, proposed×1
- `api-doc-generator-designer`: complete×3
- `api-event-architect`: planned×1
- `appsec-implementer`: accepted×1
- `architecture-designer`: proposed×2, verified×1
- `audit-log-architect`: accepted×1, durable×1
- `authority-invalidation-architect`: accepted×1, proposed×1, targeted×1, verified×1
- `aws-saas-architect`: accepted×1, complete×1, deployed×1, verified×4
- `azure-saas-architect`: accepted×1, deployed×1, verified×2
- `background-job-orchestration-architect`: complete×1
- `caching-strategy-designer`: proposed×1, targeted×1, verified×1
- `cell-based-architecture-designer`: complete×1
- `chat-backlog-reconciliation`: verified×1
- `ci-pipeline-architect`: accepted×1, committed×1, estimated×1
- `clickthrough-test-engineer`: deployed×2, planned×3
- `cloud-architecture-decider`: accepted×1, committed×4, complete×1, durable×2, verified×5
- `code-reviewer`: deployed×1
- `code-simplifier`: accepted×1, planned×1, verified×1
- `command-gateway-architect`: accepted×1, committed×1, complete×1, verified×2
- `compliance-control-foundation`: proposed×1, ready×1
- `compliance-evidence-collector`: complete×5
- `compliance-gap-auditor`: verified×2
- `context-co-update-ci-gate`: verified×5
- `contribution-guide-author`: accepted×4, verified×4
- `dast-safety-harness-designer`: complete×1
- `data-migration-runbook-author`: verified×4
- `data-partitioning-sharding-strategist`: complete×1
- `data-quality-monitor-designer`: complete×2, planned×1
- `design-review-facilitator`: complete×1, targeted×1
- `diataxis-doc-organizer`: complete×2
- `domain-modeler`: planned×1
- `error-handling-security-reviewer`: accepted×1, committed×3
- `eval-runner-designer`: complete×2, verified×1
- `feature-flag-rollout-strategist`: ready×1, targeted×1
- `file-upload-storage-architect`: complete×2
- `flaky-test-detective`: released×1, targeted×3
- `framework-edition-tracker`: released×2, verified×3
- `framework-mapping-refresher`: complete×3, proposed×9, targeted×3, verified×9
- `frontend-perf-engineer`: verified×1
- `full-codebase-auditor`: complete×1, verified×2
- `funnel-definition-designer`: complete×2
- `gated-deployment-prompt-template`: planned×1, ready×1, verified×4
- `horizontal-scalability-reviewer`: complete×1, planned×1, ready×6, verified×1
- `human-agent-trust-reviewer`: planned×1, proposed×1, verified×14
- `human-approval-boundary`: approved scope×1, durable×1
- `iac-reviewer`: committed×1, proposed×5
- `incident-response-runbook`: accepted×7, deployed×1, verified×2
- `inter-agent-comms-reviewer`: accepted×1, verified×3
- `intra-tenant-scope-architect`: complete×1
- `iso-27001-isms-architect`: accepted×1, complete×1, ready×1, verified×7
- `iso-42001-aims-architect`: verified×4
- `lane-authoring-guide`: committed×1, verified×4
- `latency-budget-architect`: estimated×1
- `library-diff-reviewer`: accepted×1
- `local-ci-mirror-preflight`: committed×2
- `manual-test-case-creator`: ready×1
- `memory-context-poisoning-reviewer`: targeted×1
- `merge-is-deploy-governance`: accepted×8, deployed×2, verified×8
- `model-context-designer`: complete×1
- `model-poisoning-reviewer`: targeted×3
- `multi-framework-crosswalk`: verified×9
- `n-plus-one-detector`: estimated×1
- `notification-webhook-ux-designer`: proposed×1
- `observability-operator`: complete×1, deployed×1, verified×2
- `offline-first-sync-architect`: accepted×1, complete×1, durable×3
- `onboarding-doc-designer`: verified×6
- `operational-vs-analytical-splitter`: durable×1, sequenced×1
- `performance-test-harness`: accepted×1, planned×1, ready×1
- `phased-work-handoff-designer`: sequenced×4, verified×1
- `principal-code-analyst`: prioritized×1
- `prioritization-frame-picker`: prioritized×1
- `profiling-methodology-designer`: proposed×1, targeted×1
- `project-orchestrator`: complete×9, deployed×1, durable×2, proposed×2, ready×4
- `promotion-packet-writer`: ready×3
- `qa-strategy-architect`: deployed×1
- `query-plan-reader`: proposed×1, sequenced×2, verified×2
- `readme-craftsman`: complete×1, verified×3
- `realtime-subscription-architect`: accepted×1, complete×1
- `release-readiness-reviewer`: ready×2, verified×2
- `reviewable-diff-discipline`: verified×1
- `rls-policy-auditor`: verified×3
- `roadmap-to-commitments-translator`: commit-able×7, committed×14
- `roadmap-under-uncertainty-planner`: committed×9, planned×7, prioritized×2
- `rollback-runbook-author`: deployed×1, verified×3
- `saas-cost-architect`: accepted×1, committed×1, complete×1
- `sast-orchestration-designer`: accepted×2, complete×1
- `schema-evolution-planner`: deployed×2, proposed×1, verified×1
- `scoped-approval-register`: committed×2, durable×5
- `screenshot-evidence-planner`: ready×2
- `search-architecture-designer`: complete×1
- `secrets-identity-hardener`: committed×9, complete×1
- `secure-migration-reviewer`: accepted×3, deployed×4, verified×1
- `security-logging-alerting-architect`: complete×1, planned×1
- `security-pr-reviewer`: accepted×1
- `security-scan-orchestrator`: complete×1, prioritized×2
- `sharded-validation-with-resume`: complete×1, targeted×2
- `share-link-access-architect`: complete×1, verified×1
- `skill-deprecation-planner`: planned×3, targeted×1
- `skill-usage-instrumenter`: committed×1, estimated×4
- `slo-reliability-architect`: complete×3, planned×5
- `soc2-trust-criteria-mapper`: committed×2, complete×1, verified×3
- `source-currency-auditor`: prioritized×2
- `source-of-truth-reconciler`: proposed×3
- `standing-approval-and-auto-advance`: planned×1
- `statement-of-applicability-author`: complete×1, planned×4, proposed×1
- `static-analysis-reviewer`: accepted×18, prioritized×3
- `streaming-event-architect`: accepted×1, deployed×1, durable×3, sequenced×1
- `structured-output-validator`: verified×1
- `sunset-deprecation-communicator`: planned×1, ready×1, targeted×7
- `superadmin-observability-console-designer`: complete×2, verified×5
- `supply-chain-security-reviewer`: accepted×4, committed×2
- `synthetic-monitoring-architect`: complete×1, verified×2
- `tech-spec-writer`: proposed×6
- `tenant-isolation-reviewer`: accepted×2, targeted×1, verified×1
- `tenant-modeler`: accepted×3, verified×1
- `test-data-architect`: planned×1
- `test-plan-designer`: complete×1, planned×3, verified×3
- `threat-modeler`: accepted×3, verified×3
- `usage-metering-and-cost-attribution-pipeline-designer`: complete×1, estimated×3
- `vite-build-qa-engineer`: ready×1, verified×3
