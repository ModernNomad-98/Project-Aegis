# ROUTE-002 dispositions — 2026-09-26

**Reading key:** This record closes the ROUTE-002 triage that the [AEGIS-060+ register](../../audits/aegis-060-plus-register.md#2-systemic-observations--no-id-assigned-evidence-incomplete) left pending. It is for maintainers reading a future contract audit. It is a review ledger, not a code change. ROUTE-002 is an informational rule in the [contract-audit engine](../../../scripts/audit-skill-contracts.py). It fires when skill A's description says "do not use this skill for X, use B" and B's description never names A back. That one-way pointer is a *finding*, or an *edge* from A (the source skill) to B (the target skill). A *yield* is the clause added to B's description that names A back. Pull request (PR) identifies a repository change.

## Owner decision

Peter decided on 2026-09-26:

- **Reciprocate 23 high-value seams.** 23 target skills gain a yield. That closes 31 edges. Three batch PRs carry the work: `docs/route002-reciprocity-1`, `-2` and `-3`.
- **Record every other ROUTE-002 finding as census data.** Census data is informational evidence about the routing graph. It is not a defect and it is not scheduled work.
- **D64 stays as decided.** The five one-way findings from `feature-flag-architect` stay census data. That decision is recorded in [D64](../../reconciliation/step-0-reconciliation-v4.md).

## Scan and reconciliation

The audit ran on `origin/main` at `0f46808d865751fac396b52422bd964e6b7c2cf1`. The engine is v1.13.1, and the scan used a `git archive` extract. It reports 352 findings, 268 of them ROUTE-002. The triage was made earlier at `032e030` on 263 edges. All 263 are still reported unchanged. The only new edges are the five from `feature-flag-architect` (added by D64, PR #383). They join bucket a as census data.

| Bucket | Meaning | Edges | Disposition |
| --- | --- | ---: | --- |
| a | Low routing value: distant neighbour, manual-only skill on one side, or a hub target that cannot name every excluder (includes the 5 D64 edges) | 149 | census-data |
| b-high | Near-miss seam where a model could pick the wrong skill | 30 | reciprocate-in-PR |
| b-medium | Plausible overlap, below the owner's cut | 36 | census-data |
| c | Target's trigger-evals already name the source; the description is silent on purpose | 51 | census-data |
| d | Special case (below) | 2 | fix-A-side (1), engine-false-positive (1) |
| **Total** | | **268** | 236 census-data, 30 reciprocate-in-PR, 1 fix-A-side, 1 engine-false-positive |

The two special cases:

- **`data-migration-runbook-author` → `rollback-runbook-author` (fix-A-side).** The source credits "the change SEQUENCE itself" to `rollback-runbook-author`. Sequencing belongs to `schema-evolution-planner`, which the same description names earlier. The seam is real, so batch 3 corrects the source clause and adds the target's yield.
- **`prompt-injection-defender` → `threat-modeler` (engine-false-positive).** The source names `ai-threat-modeler`, and the engine's substring match also finds `threat-modeler` inside it. No seam exists. The engine fix belongs to a separate, protected `scripts/` scope and is not part of this record.

## Target skills by batch

Batch assignment was read from each batch worktree's edits when this record was built. The coordinator owns the final split.

| Batch branch | Target skills that gain a yield |
| --- | --- |
| `docs/route002-reciprocity-1` | `change-classification-gate`, `code-reviewer` (2), `human-approval-boundary` (2), `model-poisoning-reviewer`, `product-spec-writer` (2), `requirements-gathering-facilitator`, `screenshot-evidence-planner`, `source-of-truth-reconciler` |
| `docs/route002-reciprocity-2` | `admin-console-architect`, `ai-misinformation-guard`, `architecture-designer` (2), `plan-entitlement-architect`, `rls-policy-auditor`, `security-pr-reviewer`, `static-analysis-reviewer` (2), `tenant-modeler` (2) |
| `docs/route002-reciprocity-3` | `adr-writer` (2), `api-event-architect` (2), `audit-log-architect`, `llm-output-safety-reviewer`, `rollback-runbook-author`, `streaming-event-architect`, `tech-spec-writer` |

A number in parentheses is the count of source skills that target will name. The [machine-readable dispositions](route002-dispositions.json) list every edge with its fingerprint, normalized message, bucket, disposition, rationale and batch.

## How future audits should read ROUTE-002

- **Expect about 237 findings after the three batches merge.** The 31 reciprocated edges disappear. The census edges, the D64 edges and the engine false positive stay.
- **Treat a listed edge as census data, not a defect.** Match a current finding to this record by source skill, target skill and normalized message. Normalization uses NFKC, maps em and en dashes to "-", collapses whitespace and lowercases, as in the [2026-09-26 skill-contract record](../skill-contract-dispositions-2026-09-26/candidate-dispositions.md).
- **Triage only new edges.** An edge absent from this record is new, for example from a new skill. Put it in a bucket, and reciprocate it only when it is a near-miss seam.
- **Recheck a reciprocated edge that comes back.** If one of the 31 still appears after its batch merges, the yield was dropped or reworded.

## Limits

- These are reviewer judgments about description text. They do not measure model routing behavior.
- Batch assignment reflects uncommitted work in the batch worktrees at record time. The PRs, not this page, are authoritative for what changed.
- The scan ran on a `git archive` extract, so the engine reports `repo_sha: unknown`. The archived engine copy hashes to SHA-256 `3e8d24cdf610…` (CRLF line endings). The raw LF Git blob hashes to `3f19d6731bea…`.
