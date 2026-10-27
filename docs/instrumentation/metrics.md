# Metrics and disclosure

The calculator answers one question honestly: **among prospectively
acknowledged, consenting starts, what happened by day 30?** It does not measure
population adoption, skill quality or causal effectiveness.

## Cohort and horizon

- One workflow is one owner-declared deliverable with an acceptance checklist
  frozen locally at start. A scope change creates a prospectively declared new
  workflow; it never deletes an unsuccessful start.
- A monthly **start cohort** groups workflows by `start_day` month.
- The outcome window is exactly **30 days**: only events effective on or before
  `start_day + 30` decide the day-30 state.
- The reporting lag is exactly **7 days**: a cohort closes on `start_day + 37`.
  A cell is reported only when the as-of day reaches its close day; open cohorts
  are counted separately.
- A workflow whose first receipt is later than `start_day + 7` is
  **retrospective** evidence and is excluded from the prospective rates.
- An event first received after the close day is **late**. It is stored and
  counted, but it cannot change the day-30 state: the rate uses events effective
  by day 30 **and** received by the close day.

## Denominator N

`N` is the number of eligible, centrally acknowledged prospective starts still
retained after withdrawal and expiry. Each workflow counts once. N is **not** a
clone count, a closeout count, an opt-in count or an invocation count. Start
events without an acknowledgement are invisible centrally; that gap is stated,
not hidden.

## Day-30 partition

Every retained start is assigned exactly one outcome, so `N = D + A + F + O + U`:

| Symbol | Outcome | Rule |
| --- | --- | --- |
| D | delivered | a terminal `delivered` event effective by day 30 |
| A | abandoned | a terminal `abandoned` event effective by day 30 |
| F | failed | a terminal `failed` event effective by day 30 |
| O | ongoing | an explicit `observation` with value `ongoing` effective exactly on day 30 |
| U | unknown | no terminal event and no day-30 observation |

A failure effective on day 31 is **not** a day-30 failure. A workflow observed
ongoing on day 30 and failed on day 31 is `O`, not `F`. A workflow with no
day-30 observation is `U`, even when it later reports a terminal outcome. Early
terminal outcomes need no repeated follow-up.

## Rates

Every rate is reported as a numerator and a denominator. A zero denominator is
**unavailable**, never `0` or a division error.

| Metric | Numerator / denominator |
| --- | --- |
| 30-day delivery | D / N — delivery, not quality |
| Stage reach | starts with that stage `complete` by day 30 / starts where the stage is applicable; not-applicable starts are reported separately, and unknown stays in the denominator |
| Follow-up coverage | (D + A + F + O) / N — known status, not all local starts |
| Unknown, ongoing, abandoned, failed share | U/N, O/N, A/N, F/N |
| Assessed acceptance (self-report) | delivered with `self_reported_pass` / delivered with a self-reported assessment by day 30 |
| Assessed acceptance (independent) | delivered with `independent_attested_pass` / delivered with an independent attestation by day 30 |
| Independently attested success | delivered **and** frozen criteria valid **and** `independent_attested_pass` by day 30 / N |

"Independently attested success" is **participant-reported independent
attestation**, not centrally verified success. Evidence stays local: only the
category, the frozen-criteria flag and the evidence category are exported. A
scope change during the window invalidates the frozen-criteria claim, so that
workflow cannot earn frozen-criteria success. A skill completion hint is not a
quality score and is not part of this dataset.

## What every report carries

The restricted report carries the as-of day, schema and capture tier, horizon
and lag, per-cohort numerator/denominator pairs, not-applicable counts, late
entry and late event counts, frozen-criteria invalidations, a non-linkable
withdrawal count, the quarantine count and the standing limitations. There is no
headline "Aegis success rate".

## Suppression

A suppressed **publishable rehearsal** view applies disclosure floors before
anything could be called public:

1. **Cohort floor** — a cohort with fewer than 20 retained starts is withheld
   entirely.
2. **Sparse outcome** — if any nonzero outcome count is below 5, the cohort is
   withheld; publishing the other cells plus N would let the withheld cell be
   recovered by subtraction.
3. **Complementary suppression** — if only one cohort in the report would
   publish, it is withheld too, so a previously published total cannot be used
   to difference a suppressed cohort.
4. **Stage cells** — a stage rate is published only when its denominator is at
   least 20 and its numerator is either 0 or at least 5; otherwise that stage
   cell is withheld.
5. **Differencing** — a cohort that passes the floors but differs from the most
   recent published cohort by 1–4 in any outcome count is withheld, because a
   small month-over-month shift can isolate one contributor.

These are disclosure controls, not anonymity guarantees. No public pilot metrics
are authorised; the publishable view always states `public_release: false` and
is a rehearsal only.
