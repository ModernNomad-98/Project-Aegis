---
name: rag-security-architect
description: Design or review the security of a RAG retrieval pipeline and vector store (OWASP LLM08) — enforce authorization AT RETRIEVAL TIME so a query returns only documents the calling user and tenant may see, scope every index/namespace by tenant, carry document ACLs into the query filter, and address embedding inversion, membership inference, poisoned documents, and stale permission metadata. Compose tenant-isolation-reviewer and multi-tenant-data-architect for tenant scoping. Use for RAG retrieval or semantic search over access-controlled data. Do NOT use for injection in retrieved content (prompt-injection-defender), training-time poisoning (model-poisoning-reviewer), disclosure in the completion (sensitive-disclosure-guard), or generic tenant-data design (multi-tenant-data-architect).
---

# RAG Security Architect

Terms used below: **RAG** means retrieval-augmented generation; an **ACL** is
an access control list recording who may access a document. **OWASP** means
Open Worldwide Application Security Project; **LLM08** is its large-language-model
risk code used here for vector and embedding weaknesses. **IDOR** means insecure
direct object reference, and **PII** means personally identifiable information.
These terms describe risks; they do not
replace authorization enforced inside the retrieval query.

## Purpose

Design or review a retrieval-augmented-generation pipeline so that retrieval
itself is access-controlled: a query returns only documents the calling user
and tenant are authorized to see, enforced AT RETRIEVAL TIME in the query,
never by filtering results after the store already returned them. The output
covers vector-store tenant scoping, document-level ACL propagation into the
retrieval filter, and embedding-specific risks (LLM08) — inversion, membership
inference, document poisoning, and stale permissions in already-embedded
content. Tenant-scoping semantics are composed from `tenant-isolation-reviewer`
and `multi-tenant-data-architect`, not re-invented here.

## Use When

- Use when: building or reviewing a RAG pipeline, vector database, embedding
  index, or semantic search over access-controlled or multi-tenant data.
- Use when: adding retrieval to an AI feature and retrieved documents have
  per-user or per-tenant access rules.
- Use when: a vector store is shared across tenants and you need to prove one
  tenant's queries cannot surface another tenant's documents.
- Do NOT use when: the risk is injected instructions in retrieved content
  once it is in context — that is `prompt-injection-defender`.
- Do NOT use when: the concern is poisoning the training/fine-tuning corpus
  (`model-poisoning-reviewer`) or sensitive data appearing in the completion
  (`sensitive-disclosure-guard`).
- Do NOT use when: designing the general tenant data layer with no retrieval
  dimension — `multi-tenant-data-architect`.

## Inputs to Inspect

1. The retrieval architecture: vector store/index, how documents are ingested
   and chunked, what metadata is stored, how queries are built and filtered.
2. The access model for the source documents: who may see what, per-tenant and
   per-user/role/document ACLs — from `authorization-matrix-designer` /
   `tenant-modeler` output where it exists.
3. Where authorization currently happens: at retrieval (in the query) or after
   (filtering the returned set) — this is the central finding.
4. Tenant scoping of the store: shared index with a filter, namespace per
   tenant, or database per tenant; `tenant-isolation-reviewer` findings for
   the vector-store surface.
5. Ingestion/permission sync: how indexed ACL metadata changes when a
   document's permissions change, how deleted vectors are removed, and
   when changed source content actually requires re-embedding.
6. Embedding/model details relevant to inversion and membership inference:
   what data is embedded, whether embeddings or raw chunks are returned to
   clients.

## Workflow

1. **Trace a query end to end.** From user query → embedding → vector search →
   candidate set → filter → context assembly. Identify exactly where
   authorization is applied. No retrieval design to inspect → Stop Conditions.
2. **Enforce authorization at retrieval time.** The query MUST carry the
   tenant scope and the user's document-level permissions as filter
   predicates so the store never returns unauthorized vectors. Post-retrieval
   filtering is a finding: it means unauthorized documents were fetched, can
   leak via ranking/counts/latency, and one filter bug exposes everything.
3. **Scope the vector store by tenant.** Verify the isolation mechanism
   (namespace/index/collection per tenant, or a mandatory tenant filter that
   cannot be omitted) using
   [references/rag-retrieval-authz.md](references/rag-retrieval-authz.md).
   Compose `multi-tenant-data-architect` for the per-store scoping decision.
4. **Propagate document-level ACLs into the index.** Store the authorization
   metadata (owner, tenant, allowed roles/groups) alongside each chunk so it
   can be a query predicate. Decide how ACL metadata changes and deletions
   propagate to the index; stale permissions on indexed content are a leak.
   Re-embed when content changes, not merely because ACL metadata changes.
5. **Address embedding-specific risks (LLM08):** embedding inversion (raw
   source recoverable from vectors — don't expose embeddings to clients,
   consider the sensitivity of what's embedded); membership inference; and
   document poisoning (an attacker-planted document engineered to rank for a
   target query — cross-reference `model-poisoning-reviewer` for corpus
   integrity and `prompt-injection-defender` for payloads inside documents).
6. **Design negative tests.** Two-tenant fixtures where tenant A queries for
   tenant B's known content and must get nothing; user-without-access queries
   for a restricted document; a deleted/ACL-changed document must stop
   appearing. Hand executable form to `multi-tenant-security-tester` and
   suite encoding to `ai-evaluation-harness`.
7. **Handle citations/evidence safely.** Returned citations must not reveal
   existence or metadata of documents the user cannot access; snippet
   boundaries must not spill adjacent unauthorized content.

## Output Format

```
RAG (RETRIEVAL-AUGMENTED GENERATION) SECURITY DESIGN/REVIEW — <system>
Query trace: <query → embed → search → filter → context> | Authorization point: <retrieval | after retrieval (finding)>
Vector-store tenant scoping: <namespace/index/filter mechanism + can-it-be-omitted>
Document access-control-list (ACL) propagation: <metadata stored | how ACL change/delete flows to the index>
Embedding risks (OWASP LLM08):
  Inversion: <embeddings exposed? sensitivity of embedded data>
  Membership inference: <exposure + mitigation>
  Poisoning: <ingestion trust + ranking abuse> (→ model-poisoning-reviewer)
Findings (severity-ranked): <severity> <issue> — <leak path> — <fix>
Negative tests: <cross-tenant / no-access / stale-ACL cases> (→ multi-tenant-security-tester)
Citation safety: <no existence/metadata leak of unauthorized docs>
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] The query trace pinpoints where authorization is applied; any
      post-retrieval filtering is flagged as a finding.
- [ ] Retrieval-time filter carries BOTH tenant scope and user document-level
      permissions; the tenant filter cannot be silently omitted.
- [ ] Vector-store isolation mechanism is named and its bypass conditions
      stated (composed from multi-tenant-data-architect, not re-derived).
- [ ] ACL-change and deletion propagation to the index is specified; stale
      permissions are treated as a leak.
- [ ] Embedding inversion, membership inference, and document poisoning are
      each addressed or explicitly ruled out with a reason.
- [ ] Negative tests include cross-tenant, no-access, and stale-ACL cases.
- [ ] Citations/snippets cannot reveal unauthorized documents' existence or
      content.

## Security Rules

- Authorization is enforced at retrieval time, in the query — never by
  filtering results after the store returns them.
- The vector store is tenant-scoped by a mechanism that cannot be omitted by
  a forgotten filter; shared indexes require a mandatory, tested predicate.
- Retrieved content remains untrusted as INSTRUCTIONS even when authorized as
  DATA — retrieval authz does not make document content safe to obey
  (`prompt-injection-defender` owns that half).
- Deletion and permission changes must reach the index; an index is a
  copy of the data and inherits its access rules.

## Gotchas

- Post-retrieval filtering feels safe and is the most common leak: the store
  already searched all tenants' vectors, so ranking, result counts, latency,
  and one filter bug all leak — the fix is filtering INSIDE the query.
- "Namespace per tenant" only isolates if the namespace is derived
  server-side from the authenticated tenant; a client-supplied namespace is
  just an IDOR with extra steps.
- Embeddings are lossy but not safe: inversion attacks reconstruct source
  text well enough to leak PII — don't hand raw vectors to clients and weigh
  what you embed.
- Chunk overlap can spill: a snippet window that runs past the authorized
  chunk into the next document leaks content the user can't see.
- Deleting the source row but leaving the embedding is a classic residual
  leak — the "deleted" document keeps answering queries.
- Updating indexed ACL metadata after a permission tightening is easy to
  forget; the old vector may remain retrievable under the old permission
  until the index metadata or affected index entry is updated.

## Stop Conditions

- No retrieval pipeline, vector store, or query code is available — stop;
  this skill secures a concrete retrieval design, not a description.
- The tenant-isolation model itself is undefined — get `tenant-modeler` /
  `multi-tenant-data-architect` output first; retrieval scoping needs a tenant
  definition to enforce.
- A review finds an active cross-tenant leak in production — route to
  `incident-response-runbook`; containment is a human decision.
- The real issue is injected instructions, corpus poisoning at training time,
  or completion-side disclosure — hand to the owning skill.

## Supporting Files

- [references/rag-retrieval-authz.md](references/rag-retrieval-authz.md) —
  retrieval-time authorization patterns, vector-store tenant-scoping
  mechanisms and their bypass conditions, ACL propagation, and the
  embedding-risk (inversion/membership/poisoning) rubric.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the data & retrieval
  cluster and against `multi-tenant-data-architect`, `tenant-isolation-reviewer`,
  and `multi-tenant-security-tester`.
