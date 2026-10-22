---
name: retrieval-engineering-designer
description: 'Use when semantic or hybrid retrieval quality must be designed or tuned: chunking policy, embedding choice, dense/lexical fusion, reranking and relevance evaluation, with authorization and leakage handed to rag-security-architect. Do NOT use for RAG authorization/leakage design (rag-security-architect) or to run evals (ai-evaluation-harness); this skill designs retrieval quality and hands security to its owner.'
---

# Retrieval Engineering Designer

Terms: **family 8** - AI security & LLM systems (README roster family 8; docs/skills-catalog.md Phase 7 AI security and LLM systems pack); **advisory/design-only** means this skill produces guidance and records and never edits code, runs commands or grants production authority.

## Purpose

Design semantic/hybrid retrieval quality: characterize corpus and query intents, choose a chunking and embedding plan, design dense/lexical fusion and reranking, build the relevance evaluation plan (golden sets, recall/precision, regression gate), analyze failure modes (staleness, ambiguity, poisoning surface) and hand authorization/leakage to the security owner; refuses live tuning or eval execution.

The skill is **auto-invocable and advisory/design-only**. It produces the named artifact below with evidence and open questions; it does not edit code, run commands, use the network or grant production authority. Implementation and approval are delegated host/user actions. It composes the named neighbouring owners instead of duplicating them.

## Use When

- The request is to design semantic/hybrid retrieval quality: characterize corpus and query intents, choose a chunking and embedding plan, design dense/lexical fusion and reranking, build the relevance evaluation plan (golden sets, recall/precision, regression gate), analyze failure modes (staleness, ambiguity, poisoning surface) and hand authorization/leakage to the security owner; refuses live tuning or eval execution..
- The named artifact is missing, disputed or about to be built against a wrong assumption.
- A review/spec must record the artifact, its edge cases and the boundary owners explicitly.
- An implementation is about to start and the ask is for the artifact it must build against.

**Do not use when:** the request belongs to a named neighbouring owner (the complete routing list is in Stop Conditions) or when no evidence exists and the answer would be invention.

## Inputs to Inspect

- Corpus shape: document types, size, update cadence, languages, metadata and ACL/tenant fields supplied.
- Query intents and observed query logs/samples; relevance expectations and known misses.
- Current retrieval stack: chunking, embedding model/cost, index, fusion/reranking and limits.
- Quality goals and evaluation constraints (golden data availability, latency/cost budget) plus authorization owner handoff.

## Workflow

1. Characterize corpus and query intents, including long-tail and ambiguous queries.
2. Choose chunking policy (size/overlap/metadata) and embedding/index approach with trade-offs.
3. Design dense/lexical fusion and reranking; state when each helps and its cost/latency.
4. Build the relevance evaluation plan: golden set construction, recall/precision metrics, regression gate and cadence.
5. Analyze failure modes (staleness, poisoning surface, ambiguity) and hand authorization/leakage to rag-security-architect; refuse live tuning.

## Output Format

Return, in this order:

1. Retrieval design: corpus/query characterization, chunking, embedding, index, fusion and reranking decisions.
2. Relevance evaluation plan with golden set, metrics, thresholds and regression gate.
3. Failure-mode table and security handoff list.
4. Tuning/rollout plan and risks.

## Validation Checklist

- [ ] Corpus/query characterization precedes component choices.
- [ ] Chunking/embedding/fusion/reranking decisions have stated trade-offs.
- [ ] Evaluation plan names golden-set source, metrics, thresholds and regression gate.
- [ ] Security/authorization is handed to rag-security-architect, not designed here.
- [ ] No live tuning or eval execution is claimed.

## Gotchas

- Choosing embeddings/rerankers before characterizing queries and corpus.
- Evaluating relevance without a golden set or with leaked labels.
- Ignoring lexical search for exact-match queries that dense retrieval misses.
- Treating authorization as a post-filter detail instead of a security-owner handoff.

## Stop Conditions

Route a request to its real owner when it is that owner's deliverable (the complete expected-owner routing list exercised by trigger-evals):

- rag-security-architect work -> `rag-security-architect`.
- search-architecture-designer work -> `search-architecture-designer`.
- ai-evaluation-harness work -> `ai-evaluation-harness`.
- model-context-designer work -> `model-context-designer`.
- ai-misinformation-guard work -> `ai-misinformation-guard`.
- sensitive-disclosure-guard work -> `sensitive-disclosure-guard`.
- hidden-context-exposure-reviewer work -> `hidden-context-exposure-reviewer`.
- prompt-injection-defender work -> `prompt-injection-defender`.
- ai-threat-modeler work -> `ai-threat-modeler`.
- data-quality-monitor-designer work -> `data-quality-monitor-designer`.
- caching-strategy-designer work -> `caching-strategy-designer`.
- multi-tenant-data-architect work -> `multi-tenant-data-architect`.
- ai-cost-guardrail-designer work -> `ai-cost-guardrail-designer`.
- ai-router-architect work -> `ai-router-architect`.
- The caller wants this skill to implement, run or approve the change: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts.

## Supporting Files

- [retrieval-eval-plan](references/retrieval-eval-plan.md) - the named artifact, tables and completion checklist for this skill.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners.

**Source:** docs/skills-catalog.md - Phase 7 AI security and LLM systems pack (Batch 5/D113); coverage: non-roadmap GOV-02 seam (no row); beyond-roadmap counting. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
