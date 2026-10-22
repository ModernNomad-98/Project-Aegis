# Retrieval eval plan: retrieval-engineering-designer artifact

## 1. Retrieval design table

| Component | Decision | Alternatives | Metric/evidence |
| --- | --- | --- | --- |
| Chunking | semantic sections + 10% overlap, metadata retained | fixed-size, parent-child | chunk recall on golden queries |
| Embedding | <model class rejected/accepted with cost> | dense-only, lexical-only | recall@k / cost per query |
| Index | HNSW with tenant scoping | flat, IVF | latency at target load |
| Fusion | RRF(dense, BM25) | weighted score, dense-only | nDCG@10 |
| Reranking | cross-encoder top-50 (if budget) | no rerank, LLM rerank | precision@5, latency delta |

## 2. Relevance evaluation plan

| Item | Specification |
| --- | --- |
| Golden set | source, size, strata (head/tail/ambiguous), labelling rule |
| Metrics | recall@k, nDCG@10, MRR; per-tenant and global |
| Baseline | current retrieval version + date |
| Regression gate | no metric drop > <tolerance> vs baseline on PR/CI cadence |
| Failure analysis | sample misses by cause (staleness, chunk boundary, lexical-only gap) |

## 3. Failure modes and handoffs

| Failure mode | Detection | Mitigation | Owner |
| --- | --- | --- | --- |
| Stale index | freshness metric, update lag | reindex schedule, versioned docs | retrieval owner |
| Ambiguous query | low-margin results | clarification/fallback rank | product/retrieval |
| Poisoning surface | anomalous docs/ingest | ingest trust, provenance | rag-security-architect |
| Authorization/leakage | cross-tenant results | retrieval-time authz | rag-security-architect |

## 4. Completion checklist

- [ ] Golden set exists or its construction plan does.
- [ ] Metrics/thresholds/regression gate stated.
- [ ] Security handoff to rag-security-architect recorded.
- [ ] No live tuning/eval run claimed.
