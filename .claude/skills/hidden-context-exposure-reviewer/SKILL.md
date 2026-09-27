---
name: hidden-context-exposure-reviewer
description: 'Review an LLM feature for hidden context exposure (OWASP LLM08:2026, formerly LLM07 System Prompt Leakage) across every non-user-facing input the model sees: system prompt, developer instructions, retrieved policy text, tool/function schemas, and other assembled rules. Two axes: CONTENTS (no credentials, keys, internal endpoints, or role, refusal, or workflow logic whose disclosure aids an attacker) and DEPENDENCE (no authorization, filtering, limit, or tool permission may rely on hidden context staying secret; enforcement is deterministic and outside the model). Assumes all hidden context is extractable; routes found secrets to secrets-identity-hardener. Use when facing a system prompt leak, tool schema exposure, retrieved policy leak, developer-instruction exposure, or security that depends on prompt secrecy. Do NOT use for injection defense (prompt-injection-defender), sensitive user data in context or output (sensitive-disclosure-guard), or tool permission design (agent-tool-safety-guard).'
---

# Hidden Context Exposure Reviewer

**Reading key:** LLM08 is the Open Worldwide Application Security Project
(OWASP) 2026 Hidden Context Exposure risk identifier (2025's LLM07 System
Prompt Leakage, broadened to all hidden, non-user-facing context). *Hidden
context* is anything the application puts in the model's context window that
end users are not meant to see: the system prompt, developer instructions,
retrieved policy text, tool and function schemas, and other rules or
directives. LLM means large language model, RAG is retrieval-augmented
generation, MCP is the Model Context Protocol, RBAC is role-based access
control, API is application programming interface, JSON is JavaScript Object
Notation, and UX is user experience.

## Purpose

Review an LLM feature for the two failure modes behind LLM08, applied to EVERY
kind of hidden context, not just the system prompt. First, CONTENTS: hidden
context must carry no credentials, keys, connection strings, internal
endpoints or architecture, and no role, refusal, or workflow logic whose
disclosure materially helps an attacker — because hidden context is
discoverable (extracted, inferred, or reconstructed) and must be assumed
public. Second, and more important, DEPENDENCE: no security property may rest
on hidden context staying hidden. The doctrine this skill enforces: **hidden
context is not a security control** — authorization, privilege separation,
content filtering, rate limits, and tool permissions are deterministic and
live OUTSIDE the LLM. The goal is that disclosure of hidden context has little
or no security impact, not that it cannot be disclosed.

## Use When

- Use when: reviewing a system prompt or developer instructions for leaked
  secrets, internal detail, or security rules ("system prompt leak").
- Use when: tool or function schemas, MCP tool descriptions, or parameter
  definitions exposed to the model may reveal credentials, internal systems,
  admin-only capabilities, or role requirements ("tool schema exposure").
- Use when: policy documents, configuration text, or profile-derived rules are
  retrieved into context as instructions and could be echoed back or
  reconstructed ("retrieved policy leak").
- Use when: a feature's security appears to depend on any hidden context
  staying confidential, or someone asks "can a user get our prompt / tool list
  / rules?" — and, more importantly, whether it MATTERS if they can.
- Do NOT use when: defending against untrusted content changing behavior
  (`prompt-injection-defender`, manual-only) — the input side; injection is
  often how hidden context is extracted, but that skill owns the defense.
- Do NOT use when: the sensitive data is regulated USER or training data in
  input, context, output, or logs (`sensitive-disclosure-guard`, LLM02
  Sensitive Information Disclosure).
- Do NOT use when: the question is which tools an agent may call, argument
  validation, or approval gates (`agent-tool-safety-guard`); this skill only
  asks what a tool schema reveals and whether its text is relied on as a gate.
- Do NOT use when: the question is which users may retrieve which documents
  (`rag-security-architect`, LLM09 Vector and Embedding Weaknesses); this
  skill reviews retrieved policy text once it is placed in hidden context.
- Do NOT use when: the exposure is an agentic amplification — persistent
  memory (`memory-context-poisoning-reviewer`), inter-agent channels
  (`inter-agent-comms-reviewer`), tool configuration persistence, or
  multi-step agent compromise (`agent-tool-safety-guard`,
  `agent-containment-reviewer`; the OWASP Top 10 for Agentic Applications
  owns these).
- Do NOT use when: the concern is generic application security inherited by
  the LLM system — client-bundle secrets (`secrets-identity-hardener`,
  manual-only; invoke explicitly), or server-side log leakage and
  infrastructure-layer side channels (`threat-modeler`; prompt and context
  log redaction is `sensitive-disclosure-guard`).

## Inputs to Inspect

1. The context-assembly code or configuration: every source that is placed
   into the model's context for a request, in order, with which parts the
   user can see.
2. System prompt and developer instructions, including framework- or
   gateway-injected instructions, role/persona messages, and few-shot
   examples.
3. Retrieved policy text: policy or rules documents pulled from a knowledge
   base, configuration store, feature settings, or user-profile service and
   inserted as instructions.
4. Tool and function schemas: names, descriptions, parameter schemas,
   defaults, enums, examples, and MCP server tool descriptions — and whether
   the tool list is the same for every caller.
5. Other hidden directives: output-format and JSON schemas, refusal and
   guardrail rules, routing and escalation criteria, workflow thresholds.
6. The enforcement layer: where authorization, filtering, limits, and tool
   permissions are actually implemented in code outside the model.
7. Extraction exposure: whether users can get the model to reveal, summarize,
   translate, or reconstruct hidden context (direct ask, roleplay,
   continuation, probing tool behavior).
8. `prompt-injection-defender` and `agent-tool-safety-guard` output where
   present — injection enables extraction, and exposed tool schemas widen
   excessive agency.

## Workflow

1. **Inventory the hidden context.** List every hidden source from Inputs 2–5
   and tag each as system prompt, developer instruction, retrieved policy
   text, tool/function schema, or other directive. No context assembly or
   hidden content available to review → Stop Conditions. Treat every item as
   PUBLIC from here on.
2. **Axis 1 — scan contents per type** using
   [references/hidden-context-checks.md](references/hidden-context-checks.md):
   - *System prompt / developer instructions:* credentials, tokens,
     connection strings, internal hostnames/URLs, architecture detail,
     business thresholds, unreleased features, real customer data in
     examples.
   - *Retrieved policy text:* internal rules (fraud thresholds, pricing
     floors, escalation criteria) inserted verbatim; whether a minimized or
     summarized form would do; whether the policy source mixes internal-only
     and user-safe text.
   - *Tool/function schemas:* secrets or tokens in descriptions, defaults,
     enums, or examples; internal hostnames or table names; admin-only or
     destructive tools registered for every caller; descriptions that state a
     role requirement ("developer role only") as the gate.
   - *Other directives:* refusal/guardrail conditions and exceptions, output
     schemas downstream parsers trust, routing criteria.
   Record location, type, and a redacted fingerprint for each finding — never
   copy secret bytes into the report. Route credential removal and rotation to
   `secrets-identity-hardener`; regulated user data found in hidden context
   routes to `sensitive-disclosure-guard`.
3. **Axis 2 — find hidden-context-as-control dependence (the important
   one).** For every security-relevant rule in ANY hidden source — a prompt
   line, a policy paragraph, a tool description, a refusal rule — ask: if the
   user saw and ignored this text entirely, is there a deterministic control
   OUTSIDE the model that still stops them? If NO, that is the finding.
4. **Classify each security rule and name its real enforcement point.**
   Authorization or role gating → RBAC/policy check
   (`authorization-matrix-designer`); tool availability or restriction →
   per-caller tool registration and tool authorization
   (`agent-tool-safety-guard`); content or refusal policy → external
   safeguard or output filter; limits → rate limiting in code
   (`ai-cost-guardrail-designer`); output format → independent validation
   (`structured-output-validator`). The hidden text may stay as UX guidance;
   it is never the control.
5. **Rate severity** on the LLM08 scale: *informational* (no secrets, no
   security-relevant logic, no reliance on confidentiality); *medium*
   (internal rules, filtering criteria, role descriptions, or workflow logic
   that meaningfully aids an attacker but does not gate critical decisions;
   Aegis reads the official LLM08 entry's example Scenario #2 — an
   extracted tool list with parameter schemas, no credential disclosed and
   no control bypassed — as medium); *high* (embedded credentials or tokens, or
   reliance on hidden-context secrecy for authorization or content
   policy); *critical*
   (disclosure chains to remote code execution, broad data exfiltration, or
   privilege escalation in a connected system).
6. **Assess extraction, then de-emphasize it.** Note how easily each source
   leaks (it will, including by inference from tool behavior), but frame the
   fix as removing what MATTERS if it leaks — never as making hidden context
   un-extractable. Hardening against extraction is defense-in-depth at best.
7. **Design canary and leak tests.** A unique non-secret canary per hidden
   source (prompt, policy chunk, tool description) asserted absent from
   output; extraction attempts per source; and, for each former
   hidden-context-as-control rule, a test that the deterministic control
   blocks the action when the rule is contradicted. Hand to
   `ai-evaluation-harness`.
8. **Report both axes per source with routing.** Secrets → removal and
   rotation; dependence → move the control out to the named owner; state
   residual risk with a named acceptor.

## Output Format

```
HIDDEN CONTEXT EXPOSURE REVIEW — <feature>
Assumption: all hidden context is treated as PUBLIC.
Hidden context inventory:
  <source> | type: system prompt | developer instruction | retrieved policy | tool schema | other | user-visible? no
Axis 1 — Contents (secrets / attacker-useful detail):
  [SEV] <source + location / type / redacted fingerprint; no secret bytes> → removal + rotation (→ secrets-identity-hardener) | minimize | remove
Axis 2 — Hidden-context-as-control (dependence):
  <rule + source> | deterministic control outside model? <yes / NO=finding>
    → move enforcement to <authorization-matrix-designer | agent-tool-safety-guard | output filter | rate limit | structured-output-validator>
Severity (LLM08 scale): <informational | medium | high | critical per finding>
Extraction exposure: <per source, framed as "does it matter?">
Canary/leak tests: <per-source canaries; extraction attempts; control-holds tests> (→ ai-evaluation-harness)
Routed out of scope: <user data → sensitive-disclosure-guard; memory/inter-agent → owning skill>
Residual risk: <what remains + named acceptor>
```

## Validation Checklist

- [ ] Every hidden source was inventoried and typed — system prompt,
      developer instructions, retrieved policy text, tool/function schemas,
      and other directives — not the system prompt alone.
- [ ] Each source was reviewed as if public (assume extractable).
- [ ] Axis 1: no credentials, keys, connection strings, internal endpoints, or
      attacker-useful logic remain in any hidden source; found secrets routed
      to `secrets-identity-hardener` for rotation.
- [ ] Tool schemas were checked for embedded secrets and for tools registered
      to callers who may not use them.
- [ ] Axis 2: every security-relevant rule in any hidden source has a
      deterministic enforcement point OUTSIDE the model, or is a finding.
- [ ] Each finding carries an LLM08 severity and routes enforcement to the
      owning skill.
- [ ] Extraction risk is noted, but remediation is "remove what matters if
      leaked", not "make it un-extractable".
- [ ] Canary/leak tests cover each hidden source; the real assertion is that
      disclosure causes no harm.

## AI Security Rules

- Hidden context is NOT a security control. Authorization, privilege
  separation, filtering, limits, and tool permissions are deterministic and
  live outside the LLM. Every finding traces back to this doctrine.
- Assume all hidden context is public: the system prompt, developer
  instructions, retrieved policy text, and tool schemas are extractable or
  inferable. Design so that disclosing them costs nothing.
- Secrets never belong in hidden context: a key in a prompt or tool
  description is a leaked key — rotate it and keep it server-side, called by
  code, never handed to the model.
- Hardening against extraction is defense-in-depth, never the primary
  control; do not report a feature safe because hidden context is hard to
  extract.

## Gotchas

- The seductive anti-pattern: "we put the API key in the prompt (or the tool
  description) so the model can call our API." That key is one extraction
  away from public; tool calls must be authenticated by server code.
- Tool schemas are hidden context too. An attacker who extracts the tool list
  and parameter schemas gains concrete targets for injection even when no
  credential leaks — register only the tools the current caller may use.
- "Requires the developer role" in a tool or MCP description is a disclosed
  rule, not a gate; the tool call must be authorized in code.
- Retrieved policy text is easy to forget: it arrives from a document store,
  not a prompt file, so prompt reviews miss it. Internal fraud thresholds or
  escalation criteria injected verbatim hand attackers the playbook.
- Leaked refusal and guardrail rules show attackers exactly which patterns to
  avoid; content policy must be enforced by an external safeguard.
- Leaked output-format rules let attackers craft well-formed but malicious
  output; downstream parsers must validate independently.
- Chasing un-extractability wastes effort; the win is making extraction
  irrelevant, not impossible.
- Don't conflate with USER data disclosure: regulated user or training data
  is `sensitive-disclosure-guard`; this skill is the application's own hidden
  control context.

## Stop Conditions

- No hidden context or context-assembly code is available to review — stop;
  this skill reviews concrete hidden sources and their enforcement
  surroundings, not a hypothetical.
- A live secret (valid key/credential) is found in any hidden source — treat
  as active exposure: route rotation through `secrets-identity-hardener` and,
  if it may already be leaked, `incident-response-runbook`.
- The real issue is injection defense, regulated user-data disclosure,
  retrieval authorization, tool-permission design, or agent memory — hand to
  the owning skill.
- Fixing a dependence finding requires building the real enforcement (RBAC,
  per-caller tool registration, filter, rate limit) — propose it;
  implementation is a classified, approved step routed to the owning skill.

## Supporting Files

- [references/hidden-context-checks.md](references/hidden-context-checks.md) —
  the per-type contents scan (system prompt, developer instructions,
  retrieved policy text, tool/function schemas, other directives), the
  hidden-context-as-control catalog with the "what enforces it outside the
  model?" test, the LLM08 severity scale, extraction techniques (for
  awareness, not as the fix), canary-test seeds, and the scope boundaries.
- `evals/evals.json` — trigger + behavior cases, including tool-schema
  exposure, retrieved-policy leakage, and developer-instruction exposure.
- `evals/trigger-evals.json` — discrimination against
  `prompt-injection-defender`, `sensitive-disclosure-guard`,
  `rag-security-architect`, `agent-tool-safety-guard`,
  `secrets-identity-hardener`, `memory-context-poisoning-reviewer`,
  `model-context-designer`, and `inter-agent-comms-reviewer`.
