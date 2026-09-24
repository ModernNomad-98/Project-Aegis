---
name: vite-build-qa-engineer
description: MANUAL-ONLY; never auto-invoke. QA the Vite build itself — run the production build and check the client bundle for known secret exposure by named, redacted checks (audit configured env prefixes, inspect dist output without printing secret values, check define/import.meta.env usage), verify build/preview parity, output size and sourcemap policy, assets and SPA fallback routing. Use when asked to verify a Vite build before deploy, audit exposed env vars or bundle contents for secret exposure, debug works-in-dev-but-not-in-build issues, or gate builds in CI with output checks. RUNS builds and preview servers. Do NOT use for moving secrets server-side and rotating leaked credentials (secrets-identity-hardener), unit/component testing (vitest-unit-component-engineer), E2E journeys (playwright-e2e-engineer), or CI pipeline design (qa-automation-architect).
disable-model-invocation: true
---

# Vite Build QA Engineer

**Reading key:** QA is quality assurance; SPA is single-page application;
MPA is multi-page application; env means environment; CI is continuous
integration; E2E is end-to-end.

## Purpose

Verify the artifact that actually ships: run the production build, check the
client bundle for known secret exposure by named methods, confirm it behaves like the
dev app (modes, env files, base path, assets, routing), and inspect the
output against size and sourcemap policy. Dev-mode green tells you nothing
about the bundle — this skill tests the build product itself and reports
with real command output.

## Use When

- Use when: asked to verify/QA a Vite build before deploy or release.
- Use when: auditing `VITE_` env vars or checking whether a secret leaked
  into the client bundle.
- Use when: something works in `vite dev` but breaks built/previewed —
  mode/env resolution, base path, dynamic imports, SPA fallback.
- Use when: adding build-output checks (bundle budget, secret grep,
  sourcemap policy) that CI will run — implementing the checks; the CI
  pipeline design itself is `qa-automation-architect`.
- Do NOT use when: a secret IS confirmed in the bundle and must be moved
  server-side + rotated — that remediation is the shipped
  `secrets-identity-hardener` (manual-only); this skill detects and proves,
  then hands off.
- Do NOT use when: testing app logic/components — 
  `vitest-unit-component-engineer`; or journeys — `playwright-e2e-engineer`.
- Do NOT use when: designing the whole automation/CI architecture —
  `qa-automation-architect`.

## Inputs to Inspect

1. Vite config(s): `vite.config.*` — `envPrefix`, `define`, `base`, build
   options, plugins that inject values, sourcemap settings.
2. Env files and their mode mapping: `.env`, `.env.production`,
   `.env.staging`, `.env.*.local` — `VITE_` is exposed by default; inspect
   configured `envPrefix` for all exposed names and list them.
3. Where env values enter code: `import.meta.env.*` usage, `define`
   replacements, runtime config endpoints.
4. Deployment intent: target base path/subdirectory, SPA vs MPA routing,
   hosting rewrite rules (affects preview parity checks).
5. Build scripts and CI: which commands/modes are actually used to produce
   the shipped artifact (test THAT mode, not just default production).

## Workflow

1. **Inventory the env surface.** List every configured exposed-prefix variable per
   mode and classify: safe-public (API base URLs, feature flags) vs
   secret-shaped (keys, tokens, connection strings, anything named
   *_SECRET/*_KEY with a private value). Secret-shaped exposed vars are
   findings BEFORE the build even runs. Check `define` and plugin injection
   too — the prefix is not the only leak path.
2. **Run the real production build** with the mode(s) CI/deploy actually
   uses; record the exact command and output (warnings included — chunk
   size warnings, mixed-import warnings are findings to triage, not noise).
3. **Check bundle cleanliness:** search `dist/` (JS, CSS, HTML, sourcemaps)
   for (a) the VALUES of known server-side secrets from the environment, (b)
   secret-shaped patterns, (c) each inventoried exposed value to confirm
   what shipped. Do not print secret values or matching bundle excerpts;
   report file/location and a redacted fingerprint. Absence is claimed only
   for what was actually searched — state the method. Recipes in
   [references/vite-build-checks.md](references/vite-build-checks.md).
4. **Verify build/preview parity:** serve with `vite preview` (or the real
   host emulation), walk the critical routes — direct-URL deep links (SPA
   fallback), asset/dynamic-import loading under the configured `base`,
   env-dependent behavior per mode. Works-in-dev-only issues get root-caused
   to the build semantics difference, not shrugged at.
5. **Inspect the output:** bundle sizes vs budget (or record the baseline if
   none exists), unexpected inclusions (server-only modules, dev tools,
   giant deps pulled into the entry chunk), sourcemap policy enforced
   (production maps per repo policy: absent, hidden, or uploaded-restricted).
6. **Report with evidence** and wire repeatable checks: the secret-grep and
   budget checks as scripts CI can run (placement per the automation
   blueprint). Confirmed secret exposure → stop wiring, hand to
   `secrets-identity-hardener` for relocation + rotation.

## Output Format

```
VITE BUILD QA — <app> @ <commit/build>
Env inventory: <configured exposed-prefix vars per mode → safe-public | SECRET-SHAPED (finding)>
Injection paths checked: <import.meta.env / define / plugins>
Build: <exact command + mode> → <result, warnings triaged>
Bundle cleanliness: <what was searched (values/patterns/files) → findings
                    or "none found by this method">
Parity checks: <route/asset/deep-link/mode results under preview + base>
Output inspection: <sizes vs budget, unexpected inclusions, sourcemap policy>
Findings: <severity-ranked, each with file/location and redacted fingerprint; no secret bytes>
CI checks wired: <scripts + placement, or handoff to automation blueprint>
Handoffs: <confirmed secrets → secrets-identity-hardener (relocate+rotate);
          app bugs → systematic-debugger>
```

## Validation Checklist

- [ ] Every variable under the configured exposed prefixes inventoried and
      classified per mode; `define`/plugin
      injection paths checked too.
- [ ] Build run with the REAL deploy mode; command + output recorded.
- [ ] Bundle search covered values AND patterns, across JS/CSS/HTML/maps;
      method stated with the claim.
- [ ] Deep links, assets, and dynamic imports verified under the configured
      `base` via preview.
- [ ] Sourcemap policy for production verified, not assumed.
- [ ] Size budget compared or baseline recorded.
- [ ] Secret findings handed to `secrets-identity-hardener`, not "fixed" by
      renaming the variable here.

## Security Rules

- Values exposed through configured `envPrefix`, `define` or plugins may
  ship in the client artifact; treat secret-shaped values as exposures even
  if "only staging" and verify the actual artifact.
- A leaked secret found in `dist/` means the value is COMPROMISED wherever
  that artifact went — removal alone is not remediation; rotation is
  (`secrets-identity-hardener` owns it).
- Sourcemaps ship your source: production map policy is a security decision,
  verified per deploy target.

## Gotchas

- `import.meta.env` values are statically replaced at build time — grepping
  source tells you intent; only grepping `dist/` tells you truth.
- `.env.local`/`.env.[mode].local` differences make local builds diverge
  from CI builds — verify with the CI env source, not just the laptop.
- `base` misconfiguration breaks only nested-route refreshes and dynamic
  imports — the home page working proves nothing; test deep links.
- `vite preview` is not the production server: host rewrites, headers, and
  compression differ — parity here is necessary, not sufficient; say so in
  the report.
- Public API keys that are legitimately client-side (analytics IDs, some
  provider publishable keys) are not findings — classify by the provider's
  own public/secret designation, and say which designation was assumed.

## Stop Conditions

- The build fails for app-code reasons → report the failure output; fixing
  app code is a separate change (`systematic-debugger` / owner), not silent
  patching here.
- A confirmed secret is in a bundle that already shipped → escalate
  immediately (rotation urgency) via `secrets-identity-hardener` /
  `human-approval-boundary`; do not sit on it until the report is polished.
- The deploy mode/env source can't be determined → verifying the wrong mode
  produces false assurance; ask before claiming the artifact is clean.
- Asked to also restructure env handling across the codebase → that is
  `secrets-identity-hardener` scope; hand off.

## Supporting Files

- [references/vite-build-checks.md](references/vite-build-checks.md) —
  bundle-grep recipes (values/patterns/file classes), parity walk checklist,
  budget/sourcemap check snippets for CI.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the unit/build/flake/data
  cluster and against `secrets-identity-hardener`.
