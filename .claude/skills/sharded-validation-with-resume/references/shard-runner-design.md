# Sharded Validation — Runner & Gate Design Detail

Companion to `sharded-validation-with-resume`. All shapes are reference
designs; installation into CI is a handoff to `ci-pipeline-architect` or a
human.

## Status-file schema

One file per run (JSON keeps it diffable and machine-checkable):

```json
{
  "run_id": "<commit-sha>-<timestamp>",
  "commit": "<sha>",
  "tier": "full",
  "shards": {
    "core-domain":     { "state": "passed",      "started": "…", "ended": "…", "duration_s": 412, "tests_executed": 238, "tests_failed": 0 },
    "api-integration": { "state": "failed",      "duration_s": 388, "tests_executed": 154, "tests_failed": 3, "failure_class": "assertions" },
    "ui-e2e":          { "state": "interrupted", "duration_s": 1800, "tests_executed": 41, "failure_class": "timeout" },
    "platform":        { "state": "pending" },
    "uncategorized":   { "state": "passed", "tests_executed": 0, "policy": "empty-or-fail", "note": "0 matched = policy-pass ONLY because membership rules matched nothing" }
  }
}
```

Schema rules:

- `state ∈ pending | running | passed | failed | interrupted`;
  `failure_class ∈ assertions | timeout | infra` — `failed` is reserved for
  real assertion/product failures; timeouts and infra deaths are
  `interrupted`.
- `tests_executed` is mandatory: a non-empty shard with 0 executed tests is
  a FAILURE (bad glob / hidden skip), not a pass. Skipped execution is
  never a pass.
- The status file binds to `commit`. A new commit = new run_id = all prior
  passes invalid.

## Runner modes & the resume law

| Mode | Semantics |
| --- | --- |
| full | fresh status file; run every shard |
| `-Resume <run_id>` | rerun ONLY shards whose state is `interrupted` or `pending` in that run, same commit. `passed` shards are not re-derived. **`failed` shards are NOT eligible** — a real failure reruns (fully, post-fix), it is never resumed around. |
| `-Shard <name>` | targeted single-shard run (post-fix rerun, local debugging); updates only that shard's record |

The resume law in one line: **resume exists to survive infrastructure, not
to survive failures.** A runner that cannot distinguish `failed` from
`interrupted` must not offer resume.

Duration capture is first-class: expected vs observed per shard; a shard
killed at its ceiling records `interrupted/timeout` with the observed
duration — remediation is the smallest safe fix (split the shard, reduce
setup, rerun once), never raising ceilings to convert red to green.

## Aggregate-gate CI shape (reference)

```yaml
# reference shape — installed via ci-pipeline-architect / human review
jobs:
  classify:            # risk-tiered-validation-selector's rules run here
    outputs: { tier: ... }
  shard-core-domain:
    needs: classify
    if: needs.classify.outputs.tier == 'full'
    ...
  # …one job per shard, same pattern…
  validation-gate:     # THE ONLY REQUIRED STATUS CHECK
    needs: [classify, shard-core-domain, shard-api-integration, shard-ui-e2e, shard-platform, shard-uncategorized]
    if: always()       # runs even when shards were skipped
    steps:
      - run: |
          # explicit evaluation — do not trust job-level defaults:
          # tier == docs-only → shards SKIPPED is satisfied; gate passes on docs checks
          # tier == full      → every shard must be 'success'; 'skipped' or
          #                     'cancelled' FAILS the gate (skip ≠ pass on full)
```

Why this shape: branch protection references ONE stable name
(`validation-gate`). Per-shard required checks break in both directions —
docs-only PRs hang forever on skipped-but-required names, and renamed shard
jobs silently drop out of protection. The gate's `if: always()` +
explicit-evaluation step is what makes conditional skipping compatible with
required checks.

## Shard-map balancing

- Build from measured durations (`tests_executed`, `duration_s` history),
  not intuition; target the critical path (slowest shard), not the mean.
- 3–6 shards is the useful range: fewer ≈ no resume benefit; more ≈
  orchestration overhead and fixture duplication.
- Shard by FUNCTION (domain, api, ui-e2e, platform) so every new test has a
  right answer; never create `misc` (that is `uncategorized` with a nicer
  name and no policy).
- Rebalance trigger: a shard's p95 duration within ~20% of its ceiling, or
  a shard consistently >2× the median.

## Worked interruption → resume trace

1. Run `full` on commit `ab12cd3` → status: core-domain `passed`,
   api-integration `passed`, ui-e2e `interrupted (timeout @1800s)`,
   platform `pending` (never started — runner died), uncategorized
   `passed (0 matched)`.
2. `-Resume ab12cd3-…` → reruns ONLY `ui-e2e` and `platform`. Passes are
   kept; nothing re-derives core-domain.
3. ui-e2e now `failed (assertions: 2)` → resume is OVER for that shard;
   fix the product/test, then `-Shard ui-e2e` post-fix; status updates on
   the same commit only if the fix didn't change the commit (it did →
   new run_id, full tier re-earns its passes — the preflight's
   worktree/local run keeps that cheap).
4. Aggregate gate evaluates final states on whatever run_id the PR's head
   commit produced — passes from older commits are unusable by
   construction.

## Interaction notes

- **`local-ci-mirror-preflight`:** local full-tier = invoke this runner
  (same shard map, same status semantics) — the preflight never re-derives
  its own bundle where shards exist.
- **`risk-tiered-validation-selector`:** the classify job IS the selector's
  rules; the gate consumes its tier output. Docs-only skip semantics are
  legitimate only because the selector said docs-only.
- **`flaky-test-detective`:** an intermittently-failing test is diagnosed,
  not resumed around and not auto-retried into green by the runner.
