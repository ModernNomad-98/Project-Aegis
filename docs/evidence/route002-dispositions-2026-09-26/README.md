# ROUTE-002 dispositions — 2026-09-26

**Reading key:** This record closes the ROUTE-002 triage that the [AEGIS-060+ register](../../audits/aegis-060-plus-register.md#2-systemic-observations--no-id-assigned-evidence-incomplete) (the list of contract-audit findings numbered AEGIS-060 and later) left pending. It is for maintainers reading a future contract audit. It is a review ledger, not a code change. ROUTE-002 is an informational rule in the [contract-audit engine](../../../scripts/audit-skill-contracts.py). It fires when skill A's description says "do not use this skill for X, use B" and B's description never names A back. That one-way pointer is a *finding*, or an *edge* from A (the source skill) to B (the target skill). A *yield* is the clause added to B's description that names A back. A *seam* is a boundary where two skills' scopes meet closely enough that a model could pick the wrong one. A *hub* is a target skill that five or more skills exclude toward. A *fingerprint* is a 12-character hash that identifies one finding. A pull request (PR) is a proposed repository change; every PR named here is merged.

## Owner decision

Peter decided on 2026-09-26:

- **Reciprocate 23 high-value seams.** 23 target skills gained a yield, closing 31 edges. Five of them are hubs (targets that five or more skills exclude toward): `api-event-architect`, `architecture-designer`, `audit-log-architect`, `code-reviewer` and `streaming-event-architect`. They are deliberate exceptions to the rule that hub targets go in bucket a as census data (see the bucket table below), and they yield only to the named near-miss sources. Three batch PRs carried the work, and all three are merged: #394 (`29c484f`, branch `docs/route002-reciprocity-1`), #395 (`741b29a`, `-2`) and #396 (`cd7af02`, `-3`).
- **Record every other ROUTE-002 finding as census data, except the one engine false positive (below), whose fix is tracked separately.** Census data is informational evidence about the routing graph. It is not a defect and it is not scheduled work.
- **D64, as amended on 2026-09-26.** Decision D64 in the [step-0 reconciliation log](../../reconciliation/step-0-reconciliation-v4.md) left five one-way findings from `feature-flag-architect` as census data. PR #395 then gave `plan-entitlement-architect` a yield that names `feature-flag-architect` back, which closed the `feature-flag-architect` → `plan-entitlement-architect` edge. The owner kept that yield on 2026-09-26, and the log records it as a [dated D64 amendment](../../reconciliation/step-0-reconciliation-v4.md#6-post-merge-corrections). The other four D64 edges stay census data.

## Scan and reconciliation

The audit ran on `origin/main` at `0f46808d865751fac396b52422bd964e6b7c2cf1`. The engine is v1.13.1, and the scan used a `git archive` extract. It reports 352 findings, 268 of them ROUTE-002. The triage was made earlier at `032e030` on 263 edges. All 263 are still reported unchanged. The only new edges are the five from `feature-flag-architect` (added by D64, PR #383). They join bucket a: four as census data, and one closed by #395 (the D64 amendment above).

| Bucket | Meaning | Edges | Disposition |
| --- | --- | ---: | --- |
| a | Low routing value: distant neighbour, manual-only skill (one that runs only when a user names it) on one side, or a hub target that cannot name every excluder (includes the 5 D64 edges); the five reciprocated hubs above are owner exceptions | 149 | census-data (148), closed-by-batch-PR (1: the D64 edge closed by #395) |
| b-high | Near-miss seam where a model could pick the wrong skill | 30 | reciprocate-in-PR |
| b-medium | Plausible overlap, below the owner's cut | 36 | census-data |
| c | Target's trigger-eval file (its tests of when the skill should or should not be chosen) already names the source; the description is silent on purpose | 51 | census-data |
| d | Special case (below) | 2 | fix-A-side (1), engine-false-positive (1) |
| **Total** | | **268** | 235 census-data, 30 reciprocate-in-PR, 1 fix-A-side, 1 engine-false-positive, 1 closed-by-batch-PR |

The two special cases:

- **`data-migration-runbook-author` → `rollback-runbook-author` (fix-A-side).** The source credits "the change SEQUENCE itself" to `rollback-runbook-author`. Sequencing belongs to `schema-evolution-planner`, which the same description names earlier. The seam is real, so batch 3 corrects the source clause and adds the target's yield.
- **`prompt-injection-defender` → `threat-modeler` (engine-false-positive).** The source names `ai-threat-modeler`, and the engine's substring match also finds `threat-modeler` inside it. No seam exists. The engine fix belongs to a separate, protected `scripts/` scope and is not part of this record.

## Target skills by batch

Batch assignment was first read from each batch worktree's edits. It was then verified against the merged PRs: every listed target's `SKILL.md` changed in its batch's merge commit, and batch 3 also changed the `data-migration-runbook-author` source.

| Batch branch (merged PR) | Target skills that gained a yield |
| --- | --- |
| `docs/route002-reciprocity-1` (#394, `29c484f`) | `change-classification-gate`, `code-reviewer` (2), `human-approval-boundary` (2), `model-poisoning-reviewer`, `product-spec-writer` (2), `requirements-gathering-facilitator`, `screenshot-evidence-planner`, `source-of-truth-reconciler` |
| `docs/route002-reciprocity-2` (#395, `741b29a`) | `admin-console-architect`, `ai-misinformation-guard`, `architecture-designer` (2), `plan-entitlement-architect`, `rls-policy-auditor`, `security-pr-reviewer`, `static-analysis-reviewer` (2), `tenant-modeler` (2) |
| `docs/route002-reciprocity-3` (#396, `cd7af02`) | `adr-writer` (2), `api-event-architect` (2), `audit-log-architect`, `llm-output-safety-reviewer`, `rollback-runbook-author`, `streaming-event-architect`, `tech-spec-writer` |

A number in parentheses is the count of triaged source skills that target names. `plan-entitlement-architect` also names `feature-flag-architect`, the D64 edge above. The [machine-readable dispositions](route002-dispositions.json) list every edge with its fingerprint, normalized message, bucket, disposition, rationale and batch.

## How future audits should read ROUTE-002

- **At `56ea7e4`, expect 234 ROUTE-002 findings.** Later merges can close more census edges, so recount before comparing. A fresh audit of `56ea7e4` (engine v1.13.1, `git archive` extract) reports 318 findings, 234 of them ROUTE-002: 233 census edges and the engine false positive. From the 268 scanned, the 31 reciprocated edges closed when the batches merged, and #395 closed one D64 edge. PR #393 (`9b8f5b2`) rewrote the `cloud-architecture-decider` description and closed two census edges toward it, from `architecture-advisor` and `aws-saas-architect`. No new edge appeared. A later audit of `b553d91` on 2026-09-27 (same engine and extract method) reports 317 findings, 233 of them ROUTE-002. PR #409 renamed `system-prompt-leakage-reviewer` to `hidden-context-exposure-reviewer`, and `agent-tool-safety-guard`'s description names the new skill, so the census edge `system-prompt-leakage-reviewer` → `agent-tool-safety-guard` no longer appears. Again no new edge appeared.
- **Treat a listed edge as census data, not a defect.** Match a current finding to this record by source skill, target skill and normalized message. Normalization applies Unicode NFKC (Normalization Form KC, compatibility composition), maps em and en dashes to "-", collapses whitespace and lowercases, as in the [2026-09-26 skill-contract record](../skill-contract-dispositions-2026-09-26/candidate-dispositions.md).
- **Triage only new edges.** An edge absent from this record is new, for example from a new skill. Put it in a bucket, and reciprocate it only when it is a near-miss seam.
- **Recheck a closed edge that comes back.** If one of the 31, the D64 edge closed by #395 or the two edges closed by #393 reappears, the naming clause was dropped or reworded.

## Limits

- These are reviewer judgments about description text. They do not measure model routing behavior.
- Batch assignment was read from the batch worktrees and then verified against the merged PRs #394, #395 and #396. The PRs, not this page, remain authoritative for what changed.
- The scan ran on a `git archive` extract, so the engine reports `repo_sha: unknown`. The archived engine copy hashes to SHA-256 (Secure Hash Algorithm, 256-bit) `3e8d24cdf610…`, with CRLF (carriage return plus line feed) line endings. The raw Git blob, with LF (line feed) endings, hashes to `3f19d6731bea…`.
