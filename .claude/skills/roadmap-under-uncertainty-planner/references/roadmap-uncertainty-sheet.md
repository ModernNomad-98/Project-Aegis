# Roadmap Uncertainty Sheet

Detail for `roadmap-under-uncertainty-planner`. Read on demand.

## Horizon models

| Model | Horizons | Grain per horizon |
|---|---|---|
| Now / Next / Later | 3 buckets | Now = specific; Next = directional; Later = themes |
| Committed / Planned / Exploratory | by confidence | Committed = dated-range; Planned = quarter; Exploratory = intent |
| Time-boxed (this Q / next Q / H2+) | calendar | nearer = finer grain |

Pick one and state it so readers calibrate. Do NOT mix a dated bar chart
with "subject to change" — the chart wins the reader's belief.

## Confidence labeling

| Confidence | Precision allowed | Language |
|---|---|---|
| High (now) | date range OK | "shipping", "committed" |
| Medium (next) | quarter | "planned", "expected" |
| Low (later) | none — theme only | "exploring", "intend to" |

The failure mode is high precision + low confidence (an exact date on a
far-out idea). Match grain to certainty.

## Uncertainty-bet patterns (sequence to learn)

- **Spike / prototype:** a few days to test a technical assumption before
  committing a quarter to it.
- **Fake door / demand test:** measure interest before building.
- **Riskiest-assumption test:** name the assumption whose being wrong most
  changes the plan; test it first and cheaply.
- **Reversible vs irreversible:** make reversible bets fast; slow down for
  one-way doors.

Front-load the cheap tests that could invalidate expensive later work.

## Outcome-vs-feature reframing

| Feature-framed (brittle) | Outcome-framed (flexible) |
|---|---|
| "Ship A, B, C, D" | "Increase activation; A/B/C are current bets" |
| "Build the mobile app" | "Let users act on the go; mobile is one path" |
| Plan "fails" if A is dropped | Dropping a dead bet is normal; outcome stands |

Tie work to outcomes so a disproven hypothesis is dropped without the
plan "failing".

## Capacity discipline

- Never plan to 100%. Reserve slack for interrupts, bugs, discovery.
- Subtract existing maintenance/support/reliability load first (rarely 0).
- If ambition > capacity, show what moves to a later horizon — a visible
  trade-off, not silent compression.

## Re-planning

- State a cadence (e.g. monthly / per-cycle roadmap review).
- Name off-cadence triggers: a disproven assumption, a shifted priority,
  a slipped dependency, a market change.
- Communicate changes with the reason, so stakeholders see the plan as
  living, not broken.
