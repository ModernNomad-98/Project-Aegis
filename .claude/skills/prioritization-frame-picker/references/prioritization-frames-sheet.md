# Prioritization Frames Sheet

Detail for `prioritization-frame-picker`. Read on demand.

## Framework selection guide

| Frame | Fits when | Inputs needed | Limits |
|---|---|---|---|
| RICE | Many comparable features; reach matters | Reach, Impact, Confidence, Effort | Precision illusion; buries strategic bets |
| WSJF / cost-of-delay | Timing/flow dominates | Cost of delay, job size | Cost-of-delay is hard to estimate |
| Value vs Effort / ICE | Fast, coarse first cut | Value, effort (+ confidence) | Too coarse for close calls |
| Kano | Classify satisfaction types | User research on features | Not a total order; classification only |
| Opportunity scoring | Find under-served needs | Importance vs satisfaction | Needs survey data |
| MoSCoW | Release scoping | Must/Should/Could/Won't judgment | Everything becomes "Must" without discipline |

Match to the decision. The wrong frame applied rigorously beats nothing —
but the right frame applied roughly beats the wrong frame applied
precisely.

## Input reliability discipline

- Mark each input **[evidence]** (real data) or **[guess]**.
- Use the confidence factor to DISCOUNT guess-heavy scores — that is its
  entire purpose. Confidence=100% on everything removes the honesty.
- Reach from analytics = evidence; reach from "feels big" = guess. Don't
  mix them silently.

## Refusing false rigor

- Score in **buckets** (S/M/L, or 1/3/5/8) not false decimals.
- The output order is only as precise as the softest input.
- Present ranges where inputs are uncertain, not point values.

## Sensitivity check

1. For each soft input, vary it across its plausible range (e.g. ±2×).
2. Re-rank. Note which pairs flip order.
3. If the top ranking is stable → trust it. If it flips on a guess →
   report "too close to call on current evidence", not a false order.

Robust rankings survive their inputs wobbling; fragile ones are noise in
a spreadsheet.

## Items outside the formula

| Category | Handling |
|---|---|
| Legal/compliance must-do | Protected lane above the value score |
| Security remediation (required) | Protected lane |
| Keep-the-lights-on / reliability | Protected lane or reserved capacity |
| Strategic bet (scores low, matters) | Flag for human judgment above the number |
| Genuinely incomparable | Separate; don't force a common unit |

The frame informs; it does not overrule required or strategic work.

## Handoff

The ranked, assumption-explicit list goes to
`roadmap-under-uncertainty-planner` for sequencing over horizons with
dependencies, capacity, and re-planning.
