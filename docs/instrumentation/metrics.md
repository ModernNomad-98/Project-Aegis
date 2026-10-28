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
  are counted separately. A month that still has an open start is withheld from
  the publishable view (`cohort_open`), because its recorded cohort would hold
  only the early starts and its denominator would grow later.
- A workflow whose first receipt is later than `start_day + 7` is
  **retrospective** evidence and is excluded from the prospective rates.
- An event first received after the close day is **late**, whatever its
  effective day. It is stored and counted, but it cannot change the day-30
  state: the rate uses events effective by day 30 **and** received by the close
  day. `late_entries` counts late higher-revision receipts; `late_events` counts
  events whose first receipt was after the close day.
- One value per event kind (and per stage, for stage events) per effective day
  is allowed. A same-day conflicting value is rejected for correction by both
  the recorder and the importer; it is never resolved by guessing which random
  event reference came last.

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
| Stage reach | starts whose latest stage event effective by day 30 has that stage `complete` / starts where the stage is applicable; not-applicable starts are reported separately, and unknown stays in the denominator |
| Follow-up coverage | (D + A + F + O) / N — known status, not all local starts |
| Unknown, ongoing, abandoned, failed share | U/N, O/N, A/N, F/N |
| Assessed acceptance (self-report) | delivered with `self_reported_pass` / delivered with a self-reported assessment by day 30 |
| Assessed acceptance (independent) | delivered with `independent_attested_pass` / delivered with an independent attestation by day 30 |
| Independently attested success | delivered **and** frozen criteria valid **and** `independent_attested_pass` by day 30 / N |

"Independently attested success" is **participant-reported independent
attestation**, not centrally verified success. Evidence content stays local:
only the acceptance status, the frozen-criteria flag and the participant-supplied
evidence category are exported. The category defaults to `none`; an independent
attestation requires a non-`none` category, and a self-reported assessment with
no record exports `none`. The exported category belongs to the acceptance
transition that wins by effective day, not to the last one recorded. A scope
change during the window invalidates the frozen-criteria claim, so that workflow
cannot earn frozen-criteria success; `frozen_criteria_invalidated` counts only
workflows that actually claimed frozen criteria and then changed scope. A skill
completion hint is not a quality score and is not part of this dataset.

## What every report carries

The restricted report carries the as-of day, schema and capture tier, horizon
and lag, per-cohort numerator/denominator pairs, not-applicable counts, late
entry and late event counts, frozen-criteria invalidations, a non-linkable
withdrawal count, the quarantine count and the standing limitations. A cohort
with an observed expired record is marked `incomplete` with that month's
`expired_excluded` count; a month with no retained cohort but an observed expired
record is listed in `incomplete_cohorts`. After housekeeping deletes the record,
a non-linkable per-month count keeps that month `incomplete` (and keeps its
exclusion counted), so deleting the raw record cannot make a partial month look
complete. If the retained store exceeds the 5,000-record cap the report sets
`truncated` and the publishable view refuses to compute at all. There is no
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
6. **Open month** — a month with any start still inside the 37-day window is
   withheld with reason `cohort_open`, because its cohort cell holds only the
   starts that already closed.
7. **Sparse attestation** — `independently_attested_success` is published only
   when its numerator is 0 or at least 5; a nonzero numerator below the cell
   floor is withheld with reason `sparse_attestation_cell`.
8. **Truncation** — a report computed from a capped store is never publishable;
   the view refuses with `report_truncated` instead of showing partial
   denominators.
9. **Late cells** — `late_entries` and `late_events` are published only when
   zero or at least 5; a nonzero count below the cell floor is withheld with
   reason `sparse_late_cell`.

A cohort marked `incomplete` is withheld from the publishable view with reason
`retention_incomplete` before the other floors apply; a month with no retained
cohort but an observed expired record is listed in `suppressed_cohorts` with
the same reason. These are disclosure
controls, not anonymity guarantees. No public pilot metrics are authorised; the
publishable view always states `public_release: false` and is a rehearsal only.
SCIF completion is not acceptance evidence and never by itself qualifies a
workflow as independently attested success.
