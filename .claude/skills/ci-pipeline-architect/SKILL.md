---
name: ci-pipeline-architect
description: MANUAL-ONLY; never auto-invoke. Design the delivery pipeline and, on request, edit the pipeline definitions — the stage graph (lint, typecheck, build-once, unit, integration, security, E2E, artifact, deploy gates) with explicit merge-blocking semantics and a latency budget, CI secret governance (OIDC over stored credentials, job-scoped secrets, none to fork PRs), artifact provenance and cache trust, environment promotion with named-human gates, deployment strategies with rollback primitives, and branch-protection alignment. Composes qa-automation-architect (test tiers), vite-build-qa-engineer, and supply-chain-security-reviewer (pinning) rather than restating them. EDITS PIPELINE FILES — behavior-steering, secret-adjacent config. Use when asked to design or overhaul CI/CD, add stages/gates, fix CI secret handling, or wire deploy approvals. Do NOT use for test-suite internals (qa-automation-architect), dependency audits (supply-chain-security-reviewer), or release go/no-go (release-readiness-reviewer).
disable-model-invocation: true
---

# CI Pipeline Architect

Terms used below: **CI/CD** means continuous integration and continuous
delivery (or deployment); **E2E** means end-to-end testing; **OIDC** means
OpenID Connect; **PR** means pull request; **SAST** means static application
security testing; and **YAML** is the human-readable configuration format
used by many pipeline definitions. These expansions do not change this
skill's manual-only invocation or its approval requirements for pipeline edits.

## Purpose

Produce a delivery pipeline that is fast enough to be obeyed and strict
enough to be worth obeying: a stage graph with explicit merge-blocking
semantics, secret governance that survives a malicious PR, artifact and
cache rules, environment promotion with human gates where they belong, and
— when asked — the concrete pipeline definition files implementing it. The
discipline is gate-placement-by-evidence: every stage exists because it
catches a class of defect at the cheapest point, every merge-blocking check
earns its latency, and nothing that guards the default branch is silently
weakened.

## Use When

- Use when: asked to design or overhaul a CI/CD pipeline, or to stand one
  up for a repo that has none.
- Use when: adding, reordering, or gating pipeline stages (security scans,
  E2E, artifact publication, deploy approvals).
- Use when: fixing CI secret handling — stored cloud keys → OIDC, secret
  exposure to fork PRs, which jobs see which secrets.
- Use when: wiring deployment strategies (rolling/blue-green/canary/flag
  gated) and environment promotion into the pipeline.
- Do NOT use when: designing test-suite structure, runners, or retry/flake
  policy — `qa-automation-architect` owns the test tiers this pipeline
  hosts.
- Do NOT use when: auditing dependencies, action provenance, or CI
  compromise paths — `supply-chain-security-reviewer` (this skill applies
  its rules; the audit is its casework).
- Do NOT use when: deciding whether a specific release ships —
  `release-readiness-reviewer` consumes the gates this skill builds.
- Do NOT use when: reviewing Terraform/Bicep the pipeline deploys —
  `iac-reviewer`.
- Do NOT use when: designing one feature's flag targeting, percentage ramp
  or kill-switch lifecycle — `feature-flag-rollout-strategist`. This skill
  only decides whether the pipeline needs a flag-gated deployment route.

## Inputs to Inspect

1. Existing pipeline definitions (workflow YAML, pipeline files), branch
   protection rules, and environment/approval configuration.
2. The repo's build/test commands and their real runtimes (CI history) —
   stage design against measured minutes, not guesses.
3. The test-automation blueprint (`qa-automation-architect` output): tiers,
   what runs on PR vs merge vs nightly, retry policy.
4. Secret inventory: what secrets CI currently holds, which jobs/steps use
   them, and which cloud roles the pipeline can assume.
5. Deploy targets and environments: staging/production topology, who may
   approve promotion, existing deployment strategy.
6. Supply-chain posture: how actions/plugins are pinned today
   (`supply-chain-security-reviewer` findings if any).
7. Monorepo/polyrepo shape and change-detection needs (path filters,
   affected-graph tooling).

## Workflow

1. **Map the current state honestly**: stages that exist, what actually
   blocks merge (branch protection vs advisory), measured stage runtimes,
   flake-driven re-runs, secret usage per job. A pipeline design that
   ignores current runtimes produces gates people bypass.
2. **Design the stage graph**: fast static feedback first (lint, typecheck,
   format), build once and reuse the artifact, test tiers per the
   `qa-automation-architect` blueprint (unit/integration on PR; E2E per its
   tier policy), security stages (SAST, dependency/secret scanning — triage
   discipline per `static-analysis-reviewer` / `supply-chain-security-reviewer`),
   build-output QA (`vite-build-qa-engineer` for Vite estates), artifact
   packaging with provenance metadata. For each stage: trigger, blocking
   semantics (merge-blocking / post-merge / nightly), timeout, and the
   defect class it exists to catch.
3. **Govern secrets**: no long-lived cloud credentials in CI where OIDC
   federation exists — pipelines assume scoped cloud roles; secrets scoped
   to the narrowest job, never exported to PR-triggered runs from forks;
   secret-bearing jobs isolated from steps that execute untrusted code
   (install scripts, PR code); missing-secret behavior explicit (skip with
   a visible report, never silently pass).
4. **Set caching and artifact governance**: caches keyed on lockfiles
   (poisoning-aware: caches restored into secret-bearing jobs are an attack
   surface), build artifacts retained with a stated retention period,
   logs/reports/coverage/screenshots collected per the QA evidence
   conventions, artifact provenance recorded (commit, run id) so
   `release-readiness-reviewer` can demand it later.
5. **Wire environments and promotion**: environment-scoped secrets,
   promotion order (staging → production), required approvers on
   production-facing environments (named humans per
   `agent-authorization-matrix` posture — merge/deploy authority is never
   the pipeline's own decision), and the deployment strategy per target:
   rolling, blue/green, canary, or flag-gated. Compare them in plain
   terms for each target: rolling gradually replaces instances but may
   expose all users before a problem is detected; blue/green holds two
   environments and switches traffic back; canary limits initial exposure
   and aborts its ramp on measured signals; a flag can disable a released
   behavior without undoing the deployed artifact. Name the exposure
   path, detection signal, rollback primitive and time to act for each
   viable option. Compare infrastructure money (including duplicate
   capacity), setup effort and ongoing monitoring/operating upkeep.
   Recommend the strategy that fits the target's risk, traffic, state
   compatibility and budget; flags do not reverse schema or data changes.
   A flag can complement the other deployment strategies; detailed flag
   targeting and ramp rules belong to `feature-flag-rollout-strategist`.
   Mark unknown
   costs as unknown and verify current prices if exact spend matters.
   Ask one discovery question before recommending when a decisive fact is
   missing; if the user must choose, ask one atomic decision question.
   Hand the chosen primitive to `rollback-runbook-author` for a rehearsed
   procedure. No strategy choice grants deployment authority.
6. **Align branch protection**: required checks list matches the
   merge-blocking stages exactly (a required check that no longer runs stays
   expected or pending and blocks merge until protection is updated),
   stale-review dismissal, and no bypass actors beyond
   the governed list.
7. **Write or edit pipeline files only when explicitly requested** (the
   side-effecting step): a design-only request ends with the reviewable
   design and no pipeline edit. For an authorized edit, use a scoped diff
   per `reviewable-diff-discipline`, pinned action/step versions per
   `supply-chain-security-reviewer` rules, and no removed or weakened
   check without a named approval. Never commit secrets or their values
   into definitions.
8. **Validate and hand off**: definitions lint/parse (actionlint or
   equivalent where available), a dry-run or PR run proves the graph
   executes, measured latency per stage is reported against the budget,
   and the go/no-go evidence contract is handed to
   `release-readiness-reviewer`.

## Output Format

```
CI PIPELINE DESIGN (CONTINUOUS INTEGRATION/DELIVERY) — <repo/scope>
Current state: <stages, what ACTUALLY blocks merge, runtimes, secret usage>
Stage graph: <stage — trigger — blocking semantics — timeout — defect class
  it catches — measured/estimated runtime>
Secret governance: <OpenID Connect (OIDC) roles vs stored secrets;
  job→secret map; forked pull-request (PR) secret-access posture;
  missing-secret behavior>
Caching & artifacts: <cache keys + poisoning posture; artifact retention +
  provenance fields; evidence collection>
Environments & promotion: <environment → secrets scope → approvers →
  recommended strategy and context → initial exposure/detection → rollback
  primitive; viable alternatives, infrastructure money (estimate or explicit
  unknown), setup effort and monitoring/operating upkeep>
Owner decision: <when needed, one atomic strategy question after recommendation;
  if decisive context is missing, one discovery question first>
Branch protection: <required checks (must equal merge-blocking stages),
  bypass list, review rules>
Files changed: <pipeline definition diffs — or "design only, no files
  touched">
Latency budget: <PR feedback target vs measured; what was moved off the
  merge path to meet it>
Handoffs: <qa-automation-architect tiers consumed; supply-chain rules
  applied; release-readiness evidence contract; rollback primitives →
  rollback-runbook-author>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every merge-blocking stage names the defect class it catches and its
      runtime; total PR latency is stated against a budget.
- [ ] Build happens once; downstream stages consume the artifact, not
      rebuilds.
- [ ] No long-lived cloud credential remains where OIDC federation was
      available; every secret is scoped to named jobs; fork-PR runs get no
      secrets.
- [ ] Missing-secret and skipped-stage behavior is visible, never a silent
      pass.
- [ ] Required checks in branch protection exactly match the
      merge-blocking stage list.
- [ ] Each target compares viable rolling, blue/green, canary and
      flag-gated options in plain terms; the recommendation names exposure,
      detection signal, rollback primitive and state limitations.
- [ ] Strategy choice records infrastructure money as an estimate or
      explicit unknown, plus setup effort and ongoing monitoring/operating
      upkeep; unknown prices are not invented.
- [ ] If owner choice is needed, the output asks one atomic decision
      question after the explanation, or one discovery question first when
      decisive context is missing; no deploy authority is inferred.
- [ ] Actions/steps are version-pinned; no check was weakened or removed
      without a named approval.
- [ ] Test-tier internals, supply-chain audit, and release go/no-go were
      composed from their skills, not restated.
- [ ] If files were edited: diff is scoped, parsed/linted, and proven by a
      real run.

## Gotchas

- The most common pipeline failure is social, not technical: a 40-minute
  merge gate trains the team to stack PRs and admin-merge. Latency is a
  security control.
- PR-triggered workflows from forks with secret access are a standing
  exfiltration hole; `pull_request_target`-style triggers plus checkout of
  PR code is the classic misconfiguration.
- Caches restored into privileged jobs can carry poisoned artifacts from
  unprivileged runs — separate cache namespaces by trust level.
- A required check whose job was renamed can leave the old required name
  expected or pending, blocking merge. Synchronize branch protection with
  the new job name as an explicit reviewed change; do not bypass the gate.
- "Temporarily" continue-on-error on a failing security stage is how scan
  gates die; expiry-dated skips only, visibly reported.
- Deploy jobs that run on every merge to main make rollback a new deploy
  race; promotion gates and concurrency groups exist for this.

## Stop Conditions

- Invoked without explicit human request → do not run; this skill edits
  behavior-steering pipeline files that execute with secret access
  (`disable-model-invocation: true` is load-bearing).
- Asked to weaken, remove, or bypass a merge-blocking check (especially
  security stages) → `human-approval-boundary` with the check, the reason,
  and the expiry; never weaken silently as part of a broader edit.
- A pipeline change would grant CI new cloud permissions or new secret
  access → propose the scoped role/secret and stop for approval.
- The change touches production deploy/approval gates → named-human
  approval per `agent-authorization-matrix` posture before the edit ships.
- Existing pipeline behavior cannot be observed (no CI history/permissions)
  → design from the repo with assumptions labeled; do not present an
  unvalidated graph as measured.

## Supporting Files

- `references/pipeline-stages.md` — canonical stage catalog with blocking
  semantics, secret-governance patterns (OIDC, fork posture), and
  deployment-strategy → rollback-primitive table.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the delivery cluster
  (`release-readiness-reviewer`, `rollback-runbook-author`) and against
  shipped `qa-automation-architect` / `supply-chain-security-reviewer` /
  `vite-build-qa-engineer`.
