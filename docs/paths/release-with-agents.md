# Prepare a release with several agents

*This path coordinates existing Aegis skills and optional independent reviewers in your own product repository. Each linked skill owns its own method.*

**Who this is for:** your app is built and you want help checking, approving and
verifying a release. Aegis gives the coding assistant a guided procedure; the
assistant's host must support separate agents for genuinely independent reviews.
A skill is an instruction for an assistant, while an agent is a separate worker
with its own context. Aegis does not provide a live deployment service. Its
[delivery control plane](../../tools/aegis_delivery_control/README.md) currently
operates on synthetic authorities and targets only.

Open **your product repository** and say:

> Use `project-orchestrator` to prepare this app for release. Identify the exact
> release candidate and deployment trigger. Where separate read-only agents
> are supported, assign relevant code, security and quality assurance (QA)
> reviews with separate
> contexts. Tell me which Aegis skill you actually invoke, why it applies,
> what it checks and what its result means in plain language. Give me an
> evidence-backed release recommendation before any live change.

When a skill is actually invoked, your assistant should explain it in four
short parts: **why now, what it checks, what it found, and what comes next**.
For example: "I'm using `release-readiness-reviewer` to check whether this
specific version is ready. It checks test results, rollback and monitoring.
The rollback plan is missing, so my recommendation is NO-GO until it exists."
The explanation accompanies the evidence; it does not count as a passed check
or permission to release.

## How the work is divided

| Role | Responsibility | What you should see |
| --- | --- | --- |
| Coordinating assistant using [`project-orchestrator`](../../.claude/skills/project-orchestrator/SKILL.md) | Read project state and repository, name the exact commit or proposed release artifact, establish the target environment and what action triggers deployment, then select relevant specialists. | One candidate and one list of open questions, reviews and approvals. |
| Independent read-only reviewers, if your host supports them | Review separate lenses using `.claude/agents/` definitions such as `secure-saas-reviewer`, `qa-automation-lead`, and `release-readiness-reviewer`; invoke the matching skills when their methods apply. Each reviewer receives the same candidate identity and only the material needed for its lens. | Separate findings with scope and evidence; disagreements stay visible. Agent output alone cannot approve or deploy. |
| Release readiness reviewer | Apply [`release-readiness-reviewer`](../../.claude/skills/release-readiness-reviewer/SKILL.md) to the **same** candidate, aggregating continuous integration (CI) results, artifact provenance, change-relevant testing, security and migration findings, rollback, monitoring and recorded approvals. | An advisory GO (ready) or NO-GO (blocked) recommendation with cited blockers and unknowns. |
| Human owner and one authorized execution path | Decide whether to release under the applicable permission policy; use the existing CI or deployment procedure when authorized, then verify what actually shipped. | An approval tied to the release identity, one operation/receipt trail, smoke checks and closeout. |

If the assistant's host has no independent agents, use the same skills in
sequence and state that their reviews share a context; never claim independent
review from one session. Scale the number of reviewers to the release's
actual risks instead of repeating the same review to spend more tokens.

## The order

1. **Pin the release.** Record the product repository, exact candidate commit
   or artifact, target environment and deploy trigger. If this cannot be
   established, stop at preparation. [`change-classification-gate`](../../.claude/skills/change-classification-gate/SKILL.md)
   identifies validation and approval depth. If a merge automatically deploys,
   [`merge-is-deploy-governance`](../../.claude/skills/merge-is-deploy-governance/SKILL.md)
   identifies the pre-merge gate and the post-merge verification path. Explain
   that a merge may itself put a change in front of customers.
2. **Check only relevant risks.** Request independent code and security review
   when changed behavior warrants it; QA review checks that tests exercise
   those changes. Reviewers inspect the same pinned candidate and return
   evidence, findings and gaps. A database migration requires the
   [`secure-migration-reviewer`](../../.claude/skills/secure-migration-reviewer/SKILL.md)
   route; a release without a viable rollback path uses
   [`rollback-runbook-author`](../../.claude/skills/rollback-runbook-author/SKILL.md)
   to prepare one. A live agent feature may also need the artificial intelligence
   (AI) runtime design
   skills below. Describe what each invoked specialist checked, not just its
   name or verdict.
3. **Check the candidate as a whole.** Apply
   [`risk-tiered-validation-selector`](../../.claude/skills/risk-tiered-validation-selector/SKILL.md)
   and, when the full tier is needed,
   [`sharded-validation-with-resume`](../../.claude/skills/sharded-validation-with-resume/SKILL.md)
   for real test results. Give those results and the independent findings to
   `release-readiness-reviewer`. A missing blocking fact produces NO-GO; an
   unknown release identity prevents a reliable verdict. If code or artifact
   changes, recheck the affected evidence against the new identity.
4. **Decide and execute once.** Use
   [`human-approval-boundary`](../../.claude/skills/human-approval-boundary/SKILL.md)
   and the applicable [`agent-authorization-matrix`](../../.claude/skills/agent-authorization-matrix/SKILL.md)
   policy for the action and environment. The matrix skill is **manual-only**:
   the user must name it explicitly to define or revise policy; the existing
   policy can be consulted without auto-invoking it. A GO recommendation is
   advice, not permission. Only the authorized owner or execution mechanism
   carries out the named merge or deployment. If a result is uncertain,
   reconcile the actual deployment and receipt before considering any retry.
5. **Verify what shipped.** Match the deployed artifact to the approved
   candidate, run the planned smoke and health checks, report any failure and
   apply the approved rollback path if needed. Record the outcome and open
   issues in the product's release record. Post-merge checks confirm what
   shipped; on merge-to-deploy platforms they cannot prevent that deployment.

This path does not automatically invoke manual-only skills such as
[`ci-pipeline-architect`](../../.claude/skills/ci-pipeline-architect/SKILL.md)
or [`observability-operator`](../../.claude/skills/observability-operator/SKILL.md).
When the release needs their work, the assistant explains why and asks you to
name the skill explicitly. The same applies to changes to agent permissions.

## Where harness, context and loop engineering fit

These are three **distinct design skills** for a product that runs AI agents,
including a proposed AI deployment worker. They can be invoked as needed when
designing that runtime; reading or using them does not mean the controls are
installed in your app or in Aegis's delivery control plane.

| Skill | Plain-language explanation to the user | Its design output for an AI deployment worker |
| --- | --- | --- |
| [`agent-harness-architect`](../../.claude/skills/agent-harness-architect/SKILL.md) | "We are designing the doorway every AI or tool call must pass through." | A governed call path with verified identity, authorization, tool limits, budget and audit checks. It enforces an existing permission policy; it does not grant deploy rights. |
| [`model-context-designer`](../../.claude/skills/model-context-designer/SKILL.md) | "We are deciding what information each agent may see to do its job." | Limited, vetted context for each reviewer or worker, with sensitive data minimized and a record of what was supplied. A short briefing to a reviewer is useful practice; the skill specifically designs a model's runtime context assembly. |
| [`agentic-loop-designer`](../../.claude/skills/agentic-loop-designer/SKILL.md) | "We are setting how many attempts the agent may make and when it must stop." | Bounded iterations, typed failures and safe retry rules. An uncertain deployment result must stop for verification, never trigger a blind repeat. A fixed release checklist may need no agentic loop. |

When no AI worker or agent runtime is being designed, use the ordinary release
steps above. If you do build a worker, design and test the relevant harness,
context and loop separately before letting it participate in a live release.
The [AI feature path](add-ai-safely.md) owns the wider threat and evaluation
sequence. Keep release authorization and the actual deployed state tied to
the product's real controls and evidence.
