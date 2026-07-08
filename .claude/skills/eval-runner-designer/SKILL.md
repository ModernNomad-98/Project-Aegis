---
name: eval-runner-designer
description: Design how a skill library's evals would actually EXECUTE — the runner left open where the eval convention is structural-only (files exist and parse; nothing runs). Covers harness architecture (fresh, isolated session per case with the library loaded), trigger verification (the expected skill fires; should_not_trigger neighbors stay silent), assertion judging (deterministic checks vs rubric-guided LLM judge), refusal-case semantics, reporting with honest UNRUN status, cost and sampling tiers, flake policy for stochastic triggering, and advisory-first CI wiring. Design/spec ONLY — it never claims a runner exists, never reports evals as "passing" without one, and builds or runs nothing. Use when asked how skill evals would run, execute, or score, or to close a structural-only eval gap. Do NOT use to judge whether eval CASES are real or hollow (skill-quality-reviewer), to evaluate an AI feature's behavior (ai-evaluation-harness), or for product test automation (qa-automation-architect).
---

# Eval Runner Designer

## Purpose

Turn "evals exist" into "evals could be executed" — by design, honestly. A
library whose eval convention is structural-only (the validator proves the
files are present and parse; decision D3 in this repo) carries a standing
gap: nothing ever exercises the cases, so no one may claim they pass. This
skill closes the DESIGN half of that gap: a complete, buildable
specification of the runner — execution semantics per case type, judging,
reporting, cost, flake policy, CI posture — while keeping the honesty rule
intact: until a runner is built and run, eval results do not exist, and this
skill never implies otherwise.

## Use When

- Use when: asked how the library's skill evals would actually be run,
  executed, scored, or verified — "design the eval runner", "how would these
  evals.json cases be exercised?"
- Use when: the eval convention is being upgraded from structural-only and
  the execution approach needs a spec before anyone builds.
- Use when: asked what it would cost, or how flaky it would be, to exercise
  the eval corpus against a live model.
- Do NOT use when: the question is whether a skill's eval CASES are real
  boundary tests or hollow filler — that is `skill-quality-reviewer`
  (check 4, eval integrity, judged structurally from the case text). This
  skill designs how cases EXECUTE; it takes their content as given.
- Do NOT use when: designing evals for an AI product feature — regression
  suites, red-team cases, or quality metrics for an LLM system — that is
  `ai-evaluation-harness`. This skill's subject is the library's own
  skill-trigger and skill-behavior evals.
- Do NOT use when: designing product test automation (unit/integration/E2E
  strategy, CI test pyramids) — that is `qa-automation-architect`.
- Do NOT use when: the question is which skills fire in REAL sessions —
  field usage signal, not deliberate exercise — that is
  `skill-usage-instrumenter`.

## Inputs to Inspect

1. The library's eval convention as written: the generation standard's evals
   section and the decision that made evals structural-only (here,
   `docs/skill-generation-standard.md` §6 and decision D3).
2. The actual shape of the corpus: `evals/evals.json` and
   `evals/trigger-evals.json` across shipped skills — case types in use
   (`should_trigger`, `should_not_trigger`, refusal cases typed as
   `should_trigger` with `triggers: true` per this library's convention),
   assertion styles, and the trigger-evals fields (`expected_skill`,
   `should_not_trigger`, `overlaps_with`).
3. How the host actually invokes skills: trigger-on-description matching,
   explicit invocation, and whatever session/context mechanics govern which
   skills are visible — the runner must reproduce the REAL selection
   surface, not a simplified one.
4. The mechanical validator (`scripts/validate-skills.py`) — the structural
   floor the runner extends and must never silently replace.
5. Cost constraints and CI topology: what budget a full-corpus run may
   spend, and where an advisory lane could attach.

## Workflow

1. **Inventory the corpus shape.** Census case types, assertion styles, and
   trigger-evals discrimination fields actually in use across the library.
   The runner is designed for the corpus as written — divergences (custom
   case types, unjudgeable assertions) are recorded as findings for authors,
   not silently normalized.
2. **Define execution semantics per case type.**
   - `should_trigger` / `triggers: true`: present the prompt to a fresh
     session with the full library loaded; PASS requires the target skill to
     activate. Refusal cases additionally require the response to refuse per
     the assertions (fire AND refuse).
   - `should_not_trigger` / `triggers: false`: the named skill must NOT
     activate; record what fired instead (routing insight, not a failure by
     itself).
   - Trigger-evals discrimination cases: `expected_skill` must win AND every
     skill in `should_not_trigger` must stay silent — scored pairwise so a
     partial win is visible.
   - Isolation rule: one case per fresh session; no case may inherit context
     from a previous one.
3. **Split assertion judging into two classes.** Deterministic (skill fired
   / did not fire; output contains the skill's required report block) —
   scripted checks. Semantic (the response "refuses the shortcut", "names
   the colliding skill") — a rubric-guided LLM judge, with the rubric
   derived from the assertion text, a judge independent of the session under
   test, and judge errors reported as JUDGE-ERROR, never converted into
   case failures or passes.
4. **Design the report.** Per-case PASS / FAIL / ERROR / UNRUN; per-skill
   rollup; corpus health metrics (trigger accuracy, discrimination wins,
   refusal compliance). UNRUN is the default state of every case — the
   report shape itself preserves the no-runner-yet honesty.
5. **Model cost and sampling tiers.** Full-corpus cost ≈ cases × repeats ×
   (session + judge) calls. Define tiers: changed-skills-only on a PR,
   sampled cross-section on cadence, full corpus rarely — plus a spend cap
   and kill switch (compose `ai-cost-guardrail-designer` for budget
   guardrails if the runner is adopted).
6. **Set the flake policy.** Trigger matching is stochastic: single-shot
   results overclaim in both directions. Specify N repeats per trigger case,
   a quorum pass rule (e.g. must win k of N), a quarantine list for
   persistently unstable cases, and the rule that quarantine is visible in
   the report, never a silent skip.
7. **Fix the CI posture: advisory first.** The runner attaches as a
   non-blocking lane; promotion to a required gate needs a stated stability
   record and a human decision. The structural validator remains the
   required floor throughout — the runner extends it, never replaces it.
8. **Deliver the design** in the Output Format, with open decisions listed
   and the non-claims section stating plainly: no runner exists as of this
   design; nothing here is an eval result.

Execution-semantics tables, the judging decision table, report schema,
sampling-tier math, and flake-policy parameters:
[references/runner-design-blueprint.md](references/runner-design-blueprint.md).

## Output Format

```
EVAL RUNNER DESIGN — <library / repo>
Corpus:         <N skills, M evals.json cases, K trigger-evals cases; case types found>
Convention:     structural-only today (<where that is recorded>); this design changes no convention
Execution:      <per case type: session setup, pass condition, isolation rule>
Judging:        <deterministic checks | LLM-judge rubric source, judge independence, JUDGE-ERROR handling>
Reporting:      <per-case states incl. UNRUN default; per-skill rollup; corpus metrics>
Cost & sampling:<full-run cost model; tiers (PR / cadence / full); spend cap + kill switch>
Flake policy:   <repeats N, quorum rule, quarantine visibility>
CI posture:     advisory lane first; promotion criteria: <stability record + human decision>; structural validator stays required
Open decisions: <judge model choice, repeat counts, budget owner, …>
Non-claims:     no runner exists as of this design; no eval has been executed; nothing above is a result
```

## Validation Checklist

- [ ] Every case type found in the actual corpus has defined execution
      semantics — including the refusal-as-should_trigger convention.
- [ ] The isolation rule (fresh session per case) is explicit.
- [ ] Every assertion class is routed: deterministic → scripted, semantic →
      judged; judge errors have their own state and never leak into
      pass/fail.
- [ ] The report design carries UNRUN as the default state.
- [ ] Cost model present with real arithmetic (cases × repeats × calls) and
      a spend cap.
- [ ] Flake policy specifies repeats, quorum, and visible quarantine.
- [ ] CI posture is advisory-first with stated promotion criteria; the
      structural validator is never replaced.
- [ ] The non-claims section is present verbatim in the deliverable.

## Gotchas

- Pass-claim leakage: design documents drift into result language ("the
  evals pass when…" reads as "the evals pass"). Every capability statement
  must stay conditional until a runner exists.
- Single-shot trigger tests: model routing is stochastic; one clean win
  proves little, one miss proves less. Repeats-with-quorum is the unit of
  evidence.
- Context leakage between cases: running cases sequentially in one session
  biases every case after the first — the previous skill load is context.
  Isolation is the most expensive and least negotiable rule.
- The judge judging itself: a judge from the same session (or sharing the
  session's context) inherits its biases. Independence means a separate
  call with only the transcript and the rubric.
- Assertions written for humans: many corpus assertions are qualitative
  prose. The design must classify which are mechanically judgeable, which
  need a rubric, and which are unjudgeable as written — that census is a
  deliverable, not a footnote.
- Cost blow-up by default: cases × repeats × judge calls grows fast;
  full-corpus-on-every-PR is usually unaffordable. Tiers are the design,
  not an optimization to add later.
- Replacing the floor: teams wiring a runner are tempted to drop the
  structural check as redundant. It is not — the runner depends on parseable
  eval files; the validator is what proves them.
- Designing for an imagined host: trigger evals only mean something if the
  runner reproduces the real skill-selection surface (all descriptions
  visible, real matching). A mock router tests the mock.

## Stop Conditions

- Asked to state or record that the library's evals PASS → refuse: no
  runner exists; a design is not execution. The structural-only convention
  stands until a built runner produces real results.
- Asked to BUILD the runner as part of this design → stop at the spec:
  implementation is a separate, separately-approved task (it adds code, CI
  lanes, and spend). Hand over the design and say so.
- Asked to weaken or remove the structural validator because "the runner
  will cover it" → refuse; the floor stays.
- The eval corpus is unreadable or its case-type conventions cannot be
  determined → stop; a runner designed against a guessed corpus shape will
  be wrong in exactly the cases that matter.
- Asked to design the runner so it always passes (retry until green, prune
  failing cases automatically) → refuse; that is result laundering, not
  flake policy.

## Supporting Files

- [references/runner-design-blueprint.md](references/runner-design-blueprint.md)
  — execution-semantics tables per case type, the judging decision table,
  report schema, sampling-tier arithmetic, flake-policy parameters, and CI
  promotion criteria.
- `evals/evals.json` — behavior cases including the budget-constrained
  sampling edge and the mark-them-passing refusal.
- `evals/trigger-evals.json` — discrimination against
  `skill-quality-reviewer` (case integrity vs execution design),
  `ai-evaluation-harness` (product-feature evals), `qa-automation-architect`
  (product test automation), and `skill-usage-instrumenter` (field usage vs
  deliberate exercise).
