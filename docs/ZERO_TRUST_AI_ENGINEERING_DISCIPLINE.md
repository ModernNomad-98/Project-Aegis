# Zero Trust AI Engineering Discipline

This guide is for developers and artificial intelligence (AI) agents using
Project Aegis skills. It describes a working rule: check a claim against the
current repository, approval record, test result or live system before acting
on it. For example, before saying a pull request (PR) is ready, inspect its exact
revision, its current checks and its approval boundary. A test result from an
older revision does not prove the new one works.

The name borrows the security principle "never trust, always verify" and
applies it to engineering claims throughout development.

## What to do in a normal change

1. **Track:** record the decision, scope and current state where another
   contributor can find them.
2. **Verify:** run or inspect the check on the exact version being changed;
   record failures and skips as they occurred.
3. **Govern:** confirm the action fits a current human grant and the delivery
   gate before executing or merging.
4. **Hand off:** leave enough file, command and evidence detail for the next
   contributor to continue without guessing.

The [approval register](approvals/APPROVAL_REGISTER.md), [offline verification
guide](offline-ci.md) and [documentation index](README.md) are the starting
points for applying these steps in this source repository.

## Core definition

**Zero Trust AI Engineering Discipline** (also called **Zet-AI Engineering**, pronounced
"zet-eye") applies that verification rule to decisions, code, tests, completion
claims and documentation across the software development lifecycle.

Recheck earlier evidence when the underlying revision, environment, approval
or source of truth may have changed. A summary points to evidence; it does
not replace that evidence.

## Relationship to security Zero Trust

Security Zero Trust verifies an access request instead of trusting a user's
network location. This engineering discipline applies the same habit to a
development claim: check whether the claim is true on the current revision
and whether the action has authority. Security access controls still apply.

## The two failure modes it prevents

- **Drift:** a description stops matching reality. For example, a guide says
  a command is supported after the code removes it.
- **Rot:** a control stops being used. For example, a skipped test is later
  reported as passing, or an expired approval is treated as current.

For both, inspect the current source and record the result. A previous green
run or accurate guide may have become stale after a change.

## Why it matters most for AI-assisted development

An AI assistant can present an outdated summary or an unverified completion
claim with confidence. Human memory can also be stale. Require a repository
revision, test output, approval record or other relevant source for a claim
that controls the next action. Record uncertainty when the source is missing.

## The concrete rules

The six pillars group the rules below. **Track, Verify, Govern and Hand off**
govern project work. **Constrain and Curate** govern the AI agent's execution
environment, including its allowed tools, loop bounds, inputs and outputs.

The codes below point to historical records, not to a required reading order:

| Code | Meaning in this guide |
| --- | --- |
| `P2`, `P13` and similar `P` numbers | Numbered workflow patterns in the [extraction report](research/aegis-workflow-extraction-report.md). These are pattern IDs here, not roadmap priority levels. |
| `P-existing` | A skill that already existed when the numbered patterns were extracted. |
| `D12.8`, `D12.4`, `D25`, `D42` | Numbered decision and delivery entries in the [reconciliation record](reconciliation/step-0-reconciliation-v4.md). `D12.8` is the operational workflow-pattern pack; `D12.4` is the documentation pack; `D25` and `D42` record later skill deliveries. |

The ten numbered operational patterns were collected in decision pack `D12.8`
from a [read-only workflow audit](research/aegis-workflow-extraction-report.md).
Each skill name below can be found in the [skills catalog](skills-catalog.md);
the sentence beside it explains the action it supports.

### TRACK — keep the record and the reality in sync

- **`scoped-approval-register` (P2)** — record every approval durably, with its status,
  reason, scope allowed, scope forbidden, and evidence, so an approval is never re-argued
  from memory.
- **`chat-backlog-reconciliation` (P13)** — extract chat-only decisions and backlog into
  dated repo docs on a cadence, then audit each item against PR/source evidence.
- **`context-co-update-ci-gate` (P8)** — fail any PR that touches important paths without
  updating the context map, so the map cannot silently drift from the territory.

### VERIFY — prove it green before trusting it

- **`local-ci-mirror-preflight` (P4)** — derive local equivalents of every
  PR-triggered continuous integration (CI) check and verify on clean mainline
  first, classifying each failure by cause.
- **`risk-tiered-validation-selector` (P5)** — classify each change to a validation depth,
  failing closed to full validation when unsure, so cost lands where risk is.
- **`sharded-validation-with-resume` (P6)** — run validation in named shards with persisted
  status and resume-after-timeout, plus a catch-shard, under one aggregate required check.

*A verifier that cannot fail is theater with an exit code — every check must be proven able
to fail before it counts.*

### GOVERN — hold the merge/deploy gate with human authority

- **`standing-approval-and-auto-advance` (P3)** — the reusable pattern for thinning low-risk
  approval fatigue, within named scope and with an explicit opt-out; it never covers a
  protected-branch merge or arming auto-merge, which stay human-only.
- **`merge-is-deploy-governance` (P7)** — when the platform auto-deploys on merge, treat PR
  validation as the authoritative gate, record branch-protection config in-repo, and keep a
  revert-PR rollback path.
- **`gated-deployment-prompt-template` (P11)** — a reusable operator prompt for risky
  operations with stop conditions, backup-then-verify gating, and evidence-based
  estimated completion times (ETAs).

Those are the generic skill boundaries. In this source repository, the owner's
[approval register](approvals/APPROVAL_REGISTER.md) records an explicit recurring
administrator-merge grant. Human authority can be exercised through that
standing delegation without repeated consent. Later task-specific instructions
and check requirements still apply; the grant does not turn a failed check
green. It does not transfer to consumer repositories or authorize auto-merge
arming.

### HAND OFF — transfer knowledge with evidence, before work begins

- **`lane-authoring-guide` (P10)** — a pre-work, evidence-cited authoring guide per parallel
  lane, transferring planner-to-implementer knowledge *before* the work starts.

The doctrine's answer to documentation **rot** specifically is **`docs-retention-index`
(P1)**, banked under D12.4 and shipped in D25: a numbered index that governs every workflow doc's lifecycle —
retention category, reason-to-keep, superseded-by, and cleanup rule — so retiring a document
becomes an approvable operation rather than something that never happens.

The next two pillars govern the agent's operating environment: the tools and
limits it runs under, the information it receives, and the output it returns.

### CONSTRAIN — build the operating environment so the AI cannot exceed its authority

Enforce permissions in the system that accepts the action. Instructions to
the agent alone do not create an access control.

- **`agent-harness-architect` (shipped — D42)** — every model call passes ONE server-side
  choke point that verifies identity from credentials (never from payload) and walks a
  deny-by-default ladder (permission, entitlement, budget, input policy) before the model
  runs; the tool/provider registry is closed so an unknown capability fails closed;
  instructions are server-side versioned artifacts no untrusted party can supply; and the
  audit write is fail-closed — an action that cannot be recorded does not happen.
- **`agentic-loop-designer` (shipped — D42)** — every loop has clamped iterations, typed
  retryability, and honest terminal states: a policy rejection is never retried; a failed
  check is retried once on identical input to classify flake vs deterministic; an empty
  result is a legitimate stop, never forced into output.
- **`agent-authorization-matrix` (P-existing)** — the standing human-vs-agent authority
  matrix names who may do each action; the execution environment must enforce
  those decisions.

### CURATE — control what enters and leaves the context; an unverified input is an unverified output

Choose and bound the information sent to a model. Keep a record of what was
included and what was excluded when that affects the result.

- **`model-context-designer` (shipped — D42)** — what enters the window is assembled
  server-side under hard caps and closed input schemas; secrets, personal data, and raw
  payloads are minimized or ride a transient never-persisted channel; what the model saw is
  reconstructible afterward; and exclusions are designed and documented, not accidental.
- **`structured-output-validator` (P-existing, extended in D42)** — nothing downstream
  trusts model output until it passes parse → strict schema → policy scan; failures are
  logged as safety evidence and rejected, never silently repaired; where possible the
  contract is encoded in types so a non-compliant output is unrepresentable.
- **`ai-evaluation-harness` (P-existing)** — the curated input diet and the output contract
  are pinned by evaluation cases, so a prompt/model/retrieval change that degrades them fails a gate,
  not a user.

An agent control plane can implement these rules with an agent registry,
separate identities, activity records and limits on tools or data. The
security skills govern identity and containment; the Constrain and Curate
skills govern execution and context. This page describes the discipline;
deploying a particular control plane requires its own design and proof.

## Proof from this project's own history

Project history includes cases where a verification step was missed:

- an **ungoverned auto-merge** that fired without human sign-off;
- **sessions acting on stale memory**, colliding on shared state;
- a **build run in the wrong directory**, against an unverified repo.

The ungoverned merge is represented by an evaluation case in
`agent-authorization-matrix`. The stale-memory and wrong-directory cases are
represented in startup and context-governance skill evaluations. These cases
make the rule testable: check current authority, state and workspace before
acting.
