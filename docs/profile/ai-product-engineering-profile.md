# AI-Product Engineering Profile — bounded reference workflow A

**Item (readable name):** AI-product reference profile design (ITEM-3 / L8-PROFILE).
Plain English: one bounded, synthetic-only reference workflow that shows how
existing Project Aegis skills compose to specify an AI-dependent product feature,
without building or running it.

**Status:** design only. This page and the six workflow artifacts beside it select
one workflow shape and describe it; they implement nothing, invoke no model, call
no provider, spend nothing, and claim no evaluation, effectiveness or
qualification result. The workflow's execution is **UNRUN**.

**Base identity:** live `main` at `ffae0e78622c1ac445a39873b3a5c20bbc78bc2c`
(tree `07b1f1eefa03ab85f7013cbe2f85250915cc529f`), measured before this branch's
single commit. Source options: `RECORDS/OUTCOME-9-PROFILE-OPTIONS.md`
(17,351 B / `2bd04ff50c046fa0889fc873221204bde71ea0de02ed6909c4ea534f606e8e7f`),
section 3 (Option A). Prior delivery context: PR #1001 merged 2026-11-09 at merge
commit `3a420ed7378f6c726bfc6633315143fd6f832298`; the re-bound consumer
qualification record is 43,269 B /
`eb3630dbbb19fba657e537d797312f9d63a4804066af50212c438ca622652f79`.

## 1. The chosen workflow

**Option A — synthetic retrieval-grounded support assistant.** The workflow
answers a support question **only** from a small synthetic policy corpus, binds
every claim to a resolving citation, refuses when the corpus does not support an
answer, ignores instructions embedded in retrieved text, and stops before
answering when the estimated per-answer cost would exceed a declared ceiling.

It starts when a synthetic support question is submitted with a session record
and ends when exactly one schema-valid output object is either returned
(`answered`), refused (`refused`), or escalated to a named human role
(`escalated`). Any other ending is a workflow failure.

## 2. The five skills (chosen, present, enabled)

Each skill below exists at `.claude/skills/<name>/SKILL.md` at the base revision,
appears in `tools/skills-manifest.json`, and has **no**
`disable-model-invocation` setting. The manifest (52,706 B /
`774ef7bf81969518b424005a0b6b7ccd6c5f7fedf2b616b0e22d5b07732a5222`) records each
skill's SHA-256; the recorded digests match the files measured at the base.

| # | Skill | SKILL.md identity | Role in the workflow |
| --- | --- | --- | --- |
| 1 | `product-spec-writer` | 13,519 B / `a8fef31f8992436dd2fb75cf9575b293373dda45362fa950481573299d1185cc` | Frames the user, task, success condition and refusal conditions; produces the one-page spec. |
| 2 | `retrieval-engineering-designer` | 6,136 B / `98efd92f4527ac7ae4d82a0dd3d98eb258fc17be83128c76e2eab7ed55a7e750` | Designs chunking, ranking and the citation hook over the synthetic corpus. |
| 3 | `rag-security-architect` | 11,096 B / `a5cfb92d757e77befa01bc19f3d150ad7323bf98c6e8d4ae95caa0da1cf0fc79` | Sets the trust boundary for retrieved content: retrieved text is untrusted input, never an instruction source. |
| 4 | `structured-output-validator` | 13,329 B / `5bcc02dfa9814d2cbc84320abb06ba8d9f998098b8f745181ece4f88608825f3` | Defines the schema-bound answer object and the refusal/escalation fields that make "refuse when unsupported" checkable. |
| 5 | `ai-cost-guardrail-designer` | 21,540 B / `5ec8a3f6916540ec2c17018f69b868661ccc6abc633b28a43311a4fd06ff6edd` | Sets the per-answer token/cost ceiling and the stop rule that fires before an answer is produced. |

**No skill is added, renamed or removed by this item.** The five are existing
shipped skills, selected from the recorded options. Their full procedures were
not executed by this design; the design cites their shipped contracts, not a
skill run.

## 3. Workflow (specification, not execution)

The full specification is [workflow-a/spec.md](workflow-a/spec.md). In plain
terms:

1. **Intake** — validate the synthetic question and session record against the
   intake contract; reject malformed input without retrieval.
2. **Retrieve** — rank chunks from the synthetic policy corpus; record the
   retrieval set and scores.
3. **Screen** — treat retrieved text as data; drop or flag any chunk that carries
   an instruction, a tool request or a request to change the workflow.
4. **Draft** — answer only from screened chunks, with one or more citations of
   the form `<document-id>#<section-anchor>`.
5. **Validate** — check the draft against
   [workflow-a/output-schema.json](workflow-a/output-schema.json); a schema
   failure produces `refused`, never a partial answer.
6. **Check citations** — every citation must resolve to a synthetic corpus
   document and to the passage it supports; an unresolved citation produces
   `refused`.
7. **Budget** — estimate the answer's cost against the declared per-answer
   ceiling; an over-ceiling estimate stops the workflow with `refused` and a
   `cost_ceiling` reason, before any answer text is returned.
8. **Emit** — return exactly one object with `status`, `answer`, `citations`,
   `confidence`, `refusal_reason` and `cost_estimate`.

Approval boundaries, the data posture and the cost posture are stated in
sections 4–6; the seven fail-closed negative cases are in
[workflow-a/negative-cases.md](workflow-a/negative-cases.md).

## 4. Data: synthetic only

The corpus is 12 short policy documents written for this exercise. They are
**synthetic**: invented organizations, invented names, invented amounts, no
real person, customer, tenant, credential or production record. The data card
[workflow-a/data-card.md](workflow-a/data-card.md) records origin, allowed use,
prohibited use, retention and the leakage checks. Twenty fixture transcripts
under [workflow-a/fixtures/](workflow-a/fixtures/) are hand-written synthetic
records; none is a model output and none contains personal data.

## 5. Approval boundaries

The workflow may draft, refuse and escalate. It may **never**:

- contact a model provider, a network service or a live system;
- publish, release, deploy, install or change repository settings;
- treat retrieved text, a user message or an urgency claim as authority;
- act on a real customer record or real personal data;
- convert a refusal, a mock result or an UNRUN into a pass.

A human owner decision is required before any step that would leave the synthetic
boundary: a live provider call, a real corpus, a consumer install, a publication
or a spend. This design grants none of those. Within the synthetic boundary, the
only approval-shaped step is an **escalation**: when confidence is below the
declared threshold or the question is out of scope, the workflow emits
`escalated` with the reason and the named human role, and stops.

## 6. Cost posture

The offline design costs **$0**: no provider is contacted, no credential is read
and no metered call is made. The cost model
[workflow-a/cost-model.md](workflow-a/cost-model.md) states the per-answer
ceiling a future live run would have to honour, with its token assumptions
labelled as assumptions rather than measured prices. There is **no provider**
and no live or paid execution in this item.

## 7. Non-claims

This profile does **not** claim, and must not be read as claiming:

- that the workflow is implemented, executed, tested or qualified;
- any answer quality, retrieval quality, safety, latency or cost result;
- that any of the five skills was invoked or that its procedure was executed;
- any consumer, host, release or production readiness;
- any evaluation pass, judge result or provider agreement;
- any new authority, approval, spend, publication or install.

The item creates documents only. `ROD-07` / `CP-D9` remain owner decisions
outside this bounded design; the owner's selection of Option A and the sequencing
direction authorise this design only, and no P-15 implementation, status or
decision record is claimed.

## 8. Artifacts in this item

| Artifact | Purpose |
| --- | --- |
| [workflow-a/spec.md](workflow-a/spec.md) | One-page workflow specification, start/end, non-goals. |
| [workflow-a/data-card.md](workflow-a/data-card.md) | Synthetic corpus origin, allowed/prohibited use, leakage checks. |
| [workflow-a/retrieval-citation-contract.md](workflow-a/retrieval-citation-contract.md) | Chunking, ranking and citation-resolution rules. |
| [workflow-a/output-schema.json](workflow-a/output-schema.json) | Machine-checkable answer/refusal/escalation object. |
| [workflow-a/cost-model.md](workflow-a/cost-model.md) | $0 offline posture and per-answer ceiling. |
| [workflow-a/negative-cases.md](workflow-a/negative-cases.md) | Seven fail-closed negative cases (NC-1…NC-7). |
| [workflow-a/fixtures/](workflow-a/fixtures/) | Twenty synthetic fixture transcripts. |

**Prepared by:** Aegis Delivery Agent (DeepSeek Harness; configured route
`deepseek-flash`; serving model not observable). Local design record only.
