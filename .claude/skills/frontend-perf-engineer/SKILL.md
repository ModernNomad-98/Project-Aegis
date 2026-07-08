---
name: frontend-perf-engineer
description: Design the frontend's share of performance — metrics in the loading/interactivity/visual-stability family (largest-paint, interaction latency, layout shift) pinned to a device/network class, bundle strategy (route code splitting, lazy loading, weight audit BEFORE micro-tuning — deletions first), asset strategy (image priority, fonts without invisible-text or reflow), rendering path (SSR/hydration cost honestly counted, long tasks), runtime fixes (re-render storms, unvirtualized lists, layout thrash), perceived performance for the residue, and regression budgets (bundle-size and metric budgets as CI gates). DESIGNS the optimization; measurement is performance-test-harness, build correctness vite-build-qa-engineer, shared response caching caching-strategy-designer. Use when pages load or interact slowly, bundles bloat, or frontend perf needs budgets. Do NOT use for functional E2E (playwright-e2e-engineer) or the end-to-end split (latency-budget-architect).
---

# Frontend Perf Engineer

## Purpose

The backend answers in 80ms and the user waits four seconds: a
two-megabyte bundle parses on a mid-range phone, a hero image loads at
full priority behind three fonts, hydration re-runs the app before the
first click lands, and every keystroke re-renders a table nobody
virtualized. This skill designs the frontend's performance work — the
metric model users actually feel (loading, interactivity, visual
stability), the bundle and asset strategy that dominates load time, the
rendering-path and runtime fixes that dominate interaction time, and
the budgets that keep both from regressing one dependency at a time.
It designs against evidence and hands measurement to the harness; the
heaviest frontend fix is usually deletion, and this skill is not shy
about prescribing it.

## Use When

- Use when: pages load slowly, interactions lag, or layout jumps — the
  user-perceived frontend symptoms, with or without prior attribution.
- Use when: the bundle has bloated (or nobody knows its weight) and a
  dependency/code-splitting strategy is needed.
- Use when: SSR/hydration cost, font/image loading, or main-thread
  work needs a rendering-path design.
- Use when: frontend performance needs BUDGETS — bundle-size and
  metric budgets wired as CI gates — so regressions fail a check
  instead of shipping.
- Use when: `latency-budget-architect` allocated the frontend a share
  of a user-perceived budget and that share needs an engineering plan.
- Do NOT use when: the slowness is API/service-side — the end-to-end
  split is `latency-budget-architect`'s table; server hops route to
  their owning skills. This skill owns the browser's share.
- Do NOT use when: building the MEASUREMENT harness (lab runs,
  percentile baselines, regression gates' mechanics) — that is
  `performance-test-harness`; this skill defines what to measure and
  the budget values, the harness owns how measurement runs.
- Do NOT use when: the build output is functionally broken (wrong
  chunks, missing assets, env-specific build failures) —
  `vite-build-qa-engineer` owns build correctness QA; this skill
  changes bundle SHAPE for speed, and composes that skill to keep the
  reshaped build verified.
- Do NOT use when: designing shared HTTP/data caching for API
  responses — `caching-strategy-designer`; this skill's caching scope
  is the browser asset path (immutable hashed assets, service-worker
  strategies).
- Do NOT use when: writing functional browser tests —
  `playwright-e2e-engineer`.

## Inputs to Inspect

1. Field or lab evidence of the symptom: loading/interactivity/
   stability metrics where collected, or a first lab capture (trace,
   waterfall, main-thread flame) — plus WHICH pages/routes and which
   device/network class the complaint lives on.
2. The bundle inventory: total and per-route weights, the dependency
   graph's heaviest nodes, duplicate/near-duplicate libraries,
   dead-weight candidates (unused exports, polyfills for retired
   targets).
3. The rendering architecture: SSR/SSG/CSR/hydration model, what
   blocks first render (synchronous scripts, blocking styles, font
   strategy), and the framework's re-render semantics.
4. Asset reality: image formats/dimensions vs display size, font
   files and their loading behavior, priority/preload usage.
5. Runtime behavior on the slow paths: long tasks, re-render counts
   on interaction, list sizes rendered without virtualization,
   layout-thrash patterns (read-write interleaving).
6. The build setup and CI: where bundle analysis can run, where
   budgets can gate (composing `vite-build-qa-engineer`'s build-QA
   surface and `performance-test-harness` gates), and the deploy
   cadence budgets must survive.

## Workflow

1. **Pin the symptom to a metric and a device class.** Loading
   (largest-content paint class), interactivity (interaction-latency
   class), or stability (layout-shift class) — measured on the
   COMPLAINT's device/network profile, not the development laptop.
   A 4-second load on a mid-range phone over throttled mobile network
   is the number; the M-series laptop's 800ms is not evidence of
   health.
2. **Audit weight before tuning anything.** The bundle inventory
   ranked by cost: heaviest dependencies (and their lighter or
   built-in replacements), duplicates, dead weight. Deletion and
   replacement beat micro-optimization by an order of magnitude —
   the design says what LEAVES before what gets clever.
3. **Design the splitting strategy.** Route-level splits as the
   floor; below-the-fold and interaction-gated lazy loading
   (modals, editors, charts load when summoned); vendor chunking
   for cache stability; prefetch on intent (hover/viewport) for the
   likely next route. Named anti-goal: a waterfall of tiny chunks —
   splitting has a floor too.
4. **Design the asset strategy.** Images: modern formats with
   fallbacks, sized to display dimensions, lazy below the fold,
   priority hints for the hero. Fonts: subset, preload the critical
   face, swap policy chosen against invisible-text vs reflow (pick
   one, on purpose, per brand tolerance). Asset caching: immutable
   hashed filenames with long-lived headers (this skill's caching
   scope — shared API/data caching stays with
   `caching-strategy-designer`).
5. **Engineer the critical rendering path.** What must exist for
   first meaningful render, in order; everything else deferred.
   SSR/hydration counted honestly: server render helps first paint
   and BILLS interactivity through hydration cost — partial/lazy
   hydration or islands where the framework offers them, and the
   trade stated where it doesn't. Third-party scripts (analytics,
   widgets) moved off the critical path with async/defer/worker
   strategies — they are the classic uncounted tax.
6. **Fix runtime patterns.** Re-render storms (state placed too
   high, missing memoization at proven hot spots, context fan-out)
   — evidenced by render counts, not vibes; virtualization for long
   lists; layout-thrash de-interleaving (batch reads, then writes);
   main-thread long tasks split or moved to workers; input handlers
   debounced where the work is genuinely per-keystroke-expensive.
7. **Design perceived performance where real latency remains.**
   Skeletons matching final layout (stability metric protected),
   optimistic UI for mutation feedback (with reconciliation/rollback
   states designed, not assumed), progressive rendering of
   above-the-fold first. Perceived work never replaces step 2–6 —
   it is the residue's treatment, and the design says so.
8. **Install the budgets.** Bundle-size budgets per route (gzip
   numbers, with the rationale) and metric budgets per key page on
   the stated device class — wired as CI gates: size budgets at
   build time (composing `vite-build-qa-engineer`'s surface), metric
   budgets via `performance-test-harness` lab runs where wired.
   A new dependency that blows the size budget claims it in review —
   the frontend twin of the latency budget-claim rule.
9. **Deliver** in the Output Format: evidence, the ranked plan
   (deletion first), per-fix expected metric movement, and the
   budget table with gate placement. Measured verification runs
   through the harness; this design predicts, the harness confirms.

Metric-model vocabulary, weight-audit worksheet, split/asset/hydration
decision tables, and budget-gate examples:
[references/frontend-metric-budget-sheet.md](references/frontend-metric-budget-sheet.md).

## Output Format

```
FRONTEND PERF DESIGN — <route(s)/page(s)>
Symptom: <metric class @ device/network profile — measured value vs target>
Weight audit: <total/per-route; top dependencies with replace/delete verdicts;
               duplicates; dead weight> — DELETIONS FIRST
Splitting: <route splits; lazy candidates (below-fold, interaction-gated);
            vendor chunking; prefetch-on-intent; anti-waterfall floor>
Assets: <image format/size/priority plan; font subset+preload+swap policy;
         immutable hashed asset caching>
Rendering path: <first-render critical set; SSR/hydration honesty (cost + mitigation);
                 third-party scripts off the critical path>
Runtime: <re-render fixes (evidence: render counts); virtualization; layout-thrash;
          long tasks; worker offloads>
Perceived: <skeletons/optimistic UI for the residue — with reconciliation states>
BUDGETS: <per-route size budgets; per-page metric budgets @ device class;
          CI gate placement → vite-build-qa-engineer surface + performance-test-harness>
Expected movement: <per fix: which metric, direction, rough magnitude>
Routed out: <API-side share → latency-budget-architect table; harness mechanics;
             build correctness>
```

## Validation Checklist

- [ ] The symptom is a metric value on a stated device/network class —
      not a developer-laptop impression.
- [ ] The weight audit ran BEFORE tuning: deletions/replacements are
      listed first and micro-optimizations last.
- [ ] Splitting has both a strategy and a floor (no chunk-waterfall);
      lazy candidates are interaction/viewport-gated.
- [ ] The font policy chose its trade (invisible-text vs reflow)
      explicitly; images are sized to display dimensions.
- [ ] SSR/hydration cost is counted on the interactivity side, not
      just credited on first paint.
- [ ] Runtime fixes cite evidence (render counts, long-task traces) —
      no reflexive memoize-everything.
- [ ] Perceived-performance work is labeled as residue treatment, and
      optimistic UI has designed rollback states.
- [ ] Budgets exist with numbers, device class, and CI gate placement;
      the dependency budget-claim rule is stated.
- [ ] Measurement is routed to the harness; build verification to
      vite-build-qa-engineer.

## Gotchas

- The developer-laptop mirage: an M-series machine on fiber hides
  every problem a mid-range phone on mobile network has. Device/
  network class is part of the metric's identity — a budget without
  one is unfalsifiable.
- Hydration's double bill: SSR shows content fast, then hydration
  freezes the thread right when the user first tries to interact —
  the metric moves from loading to interactivity and looks like a
  win if only first paint is watched. Count both.
- The framework is rarely the heavy part: the charting library pulled
  in for one sparkline, the date library shipped whole, the duplicate
  utility libraries — weight audits find kilotons where rewrites
  would find grams.
- Memoize-everything is its own storm: blanket memoization adds
  comparison cost everywhere and hides the real fix (state placed too
  high). Memoize at PROVEN hot spots; restructure state placement
  first.
- Skeletons that lie: a skeleton whose layout differs from the loaded
  state converts loading delay into layout shift — protecting one
  metric by damaging another. Skeletons match final geometry.
- Lazy-loading the hero: viewport-lazy applied indiscriminately
  delays the largest-paint element itself; above-the-fold assets load
  eagerly with priority, below-the-fold lazily — the fold is the
  boundary, not the technique.
- Third-party script amnesia: the tag manager loads a manager that
  loads five vendors, none in the bundle analysis because none are in
  the bundle. The rendering-path audit counts them; async/defer/
  worker isolation contains them.
- Optimistic UI without rollback design: the mutation fails, the UI
  already celebrated, and the reconciliation state was never designed
  — perceived performance becoming actual incorrectness.
- Budget rot by a thousand approvals: every dependency "only adds 30KB".
  The budget-claim rule exists because size budgets die by exception;
  an exception spends the budget or renegotiates it, visibly.

## Stop Conditions

- The complaint's evidence points server-side (API latency dominates
  the waterfall) → stop and route to `latency-budget-architect`'s
  split / the owning backend skills; frontend tuning cannot fix an
  1,800ms API hop.
- No measurement exists and none can be captured (no lab run, no
  field data, no trace) → capture the first lab evidence before
  designing; a perf plan without a baseline cannot claim movement.
  (Standing measurement design routes to `performance-test-harness`.)
- Asked to delete or skip the perf budgets/gates to ship a feature
  ("just raise the budget this once, quietly") → refuse the silent
  path; a budget exception is a recorded review decision (claim,
  reallocation, or renegotiation), not a config edit.
- The design would require product decisions (dropping features,
  visible fidelity loss — heavy imagery, animation) → present the
  options with their metric movement and stop for the product
  owner's call; perf does not silently outrank product intent.
- Asked to also implement the harness runs, edit CI pipelines, or
  restructure the build system in the same pass → hand those slices
  to `performance-test-harness`, `ci-pipeline-architect`, and
  `vite-build-qa-engineer` respectively; this design composes them.

## Supporting Files

- [references/frontend-metric-budget-sheet.md](references/frontend-metric-budget-sheet.md)
  — vendor-neutral metric-model vocabulary, weight-audit worksheet,
  splitting/asset/hydration decision tables, runtime-pattern evidence
  guide, and budget-gate examples with device-class definitions.
- `evals/evals.json` — behavior cases including the hydration
  double-bill edge and the quiet-budget-raise refusal.
- `evals/trigger-evals.json` — discrimination against
  `performance-test-harness`, `vite-build-qa-engineer`,
  `caching-strategy-designer`, `latency-budget-architect`, and
  `playwright-e2e-engineer`.
