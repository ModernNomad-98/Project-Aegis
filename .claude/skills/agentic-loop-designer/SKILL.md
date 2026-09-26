---
name: agentic-loop-designer
description: Design an agentic loop's shape and bounds — decide explicitly whether a loop is needed; clamp iteration ceilings; classify failures before retrying; stop on policy denials and permanent errors; retry a transient failure at most once on identical input only when the operation is safe to repeat; distinguish retry exhaustion and unknown outcomes from proven permanent failures; report empty results honestly. Consumes cost caps from ai-cost-guardrail-designer, gives recovery checkpoints to agent-failure-recovery, and runs inside agent-harness-architect's harness. Use for loop design, retry and stop behavior, unbounded loops, or fabricated results. Manipulation attack review belongs to agent-goal-hijack-defender and ai-threat-modeler.
---

# Agentic Loop Designer

**Terms used here:** A *transient failure* is an event such as a timeout or
temporary service error that may clear without changing the request. A
*permanent failure* has evidence such as a validation error that the same
request cannot succeed. An *idempotent operation* can be repeated without
adding another external effect. A *reproducibility key* identifies the exact
input bytes; it does not prove that external state stayed the same or that a
side effect occurred only once.

## Purpose

A loop needs an honest way to stop, including the honest empty set. This
skill designs the shape and bounds of an agentic loop — or establishes that
no loop is needed. The deliverable is a loop design with five load-bearing
parts: (1) the single-shot-vs-agentic decision made EXPLICITLY up front,
with the reasons recorded — a loop is a cost and a risk you take on purpose,
not a default; (2) clamped iteration ceilings that cannot be exceeded; (3)
TYPED retryability — every failure is classified before any retry: policy
rejections and evidenced permanent errors stop immediately; a transient
failure may be retried at most once on identical input only when repeating
the operation is safe, within the budget, and allowed by any retry delay.
Success after retry shows an intermittent outcome; a second transient failure
exhausts the retry without establishing its cause. An uncertain side effect
stops unless idempotency is proven. A reproducibility key records the exact
input, but cannot prove external state or deduplication; (4) honest terminal
states — success, policy-stop, deterministic-failure, retry-exhausted,
unknown-outcome, ceiling/budget-stop, and the honest
empty set: an empty result is a legitimate stop, never forced into
fabricated output; and (5) a plan → act → observe → reflect structure with
the stop check run every iteration. This skill DESIGNS the loop; the
security review of loop manipulation — hijacked goals, adversarial threat
paths — belongs to `agent-goal-hijack-defender` and `ai-threat-modeler`. It
PRODUCES the artifact those skills review.

## Use When

- Use when: deciding whether a task needs an agentic loop at all — the
  single-shot-vs-agentic call, made before any loop is built.
- Use when: designing or overhauling a loop's structure — iterations,
  retries, stop conditions, terminal states — for an agent that plans and
  acts over multiple steps.
- Use when: an agent loops unbounded, retries policy rejections, re-rolls
  failures with tweaked prompts until something passes, or pads an empty
  result into invented output.
- Use when: retry behavior needs to distinguish a typed permanent failure,
  an intermittent success, retry exhaustion, and an unknown side effect.
- Auto-invocable: a pure design skill — it produces a loop specification and
  changes no live system.
- Do NOT use when: the job is the ATTACK REVIEW of the loop — can injected
  content redirect the agent's goal or plan — that is
  `agent-goal-hijack-defender`, with `ai-threat-modeler` for the broader
  adversarial threat map. This skill DESIGNS the loop; the security review
  of it belongs to those skills.
- Do NOT use when: the question is the BUDGET — token caps, spend limits,
  loop/recursion cost bounds as policy — that is `ai-cost-guardrail-designer`;
  its caps are an INPUT this design consumes, and this skill owns the loop's
  semantics and stopping, not its price.
- Do NOT use when: a run has already broken the working state (dirty tree,
  interrupted operation, partial commit) — recovery is
  `agent-failure-recovery`; this skill designs the loop structure
  (checkpoints, typed failures, resumable state) that recovery plugs into.
- Do NOT use when: the subject is the operating environment's gating —
  mediation point, pre-flight ladder, registry, instruction custody — that
  is `agent-harness-architect`; the loop this skill designs runs INSIDE that
  harness, and every iteration's calls still pass its ladder.
- Do NOT use when: designing multi-agent containment — cascade isolation,
  drift baselines, kill switches across a fleet — that is
  `agent-containment-reviewer`'s review lane; this skill designs ONE loop's
  internal semantics.

## Inputs to Inspect

1. The task itself: is the output reachable by a fixed pipeline
   (deterministic steps, no observation-dependent branching), or does the
   next step genuinely depend on what the last step observed? This decides
   single-shot vs agentic.
2. The current loop, if one exists: its iteration behavior, what it retries,
   how it stops today, and any history of runaway runs or fabricated
   endings.
3. The failure surface: which step failures are policy rejections, which
   are transient (network, rate limit, timeout), which are evidenced
   permanent failures, and which have an uncertain side effect; determine
   whether the code can tell them apart and whether a retry is safe.
4. The caps in force (`ai-cost-guardrail-designer` output if present):
   iteration/cost/recursion bounds the loop must respect as inputs.
5. The harness context (`agent-harness-architect` output if present): the
   ladder each iteration's calls pass, and what a mid-loop policy denial
   looks like to the loop.
6. What downstream consumes the terminal state: does the caller distinguish
   "empty result" from "failure" from "gave up at ceiling" — or does
   everything collapse into one shape that invites padding?

## Workflow

1. **Make the single-shot-vs-agentic decision explicitly.** If a fixed
   pipeline reaches the output, design that instead — a summarization, a
   transformation, a lookup does not need a loop. Record the decision and
   its reasons. A loop entered by default is an unbounded liability entered
   silently. If a genuine owner choice remains, explain that a fixed
   pipeline follows known steps while an agentic loop chooses later steps
   from observed results. Compare only viable paths: why each fits, what
   adaptability it gains or loses, failure and control risks, and estimated
   calls, latency, setup, upkeep, and money cost or explicit unknowns under
   the existing caps. Recommend the case-fit path with a reason and the
   missing fact that could change it, then ask one decision question. Do
   not ask merely to confirm a design disposition already settled by
   observation-dependence; pricing policy stays with
   `ai-cost-guardrail-designer`.
2. **Structure the loop: plan → act → observe → reflect.** Each iteration
   plans the next step, acts, observes the real outcome (not the intended
   one), and reflects against the goal. The stop check runs EVERY iteration
   — not only on success.
3. **Clamp the iterations.** A hard ceiling the loop cannot exceed,
   consuming the bounds `ai-cost-guardrail-designer` prices. Hitting the
   ceiling is a named terminal state that reports honestly ("stopped at
   ceiling with partial result X"), never a silent truncation dressed as
   completion.
4. **Type the retryability.** Classify EVERY failure before any retry:
   - **Policy rejection → TERMINAL.** A denial from the harness ladder, an
     authorization failure, a refused action is never retried — retrying a
     policy stop is an attempt to wear the gate down, and each attempt burns
     budget probing a boundary that will not move.
   - **Evidenced permanent failure → TERMINAL.** A validation error that
     cannot succeed on the same request needs no retry. Surface the evidence.
   - **Transient failure → at most ONE retry on IDENTICAL input.** First
     establish that the prior effect is known absent, or that safe or
     idempotent repetition is proven despite an uncertain response. Meet
     any required retry delay, and ensure the retry fits
     the iteration and cost ceilings. A successful retry is an observed
     intermittent success. A second timeout or temporary service error is
     `retry-exhausted`: stop and report that the cause is unresolved. Do not
     call repeated transient failures deterministic. The **reproducibility
     key** (hash of the exact input) verifies the input bytes only; a changed
     prompt is a new attempt, not a retry. The key does not prove unchanged
     external state or deduplicate effects.
   - **Uncertain side effect → unknown-outcome.** If an operation may have
     acted before timing out, stop without retrying unless idempotency and
     safe repetition are established. Report the uncertainty to the caller.
5. **Define the honest terminal states.** Enumerate them: success;
   policy-stop; deterministic-failure; retry-exhausted (cause unresolved);
   unknown-outcome; ceiling/budget-stop; and the honest
   EMPTY SET — "nothing matched" is a legitimate, first-class answer. The
   loop never pads, invents, or force-fills an empty result into output
   that looks like success. Downstream must be able to distinguish every
   terminal state.
6. **Design the checkpoint/resume sockets.** Persist enough state per
   iteration that a broken run can be diagnosed and resumed —
   `agent-failure-recovery` handles the recovery; this design gives it
   something to recover.
7. **Prove the stops can fire.** Design the tests: the ceiling actually
   halts a run; a policy rejection and an evidenced permanent failure are
   demonstrably not retried; a safe transient succeeds
   after one retry or reaches retry-exhausted after a second transient; an
   uncertain side effect stops without idempotency proof; changed input is
   a new attempt; and the empty set reaches the caller as empty. A verifier
   that cannot fail is theater with an exit code — a stop
   condition that has never fired in a test is an unbounded loop you
   haven't met yet.
8. **Deliver the design** in the Output Format, seams cited: budget, the
   harness, recovery, and the attack review — composed, never restated.

## Output Format

```
AGENTIC LOOP DESIGN — <task/agent>
Decision: <single-shot | agentic | owner decision pending> — <reasons;
  what observation-dependence justifies the loop, why a fixed pipeline
  suffices, or which fact/choice remains open>
Owner choice brief (only if genuinely unresolved): <plain terms; viable
  paths and reasons; adaptability and risk pros/cons; calls/latency,
  setup/upkeep and money costs or unknowns; recommendation and why;
  one decision question>
Structure: plan → act → observe → reflect; stop check every iteration
Ceilings: <hard iteration cap; per-iteration and total bounds consumed from
  ai-cost-guardrail-designer>
Retryability (typed):
  policy rejection → TERMINAL, never retried
  evidenced permanent error → TERMINAL, no retry
  transient → at most ONE retry on identical input only if safe/idempotent,
    within ceilings, and after any required delay (input hash: <hash>);
    success=intermittent success; second transient=retry-exhausted, cause
    unresolved
  uncertain side effect → unknown-outcome unless safe repetition is proven
Terminal states: <success | policy-stop | deterministic-failure |
  retry-exhausted | unknown-outcome | ceiling/budget-stop | HONEST EMPTY SET>
  — each distinguishable downstream;
  empty is never padded into output
Checkpoints/resume: <per-iteration persisted state; what
  agent-failure-recovery can plug into>
Stop proofs: <ceiling-fires; policy and permanent errors not retried;
  safe transient succeeds or exhausts one retry; changed input is a new
  attempt; uncertain side effect stops without idempotency; empty reaches caller>
Handoffs: budget/caps → ai-cost-guardrail-designer; call gating →
  agent-harness-architect; broken-state recovery → agent-failure-recovery;
  attack review → agent-goal-hijack-defender + ai-threat-modeler
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] The single-shot-vs-agentic disposition is explicit and recorded,
      including a genuinely pending owner choice; a loop exists because
      observation-dependence requires it, not by default.
- [ ] If an owner must choose, the brief teaches terms, reasons,
      benefits/drawbacks, costs or unknowns, and a reasoned recommendation
      before one question; routine design dispositions do not force a vote.
- [ ] The loop is plan → act → observe → reflect with the stop check every
      iteration.
- [ ] A hard iteration ceiling exists, consumes the priced caps, and
      hitting it is an honest named terminal state.
- [ ] Every failure is typed before any retry; policy rejections are
      TERMINAL and demonstrably never retried.
- [ ] A transient retry occurs at most once on identical input only when
      repetition is safe, ceilings allow it, and any required delay is met.
      A second transient is retry-exhausted, with cause unresolved.
- [ ] Evidenced permanent errors stop without retry; uncertain side effects
      stop unless idempotency and safe repetition are established. The input
      hash is not treated as proof of external state or deduplication.
- [ ] The terminal states are enumerated and downstream-distinguishable,
      including the honest empty set; nothing pads empty into output.
- [ ] Per-iteration checkpoints give `agent-failure-recovery` a socket.
- [ ] Every stop has a designed proof it can fire — ceiling, policy-stop,
      retry exhaustion, uncertain side effects, and empty-set delivery have
      must-fail/must-fire
      tests.
- [ ] The yields are stated: manipulation attack review →
      agent-goal-hijack-defender + ai-threat-modeler; seams cited, not
      restated.

## Gotchas

- "Make it agentic" is a cost decision disguised as an architecture
  decision: a loop buys adaptability with unboundedness, and most
  transformations don't need the purchase. The explicit up-front decision
  is the cheapest control in this skill.
- Retrying a policy rejection is not resilience — it is probing a gate.
  The commonest form: catching ALL exceptions in one handler and retrying,
  which silently converts denials into retry storms.
- A retry with a tweaked prompt is a new attempt. Identical input makes the
  outcomes comparable, but repeating a timeout does not prove its cause.
  An input hash does not establish what happened in an external service.
- A timeout after a side effect may leave the outcome unknown. Do not repeat
  that operation without evidence that repetition is safe and idempotent.
- The empty set is where fabrication pressure concentrates: a loop that
  "must return something" will eventually return something false. Empty
  reaching the caller as empty is a feature the design must defend, not a
  user experience (UX) bug to paper over.
- A ceiling that only lives in a prompt ("stop after 10 tries") is not a
  ceiling — the clamp must be enforced by the code that runs the loop, not
  requested of the model inside it.
- Terminal states that collapse into one shape ("done") invite the padding
  they were meant to prevent: if the caller cannot tell ceiling-stop from
  success, the loop will be pressured to make them look alike.
- A stop condition that has never fired in a test may be unreachable in
  the code path that matters — theater with an exit code. Fire each one
  deliberately before trusting it.

## Stop Conditions

- The request is to force output on the empty set — "never return nothing,
  generate something plausible" → refuse; an empty result is a legitimate
  terminal state, and fabricating past it is the exact failure this design
  exists to prevent. Escalate if the requirement survives.
- The request is to retry policy rejections until they pass → refuse;
  policy stops are terminal by design, and automated gate-probing is not a
  loop feature this skill will design.
- The failure surface cannot be typed — the system cannot distinguish a
  policy denial from a transient error, a permanent error, or an uncertain
  side effect → fix the error taxonomy first (`error-taxonomy-designer` for the model, the
  harness for denial signaling); typed retryability over untyped failures
  is guesswork.
- No iteration/cost caps exist to consume → obtain them from
  `ai-cost-guardrail-designer` (or a human names the bound); a loop
  designed without a ceiling input is a loop with a default ceiling of
  infinity.
- Wiring the designed loop into a live agent → implementation under the
  repo's approval path; this skill designs, it does not deploy.
- The real concern is goal hijack, adversarial manipulation, or the threat
  map → hand to `agent-goal-hijack-defender` / `ai-threat-modeler` and
  stop.

## Supporting Files

- `evals/evals.json` — behavior cases: the research-loop design, the
  loop-by-default challenge, the retry-typing edge, the fabricate-on-empty
  refusal, and the hijack-review should-not-trigger.
- `evals/trigger-evals.json` — discrimination against
  `ai-cost-guardrail-designer` (budget authoring vs consumption),
  `agent-failure-recovery` (broken-state recovery vs loop structure),
  `agent-harness-architect` (in-batch: call gating vs loop semantics),
  `agent-containment-reviewer` (multi-agent containment review vs one
  loop's design), and the design-vs-review seam against
  `agent-goal-hijack-defender` / `ai-threat-modeler`.
- No `references/` — the loop contract above is the complete procedure;
  detail lives in the produced design artifact.
