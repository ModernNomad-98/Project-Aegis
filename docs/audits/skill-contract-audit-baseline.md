# Skill-contract audit — baseline report

> **What this page is.** The machine-generated summary of the latest
> skill-contract audit, for maintainers checking which skill texts the audit
> script flags for review. Everything below this note is script output.
>
> **Regenerated 2026-10-08 under AEGIS-APR-119** (an owner grant in the
> [approval register](../approvals/APPROVAL_REGISTER.md)) with engine v1.13.4,
> unchanged, over the Repo SHA below on branch
> `claude/sharp-lovelace-urgxpz-fu2`: a commit that contains every change the
> regenerating pull request (PR) makes to the files the audit reads (checkout
> with core.autocrlf=false, so the corpus hash is over LF (line feed,
> Unix-style line ending) bytes). The previous baseline (186 skills, 316
> findings, engine v1.13.4 over `5dbf7bc9e958d932bd0c5b093ebecfe61be41840`,
> PR #503 under AEGIS-APR-079) is in git history at
> `c14338d254bde3fd7fb9b8060033299cde5d5197` (#503's merge).
> Structural findings are not behavioral proof.

- Tool: `audit-skill-contracts` v1.13.4 (engine sha256 `e64b7430488c5f47…`)
- Repo SHA: `cbb084d6f1f2acbd2373510dbd5290dcb18f285a` (branch `claude/sharp-lovelace-urgxpz-fu2`; working tree dirty: false; dirty scanned surfaces: none)
- Corpus content hash: `673e7fe93c6ddfb84e485dae4be1f1538f85af6c4fbaed893323e42e7e886b14` (755 files, 5193044 bytes)
- Skills scanned: **195**; rules implemented: **27** (complete inventory, incl. zero-hit rules, in the JSON report)
- Findings: **339** (255 mechanical, 84 semantic-review candidates)

Findings are EXPECTED here: this report records the corpus as it is
at the Repo SHA above, after whatever remediation that commit already
contains. A finding below is open work or census data, not a tool
failure; structural findings are not behavioral proof, and rows marked
SEMANTIC-REVIEW CANDIDATE are readings for a reviewer skill — never
mechanically proven defects.

## How to read this report

- **SHA-256 / sha256:** a fingerprint of some bytes; any change to the bytes changes it. `engine sha256` fingerprints this audit script (first 16 hexadecimal, or hex, characters shown).
- **Repo SHA:** the Git commit ID of the checkout that was scanned.
- **Corpus content hash:** one SHA-256 over every audited skill file, so two reports with the same hash scanned the same bytes.
- **JSON report:** the machine-readable output of the same run (`--json`; JSON is JavaScript Object Notation). It holds every finding in full plus the complete rule inventory.
- **Severity:** P0 is the most serious, then P1, then P2; `info` is census data to look at, not a defect.
- **`[severity/confidence/kind]`:** after each finding's rule code. Confidence (high, medium or low) is how sure the rule is of its reading. Kind is `mechanical` (a text check that is true or false) or `SEMANTIC-REVIEW CANDIDATE` (a person must judge it). The rule table and the Coverage section call the same kind `semantic-candidate`, and the summary counts them as semantic-review candidates.
- **owner:** the skill whose files should change to resolve the finding.
- **maps: AEGIS-0NN:** the numbered defect this finding relates to (AEGIS-001 to AEGIS-059 in `docs/audits/volunteerflow/`, later ones in `docs/audits/aegis-060-plus-register.md`); `—` means none.
- **§5:** section 5, "Least privilege & side effects", of `docs/skill-generation-standard.md`.
- **Rule-table tags:** `(CENSUS)` marks a rule whose hits are `info` census data, not defects; `(STRUCTURAL)` means the rule checks only that something is present, not that it works.
- **Stage-2 / NOT-COMMIT-ABLE (ROUTE-003):** Stage 2 is project-orchestrator's "Define the product" stage. NOT COMMIT-ABLE is the readiness result recorded there, and by roadmap-to-commitments-translator, when the evidence a delivery commitment needs is missing.
- **auto-invocable:** a skill the model may start on its own, that is, one whose description does not begin MANUAL-ONLY.
- **SIDE-004 `[class]`:** the §5 side-effect class the matched text looks like: `source-write` (code, test or configuration edits), `doc-state-write` (writing a document or state file), `data-store-write` (writing to a database or live state), `deploy-provision` (deploying or creating infrastructure), `spend` (spending money), `vcs-mutation` (changing Git history or the working tree), `install` (installing packages or tools) or `network` (sending requests). The quoted text after the colon is the matched excerpt.
- **`term×N`** (vocabulary census): the skill uses that word N times.

| Rule | Default severity | Kind | What it flags | Findings |
|---|---|---|---|---:|
| SIDE-001 | P1 | mechanical | read-only-declared skill instructs artifact writes | 0 |
| SIDE-002 | P0 | mechanical | read-only-declared skill mentions scratch/temp/memory writes | 0 |
| SIDE-003 | P0 | mechanical | read-only-declared skill grants write-capable tools | 0 |
| SIDE-004 | P1 | semantic-candidate | auto-invocable skill's Workflow instructs a §5 mutation class without cover | 73 |
| APPR-001 | P1 | mechanical | bare generic status value with no approval class | 0 |
| APPR-002 | P0 | semantic-candidate | scope grant authorizing BUILD from a requirements-stage approval | 0 |
| APPR-003 | P1 | mechanical | approval record with allowed scope but no forbidden scope | 0 |
| STATE-001 | P0 | semantic-candidate | append-only-declared file carries mutable placeholders | 2 |
| STATE-002 | P0 | mechanical | append-only-declared file instructs overwrite/rewrite/truncate | 0 |
| STATE-003 | P0 | mechanical | middle insertion described inside an append-only contract | 0 |
| STATE-004 | P0 | semantic-candidate | exact-operation claim with unbound placeholders in command fences | 0 |
| STATE-005 | P1 | semantic-candidate | narrative approved-state section inside an append-only contract | 0 |
| ARTF-001 | P1 | semantic-candidate | durability claim without a durability level | 9 |
| ROUTE-001 | P1 | mechanical | routing reference to a name that is not on disk | 0 |
| ROUTE-002 | info | mechanical | exclusion toward a neighbor that never reciprocates (CENSUS) | 255 |
| ROUTE-003 | P1 | mechanical | a Stage-2 route reaches the commitments skill without a readiness/NOT-COMMIT-ABLE guard ON THAT ROUTE, or the roadmap owner is not independently classified | 0 |
| VOCAB-002 | P1 | semantic-candidate | committed used as a roadmap horizon label | 0 |
| VOCAB-003 | P0 | semantic-candidate | approved scope described as a commitment | 0 |
| PARITY-001 | P2 | mechanical | Validation Checklist with no checkable items | 0 |
| PARITY-002 | P2 | mechanical | Output Format too thin to verify against | 0 |
| EVAL-001 | P2 | mechanical | no negative discrimination case anywhere in the skill's evals (STRUCTURAL) | 0 |
| EVAL-002 | P2 | mechanical | eval case unjudgeable as written (per schema) | 0 |
| EVAL-003 | P1 | semantic-candidate | approval/state-related skill with no refusal or boundary case | 0 |
| EVAL-004 | P1 | mechanical | trigger-eval target does not resolve in the namespace its syntax declares | 0 |
| REF-001 | P1 | mechanical | markdown link target missing on disk | 0 |
| REF-002 | info | semantic-candidate | absolute user-machine path in shipped content | 0 |
| REF-003 | P1 | mechanical | bare references/ file mention missing on disk | 0 |

## Coverage (what was and was not reviewed)

- **Mechanically scanned:** all 195 shipped skills' SKILL.md + references + eval JSONs (this report).
- **Enumerated only (NOT content-audited):** reviewer agents (`.claude/agents/`) and guided-path docs (`docs/paths/`) — their FILENAMES feed name resolution and the manifest; their content is left to `scripts/validate-skills.py`, which checks agent frontmatter and guided-path links.
- **Auxiliary input (content read, NOT in the corpus hash):** `docs/skills-catalog.md` supplies the manifest `family` field. It, and the agent/guided-path filenames, are recorded separately under provenance `auxiliary_inputs`; the corpus content hash covers the skill corpus only. All input surfaces are containment-checked fail-closed before any read: a link or path that leads outside the repository stops the run.
- **Semantically reviewed:** none by this tool — semantic candidates are queued for the named reviewer skills, not executed here.
- **Behavioral evals:** UNRUN. No eval case is executed or reported as passing by this tool.
- **Rules whose own limits admit use-vs-mention or contextual ambiguity** (STATE-001, VOCAB-002/003, EVAL-003, SIDE-004, APPR-002, STATE-004/005, ARTF-001, REF-002) are classified semantic-candidate: their findings are review-queue entries a reviewer confirms, never mechanically proven defects.

| Severity | Count |
|---|---:|
| P0 | 2 |
| P1 | 82 |
| P2 | 0 |
| info | 255 |

| Rule | Count |
|---|---:|
| ARTF-001 | 9 |
| ROUTE-002 | 255 |
| SIDE-004 | 73 |
| STATE-001 | 2 |

## Findings (P0/P1 + all semantic-review candidates)

- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/adr-sequencer/SKILL.md` (owner: adr-sequencer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'record while a new ADR' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/adr-writer/SKILL.md` (owner: adr-writer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/adr-writer/SKILL.md` (owner: adr-writer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'Persist an ordinary non-executable ADR' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-authorization-matrix/SKILL.md:77` (owner: agent-authorization-matrix; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-containment-reviewer/SKILL.md:90` (owner: agent-containment-reviewer; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-governance-audit/SKILL.md` (owner: agent-governance-audit; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-harness-architect/SKILL.md` (owner: agent-harness-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'record schema itself is `audit-log' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-harness-architect/SKILL.md` (owner: agent-harness-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'write, design the test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/agent-memory-governance/SKILL.md:66` (owner: agent-memory-governance; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/ai-cost-guardrail-designer/SKILL.md` (owner: ai-cost-guardrail-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'spend budgets' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/ai-lifecycle-risk-manager/SKILL.md` (owner: ai-lifecycle-risk-manager; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/ai-sdlc-operating-model/SKILL.md` (owner: ai-sdlc-operating-model; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/architecture-advisor/SKILL.md` (owner: architecture-advisor; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/architecture-designer/SKILL.md` (owner: architecture-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the migration' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/audit-log-architect/SKILL.md` (owner: audit-log-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'update/delete attempts on audit records' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/audit-log-architect/SKILL.md` (owner: audit-log-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the negative-test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/audit-log-architect/SKILL.md:22` (owner: audit-log-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('durably') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/azure-saas-architect/SKILL.md` (owner: azure-saas-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/background-job-orchestration-architect/SKILL.md` (owner: background-job-orchestration-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/caching-strategy-designer/SKILL.md` (owner: caching-strategy-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/cell-based-architecture-designer/SKILL.md` (owner: cell-based-architecture-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/change-classification-gate/SKILL.md` (owner: change-classification-gate; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'apply per class' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/cloud-architecture-decider/SKILL.md` (owner: cloud-architecture-decider; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/cloud-architecture-decider/SKILL.md` (owner: cloud-architecture-decider; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'record to `adr' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/code-reviewer/SKILL.md` (owner: code-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/docs-as-code-architect/SKILL.md` (owner: docs-as-code-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/domain-modeler/SKILL.md` (owner: domain-modeler; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'buy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/feature-flag-rollout-strategist/SKILL.md` (owner: feature-flag-rollout-strategist; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'stage advances; do not assume a test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/full-codebase-auditor/SKILL.md` (owner: full-codebase-auditor; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/gated-deployment-prompt-template/SKILL.md` (owner: gated-deployment-prompt-template; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/gated-deployment-prompt-template/SKILL.md` (owner: gated-deployment-prompt-template; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'writes its report' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/gated-deployment-prompt-template/SKILL.md` (owner: gated-deployment-prompt-template; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the hard rules** — non-negotiables for every run of this class' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/horizontal-scalability-reviewer/SKILL.md` (owner: horizontal-scalability-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/human-approval-boundary/SKILL.md` (owner: human-approval-boundary; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/human-approval-boundary/SKILL.md:55` (owner: human-approval-boundary; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/incident-response-runbook/SKILL.md` (owner: incident-response-runbook; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploys' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/latency-budget-architect/SKILL.md` (owner: latency-budget-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'spend budget' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/llm-output-safety-reviewer/SKILL.md` (owner: llm-output-safety-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'writes and runs code' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/memory-context-poisoning-reviewer/SKILL.md` (owner: memory-context-poisoning-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'write — untrusted-derived entries' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/merge-is-deploy-governance/SKILL.md` (owner: merge-is-deploy-governance; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/merge-is-deploy-governance/SKILL.md` (owner: merge-is-deploy-governance; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'fix-forward — not a "gate failure' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/multi-tenant-data-architect/SKILL.md` (owner: multi-tenant-data-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the migration' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/offline-first-sync-architect/SKILL.md:89` (owner: offline-first-sync-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/onboarding-doc-designer/SKILL.md` (owner: onboarding-doc-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/operational-vs-analytical-splitter/SKILL.md:99` (owner: operational-vs-analytical-splitter; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/phased-work-handoff-designer/SKILL.md` (owner: phased-work-handoff-designer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'stage doesn\'t say "tests' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/product-analytics-instrumenter/SKILL.md` (owner: product-analytics-instrumenter; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'purchases' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/project-orchestrator/SKILL.md` (owner: project-orchestrator; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deployment' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/project-orchestrator/SKILL.md` (owner: project-orchestrator; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'create leg — the COMPLETE initial document' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **STATE-001** [P0/high/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/project-orchestrator/references/project-state-template.md:187` (owner: project-orchestrator; maps: AEGIS-002, AEGIS-006) — append-only-declared file carries mutable placeholder 'none yet' (will demand later replacement the contract forbids)
- **STATE-001** [P0/high/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/project-orchestrator/references/project-state-template.md:199` (owner: project-orchestrator; maps: AEGIS-002, AEGIS-006) — append-only-declared file carries mutable placeholder 'none yet' (will demand later replacement the contract forbids)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/qa-automation-architect/SKILL.md` (owner: qa-automation-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploys' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/qa-automation-architect/SKILL.md` (owner: qa-automation-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the migration' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/qa-strategy-architect/SKILL.md` (owner: qa-strategy-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'seeded database' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/qa-strategy-architect/SKILL.md` (owner: qa-strategy-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploys' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/realtime-subscription-architect/SKILL.md` (owner: realtime-subscription-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/regression-suite-curator/SKILL.md` (owner: regression-suite-curator; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'fixed bug' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/release-readiness-reviewer/SKILL.md` (owner: release-readiness-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploying' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/risk-tiered-validation-selector/SKILL.md` (owner: risk-tiered-validation-selector; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'Write the docs' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/risk-tiered-validation-selector/SKILL.md` (owner: risk-tiered-validation-selector; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the forced-full list:** surfaces whose risk ignores diff' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/rls-policy-auditor/SKILL.md` (owner: rls-policy-auditor; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'INSERT/effective check:** can a row' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/rls-policy-auditor/SKILL.md` (owner: rls-policy-auditor; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the negative-test' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/rollback-runbook-author/SKILL.md` (owner: rollback-runbook-author; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/saas-platform-architect/SKILL.md` (owner: saas-platform-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/saas-platform-architect/SKILL.md` (owner: saas-platform-architect; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'buy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/schema-evolution-planner/SKILL.md` (owner: schema-evolution-planner; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'deploy' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/schema-evolution-planner/SKILL.md` (owner: schema-evolution-planner; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'write from application code' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/scoped-approval-register/SKILL.md` (owner: scoped-approval-register; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [doc-state-write]: 'append-only file' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
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
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/soc2-trust-criteria-mapper/SKILL.md` (owner: soc2-trust-criteria-mapper; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [spend]: 'purchase' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/standing-approval-and-auto-advance/SKILL.md:117` (owner: standing-approval-and-auto-advance; maps: AEGIS-056, AEGIS-049) — claims durability ('durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **ARTF-001** [P1/medium/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/streaming-event-architect/SKILL.md:99` (owner: streaming-event-architect; maps: AEGIS-056, AEGIS-049) — claims durability ('Durable') without naming a durability level (transcript-only / workspace-persisted / Git-tracked / locally committed / remote-persisted / released)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/structured-output-validator/SKILL.md` (owner: structured-output-validator; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [data-store-write]: 'seeding a banned-content fixture' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/tenant-isolation-reviewer/SKILL.md` (owner: tenant-isolation-reviewer; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [source-write]: 'Write the negative-test plan**: concrete tests' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)
- **SIDE-004** [P1/low/SEMANTIC-REVIEW CANDIDATE] `.claude/skills/tenant-modeler/SKILL.md` (owner: tenant-modeler; maps: AEGIS-020, AEGIS-057) — auto-invocable skill's Workflow instructs a §5 mutation [deploy-provision]: 'provisioning' — semantic-review candidate (instruction vs teaching is the reviewer's judgment)

## P2/info findings (summarized; full detail in the JSON report)

- **ROUTE-002** × 255 — e.g. `.claude/skills/ab-test-designer/SKILL.md`: exclusion toward `event-schema-architect` is not reciprocated (event-schema-architect's description never mentions this skill) — census evidence, no AEGIS id

## Vocabulary census (non-zero skills)

- `ab-test-designer`: estimated×1, planned×5
- `acceptance-criteria-reviewer`: accepted×2, ready×4, verified×3
- `accessibility-test-harness`: accepted×1, committed×5, complete×1
- `admin-console-architect`: committed×1, complete×1, durable×2
- `adr-sequencer`: accepted×11, proposed×14
- `adr-writer`: accepted×4, complete×1, durable×1, proposed×5
- `aegis-setup`: complete×2, verified×3
- `agent-authorization-matrix`: accepted×1, complete×1, deployed×1, durable×8, verified×1
- `agent-containment-reviewer`: durable×3
- `agent-failure-recovery`: committed×1, complete×1, verified×7
- `agent-goal-hijack-defender`: planned×1, verified×1
- `agent-governance-audit`: accepted×1, complete×1, durable×1, verified×1
- `agent-harness-architect`: complete×1, deployed×1, verified×4
- `agent-identity-privilege-reviewer`: durable×1, verified×2
- `agent-instruction-consolidator`: complete×1, verified×1
- `agent-memory-governance`: complete×4, durable×6, proposed×1, verified×8
- `agent-startup-context-gate`: committed×1, verified×11
- `agentic-loop-designer`: complete×1, estimated×1
- `ai-closeout-reporter`: complete×5, verified×3
- `ai-cost-guardrail-designer`: estimated×4, verified×4
- `ai-evaluation-harness`: verified×1
- `ai-governance-risk-reviewer`: accepted×1
- `ai-human-in-the-loop-designer`: committed×9, proposed×6
- `ai-lifecycle-risk-manager`: accepted×1, complete×1, prioritized×1, released×2, verified×2
- `ai-misinformation-guard`: verified×4
- `ai-router-architect`: estimated×2
- `ai-sdlc-operating-model`: complete×1, durable×1, verified×2
- `ai-task-decomposer`: planned×2, ready×2, verified×4
- `ai-threat-modeler`: accepted×4, targeted×1
- `api-contract-test-designer`: accepted×1, proposed×1
- `api-doc-generator-designer`: complete×3, verified×3
- `api-event-architect`: complete×1, durable×1, planned×2
- `appsec-implementer`: accepted×1
- `architecture-designer`: proposed×1, verified×1
- `audit-log-architect`: accepted×1, durable×1
- `authority-invalidation-architect`: accepted×2, proposed×2, targeted×1, verified×1
- `aws-saas-architect`: accepted×1, complete×1, deployed×1, verified×5
- `azure-saas-architect`: accepted×1, deployed×1, verified×2
- `background-job-orchestration-architect`: complete×1
- `caching-strategy-designer`: accepted×1, proposed×1, targeted×1, verified×1
- `cell-based-architecture-designer`: complete×1
- `chat-backlog-reconciliation`: proposed×1, verified×2
- `ci-pipeline-architect`: accepted×1, committed×1, deployed×1, estimated×1, released×1
- `clickthrough-test-engineer`: deployed×2, planned×3, proposed×1
- `cloud-architecture-decider`: accepted×1, committed×4, complete×1, durable×3, estimated×3, verified×14
- `cloud-security-baseline-reviewer`: accepted×6, committed×1, complete×1
- `code-reviewer`: accepted×4, committed×2, deployed×1, proposed×1
- `code-simplifier`: accepted×1, planned×1, verified×1
- `command-gateway-architect`: accepted×1, committed×1, complete×1, verified×2
- `compliance-control-foundation`: proposed×1, ready×1, verified×11
- `compliance-evidence-collector`: complete×5, verified×1
- `compliance-gap-auditor`: verified×3
- `context-co-update-ci-gate`: verified×5
- `contribution-guide-author`: accepted×4, verified×5
- `cross-team-dependency-negotiator`: proposed×1
- `dast-safety-harness-designer`: complete×1
- `data-migration-runbook-author`: verified×4
- `data-partitioning-sharding-strategist`: complete×1, verified×1
- `data-quality-monitor-designer`: complete×2, planned×1
- `database-backup-verifier`: committed×3, estimated×11, proposed×1, verified×7
- `design-review-facilitator`: complete×1, targeted×1
- `diataxis-doc-organizer`: complete×2
- `docs-as-code-architect`: verified×1
- `docs-first-implementer`: proposed×1
- `docs-retention-index`: targeted×4
- `domain-modeler`: planned×1
- `environment-parity-reviewer`: committed×1
- `error-handling-security-reviewer`: accepted×1, committed×3
- `eval-runner-designer`: complete×2, proposed×2, verified×1
- `event-schema-architect`: complete×1, verified×4
- `feature-flag-architect`: planned×5, verified×4
- `feature-flag-rollout-strategist`: ready×1, targeted×1
- `file-upload-storage-architect`: complete×3
- `flaky-test-detective`: released×1, targeted×3
- `framework-edition-tracker`: released×2, verified×3
- `framework-mapping-refresher`: complete×3, proposed×10, targeted×3, verified×9
- `frontend-perf-engineer`: estimated×1, proposed×1, verified×1
- `full-codebase-auditor`: complete×1, verified×2
- `funnel-definition-designer`: complete×2
- `gated-deployment-prompt-template`: complete×2, estimated×3, planned×1, proposed×1, ready×1, verified×4
- `horizontal-scalability-reviewer`: complete×1, planned×1, ready×6, verified×1
- `human-agent-trust-reviewer`: planned×1, proposed×1, verified×14
- `human-approval-boundary`: approved scope×1, durable×3
- `iac-reviewer`: committed×1, proposed×5
- `incident-response-runbook`: accepted×5, deployed×1, verified×2
- `inter-agent-comms-reviewer`: accepted×1, verified×8
- `intra-tenant-scope-architect`: complete×1
- `iso-27001-isms-architect`: accepted×1, complete×1, deployed×1, ready×1, verified×10
- `iso-42001-aims-architect`: verified×9
- `lane-authoring-guide`: proposed×1, verified×4
- `latency-budget-architect`: estimated×1
- `library-diff-reviewer`: accepted×1
- `llm-output-safety-reviewer`: committed×4, verified×1
- `local-ci-mirror-preflight`: committed×2
- `manual-test-case-creator`: ready×1
- `memory-context-poisoning-reviewer`: targeted×1
- `merge-is-deploy-governance`: accepted×7, deployed×2, proposed×4, verified×8
- `model-poisoning-reviewer`: targeted×3
- `multi-framework-crosswalk`: proposed×1, verified×13
- `multi-tenant-data-architect`: verified×1
- `n-plus-one-detector`: proposed×3
- `notification-webhook-ux-designer`: proposed×1, verified×1
- `observability-operator`: complete×1, deployed×1, verified×2
- `offline-first-sync-architect`: accepted×1, complete×1, durable×4
- `onboarding-doc-designer`: verified×6
- `operational-vs-analytical-splitter`: durable×1, sequenced×1, verified×1
- `performance-test-harness`: accepted×1, planned×2, proposed×1, ready×1
- `phased-work-handoff-designer`: sequenced×4, verified×1
- `pii-lifecycle-designer`: proposed×2, verified×3
- `playwright-e2e-engineer`: deployed×1, estimated×1
- `principal-code-analyst`: prioritized×1
- `prioritization-frame-picker`: prioritized×1
- `product-analytics-instrumenter`: committed×1
- `product-spec-writer`: verified×1
- `profiling-methodology-designer`: complete×1, proposed×1, targeted×1
- `project-orchestrator`: accepted×22, approved scope×4, commit-able×9, committed×2, complete×42, deployed×1, proposed×11, ready×3, verified×3
- `promotion-packet-writer`: ready×3
- `prompt-injection-defender`: accepted×2
- `qa-strategy-architect`: deployed×1
- `query-plan-reader`: estimated×1, planned×1, proposed×1, sequenced×2, verified×2
- `readme-craftsman`: complete×1, verified×3
- `realtime-subscription-architect`: accepted×1, complete×1
- `release-readiness-reviewer`: deployed×1, ready×1, verified×3
- `requirements-gathering-facilitator`: complete×2
- `resilience-architecture-reviewer`: accepted×1, planned×1, verified×4
- `reviewable-diff-discipline`: verified×1
- `rls-policy-auditor`: verified×4
- `roadmap-to-commitments-translator`: approved scope×1, commit-able×34, committed×28, durable×2, proposed×2, verified×9
- `roadmap-under-uncertainty-planner`: commit-able×2, committed×3, estimated×3, planned×5, prioritized×2
- `rollback-runbook-author`: complete×1, deployed×1, verified×3
- `saas-cost-architect`: accepted×1, committed×1, complete×1
- `sast-orchestration-designer`: accepted×2, complete×1
- `schema-evolution-planner`: deployed×2, planned×1, proposed×2, verified×2
- `scoped-approval-register`: committed×3, complete×2, durable×2, proposed×3, verified×3
- `screenshot-evidence-planner`: ready×2, verified×3
- `search-architecture-designer`: complete×1
- `secrets-identity-hardener`: committed×9, complete×3
- `secure-migration-reviewer`: accepted×3, deployed×4, verified×1
- `security-logging-alerting-architect`: complete×1, planned×1
- `security-pr-reviewer`: accepted×1
- `security-scan-orchestrator`: complete×1, prioritized×2
- `sharded-validation-with-resume`: complete×1, targeted×2
- `share-link-access-architect`: complete×1, verified×2
- `skill-deprecation-planner`: planned×3, ready×1, targeted×1, verified×1
- `skill-usage-instrumenter`: estimated×4
- `slo-reliability-architect`: complete×4, planned×5
- `soc2-trust-criteria-mapper`: committed×2, complete×1, proposed×1, verified×5
- `source-currency-auditor`: prioritized×2
- `source-of-truth-reconciler`: deployed×1, proposed×5, verified×2
- `standing-approval-and-auto-advance`: durable×1, planned×1, proposed×1
- `statement-of-applicability-author`: complete×1, planned×4, proposed×1
- `static-analysis-reviewer`: accepted×20, prioritized×3
- `streaming-event-architect`: accepted×1, deployed×1, durable×3, sequenced×1
- `structured-output-validator`: verified×1
- `sunset-deprecation-communicator`: ready×1, targeted×7
- `superadmin-observability-console-designer`: complete×2, verified×5
- `supply-chain-security-reviewer`: accepted×4, committed×2, verified×8
- `synthetic-monitoring-architect`: complete×1, verified×2
- `tech-spec-writer`: proposed×6
- `tenant-isolation-reviewer`: accepted×2, targeted×1, verified×1
- `tenant-modeler`: accepted×3, verified×2
- `test-coverage-mapper`: verified×1
- `test-data-architect`: planned×1
- `test-plan-designer`: complete×1, planned×7, verified×3
- `test-tenant-provisioner`: committed×1
- `threat-modeler`: accepted×3, complete×1, proposed×1, verified×3
- `usage-metering-and-cost-attribution-pipeline-designer`: complete×1, estimated×3
- `vite-build-qa-engineer`: deployed×3, ready×1, verified×3
- `warehouse-lake-architect`: verified×1
