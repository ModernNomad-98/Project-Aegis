---
name: ai-router-architect
description: 'MANUAL-ONLY; never auto-invoke. Design the centralized model-routing layer all AI calls flow through: one internal interface in front of every provider/model; per-provider adapters mapping requests, responses, tool calls, streaming and errors onto it so no provider-specific type leaks past it; a capability matrix so routing and fallback never pick a model lacking a needed feature; adapter conformance tests. Credentials stay server-side; routing picks the model by task/cost/availability; per-call telemetry; budgets/rate limits from ai-cost-guardrail-designer enforced at the choke point; retries/backoff, fallback, degraded responses and a kill switch. Use when building or refactoring the AI provider/routing/gateway layer, adding or swapping a provider, or centralizing scattered model calls. Do NOT use for the cost policy (ai-cost-guardrail-designer), telemetry implementation (observability-operator), output schema (structured-output-validator), or prompt/injection design (prompt-injection-defender).'
disable-model-invocation: true
---

# AI Router Architect

**Reading key:** A software development kit (SDK) is a provider's programming
package; an application programming interface (API) is its call boundary.
Personally identifiable information (PII) can identify a person. A provider
adapter translates one provider's requests, responses, tool calls, streaming
chunks and errors to and from the router's internal interface. A capability
matrix records which features each model supports, such as tool calling,
structured output, context size and image input. The client bundle is the code shipped to users' browsers. A circuit breaker stops calls to a failing provider for a while; backoff with jitter waits a growing, slightly random time between retries; an idempotency key lets a repeated call be recognized so its effect happens only once. This
manual-only skill designs routing and live-provider wiring; it does not grant
permission to use credentials or call a provider.

## Purpose

Design the single layer every model call flows through, so the artificial intelligence (AI) system has
one place to enforce credential custody, model selection, cost controls,
telemetry, and failure handling — instead of scattered SDK calls each doing
their own thing. The deliverable: an internal routing interface in front of
all providers/models; a per-provider adapter behind it, with a capability
matrix and adapter conformance tests; server-side-only credentials; routing by
task/cost/availability; a per-call telemetry contract; enforcement of the budgets and
rate limits `ai-cost-guardrail-designer` defines; and resilient failure
handling (retry/backoff, provider fallback, cached/degraded responses, kill
switch). This skill **wires live providers and credentials**, so it is
**manual-only**. It composes `secrets-identity-hardener` *(manual-only)*,
`observability-operator` *(manual-only)* and `ai-cost-guardrail-designer`
rather than redoing their work.

## Use When

- Use when: building or refactoring the AI provider/routing/gateway layer, or
  centralizing model calls that are currently scattered across the codebase.
- Use when: adding or swapping a provider/model and needing its adapter,
  capability matrix entry, routing, fallback, and key custody.
- Use when: the system needs one choke point to enforce cost, telemetry, and
  kill-switch behavior across all AI calls.
- Do NOT use when: defining the cost/quota POLICY — `ai-cost-guardrail-designer`
  (this skill enforces it at the router).
- Do NOT use when: implementing the telemetry/alerts (`observability-operator`
  *(manual-only)*), validating output shape (`structured-output-validator`),
  designing prompt/injection defenses (`prompt-injection-defender`
  *(manual-only)*), or keeping an agent's closed tool and provider registry
  (`agent-harness-architect`).

## Inputs to Inspect

1. Current model-call sites: where the codebase calls providers today, whether
   keys are server-side, and how much logic is duplicated per call site.
2. Provider/model inventory: which providers and models, their pricing tiers,
   rate limits, and failure modes.
3. Credential handling: where API keys live now — a key in the client bundle
   or a public environment variable is a top finding (compose `secrets-identity-hardener`
   *(manual-only)*).
4. Cost/rate policy: the budgets, caps, and model-tier intent from
   `ai-cost-guardrail-designer` this layer must enforce.
5. Telemetry needs: the per-call metrics contract from
   `observability-operator` *(manual-only)* / `saas-cost-architect` (attribution).
6. Resilience requirements: acceptable degraded behavior when a provider is
   down or rate-limited; idempotency needs for retried calls.
7. Provider formats and capabilities: each provider's request, tool-call,
   streaming and error formats, and which features each model supports.

## Workflow

1. **Inventory call sites and consolidate.** Find every place the code calls a
   model; design the single internal interface they will all route through.
   Scattered direct SDK calls are the anti-pattern this fixes. No call sites/
   provider design to inspect → Stop Conditions.
2. **Lock credential custody.** All provider keys server-side only, injected
   at runtime, never in the client bundle or a public `VITE_`/`NEXT_PUBLIC_` variable.
   Verify with a client-bundle-absence check (compose
   `secrets-identity-hardener` *(manual-only)*). Per-provider key rotation path.
3. **Define the adapter contract and capability matrix.** Give each provider
   one adapter that maps its requests, responses, tool calls, streaming chunks
   and error codes onto the internal interface. No provider-specific type
   crosses the interface, so calling code never imports a provider SDK type.
   Map provider errors (rate limit, overload, content refusal) to the
   router's own error classes before any retry decision. Record the
   capability matrix per model; routing (step 4) and fallback (step 7) must
   consult it. Every adapter passes one shared conformance suite (request and
   response round trip, tool call, streaming order and end, each error class)
   before it serves traffic.
4. **Design routing** using
   [references/ai-router-design.md](references/ai-router-design.md): select
   model by task type, cost tier, latency need, and availability. Encode the
   `ai-cost-guardrail-designer` model-tier intent (cheap model for simple
   tasks). Never select a model the capability matrix shows lacks a feature
   the task needs. Routing decisions are deterministic and logged.
5. **Enforce cost and rate limits at the choke point.** The router is where
   per-request token caps, per-tenant/plan budgets, rate limits, and
   concurrency bounds are applied — one enforcement point for all calls.
   Fail safe at the limit (degrade/deny), never fail open.
6. **Emit the telemetry contract.** Every call emits model, tokens (in/out),
   estimated cost, latency, tenant/user/feature, error class, and correlation
   id — attributable, with prompt content redacted. Hand implementation to
   `observability-operator` *(manual-only)*.
7. **Design failure handling.** Bounded retries with backoff and jitter (only
   for idempotent/safe calls); provider/model fallback order, limited to
   models the capability matrix shows can do the task, so a fallback never
   silently drops a needed feature; cached or degraded responses when all
   providers fail; a circuit breaker per provider.
   Define what "degraded" returns to the caller.
8. **Design the kill switch.** Disable a provider, a model, a feature, or a
   tenant fast without a deploy — for incidents or cost spikes. Route a
   confirmed live incident to the human incident owner and approved runbook;
   activating the switch requires the applicable live authority. Use
   `incident-response-runbook` to author or improve the procedure.
9. **Handle idempotency and side effects.** Retries must not duplicate
   side-effecting calls; carry an idempotency key where a call triggers an
   external effect (compose `api-event-architect` for the pattern).

## Output Format

```
AI ROUTER DESIGN — <system>  (manual-only; wires live providers/credentials)
Call-site consolidation: <scattered sites → single interface>
Credential custody: <server-side only proof | rotation> (→ secrets-identity-hardener)
Provider adapters: <per provider: request/response, tool-call, streaming, error → internal interface; no provider type crosses it>
Capability matrix: <model × tool calling / structured output / context size / image input; consulted by routing and fallback>
Adapter conformance tests: <shared suite every adapter passes: round trip, tool call, streaming, each error class>
Routing: <task/cost/latency/availability → model tier> (deterministic, logged)
Cost/rate enforcement: <caps/budgets/rate/concurrency at the choke point> (→ ai-cost-guardrail-designer)
Telemetry contract: <per-call metrics, attribution, redaction> (→ observability-operator)
Failure handling: <retry/backoff (idempotent only) | fallback order | degraded response | circuit breaker>
Kill switch: <granularity, no-deploy, trigger, human authority and approved runbook>
Idempotency: <key/dedup for side-effecting calls> (→ api-event-architect)
Residual risk: <what remains + named acceptor>
```

## Validation Checklist

- [ ] All model calls route through one internal interface; scattered direct
      SDK calls are consolidated.
- [ ] Provider credentials are server-side only with a client-bundle-absence
      proof and a rotation path.
- [ ] Each provider has an adapter mapping requests, responses, tool calls,
      streaming and errors onto the internal interface; no provider-specific
      type crosses it.
- [ ] A capability matrix exists, and routing and fallback consult it so no
      task goes to a model lacking a feature it needs.
- [ ] Every adapter passes the shared conformance suite before serving traffic.
- [ ] Routing selects model by task/cost/availability deterministically and
      logs the decision.
- [ ] Cost/rate/concurrency limits are enforced at the router and fail safe.
- [ ] Per-call telemetry is attributable and redacts prompt content.
- [ ] Failure handling covers bounded retries (idempotent only), provider
      fallback, degraded responses, and a per-provider circuit breaker.
- [ ] A no-deploy kill switch exists at provider/model/feature/tenant
      granularity.
- [ ] Retries cannot duplicate side-effecting calls (idempotency key).

## Security Rules

- Provider credentials are server-side only — a key reachable from the client
  bundle is a critical finding, not a convenience (compose
  `secrets-identity-hardener` *(manual-only)*).
- The router is a security choke point: budget, rate, and kill-switch
  enforcement live here so no call site can bypass them.
- Failure fails safe: a provider outage or budget-check error degrades or
  denies; it never falls open into uncapped spend or an unauthenticated path.
- Telemetry must not log prompts/responses containing secrets or PII — emit
  metadata, redact content.

## Gotchas

- The client-side key leak is the classic AI-router failure: calling the
  provider straight from the browser to "avoid a backend hop" ships the key to
  every user. Always route server-side.
- Retrying non-idempotent calls doubles side effects — a retried "send email"
  or a tool call fires twice. Retry only safe calls; use idempotency keys.
- Fallback can leak quality/cost silently: falling back to a cheaper model on
  every timeout can degrade output without anyone noticing — surface fallback
  in telemetry.
- Capability-blind fallback: a fallback model without structured output or
  tool calling "succeeds" but returns something the caller cannot use. Check
  the capability matrix before falling back; return the defined degraded
  response when no model qualifies.
- One provider's rate limit becoming your outage: without a circuit breaker,
  retry storms against a limited provider make it worse. Break the circuit.
- A kill switch that needs a deploy is not a kill switch during an incident —
  make it runtime config.
- Centralizing is the point, but a god-object router that also does prompt
  construction, output parsing, and business logic becomes unmaintainable —
  keep it to routing, provider adapters, custody, telemetry and resilience; compose the rest.

## Stop Conditions

- No call sites or provider design exist to route — stop; this skill
  consolidates a concrete implementation.
- The layer wires live providers/credentials: this skill is manual-only —
  propose the design/diff; applying it is a classified, approved step
  (`human-approval-boundary`).
- A provider key is found in the client bundle or a public variable — flag as a
  blocking finding and route rotation through `secrets-identity-hardener`
  *(manual-only)*.
- The ask is really the cost policy, telemetry implementation, output schema,
  or injection design — hand to the owning skill.

## Supporting Files

- [references/ai-router-design.md](references/ai-router-design.md) — the
  routing-decision rubric, credential-custody patterns, failure-handling and
  circuit-breaker design, the per-call telemetry contract, and kill-switch
  granularity.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the AI-platform-ops
  cluster and against `ai-cost-guardrail-designer`, `observability-operator`,
  `secrets-identity-hardener`, `structured-output-validator` and
  `agent-harness-architect`.
