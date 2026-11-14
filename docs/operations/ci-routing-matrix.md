# C3.2 dependency-aware CI routing

**Scope.** This page records the path-to-check matrix, the required-check
never-skip invariant and the one bounded edit to
[`.github/workflows/validate-skills.yml`](../../.github/workflows/validate-skills.yml).
It changes no required context, settings, branch protection, permission,
trigger or job set.

## Matrix

The closed matrix (`aegis.ops-routing/v1`) has one row per existing job:

| Check | Required | Inputs | Never skip | Push lane |
| --- | --- | --- | --- | --- |
| `changes` | no | every changed path | no | computes flags |
| `validate-skills` | **yes** | every changed path | **yes** | runs |
| `gate-guard` | **yes** (pull requests only) | every changed path | **yes** | pull-request-only |
| `windows-offline-checks` | no | `tools/**`, `requirements-ci.in`, `requirements-ci.txt` | no | runs |
| `tools-tests-linux` | no | `tools/**`, `docs/instrumentation/workflow-outcomes-v1.schema.json` | no | runs |
| `tools-tests-windows` | no | `tools/**`, `docs/instrumentation/workflow-outcomes-v1.schema.json` | no | runs |

Rules enforced by `tools/aegis_ops/routing.py`:

- `validate-skills` and `gate-guard` must set `required=true` and
  `never_skip=true` and claim the full changed-path surface;
- a row that would route a required check away is `INVALID`;
- an advisory row may not be declared a required context;
- every changed path must map to at least one row; an unmapped path fails
  closed;
- the `docs_skills` predicate is closed: it is true only when every changed
  path is under `docs/` or `.claude/skills/`. "Other non-code paths" is not
  guessed.

The advisory jobs are routed with:

```
if: github.event_name == 'push' || needs.changes.outputs.tools == 'true'
```

for `tools-tests-linux` and `tools-tests-windows`, and:

```
if: github.event_name == 'push' || (needs.changes.outputs.offline == 'true' && needs.changes.outputs.docs_skills != 'true')
```

for `windows-offline-checks`. A docs/skills-only pull request sets
`docs_skills=true` and, for every docs/skills path other than
`docs/instrumentation/workflow-outcomes-v1.schema.json`, `tools=false`; the
tools jobs skip because `tools` is false, not because `docs_skills` is true. The
schema-path exception: a schema-only pull request that changes only
`docs/instrumentation/workflow-outcomes-v1.schema.json` sets `tools=true` and
`docs_skills=true`, so the tools jobs **run** while the offline job skips. The push lane forces every output true, so the detection lane still
runs the full suite. `validate-skills` has no job-level `if:`; `gate-guard`
keeps its existing pull-request-only condition.

## Regression fixed (2026-11-13)

Before this fix the two tools jobs required both `tools=true` and
`docs_skills != 'true'`. A schema-only PR changes only
`docs/instrumentation/workflow-outcomes-v1.schema.json`; the `changes` job sets
`tools=true` and `docs_skills=true`, so both tools jobs skipped before merge
while the post-merge push lane ran them. The fix removes the `docs_skills`
exclusion from `tools-tests-linux` and `tools-tests-windows` only;
`windows-offline-checks` keeps it, and no required check, trigger, permission,
pinned action or job set changes. Local condition simulation for the
schema-only diff (recorded in the PR body): push lane true; pull-request flags
`tools=true`, `offline=false`, `docs_skills=true` -> tools jobs run, offline
skips. CI run ids at this PR's head are recorded in the PR receipt; this page
makes no claim that the schema-only path ran in CI.

## E1 edit and expected gate-guard red

E1 is a **protected-path** change and is made under AUTH-C3-PROTECTED, the
one-time gate-guard exception. Gate-guard is **expected red** on the Stage C PR
because `.github/workflows/` matches its protected pattern. That red is:

- **not** approval, **not** a green result and **not** a passing check;
- crossed only by the owner's separate merge line, recorded as an
  administrator **bypass** with its authority and the failed check named;
- never represented as `gate-guard passed`;
- accompanied by every other required check green at the final head, or the
  slice stops.

The edit is bounded to the `changes` job filter/outputs and the advisory job
`if:` conditions:

1. add `docs_skills` and keep `tools`/`offline`;
2. route the three advisory jobs on push or their flag, with the docs/skills
   skip;
3. leave `validate-skills` and `gate-guard` unconditional on pull requests;
4. force all three outputs true on push;
5. add no job, remove no job, rename no job, change no trigger, permission,
   required context, setting or pinned action;
6. keep the next-to-merge comment and the final-base revalidation statement.

`python -m tools.aegis_ops routing --input <matrix> --workflow .github/workflows/validate-skills.yml`
checks the job set, output names, required-job conditions, push forcing, the
closed predicate and action pinning. CI's own YAML parse and the workflow run
are the external confirmation.

## R8 and C2.2 reuse

The change reuses the existing six jobs and the existing `changes` filter; it
adds no runner, workflow, script or dependency. It is scoped to the affected
paths and keeps a legitimate passing path for every job. C2.2's mechanical
preflight is **consumed by reference**, not duplicated: this page does not
re-implement preflight checks. Repo-wide adoption (T11) is not assumed; only
these six jobs are described.

**Measured-overhead justification (REPORTED; not re-measured here).** The
efficiency review recorded 68.6% skipped workflow runs, 88.1% skipped DeepSeek
review runs, median green-to-merge idle wait 19m19s and 174.6 minutes of
failed-run CI waste (122.1 minutes by-design gate-guard reds). This slice does
not claim a new saving; C4.2 is the measurement route, and it has not started.
No dollar or hours-to-delay figure is inferred.

## Next-to-merge and exact base

The branch is kept next-to-merge. The `changes` job fetches
`origin/$BASE_REF` and computes a three-dot diff at the current base; the
`gate-guard` job does the same with NUL records. The final base/head are
revalidated by the PR process at the head being merged. No strict/up-to-date
setting is added, and no "resync" claim is made; T4 was declined.

## Bypass accounting

| Field | Required record |
| --- | --- |
| Failed check | `gate-guard` at the exact head, with its run id |
| Authority | AUTH-C3-PROTECTED and the owner merge line |
| Classification | administrator bypass, not a pass |
| Scope | the E1 workflow edit only |
| Other required checks | green at the final head, or the slice stops |

A bypass without that record is not a bypass; it is an unresolved red.

## UNRUN

The actual PR's CI at the exact head, the gate-guard red run id and the owner
merge line are **UNRUN** until the PR exists and is reviewed. The static
invariants are testable locally; the hosted result is not claimed before it
happens.
