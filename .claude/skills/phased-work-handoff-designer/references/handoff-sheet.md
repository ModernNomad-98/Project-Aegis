# Handoff Sheet

Detail for `phased-work-handoff-designer`. Read on demand.

## Handoff template (per stage)

```
## Stage <N> — <name>

### Decision register (carried forward)
| D-id | Decision | Made in | Still binding? | Superseded-by |
|------|----------|---------|----------------|---------------|
| D01  | Use keyset pagination | S1 | yes | — |
| D02  | tenant scope server-side | S1 | yes | — |

### Changed files
- <path> — <what/why>

### NOT touched (intentional)
- <path> — left alone because <reason>

### Proven invocation
$ <command>
<tell-tale output: counts / ids / timestamps / distinctive line>

### Deviations
- Departed from <plan/decision> because <rationale> — flagged.

### Open items → next stage
- <item> ; entry criteria for stage N+1
```

## Decision-ID register

- Every binding decision gets a stable ID + one-line statement.
- Carried across ALL stages.
- Each stage marks prior decisions still-binding; a change = a DEVIATION
  with `superseded-by`, never a silent edit.
- Prevents stage N contradicting stage 1.

## Proven-invocation pattern

Not: "tests pass".
Instead:
```
$ python scripts/validate-skills.py
OK: 148 skill(s) valid, 0 warning(s)
```
The tell-tale output (counts, IDs, the distinctive line) is the receipt
that the step actually ran. No receipt → flag the claim, don't carry it.

## NOT-touched list

- Explicitly lists what a stage deliberately left alone.
- Silence reads as "forgotten" and invites "helpful" cleanup that undoes
  restraint.
- The explicit list reads as "intentional" and must be honored downstream.

## Deviation flags

- Any departure from the plan or a prior decision is flagged with
  rationale, in-flight.
- Silent deviation compounds across stages into an untrustworthy effort.
- Visible deviation is correctable now.

## Continuation contract

What a fresh stage/agent needs to pick up COLD:
- Current decision register.
- Changed / not-touched state.
- Proven-invocation evidence so far.
- Open items + next stage entry criteria.

Goal: continue by READING the handoff, not by re-deriving the effort.
