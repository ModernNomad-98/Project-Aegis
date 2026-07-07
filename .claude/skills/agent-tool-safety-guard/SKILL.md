---
name: agent-tool-safety-guard
description: Design or review least-privilege tool/function access for an LLM agent, containing excessive agency and tool misuse (OWASP LLM06 + ASI02) — build the per-tool permission matrix (side effects, blast radius, who it runs as), validate arguments against a schema before execution, run tools with the CALLING USER's authority (not a service account's), gate irreversible/high-impact actions behind human approval, map tool-chain abuse paths where one tool's output drives another's arguments, and class code-execution tools (interpreter/shell/eval) as maximal blast radius needing sandbox plus approval (the tool-side ASI05 slice). Composes human-approval-boundary and agent-authorization-matrix. Use when an agent can call tools/functions/APIs and you need to scope what it may do. Do NOT use for injection defense (prompt-injection-defender), the sandbox itself (llm-output-safety-reviewer), retrieval authz (rag-security-architect), or standing merge/deploy authority (agent-authorization-matrix).
---

# Agent Tool Safety Guard

## Purpose

Contain excessive agency (LLM06): design or review the tool/function surface
of an LLM agent so it can only do what the task needs, with the authority of
the user it acts for, and cannot cause irreversible harm without a human. The
deliverable is a per-tool permission matrix (side effects, blast radius,
identity), argument validation before execution, an identity/authority model
that binds tool calls to the CALLING USER, approval gates on high-impact
actions, and a map of tool-chain composition abuse. Approval mechanics come
from `human-approval-boundary`; standing agent authority from
`agent-authorization-matrix` — this skill composes both.

## Use When

- Use when: an LLM agent, assistant, or workflow can invoke tools, functions,
  plugins, or APIs and you need to scope what it may do and how far a mistake
  or injection can reach.
- Use when: reviewing an agent for excessive agency — too many tools, too
  broad scopes, actions that run as a privileged service account, missing
  approval on destructive operations.
- Use when: adding a new tool to an existing agent and its blast radius needs
  assessing.
- Use when: reviewing tool misuse/exploitation paths (ASI02) — a manipulated
  agent abusing its legitimate tools within granted scopes, side-effect
  limits per tool, or a code-execution tool (interpreter/shell/eval) whose
  blast-radius class and approval posture need setting (the tool-side slice
  of ASI05; the sandbox internals are `llm-output-safety-reviewer`'s).
- Do NOT use when: the concern is stopping injected instructions from
  reaching the tools (`prompt-injection-defender` — this skill assumes the
  boundary and designs it).
- Do NOT use when: the agent EXECUTES generated code
  (`llm-output-safety-reviewer` for the exec/sandbox surface), retrieves
  documents (`rag-security-architect`), or the question is agent-vs-human
  merge/deploy authority (`agent-authorization-matrix`).

## Inputs to Inspect

1. The tool/function inventory: every tool the agent can call, its
   description as the model sees it, its parameters, and what it actually does.
2. Side effects per tool: read vs write, reversible vs irreversible, internal
   vs external, money-spending, data-exposing.
3. The identity the tool runs as: the calling user's permissions, the agent's
   own identity, or a shared service account (the last is usually the bug).
4. Argument handling: is input validated/typed before execution, or is the
   model's free-text passed through?
5. Existing approval gates and their triggers; `human-approval-boundary` and
   `agent-authorization-matrix` output where present.
6. The autonomy context: is the agent autonomous, human-in-the-loop, or
   advisory; how tool outputs feed back into the next model call.
7. Code-execution tools if any (interpreter, shell, eval, code-runner):
   their sandbox posture, what executed code can reach, and which
   natural-language paths can trigger execution (ASI05 tool slice — the
   sandbox rubric itself lives with `llm-output-safety-reviewer`).

## Workflow

1. **Inventory tools and side effects.** For each tool, record: purpose, real
   side effect, reversibility, blast radius (one record / one tenant / all
   tenants / external), and cost. Class any code-execution tool (interpreter,
   shell, eval) as maximal blast radius from the start (ASI05). No tool
   surface to inspect → Stop Conditions.
2. **Apply least privilege.** Challenge every tool: does the task require it?
   Can a read-only or narrower-scope version do? Remove or narrow tools that
   exceed the task. Fewer tools and tighter scopes shrink the surface an
   injection or hallucination can reach.
3. **Bind tool calls to the calling user's authority.** Every tool executes
   with the CALLING USER's permissions and tenant scope, enforced by code —
   not the agent's identity and not a broad service account. An agent must not
   be able to do for a user what the user cannot do themselves.
4. **Validate arguments before execution.** Each tool's arguments are checked
   against a schema and value constraints (allowlists, ranges, tenant-scoped
   ids) BEFORE the side effect runs — the model's output is untrusted input
   to the tool (compose `structured-output-validator`).
5. **Gate high-impact actions.** Irreversible, destructive, costly, or
   cross-boundary actions require human approval via `human-approval-boundary`;
   define the trigger per tool. Standing "agent may never do X autonomously"
   rules come from `agent-authorization-matrix`. Code-execution tools default
   to sandbox-required plus approval (per-tool side-effect limits set here;
   the sandbox itself per `llm-output-safety-reviewer`, ASI05).
6. **Map tool-chain composition abuse** using
   [references/tool-permission-matrix.md](references/tool-permission-matrix.md):
   where one tool's (untrusted) output becomes another tool's arguments, a
   safe-looking chain can compose into harm (read → summarize → send). Model
   the chains, not just single calls — including natural-language-driven
   execution paths where untrusted content steers WHICH tool runs with WHICH
   arguments (ASI02 misuse runs through legitimate grants).
7. **Design containment and telemetry.** Rate/quantity limits per tool,
   a kill switch to disable a tool or the agent, and logging of every tool
   call with arguments and outcome (compose `observability-operator`).
   Confirmed abuse routes to `incident-response-runbook`.
8. **Design the red-team cases.** For each high-risk tool: an injection or
   hallucination that tries to trigger it out of scope, with the expected
   SAFE outcome (denied at authz/approval). Hand to `ai-evaluation-harness`.

## Output Format

```
AGENT TOOL SAFETY — <agent/feature>
Tool matrix:
  <tool> | side effect: <r/w, reversible?> | blast radius: <scope> | runs as: <identity> | cost: <>
Least-privilege changes: <tools removed/narrowed + why>
Identity model: <calling-user authority enforcement per tool>
Argument validation: <schema/constraints per tool> (→ structured-output-validator)
Approval gates: <tool → trigger → approver> (→ human-approval-boundary)
Tool-chain abuse: <chain → composed harm → break point>
Containment: <rate/qty limits | kill switch | telemetry> (→ observability-operator)
Red-team cases: <out-of-scope trigger attempt → SAFE outcome> (→ ai-evaluation-harness)
Residual risk: <what remains + named acceptor>
```

## Validation Checklist

- [ ] Every tool has a recorded side effect, reversibility, blast radius, and
      the identity it runs as.
- [ ] Least privilege applied: unnecessary or over-broad tools removed or
      narrowed with rationale.
- [ ] Every tool executes with the calling user's authority/tenant scope,
      enforced by code — no broad service-account execution left unjustified.
- [ ] Arguments are schema/constraint-validated before the side effect runs.
- [ ] Irreversible/costly/cross-boundary actions are approval-gated with a
      defined trigger.
- [ ] Tool-chain composition abuse paths are mapped, not just single calls.
- [ ] Code-execution tools (if any) are classed maximal-blast-radius:
      sandbox-required (per `llm-output-safety-reviewer`), approval-gated,
      with misuse and NL-driven execution paths mapped (ASI02/ASI05).
- [ ] Kill switch, per-tool limits, and per-call telemetry are specified;
      abuse routes to `incident-response-runbook`.

## Tool Permission Rules

- Least privilege by default: a tool the task doesn't need is removed, not
  left "just in case".
- Tools run as the user, not the agent: an agent must never let a user do
  through it what they can't do directly (confused-deputy prevention).
- Model output driving a tool is untrusted input: validate arguments before
  execution; never pass free-text straight to a side effect.
- Irreversible actions are approval-gated — the model does not get to decide
  to delete, pay, deploy, or externally send on its own.
- The tool description the model sees is part of the attack surface: a tool
  named/described to invite misuse is a finding.

## Gotchas

- The service-account trap: wiring every tool to one privileged backend
  identity means a single injection can act as admin for all tenants. Bind to
  the caller.
- Over-tooling: giving the agent 30 tools "for flexibility" hands an attacker
  30 primitives. Scope to the task.
- Reversibility is a spectrum: "send email" and "delete account" are both
  writes but only one is catastrophic — gate by impact, not just by verb.
- Chains hide harm: read-file + post-webhook are each innocuous; together
  they exfiltrate. Enumerate compositions.
- Approval fatigue undermines gates: if everything prompts, users click
  through (see the agentic `human-agent-trust-reviewer`). Gate the genuinely
  high-impact actions, not everything.
- "The model decided" is not authorization — authorization is a code
  decision about the user, checked before the effect.
- A code-execution tool makes the rest of the matrix moot if unsandboxed:
  "run this Python" with network and ambient credentials is RCE with extra
  steps — class interpreter/shell/eval tools as their own maximal-blast-
  radius row (ASI05), sandbox-required and approval-gated, never wired to a
  service account. ASI02 misuse needs no new tools at all: the abuse runs
  THROUGH legitimate grants, which is why side-effect limits and chain
  mapping matter even when every single tool looks properly scoped.

## Stop Conditions

- No tool/function inventory or agent design is available — stop; this skill
  scopes concrete tools, not a hypothetical agent.
- A tool runs as a broad service account with no way to bind it to the caller
  and it performs cross-tenant writes — flag as a blocking finding and route
  the fix through `human-approval-boundary`.
- The gap is really injection reaching the tools, code execution, or standing
  merge/deploy authority — hand to the owning skill.
- A review finds a tool already being abused in production — route to
  `incident-response-runbook`.

## Supporting Files

- [references/tool-permission-matrix.md](references/tool-permission-matrix.md)
  — the per-tool matrix template, blast-radius rubric, calling-user identity
  patterns, argument-validation checklist, the tool-chain composition
  abuse catalog, and the ASI02/ASI05 extension (tool misuse paths,
  code-execution tool class, NL-driven execution).
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the output & agency
  cluster and against `agent-authorization-matrix` and `human-approval-boundary`.
