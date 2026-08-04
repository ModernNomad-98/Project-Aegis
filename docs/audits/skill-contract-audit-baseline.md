# Skill-contract audit — baseline report

- Tool: `audit-skill-contracts` v1.6.0 (engine sha256 `b287c96efc95c93d…`)
- Repo SHA: `ec58df0919ec9833d43482be107c088dcac028d0` (branch `fix/aegis-stage2-evidence-driven-route`; working tree dirty: false; dirty scanned surfaces: none)
- Corpus content hash: `f0d20f456671c9f6cf42b1cf3043557fc235e234424d1747f00c04df69ca2497` (704 files, 3918109 bytes)
- Skills scanned: **184**; rules implemented: **27** (complete inventory, incl. zero-hit rules, in the JSON report)
- Findings: **412** (316 mechanical, 96 semantic-review candidates)

A baseline finding is EXPECTED here: this report freezes the state of
the corpus BEFORE remediation. A finding below is not a tool failure,
structural findings are not behavioral proof, and rows marked
SEMANTIC-REVIEW CANDIDATE are readings for a reviewer skill — never
mechanically proven defects.

## Coverage (what was and was not reviewed)

- **Mechanically scanned:** all 184 shipped skills' SKILL.md + references + eval JSONs (this report).
- **Enumerated only (NOT content-audited):** reviewer agents (`.claude/agents/`) and guided-path docs (`docs/paths/`) — their FILENAMES feed name resolution and the manifest; their content is the validator's surface.
- **Auxiliary input (content read, NOT in the corpus hash):** `docs/skills-catalog.md` supplies the manifest `family` field. It, and the agent/guided-path filenames, are recorded separately under provenance `auxiliary_inputs`; the corpus content hash covers the skill corpus only. All input surfaces are containment-checked fail-closed before any read (no symlink/junction/repo-escape).
- **Semantically reviewed:** none by this tool — semantic candidates are queued for the named reviewer skills, not executed here.
- **Behavioral evals:** UNRUN. No eval case is executed or reported as passing by this tool.
- **Rules whose own limits admit use-vs-mention or contextual ambiguity** (STATE-001, VOCAB-002/003, EVAL-003, SIDE-004, APPR-002, STATE-004/005, ARTF-001, REF-002) are classified semantic-candidate: their findings are review-queue entries a reviewer confirms, never mechanically proven defects.

| Severity | Count |
|---|---:|
| P0 | 0 |
| P1 | 96 |
| P2 | 5 |
| info | 311 |

| Rule | Count |
|---|---:|
| ARTF-001 | 10 |
| EVAL-004 | 5 |
| ROUTE-002 | 311 |
| SIDE-004 | 82 |
| VOCAB-002 | 4 |

## Findings (P0/P1 + all semantic-review candidates)

- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/adr-sequencer/SKILL.md` (owner: adr-sequencer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'record) is written by `adr' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/adr-writer/SKILL.md` (owner: adr-writer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/adr-writer/SKILL.md` (owner: adr-writer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'create `docs/adr/` with `NNNN-title.md`' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-authorization-matrix/SKILL.md:72` (owner: agent-authorization-matrix; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-containment-reviewer/SKILL.md:76` (owner: agent-containment-reviewer; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-governance-audit/SKILL.md` (owner: agent-governance-audit; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-harness-architect/SKILL.md` (owner: agent-harness-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'record schema itself is `audit-log' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-harness-architect/SKILL.md` (owner: agent-harness-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'write, design the test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-memory-governance/SKILL.md:56` (owner: agent-memory-governance; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/ai-cost-guardrail-designer/SKILL.md` (owner: ai-cost-guardrail-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'spend budgets' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/ai-lifecycle-risk-manager/SKILL.md` (owner: ai-lifecycle-risk-manager; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/ai-sdlc-operating-model/SKILL.md` (owner: ai-sdlc-operating-model; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/architecture-advisor/SKILL.md` (owner: architecture-advisor; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/architecture-designer/SKILL.md` (owner: architecture-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the migration' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/audit-log-architect/SKILL.md` (owner: audit-log-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'update/delete attempts on audit records' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/audit-log-architect/SKILL.md` (owner: audit-log-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the negative-test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/audit-log-architect/SKILL.md:7` (owner: audit-log-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('durably') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/azure-saas-architect/SKILL.md` (owner: azure-saas-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/background-job-orchestration-architect/SKILL.md` (owner: background-job-orchestration-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/caching-strategy-designer/SKILL.md` (owner: caching-strategy-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/cell-based-architecture-designer/SKILL.md` (owner: cell-based-architecture-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/change-classification-gate/SKILL.md` (owner: change-classification-gate; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'apply per class' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/chat-backlog-reconciliation/SKILL.md` (owner: chat-backlog-reconciliation; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'Write the dated reconciliation doc' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/cloud-architecture-decider/SKILL.md` (owner: cloud-architecture-decider; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/cloud-architecture-decider/SKILL.md` (owner: cloud-architecture-decider; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'record to `adr' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/code-reviewer/SKILL.md` (owner: code-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/docs-as-code-architect/SKILL.md` (owner: docs-as-code-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/docs-first-implementer/SKILL.md` (owner: docs-first-implementer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'implemented defensively' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/domain-modeler/SKILL.md` (owner: domain-modeler; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'buy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/flaky-test-detective/SKILL.md` (owner: flaky-test-detective; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Fix that one cause at the test layer** when it is a test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/full-codebase-auditor/SKILL.md` (owner: full-codebase-auditor; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/gated-deployment-prompt-template/SKILL.md` (owner: gated-deployment-prompt-template; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/gated-deployment-prompt-template/SKILL.md` (owner: gated-deployment-prompt-template; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'writes its report' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/gated-deployment-prompt-template/SKILL.md` (owner: gated-deployment-prompt-template; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the hard rules** — non-negotiables for every run of this class' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/horizontal-scalability-reviewer/SKILL.md` (owner: horizontal-scalability-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/human-approval-boundary/SKILL.md:44` (owner: human-approval-boundary; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/incident-response-runbook/SKILL.md` (owner: incident-response-runbook; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploys' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/latency-budget-architect/SKILL.md` (owner: latency-budget-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'spend budget' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/llm-output-safety-reviewer/SKILL.md` (owner: llm-output-safety-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'writes and runs code' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/local-ci-mirror-preflight/SKILL.md` (owner: local-ci-mirror-preflight; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [vcs-mutation]: 'git worktree' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/memory-context-poisoning-reviewer/SKILL.md` (owner: memory-context-poisoning-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'write — untrusted-derived entries' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/merge-is-deploy-governance/SKILL.md` (owner: merge-is-deploy-governance; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/merge-is-deploy-governance/SKILL.md` (owner: merge-is-deploy-governance; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'fix-forward — not a "gate failure' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/multi-tenant-data-architect/SKILL.md` (owner: multi-tenant-data-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the migration' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/multi-tenant-security-tester/SKILL.md` (owner: multi-tenant-security-tester; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'Seed tenant A and tenant' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/multi-tenant-security-tester/SKILL.md` (owner: multi-tenant-security-tester; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'implement the suite' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/n-plus-one-detector/SKILL.md` (owner: n-plus-one-detector; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [install]: 'Install the regression guard' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/offline-first-sync-architect/SKILL.md:74` (owner: offline-first-sync-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/onboarding-doc-designer/SKILL.md` (owner: onboarding-doc-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/operational-vs-analytical-splitter/SKILL.md:88` (owner: operational-vs-analytical-splitter; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/phased-work-handoff-designer/SKILL.md` (owner: phased-work-handoff-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'stage doesn\'t say "tests' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/product-analytics-instrumenter/SKILL.md` (owner: product-analytics-instrumenter; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'purchases' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/project-orchestrator/SKILL.md` (owner: project-orchestrator; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/project-orchestrator/SKILL.md` (owner: project-orchestrator; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'create leg — the COMPLETE initial document' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/project-orchestrator/SKILL.md:332` (owner: project-orchestrator; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/qa-automation-architect/SKILL.md` (owner: qa-automation-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the migration' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/qa-strategy-architect/SKILL.md` (owner: qa-strategy-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'seeded database' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/query-plan-reader/SKILL.md` (owner: query-plan-reader; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'execution EXECUTES the write' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/query-plan-reader/SKILL.md` (owner: query-plan-reader; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'apply (via the change' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/realtime-subscription-architect/SKILL.md` (owner: realtime-subscription-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/regression-suite-curator/SKILL.md` (owner: regression-suite-curator; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'fixed bug' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/release-readiness-reviewer/SKILL.md` (owner: release-readiness-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploying' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/reviewable-diff-discipline/SKILL.md` (owner: reviewable-diff-discipline; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'record it for the closeout' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/risk-tiered-validation-selector/SKILL.md` (owner: risk-tiered-validation-selector; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'Write the docs' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/risk-tiered-validation-selector/SKILL.md` (owner: risk-tiered-validation-selector; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the forced-full list:** surfaces whose risk ignores diff' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/rls-policy-auditor/SKILL.md` (owner: rls-policy-auditor; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'INSERT/WITH CHECK:** can a row' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/rls-policy-auditor/SKILL.md` (owner: rls-policy-auditor; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the negative-test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **VOCAB-002** [P1/high/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/roadmap-under-uncertainty-planner/SKILL.md:3` (owner: roadmap-under-uncertainty-planner + roadmap-to-commitments-translator; maps: AEGIS-044, AEGIS-039) — 'committed' used as a roadmap HORIZON label ('committed/planned/exploratory') while roadmap-to-commitments-translator reserves 'committed' for capacity-backed promises (AEGIS-044)
- **VOCAB-002** [P1/high/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/roadmap-under-uncertainty-planner/SKILL.md:62` (owner: roadmap-under-uncertainty-planner + roadmap-to-commitments-translator; maps: AEGIS-044, AEGIS-039) — 'committed' used as a roadmap HORIZON label ('committed/planned/\n   exploratory') while roadmap-to-commitments-translator reserves 'committed' for capacity-backed promises (AEGIS-044)
- **VOCAB-002** [P1/high/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/roadmap-under-uncertainty-planner/SKILL.md:100` (owner: roadmap-under-uncertainty-planner + roadmap-to-commitments-translator; maps: AEGIS-044, AEGIS-039) — 'committed' used as a roadmap HORIZON label ('Now (committed)') while roadmap-to-commitments-translator reserves 'committed' for capacity-backed promises (AEGIS-044)
- **VOCAB-002** [P1/high/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/roadmap-under-uncertainty-planner/references/roadmap-uncertainty-sheet.md:10` (owner: roadmap-under-uncertainty-planner + roadmap-to-commitments-translator; maps: AEGIS-044, AEGIS-039) — 'committed' used as a roadmap HORIZON label ('Committed / Planned / Exploratory') while roadmap-to-commitments-translator reserves 'committed' for capacity-backed promises (AEGIS-044)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/rollback-runbook-author/SKILL.md` (owner: rollback-runbook-author; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/saas-platform-architect/SKILL.md` (owner: saas-platform-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/saas-platform-architect/SKILL.md` (owner: saas-platform-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'buy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/schema-evolution-planner/SKILL.md` (owner: schema-evolution-planner; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/schema-evolution-planner/SKILL.md` (owner: schema-evolution-planner; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'write from application code' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/scoped-approval-register/SKILL.md` (owner: scoped-approval-register; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'create the register' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/scoped-approval-register/SKILL.md:6` (owner: scoped-approval-register; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/screenshot-evidence-planner/SKILL.md` (owner: screenshot-evidence-planner; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'seeded data' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/search-architecture-designer/SKILL.md` (owner: search-architecture-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'write latency) vs asynchronous (index via change' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/search-architecture-designer/SKILL.md` (owner: search-architecture-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'buys' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/secure-migration-reviewer/SKILL.md` (owner: secure-migration-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'Deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/security-logging-alerting-architect/SKILL.md` (owner: security-logging-alerting-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'implemented by `observability-operator` (manual-only); logging changes' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/skill-deprecation-planner/SKILL.md` (owner: skill-deprecation-planner; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'record (catalog retired section + decision-log entry' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/skill-deprecation-planner/SKILL.md` (owner: skill-deprecation-planner; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'write the coverage diff' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/skill-quality-reviewer/SKILL.md` (owner: skill-quality-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploys' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/skill-quality-reviewer/SKILL.md` (owner: skill-quality-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'edits files/config' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/skill-quality-reviewer/SKILL.md` (owner: skill-quality-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'spends money' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/soc2-trust-criteria-mapper/SKILL.md` (owner: soc2-trust-criteria-mapper; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'buy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/streaming-event-architect/SKILL.md:75` (owner: streaming-event-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('Durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/structured-output-validator/SKILL.md` (owner: structured-output-validator; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'seeding a banned-content fixture' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/systematic-debugger/SKILL.md` (owner: systematic-debugger; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Fix one thing' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/tdd-engineer/SKILL.md` (owner: tdd-engineer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the failing test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/tenant-isolation-reviewer/SKILL.md` (owner: tenant-isolation-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the negative-test plan**: concrete tests' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/tenant-modeler/SKILL.md` (owner: tenant-modeler; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'provisioning' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/threat-modeler/SKILL.md` (owner: threat-modeler; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the validation test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)

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
- `project-orchestrator`: accepted×19, approved scope×4, commit-able×9, complete×41, deployed×1, durable×2, proposed×7, ready×3
- `promotion-packet-writer`: ready×3
- `qa-strategy-architect`: deployed×1
- `query-plan-reader`: proposed×1, sequenced×2, verified×2
- `readme-craftsman`: complete×1, verified×3
- `realtime-subscription-architect`: accepted×1, complete×1
- `release-readiness-reviewer`: ready×2, verified×2
- `reviewable-diff-discipline`: verified×1
- `rls-policy-auditor`: verified×3
- `roadmap-to-commitments-translator`: approved scope×1, commit-able×32, committed×25, durable×2, proposed×2, verified×7
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
