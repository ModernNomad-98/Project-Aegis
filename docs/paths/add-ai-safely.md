# Add artificial intelligence (AI) features safely

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** you want to add an AI feature — a chatbot, an assistant, an agent,
anything that calls a model — without opening a security hole. The threats here are
different from classic app security (a model can be talked into things a database cannot),
so the order matters: map the threats first, design the guardrails second, prove they hold
last.

**How to run it:** open your project in your agent tool (Claude Code, Codex
command-line interface (CLI), or any Agent
Skills tool) and take the steps top to bottom. For most steps, plain words are enough — the
named skill selects itself. (Auto-selection quality varies by tool — see the README's [tools
section](../../README.md#using-aegis-with-codex-cli-and-other-agent-skills-tools).) Two steps are marked
**manual-only — name it explicitly**: you start them by typing the skill's name.
Start with: **"In this product repository, I want to add a chatbot that answers
customer questions. Use the ai-threat-modeler skill to map its data, tools,
trust boundaries and abuse cases before designing it."** For the later
manual-only steps, say **"Use the prompt-injection-defender skill on that threat
map"** and **"Use the ai-evaluation-harness skill to propose cases, limits and
a budget before any paid run."**

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

6. **Make it hold over time —
   [`ai-evaluation-harness`](../../.claude/skills/ai-evaluation-harness/SKILL.md)**
   *(manual-only — name it explicitly).* Yields the red-team cases from steps 1 and 5
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
