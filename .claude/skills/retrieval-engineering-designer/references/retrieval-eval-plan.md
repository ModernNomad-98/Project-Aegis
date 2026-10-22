# Method record: retrieval engineering designer

Reference for the retrieval-engineering-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Design semantic/hybrid retrieval quality: characterize corpus and query intents, choose a chunking and embedding plan, design dense/lexical fusion and reranking, build the relevance evaluation plan (golden sets, recall/precision, regression gate), analyze failure modes (staleness, ambiguity, poisoning surface) and hand authorization/leakage to the security owner; refuses live tuning or eval execution.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- rag security architect requests route to `rag-security-architect`; this skill does not perform that owner work.
- search architecture designer requests route to `search-architecture-designer`; this skill does not perform that owner work.
- ai evaluation harness requests route to `ai-evaluation-harness`; this skill does not perform that owner work.
- model context designer requests route to `model-context-designer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `ai-cost-guardrail-designer`, `ai-evaluation-harness`, `ai-misinformation-guard`, `ai-router-architect`, `ai-threat-modeler`, `caching-strategy-designer`, `data-quality-monitor-designer`, `hidden-context-exposure-reviewer`, `model-context-designer`, `multi-tenant-data-architect`, `prompt-injection-defender`, `rag-security-architect`, `search-architecture-designer`, `sensitive-disclosure-guard` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
