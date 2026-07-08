# Eval runner design — blueprint tables

Companion to [../SKILL.md](../SKILL.md). These tables are the reusable core
of a runner spec; every value marked ⟨choose⟩ is an open decision the design
must surface, not silently default.

## Execution semantics per case type

| Case type (as found in corpus) | Session setup | PASS condition | Notes |
| --- | --- | --- | --- |
| `should_trigger` (`triggers: true`) | Fresh session, full library visible, case prompt verbatim | Target skill activates | Repeats-with-quorum applies |
| Refusal case (typed `should_trigger`, `triggers: true` by convention) | Same | Target skill activates AND response satisfies the refusal assertions | Two-part pass; report each part |
| `should_not_trigger` (`triggers: false`) | Same | Named skill does NOT activate | Record what fired instead — routing telemetry, not a verdict |
| Trigger-evals discrimination case | Same | `expected_skill` activates AND every `should_not_trigger` entry stays silent | Score pairwise; partial wins visible |

Isolation rule: one case = one fresh session. No shared context, no case
ordering effects, no reuse of a session that has already routed a prompt.

## Judging decision table

| Assertion class | Example from a real corpus | Judge |
| --- | --- | --- |
| Deterministic — activation | "skill X fires" | Harness observation |
| Deterministic — artifact shape | "delivers the Output Format block" | Script: block/header match |
| Semantic — content | "names the colliding skill", "refuses the shortcut" | LLM judge with rubric derived from the assertion text |
| Unjudgeable as written | "handles the situation well" | Neither — flag to the skill author (feeds `skill-quality-reviewer` check 4) |

Judge rules:

- Judge independence: a separate call seeing ONLY the case transcript and
  the rubric — never the session's own reasoning or the runner's expected
  answer beyond the rubric.
- Judge model: ⟨choose⟩ — document family and version; changing the judge
  re-baselines all semantic results.
- Judge failure (malformed verdict, refusal, timeout) → state JUDGE-ERROR.
  Never mapped to case PASS or FAIL; counted separately in corpus metrics.

## Report schema

Per case: `case_id`, `skill`, `type`, `state ∈ {PASS, FAIL, ERROR, JUDGE-ERROR, QUARANTINED, UNRUN}`,
`repeats_run`, `wins`, `what_fired_instead` (should-not-trigger only),
`evidence_ref` (transcript pointer).

Per skill: case totals by state, trigger accuracy (quorum wins /
trigger cases run), discrimination record (pairwise wins/losses),
refusal compliance.

Corpus: run coverage (run vs UNRUN), spend vs cap, quarantine list with
reasons, judge-error rate, cases flagged unjudgeable-as-written.

UNRUN is the default state of every case in every report. A case acquires
another state only from an actual execution in the reported run.

## Sampling tiers and cost arithmetic

Cost model per full run:

```
sessions   = trigger_cases × N_repeats + discrimination_cases × N_repeats
judge_calls = semantic_assertions_exercised (≤ sessions × avg_semantic_per_case)
cost       ≈ sessions × session_cost + judge_calls × judge_cost
```

| Tier | Scope | When | Purpose |
| --- | --- | --- | --- |
| PR tier | Cases of skills CHANGED in the PR + their named overlap neighbors | Per PR, advisory lane | Catch regressions where they were edited |
| Cadence tier | Stratified sample across all skills (⟨choose⟩ fraction), rotating | Scheduled | Drift detection across the untouched corpus |
| Full tier | Entire corpus | Rare: convention changes, runner upgrades, judge swaps | Re-baseline |

Spend cap: a per-run and per-period budget with a kill switch that stops
launching sessions and marks the remainder UNRUN — never a silent partial
report that looks complete. Budget guardrail patterns:
`ai-cost-guardrail-designer`.

## Flake policy parameters

- `N_repeats` per trigger/discrimination case: ⟨choose⟩ (odd; 3 or 5 are
  common starting points).
- Quorum: PASS requires ≥ k of N (⟨choose⟩ k > N/2). Report wins/N, not
  just the verdict.
- Instability: a case oscillating across runs (quorum flips ≥ ⟨choose⟩
  times in a window) → QUARANTINED with a dated reason; quarantined cases
  appear in every report until resolved by a case fix or a trigger fix.
- Forbidden: auto-retry-until-green, auto-pruning failing cases, or
  excluding quarantined cases from the report. All three are result
  laundering.

## CI posture and promotion criteria

1. Attach as a NON-BLOCKING advisory lane; failures inform, never gate.
2. Promotion to required gate needs, at minimum: a stability record over
   ⟨choose⟩ consecutive scheduled runs (quarantine list flat or shrinking,
   judge-error rate under ⟨choose⟩%), a spend history within cap, and a
   recorded human decision.
3. The structural validator remains a required check regardless of
   promotion — the runner consumes what the validator proves parseable.

## Non-claims language (include verbatim in every design deliverable)

> No runner exists as of this design. No eval case has been executed. This
> document specifies how execution WOULD work; nothing in it is an eval
> result, and the library's eval convention remains structural-only until a
> built runner produces real, reported runs.
