# Flag Rollout Sheet

Detail for `feature-flag-rollout-strategist`. Read on demand.

## Flag-type classification (decide FIRST)

| Type | Lifetime | Purpose | Owner skill if mislabeled |
|---|---|---|---|
| Release | Temporary — remove after GA | De-risk shipping a change | — (this skill) |
| Operational / kill-switch | Long-lived | Turn a subsystem off in an incident | — (this skill; documented) |
| Experiment | Duration of test | A/B variant assignment | design → ab-test-designer |
| Entitlement / permission | Permanent | Plan feature / role gate | plan-entitlement-architect / authorization-matrix-designer |

Most flag pathologies trace to a release flag that was actually an
entitlement, or an entitlement modeled as a "permanent flag". Classify
before designing.

## Progressive stages

| Stage | Population | Advance when |
|---|---|---|
| Internal / dogfood | Employees | No obvious breakage; team confidence |
| Canary | 1–5%, low-risk segment | Guardrails green for the bake time |
| Ramp | 10 → 25 → 50% | Guardrails hold at each step |
| Cohorts | Segment by segment | Per-cohort guardrails green |
| GA | 100% | Stable at 50%+; ready to remove flag |

Every stage has BOTH advance criteria and rollback criteria. Bake time
must exceed the metric's detection window — ramping faster than you can
see harm defeats the point.

## Guardrail selection

Pick the FEW signals that mean "this is going wrong":
- Error rate / crash rate
- Latency (p95/p99) on the affected path
- A key conversion or correctness metric for the changed flow
Each gets a rollback threshold. Automatic rollback where the platform
supports it; otherwise a named human on the hook with the kill switch.

## Fail-safe default (flag service unavailable)

| Flag type | Safe default when service is down |
|---|---|
| Release | OLD behavior (never fail into half-built code) |
| Kill-switch | Protective state (off = safe) |
| Experiment | Control variant |
| Entitlement | Deny (least privilege) — but this belongs to the entitlement skill |

Failing OPEN turns a flag-service blip into a feature outage. Default to
the safe state.

## Sticky targeting

- Bucket by a STABLE id (user/account id, not a per-request random) so a
  user stays in one variant across sessions and devices.
- Non-sticky assignment flip-flops UX and invalidates analytics.
- State first segments (internal, beta, low-risk) and exclusions.

## Lifecycle / flag debt

- At creation: assign an owner and a removal trigger (e.g. "remove 2
  weeks after GA").
- Removal = delete the flag config AND the dead code branch. A flag left
  in code still doubles the test matrix.
- Long-lived operational flags are documented as intentional, with the
  conditions under which they're used.
- Executing rollout changes on live systems follows the repo's approval
  path; this skill designs the plan.
