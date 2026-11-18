# Add artificial intelligence (AI) features safely

*This path names who acts and in what order — each skill owns its own how.*

**Source-only links.** Links to skills or pages outside the starter package are source-repository links; in a consumer copy they do not resolve — copy the skill first (starter sections 4.1–4.2).

**Who this is for:** you want to add an artificial intelligence (AI) feature — a chatbot, an assistant, an agent,
anything that calls a model — without opening a security hole. The threats here are
different from classic app security (a model can be talked into things a database cannot),
so the order matters: map the threats first, design the guardrails second, prove they hold
last.

**How to run it:** open your project in your agent tool (Claude Code, Codex
command-line interface (CLI), or any Agent
Skills tool) and take the steps top to bottom. For most steps, plain words are enough — the
named skill selects itself. (Auto-selection quality varies by tool — see the source-only Aegis README's tools
section.) Four steps are marked
**manual-only — name it explicitly**: you start them by typing the skill's name.
Start with: **"In this product repository, I want to add a chatbot that answers
customer questions. Use the ai-threat-modeler skill to map its data, tools,
trust boundaries and abuse cases before designing it."** For the later
manual-only steps, say **"Use the prompt-injection-defender skill on that threat
map"** and **"Use the ai-evaluation-harness skill to propose cases, limits and
a budget before any paid run"**, and, for a multi-step agent whose goal or plan could be
redirected, **"Use the agent-goal-hijack-defender skill on that agent loop."** And when provider routing is in scope (a new or refactored provider/gateway layer, adding or swapping a provider, or centralizing model calls that are currently scattered), say **"Use the ai-router-architect skill to design the provider routing on that call path."**

Steps marked *"if…"* are conditional — skip them honestly when they don't match your
feature's shape.

## The order

1. **Map the threats first —
   [`ai-threat-modeler`](../../.claude/skills/ai-threat-modeler/SKILL.md).**
   Yields the feature's threat map, with each mitigation naming the skill that owns it.
   Handoff: this map decides which of the steps below your feature actually needs — it is
   the reason this path starts here.

2. **Design the operating environment** — use the parts that match your feature:

   - **[`agent-harness-architect`](../../.claude/skills/agent-harness-architect/SKILL.md)** —
     for model or tool calls that need one governed path; yields the mediation,
     identity and policy checks those calls must pass.
   - **[`model-context-designer`](../../.claude/skills/model-context-designer/SKILL.md)** —
     when prompts assemble user data, retrieved material or tool output; yields
     the contract for what the model is allowed to see.
   - **[`agentic-loop-designer`](../../.claude/skills/agentic-loop-designer/SKILL.md)** —
     *only if the feature loops or acts on its own* — yields the loop's bounds and its
     honest ways to stop.

   Handoff: these designs are what the later steps defend and test.

3. **Contract the outputs and the spend:**

   - **[`structured-output-validator`](../../.claude/skills/structured-output-validator/SKILL.md)** —
     yields the validation contract for model output your code parses and acts on.
   - **[`llm-output-safety-reviewer`](../../.claude/skills/llm-output-safety-reviewer/SKILL.md)** —
     yields the handling rules for model output that gets rendered, executed, or passed
     downstream.
   - **[`ai-cost-guardrail-designer`](../../.claude/skills/ai-cost-guardrail-designer/SKILL.md)** —
     designs token caps, budgets, and a fail-closed stop control. Implement and
     test those limits before relying on them to bound spending.

4. **Defend the data going in:**

   - **[`sensitive-disclosure-guard`](../../.claude/skills/sensitive-disclosure-guard/SKILL.md)** —
     yields the controls on personally identifiable information (PII) and
     secrets flowing toward the model.
   - *If the feature retrieves your documents or data to answer (retrieval-augmented
     generation, RAG):*
     **[`rag-security-architect`](../../.claude/skills/rag-security-architect/SKILL.md)** —
     designs retrieval-time authorization checks and reports unreviewed paths.
     Implement and verify those checks before treating retrieved content as
     access-controlled.

5. **Defend against injection —
   [`prompt-injection-defender`](../../.claude/skills/prompt-injection-defender/SKILL.md)**
   *(manual-only — name it explicitly if the step-1 threat map identifies
   injection risk).* Yields layered defenses for the mapped injection paths.
   Handoff: its red-team cases feed step 6.

*If your feature is an agent, or an assistant that persists memory, connects to MCP servers, or runs a multi-step planner whose goal or plan could be redirected:* review it against the agentic risks.

These rows are conditional — run only the rows that match the feature; none is required for every AI feature. If a copy of Aegis does not include a reviewer, copy it with the **selected-skills allow-list** route in the source-only *Using the skills in your own project* section; the starter package installs none of these reviewers. For a starter consumer, record the extension as a DECISION in `docs/project-state.md` before first use (the starter §4.2 rule).

| Use when the feature… | Reviewer (linked to its SKILL.md) | What it yields (from its own description) | Its own stop conditions — stop and hand off when (quoted) |
|---|---|---|---|
| has its own identities, credentials or delegated authority | [`agent-identity-privilege-reviewer`](../../.claude/skills/agent-identity-privilege-reviewer/SKILL.md) | least-privilege identity and delegation findings (OWASP Agentic ASI03) | "No identity/credential information is available for the agent system — stop; this skill reviews concrete identity architecture, not intentions." |
| keeps memory or stored context across sessions | [`memory-context-poisoning-reviewer`](../../.claude/skills/memory-context-poisoning-reviewer/SKILL.md) | whether untrusted content can write into long-term memory (ASI06) | "No persistent memory exists (stateless agent, context window only) — state that ASI06 is mostly not applicable and route any in-context concern to prompt-injection-defender." |
| has agents talking to other agents or to MCP servers | [`inter-agent-comms-reviewer`](../../.claude/skills/inter-agent-comms-reviewer/SKILL.md) | authentication, integrity and replay findings (ASI07) | "No topology, transport, or protocol details are available — stop; this skill reviews a concrete message layer, not the idea of one." |
| runs several agents that could cascade or drift | [`agent-containment-reviewer`](../../.claude/skills/agent-containment-reviewer/SKILL.md) | blast-radius and rogue-agent findings (ASI08, ASI10) | "No topology, autonomy, or lifecycle information is available — stop; this skill reviews a concrete agent system, not the concept of containment." |
| asks humans to approve agent actions | [`human-agent-trust-reviewer`](../../.claude/skills/human-agent-trust-reviewer/SKILL.md) | consent-fatigue and deceptive-approval findings (ASI09) | "No approval flow, UX, or telemetry is available and none can be described — stop; this skill attacks a concrete oversight layer, not the idea of one." |
| runs a multi-step planner/agent whose goal or plan an attacker could redirect (single prompt→response features stay with prompt-injection-defender) | [`agent-goal-hijack-defender`](../../.claude/skills/agent-goal-hijack-defender/SKILL.md) *(manual-only — name it explicitly)* | defenses for goal and plan hijack (ASI01) | "No agent loop/planner implementation or design is available — stop; this skill hardens a concrete multi-step agent, not a description." (manual-only: the proposed diff applies only under a human invocation and an approved step) |

*If your feature is a model-backed feature, review it against these model and retrieval risks. This block applies in addition to the agentic table above — including to an agent that invokes tools, whose tool-safety row applies here too:*

| Use when the feature… | Reviewer (linked to its SKILL.md) | What it yields (from its own description) | Its own stop conditions — stop and hand off when (quoted) |
|---|---|---|---|
| building or refactoring the AI provider/routing/gateway layer, adding or swapping a provider, or centralizing model calls that are currently scattered across the codebase | [`ai-router-architect`](../../.claude/skills/ai-router-architect/SKILL.md) *(manual-only — name it explicitly)* | the centralized model-routing layer all AI calls flow through, with provider adapters and a capability matrix | "No call sites or provider design exist to route — stop; this skill consolidates a concrete implementation." |
| an LLM agent, assistant, or workflow can invoke tools, functions, plugins, or APIs and you need to scope what it may do and how far a mistake or injection can reach | [`agent-tool-safety-guard`](../../.claude/skills/agent-tool-safety-guard/SKILL.md) | a per-tool permission matrix and least-privilege tool/function boundaries (OWASP LLM03/ASI02/ASI05) | "No tool/function inventory or agent design is available — stop; this skill scopes concrete tools, not a hypothetical agent." |
| an AI feature drafts, suggests or changes records that a person must check before they become real (support replies, refunds, record updates, extracted fields, classifications) | [`ai-human-in-the-loop-designer`](../../.claude/skills/ai-human-in-the-loop-designer/SKILL.md) | a review workflow for AI-originated writes using the action dispositions AUTONOMOUS/CONFIRM/FORBIDDEN, with the risk tier supplied first by `ai-governance-risk-reviewer` (step 7) | "The person or identity that triggered an AI run is set up to approve its own proposal → refuse that design; require a different reviewer." |
| an AI feature makes factual claims, gives advice, or produces output that users or systems act on, and wrong-but-confident output would cause harm | [`ai-misinformation-guard`](../../.claude/skills/ai-misinformation-guard/SKILL.md) | grounding, checked citations, calibrated uncertainty/refusal and pre-action validation (OWASP LLM07) | "No feature or output behavior is available to review — stop; this skill needs concrete claims/consequences to assess." |
| reviewing a system prompt, developer instructions, tool/function schema, retrieved policy text, or hidden authorization rules for leaked secrets, internal detail, or security-rule disclosure (hidden-context exposure) | [`hidden-context-exposure-reviewer`](../../.claude/skills/hidden-context-exposure-reviewer/SKILL.md) | hidden-context exposure findings across system prompts, developer instructions and assembled rules (OWASP LLM08) | "No hidden context or context-assembly code is available to review — stop; this skill reviews concrete hidden sources and their enforcement surroundings, not a hypothetical." |
| you train or fine-tune a model, collect user feedback that shapes behavior (RLHF, thumbs up/down, correction data), or ingest external content into a knowledge base or embedding index | [`model-poisoning-reviewer`](../../.claude/skills/model-poisoning-reviewer/SKILL.md) | data/pipeline poisoning findings across training, feedback and RAG ingestion paths (OWASP LLM05) | "The concern is retrieval authorization, third-party artifact acquisition, inference-time injection, or agent memory — hand to the owning skill." |
| designing or tuning semantic or hybrid retrieval quality — chunking, embeddings, fusion and reranking | [`retrieval-engineering-designer`](../../.claude/skills/retrieval-engineering-designer/SKILL.md) | chunking, embedding, fusion and reranking design with relevance evaluation; authorization/leakage is out of scope for this skill | "The caller wants this skill to implement, run or approve the change: refuse; return the artifact for the authorized owner." |

6. **Make it hold over time —
   [`ai-evaluation-harness`](../../.claude/skills/ai-evaluation-harness/SKILL.md)**
   *(manual-only — name it explicitly).* Yields the red-team cases from steps 1 and 5, the agentic
   block above, and the applicable model-risk cases from the new block above
   encoded as repeatable regression checks. Run those checks after relevant
   changes and report untested paths; covered cases alone do not prove every
   defense holds.

7. ***Optional close* — [`ai-governance-risk-reviewer`](../../.claude/skills/ai-governance-risk-reviewer/SKILL.md).**
   Yields the feature's risk tier, its user-facing disclosure posture, and the human
   oversight it requires — worth running when the feature touches real users' decisions,
   money, or data.

## What this is — and isn't

This is a guided order, not a guarantee. Each skill's own output is the evidence — the
threat map, the contracts, and any completed evaluation runs. Those results
support only the tested scope and known limits; they cannot guarantee that an
AI feature is universally safe. Re-run the relevant tests when the feature,
model, data or tools change, and report gaps rather than treating them as passes.
