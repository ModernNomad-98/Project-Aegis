# A/B Test Sheet

Use this [A/B Test Designer reference](../SKILL.md) to choose and record experiment sample-size and analysis inputs. Here α is the false-positive threshold, β the false-negative probability, n the sample size, a conversion proportion is a rate, a p-value is the probability measure used in a significance comparison, CI is a confidence interval, and SUTVA is the assumption that one unit's assignment does not alter another unit's outcome.

Detail for `ab-test-designer`. Read on demand.

## Power / sample-size inputs

To compute required sample size you need:
- **Baseline rate** (or mean + variance) of the primary metric.
- **Minimum detectable effect (MDE):** the smallest lift worth acting on
  — chosen for PRACTICAL relevance, not "smallest detectable".
- **Significance level (α):** typically 0.05.
- **Power (1−β):** typically 0.80–0.90.

Smaller MDE → much larger n. Then derive DURATION = required n ÷ eligible
traffic per period, rounded UP to whole weekly cycles. If duration is
infeasible, the test can't answer the question — say so.

## Peeking inflation

Fixed-horizon tests assume ONE analysis at the end. Checking repeatedly
and stopping at the first p<0.05 inflates the false-positive rate well
beyond 5%; the amount depends on the number and timing of looks and the
decision rule. Options:
- Fix the horizon; analyze once at the end. (simplest)
- Use a sequential / always-valid method (group-sequential, alpha
  spending, Bayesian) declared IN ADVANCE with its correction.
Never "we'll just keep an eye on it and call it when it's significant".

## Multiple comparisons

Testing many metrics/segments inflates false positives: under independent
null tests at p<0.05, about one in twenty would pass by chance in expectation,
not with certainty.
- Pre-register ONE primary metric; others are guardrails or exploratory.
- If multiple primary comparisons are unavoidable, preselect a correction
  matching the decision: Bonferroni controls family-wise error; Benjamini–
  Hochberg controls the expected false discovery rate across discoveries.
- Post-hoc segment "wins" are hypotheses to confirm, not results.

## Validity checks (run before trusting a result)

| Check | What it catches |
|---|---|
| Sample ratio mismatch (SRM) | Test observed allocation against the planned split and sample size; a significant mismatch triggers assignment/exposure/logging investigation before outcome inference |
| Simpson's paradox | Aggregate reverses within segments as segment sizes shift |
| Novelty / primacy | Early behavior ≠ steady state; needs enough time |
| Guardrail regressions | A "win" that tanks revenue/latency/retention is not a win |
| Practical vs statistical | Significant but tiny lift may be worthless at large n |

## Reading a result

- Report **effect size + confidence interval**, not a bare p-value.
- "Not significant" is inconclusive unless the confidence interval rules out
  effects at or above the prespecified practical threshold; it is not proof
  of no effect.
  A wide CI around zero = "we don't know".
- Judge the effect against the MDE you set for a reason.
- Decision: ship / kill / iterate, stating the effect, its interval,
  guardrail status, and residual uncertainty.

## Assignment integrity

- Sticky by a stable id; consistent across sessions/surfaces.
- Watch contamination: shared accounts, network/marketplace spillover
  (treatment leaks to control) violate independence (SUTVA).
- The experiment may ride a flag from `feature-flag-rollout-strategist`,
  but its statistics live here.
