# Agent tool permission matrix & abuse catalog

Detail for `agent-tool-safety-guard`. OWASP LLM06 (Excessive Agency), 2025;
extended for the OWASP Agentic Top 10 (2026): ASI02 (Tool Misuse and
Exploitation) and the tool-side slice of ASI05 (Unexpected Code Execution).

## Per-tool matrix template

| Field | What to record |
|---|---|
| Tool | name as the model sees it |
| Purpose | why the task needs it |
| Side effect | read / write; reversible / irreversible |
| Blast radius | one record / one tenant / all tenants / external world |
| Runs as | calling user / agent identity / service account |
| Cost | money, rate limits, quota consumed |
| Args | parameters + validation applied before execution |
| Approval | none / triggered gate / always human |

## Blast-radius rubric

- **Contained** — affects only the calling user's own data, reversible.
- **Tenant** — affects the tenant's shared data; needs tenant-scope enforcement.
- **Cross-tenant / global** — can touch other tenants or platform state; must
  run as the caller and be gated. A tool with global blast radius on a service
  account is a top finding.
- **External** — sends email, calls third-party APIs, moves money, publishes.
  Irreversible in practice; approval-gate.

## Least-privilege challenges

For each tool ask:
- Does the task actually require it, or is it "for flexibility"?
- Is there a read-only or narrower-scope variant that suffices?
- Can its parameters be constrained (allowlist of actions, tenant-scoped ids,
  value ranges) so the dangerous shape is unreachable?
- If removed, what breaks — and is that acceptable?

## Calling-user identity patterns

- **Bind to caller (preferred):** the tool executes an operation the CALLING
  USER is authorized for, checked by code against their permissions and tenant.
- **Delegated/scoped credential:** short-lived, least-privilege credential
  minted for this user+task, not a standing admin token.
- **Service account (danger):** one privileged identity for all tool calls —
  a single injection acts as that identity for everyone. Justify explicitly or
  remove; if unavoidable, compensate with strict argument allowlists + approval.

Confused-deputy test: can the agent, acting for user U, perform an action U
cannot perform directly? If yes, the identity model is broken.

## Argument validation checklist

- Arguments parsed and validated against a schema before ANY side effect
  (compose `structured-output-validator`).
- Ids are tenant-scoped and ownership-checked, not trusted from model text.
- Enumerated actions come from an allowlist; free-text that becomes a command,
  path, URL, or query is validated/escaped.
- Quantities/amounts bounded (max rows, max spend, max recipients).

## Tool-chain composition abuse catalog

One tool's untrusted output becoming another's input is the dangerous seam:

- **Exfiltration chain:** read_data → send_email/post_webhook. Each safe;
  together they leak. Gate the egress tool; treat read output as untrusted.
- **Escalation chain:** search_users → update_role. Model-chosen target from
  step 1 drives a privileged write in step 2. Validate the target against the
  caller's authority at step 2.
- **Amplification chain:** generate_list → for-each side effect (email/delete).
  Bound the fan-out; approval-gate bulk effects.
- **Injection-carried chain:** injected instruction in retrieved content →
  tool call. The action boundary (this skill) is what stops it even when
  `prompt-injection-defender`'s separation is bypassed.

Model chains as first-class: draw the graph of which tool outputs can reach
which tool inputs, and place validation/approval at the harmful edges.

## Containment & telemetry

- Per-tool rate and quantity limits; per-agent global budget.
- Kill switch: disable one tool, one agent, or the feature (compose
  `ai-cost-guardrail-designer` / `ai-router-architect` for the switch plumbing).
- Log every tool call: tool, validated arguments, caller identity, outcome,
  cost (compose `observability-operator`); redact sensitive arguments.
- Confirmed abuse → `incident-response-runbook`.

## Tool misuse & code-execution tools (ASI02 / ASI05 extension)

**ASI02 — misuse of legitimate grants.** The attack needs no new tools: a
manipulated agent abuses exactly what the matrix already allows. Beyond
single-call authz, review:

- **Side-effect limits per tool:** volume, rate, spend, and recipient bounds
  so a legitimately-granted tool can't be driven to harmful scale (mass
  emails, bulk deletes within scope).
- **NL-driven execution paths:** where natural-language content (user input,
  retrieved docs, peer-agent messages) determines WHICH tool runs and WITH
  WHAT arguments — map content→tool-choice edges the way chains are mapped;
  the deterministic argument/authority checks are what hold when content
  steers the choice.
- **Parameter pollution:** valid tool, valid schema, hostile values (a
  correct `send_report` call pointed at an attacker address). Value
  constraints and ownership checks, not just shape.
- **Cross-tool state abuse:** a tool that mutates state another tool trusts
  (write-config → deploy) is a chain even when calls are minutes apart.

**ASI05 (tool slice) — code-execution tools.** Interpreter, shell, `eval`,
code-runner, and "computer use" tools are their own matrix class:

- **Blast radius = maximal by default:** executed code can attempt anything
  the runtime allows; the matrix row records the SANDBOX limits as the
  effective blast radius (sandbox rubric: `llm-output-safety-reviewer`).
- **Approval posture:** execution tools default to approval-gated; autonomous
  generate-and-run loops need the compensating controls in
  `llm-output-safety-reviewer`'s ASI05 section before the gate is relaxed.
- **Identity:** never a service account; executed code inherits NO ambient
  credentials — anything it needs is injected per-task, least-privilege
  (`agent-identity-privilege-reviewer` for the identity model).
- **Arguments are code:** the "argument" IS a program — schema validation
  can't clear it; the sandbox is the control, plus source/intent limits
  (what the code is allowed to be about) where feasible.

## Red-team seeds (→ ai-evaluation-harness)

- Injected instruction attempts to trigger the highest-blast-radius tool →
  expect denied at authz/approval.
- Hallucinated tool call with out-of-scope arguments (another tenant's id) →
  expect argument validation rejects it.
- Chain attempt (read then exfiltrate) → expect egress gate blocks/approves.
- Bulk fan-out request → expect quantity bound / approval.
- Content-steered tool choice (retrieved doc nudges the agent from
  `read_file` to `send_email` with attacker recipient) → expect value
  constraints + egress gate hold (ASI02).
- Code-execution tool asked to run network/credential-touching code →
  expect sandbox denies egress/secrets and the call is approval-gated (ASI05).
