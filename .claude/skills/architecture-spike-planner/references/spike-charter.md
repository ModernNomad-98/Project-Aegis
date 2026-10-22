# Spike Charter - spike charter with question, hypotheses, timebox, evidence and exit criteria

Concrete artifact guide for the `architecture-spike-planner` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Question the spike must answer**
- **Hypotheses and disconfirming evidence**
- **Timebox and stop rule**
- **Evidence to collect and how**
- **Exit criteria and decision record**
- **Threats to validity**
- **What is thrown away vs kept**

## 2. Worked table (spike charter with question, hypotheses, timebox, evidence and exit criteria)

| Spike | Question | Timebox | Evidence | Exit criterion |
| --- | --- | --- | --- | --- |
| S-1 | can event ordering hold at 5k/s | 2 days | throughput/latency run | ordering violations 0 |
| S-2 | is the index usable at scale | 1 day | query plan + data | p95 under budget |

## 3. Construction steps

1. State the decision the spike informs.
2. List hypotheses and disconfirming evidence.
3. Set timebox and stop rule.
4. Define the evidence collection method.
5. Write exit criteria before starting.
6. Plan the decision record and owner.
7. Mark artifacts throwaway vs durable.

## 4. Quality checks before returning

- Question is decision-relevant
- Hypotheses are falsifiable
- Timebox and stop rule are explicit
- Evidence method is credible
- Exit criteria exist before the spike
- Decision and owner are recorded

## 5. Failure/gotcha handling

- A spike without a question becomes a prototype
- No stop rule means scope creep
- A spike whose artifacts become production code was not a spike

## 6. Boundaries

- roadmap under uncertainty planner requests route to `roadmap-under-uncertainty-planner`; this skill does not perform that owner work.
- ai task decomposer requests route to `ai-task-decomposer`; this skill does not perform that owner work.
- exploratory charter designer requests route to `exploratory-charter-designer`; this skill does not perform that owner work.
- architecture designer requests route to `architecture-designer`; this skill does not perform that owner work.
- tech spec writer requests route to `tech-spec-writer`; this skill does not perform that owner work.
- design review facilitator requests route to `design-review-facilitator`; this skill does not perform that owner work.
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `ai-task-decomposer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `exploratory-charter-designer`, `human-approval-boundary`, `observability-by-design`, `release-readiness-reviewer`, `roadmap-under-uncertainty-planner`, `rollback-runbook-author`, `security-pr-reviewer`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
