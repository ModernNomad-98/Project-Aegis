# Frontend Metric & Budget Sheet

Vocabulary, worksheets, and gate examples backing the workflow.
Vendor-neutral: the metric trio is named by what it measures; map to
your measurement stack's current names.

## Metric model (the standard trio, vendor-neutral)

| Class | What users feel | Typical dominant causes |
|---|---|---|
| Loading (largest-content paint class) | "it's still loading" | bundle weight, blocking resources, image priority, server response |
| Interactivity (interaction-latency class) | "I clicked and nothing happened" | hydration, long tasks, re-render storms, heavy handlers |
| Visual stability (layout-shift class) | "the page jumped" | unsized media, late fonts, injected banners, lying skeletons |

Metric identity = metric + page/route + DEVICE/NETWORK CLASS. Define
classes explicitly, e.g.:

```
device-class "baseline-mobile": mid-range phone CPU profile (4x throttle),
  throttled mobile network (~1.5Mbps down, 150ms RTT), cold cache
device-class "desktop": no throttle, warm cache permitted (say which)
```

## Weight-audit worksheet

```
Total gz: <n KB>   Per-route: <route: n KB ...>
Top dependencies by cost:
  <lib>: <KB gz> — used for <what> — verdict: KEEP | REPLACE with <lighter/built-in> | DELETE (unused)
Duplicates/near-duplicates: <two date libs, two utility libs, ...>
Dead weight: <unused exports, legacy polyfills for retired targets>
DELETIONS FIRST: the plan's first section is what leaves.
```

## Splitting decision table

| Candidate | Split? | Mechanism |
|---|---|---|
| Route | yes, always (floor) | router-level dynamic import |
| Below-the-fold section | usually | viewport-gated lazy |
| Interaction-gated UI (modal, editor, chart) | yes | import-on-summon |
| Above-the-fold/hero content | NO — eager + priority | anti-pattern: lazy-loading the largest-paint element |
| Vendor core (framework) | separate stable chunk | long-cache benefits |
| Everything into 40 micro-chunks | NO | request waterfall — splitting has a floor |

## Asset decision rows

- Images: modern format + fallback; dimensions match display size
  (attribute-sized to protect stability metric); hero = eager +
  priority hint; below fold = lazy.
- Fonts: subset to used glyph ranges; preload the critical face; swap
  policy is a CHOSEN trade — swap (reflow risk, text visible) vs
  block-brief (brief invisible text, no reflow) — per brand tolerance,
  stated.
- Asset caching (this skill's caching scope): content-hashed
  filenames + immutable long-lived headers; HTML short-cache;
  service-worker strategy only with an update path designed
  (stale-app-forever is the failure mode). Shared API/data response
  caching → caching-strategy-designer.

## Hydration honesty table

| Strategy | First paint | Interactivity bill |
|---|---|---|
| CSR only | slowest | pay once (parse/execute) |
| SSR + full hydration | fast paint | full hydration freeze right at first interaction — count it |
| SSR + partial/lazy hydration (islands) | fast paint | pay per island on demand — the usual best trade |
| SSG for static routes | fastest | minimal — prefer where content allows |

## Runtime-pattern evidence guide

| Pattern | Evidence to capture (before fixing) |
|---|---|
| Re-render storm | render counts per interaction (framework devtools/profiler) — fix state placement first, memoize proven hot spots second |
| Unvirtualized list | DOM node count on the route; interaction latency scaling with list size |
| Layout thrash | forced-reflow warnings in a trace; read/write interleaving in handlers |
| Long tasks | main-thread trace: tasks > 50ms attributed to source |
| Third-party tax | request waterfall + main-thread share attributed to third-party origins |

## Budget-gate examples

```
# size budgets (build-time gate, composing vite-build-qa-engineer surface)
route "/app":       ≤ 220 KB gz   (rationale: baseline-mobile parse budget)
route "/marketing": ≤ 120 KB gz
vendor chunk:       ≤ 150 KB gz   delta-per-PR alert at +10 KB

# metric budgets (lab gate via performance-test-harness where wired)
page "/app" @ baseline-mobile: loading-class ≤ 2.5s; interaction-class ≤ 200ms;
                               shift-class ≤ 0.1
```

Budget-claim rule (the frontend twin of the latency claim rule): a PR
exceeding a size budget states the claim — funded by deletion
elsewhere, budget reallocation with the owner's sign-off, or a
recorded renegotiation. Silent raises are review blocks.
