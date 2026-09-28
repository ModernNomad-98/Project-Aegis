---
name: environment-parity-reviewer
description: 'Review how local, CI, preview, staging and production differ, so "works in staging, fails in production" is caught early: a parity matrix across runtime and dependency versions, environment-variable NAMES and non-secret values, feature-flag defaults, database engine, version and extensions, third-party sandbox versus live modes, auth callbacks, build mode, region, time zone and data shape. Each difference is INTENDED (documented), ACCIDENTAL or UNKNOWN, with evidence and a fix owner; it also drafts the required-configuration manifest and startup validation that fail fast on a missing or wrong setting. Reads repository files and exports it is given, never secret values; connects to nothing. Use when behavior differs between environments, or before promoting to production. Do NOT use for IaC diffs or IaC-to-runtime drift (iac-reviewer), secret handling (secrets-identity-hardener), Vite build checks (vite-build-qa-engineer), or local CI mirroring (local-ci-mirror-preflight).'
---

# Environment Parity Reviewer

**Reading key:** An environment is one place the product runs: a
developer's machine (local), continuous integration (CI, the automated
build-and-test run on each change), a preview deployment made for one
change, staging (the rehearsal copy) and production (what customers use).
Parity means two environments behave the same where they are meant to. An
environment variable is a named setting the running app reads, such as
`DATABASE_URL`; its NAME is safe to show, while a secret VALUE (a password,
key or token) is not. Infrastructure as code (IaC) is cloud setup written
as files, for example Terraform. A sandbox mode is a payment or email
provider's test mode that moves no real money and sends no real mail. An
auth callback is the web address a sign-in provider sends the user back
to. A feature flag is a setting that turns behavior on or off without a
code change. A lockfile pins the exact dependency versions a build uses.
Startup validation is a check the app runs as it starts that stops it with
a clear error when a required setting is missing or malformed ("fail
fast"). A tenant is one customer organization whose data the product keeps
apart from other customers' data.

## Purpose

Most "works in staging, fails in production" incidents are not code bugs;
they are differences nobody wrote down: a missing variable, a newer
database extension in one place, a provider left in sandbox mode, a
callback address pointing at the wrong host, a different time zone. This
skill compares the environments a product runs in, dimension by dimension,
and classifies every difference it finds as INTENDED (a documented reason
exists), ACCIDENTAL (no reason, and it can break behavior) or UNKNOWN (the
evidence cannot say), each with the evidence and a fix owner. It then
drafts the required-configuration manifest (every setting the app needs,
per environment, with its allowed shape) and the startup validation
specification that makes a missing or wrong setting stop the app at boot
instead of failing a user later. It reads repository files and the exports
a person supplies, reads variable NAMES and non-secret values only, never
a secret value, and connects to nothing. The manifest and validation are a
specification in the report for the implementing engineer, not code this
skill writes. Built under owner decision D71 (2026-09-28) from roadmap
category 07 item #244, with #246 (runtime configuration validation) folded
in as an output.

## Use When

- Use when: something works in one environment and fails or behaves
  differently in another ("fine in staging, broken in production", "only
  preview deployments fail sign-in").
- Use when: a release is about to be promoted to production and someone
  asks what differs between the environments it has passed through.
- Use when: a team wants a list of every setting the app needs per
  environment, or asks how the app should refuse to start with a missing
  or malformed setting.
- Use when: a new environment (a second region, a new preview setup, a
  customer-dedicated copy) is being added and must match the existing ones
  where it should.
- Do NOT use when: the question is what an IaC change will destroy or
  expose, or whether the IaC matches what is running (drift) — that is
  `iac-reviewer`. This skill compares environments with each other,
  including settings held outside IaC.
- Do NOT use when: the configured cloud account is being checked against a
  security baseline, control by control — that is
  `cloud-security-baseline-reviewer`. A security setting that differs
  between environments is reported here as a difference and handed there.
- Do NOT use when: a secret must be moved, classified as public or
  server-only, or rotated — that is `secrets-identity-hardener`
  *(manual-only)*, which a person must invoke by name.
- Do NOT use when: the problem is a Vite build that works in the
  development server but not once built or previewed — that is
  `vite-build-qa-engineer` *(manual-only)*, which runs the build.
- Do NOT use when: the ask is to run the CI checks locally before a push,
  or why a change passes locally and fails in CI on the same checks — that
  is `local-ci-mirror-preflight` *(manual-only)*.
- Do NOT use when: designing the flag system, its defaults policy or its
  outage behavior — that is `feature-flag-architect`. This skill only
  reports that a flag's default differs between environments.
- Do NOT use when: deciding what test data each environment should hold —
  that is `test-data-architect`.

## Inputs to Inspect

1. The list of environments in scope and which pair or set the question is
   about. Default to the path a change travels: local → CI → preview →
   staging → production.
2. Environment templates and per-environment config files in the
   repository (`.env.example`, `.env.staging.example`, config maps,
   platform settings files), read for variable NAMES and non-secret
   values. Never open a real `.env` file with secret values; if only one
   exists, read its names and stop reading at the first secret-looking
   value.
3. Runtime and dependency pins: language runtime version files
   (`.nvmrc`, `.python-version`, `.tool-versions`), lockfiles, container
   files (`Dockerfile`, base-image tags), and CI workflow files for the
   versions CI uses.
4. Database facts per environment: engine, major and minor version,
   enabled extensions, collation and encoding, time zone setting, and the
   migration version applied, from IaC, migration history or a supplied
   export.
5. Exports the person supplies from each environment: a hosting
   platform's variable list with values masked, a provider dashboard
   screenshot or export showing sandbox or live mode, a flag service's
   per-environment defaults, the registered auth callback addresses. An
   export that contains a secret value is not read further (Stop
   Conditions).
6. Documented intent: architecture decision records, runbooks, README
   sections or comments that say why an environment differs. A difference
   is INTENDED only when one of these says so.
7. The failure report, when the review was triggered by one: what broke,
   where, and when, so the matrix starts with the dimensions most likely
   to explain it.

## Workflow

1. **Fix the scope.** Name the environments compared and the source of
   evidence for each. An environment with no evidence at all is listed as
   UNKNOWN across the board, not assumed equal to its neighbor.
2. **Build the parity matrix.** One row per dimension, one column per
   environment, each cell a value or `not found`, with the file path, line
   or export that shows it. Cover every dimension in
   [references/parity-matrix-sheet.md](references/parity-matrix-sheet.md):
   runtime and dependency versions; environment-variable names (present or
   missing) and non-secret values; feature-flag defaults; database engine,
   version and extensions; third-party sandbox versus live modes; auth
   callback addresses and allowed origins; build mode; region; time zone
   and locale; data shape (volume, seed versus real data, tenants
   present). A secret variable's cell shows `set` or `missing`, never the
   value.
3. **Classify every difference.**
   - **INTENDED:** a document in the inputs states the reason (for
     example "staging uses the payment sandbox; see runbook section 2").
     Cite it.
   - **ACCIDENTAL:** no documented reason, and the difference can change
     behavior (a missing variable, a different database extension, a
     callback pointing at the wrong host).
   - **UNKNOWN:** the evidence cannot say whether it is intended, or one
     side's value is not visible. Pair it with one question for the owner.
   A difference that "looks deliberate" (sandbox in staging, live in
   production) is still UNKNOWN until a document says so.
4. **Rank by risk.** Differences that can break sign-in, payments, data
   integrity or tenant separation come first; cosmetic differences last.
   Give each ACCIDENTAL and UNKNOWN finding a fix owner: the environment's
   owner for a missing setting, `iac-reviewer` for a fix that belongs in
   IaC, `secrets-identity-hardener` *(manual-only)* for a secret that is
   misplaced or exposed, `feature-flag-architect` for a flag-default
   policy question, `cloud-security-baseline-reviewer` for a security
   control present in one account and absent in another.
5. **Draft the required-configuration manifest.** For every setting the
   app reads, one entry: name, which environments require it, whether it
   is secret (value never shown), the allowed shape (URL with an `https`
   scheme, one of a fixed list of modes, an integer range), the default if
   any, and the owner. Derive it from the code's reads and the templates;
   a setting the code reads but no template lists is itself a finding.
6. **Draft the startup validation specification.** For each manifest
   entry: the check the app performs before serving traffic (present,
   parses, matches the allowed shape, is consistent with the environment,
   for example "live payment keys refused outside production"), the error
   message that names the setting but never its value, and whether a
   failure stops the app or only warns. Hand the specification to the
   implementing engineer; a health or readiness check that reports it
   belongs to `observability-operator` *(manual-only)*.
7. **Deliver the report** in the Output Format, with the owner questions
   ranked so the one that resolves the most UNKNOWN rows comes first. If
   an owner product choice is needed (for example, whether preview
   deployments should share staging's database), define the terms, explain
   each viable option's reason, cost or uncertainty, and benefits and
   drawbacks for this product, recommend one with a reason, and ask one
   atomic question.

## Output Format

```
ENVIRONMENT PARITY REVIEW — <product / service>
Environments: <local | CI | preview | staging | production> with the
              evidence source for each
Summary:      <n> dimensions · <n> INTENDED · <n> ACCIDENTAL · <n> UNKNOWN
Parity matrix (secret cells show set / missing only):
  | Dimension | local | CI | preview | staging | production | Evidence |
Findings (risk order):
  F<n> <dimension> — <what differs, between which environments>
       Class:    INTENDED | ACCIDENTAL | UNKNOWN
       Evidence: <file:line or export name>; for INTENDED, the document
                 that states the reason
       Impact:   <what breaks or could break, and for whom>
       Owner:    <environment owner or skill>
       Question: <one owner question, UNKNOWN only>
Required-configuration manifest (draft):
  | Name | Required in | Secret? | Allowed shape | Default | Owner |
Startup validation specification (draft, for the implementing engineer):
  | Name | Check at startup | Error message (names the setting, never
    the value) | Stop or warn |
Owner questions (ranked, most UNKNOWN rows unblocked first):
  Q<n> <question> — resolves <finding ids>
Not done: no environment was connected to, no secret value was read or
          printed, no file or setting was changed.
```

For an owner product choice, include the defined terms, the options with
reasons, benefits, drawbacks and cost or unknowns, and the recommendation
with its reason before the one question.

## Validation Checklist

- [ ] Every environment in scope has a column and a named evidence source,
      or is marked UNKNOWN for want of evidence.
- [ ] Every dimension in the parity sheet was checked, or the report says
      why it does not apply.
- [ ] Every difference has exactly one class; every INTENDED cites the
      document that states the reason.
- [ ] Every ACCIDENTAL and UNKNOWN finding has evidence, an impact and a
      fix owner; every UNKNOWN has one owner question.
- [ ] No secret value appears anywhere in the report, including the
      matrix, the manifest, examples and error messages.
- [ ] The manifest lists every setting the code reads, and flags settings
      read in code but missing from every template.
- [ ] The startup validation specification names each check, its error
      message and whether failure stops the app.
- [ ] The report states that nothing was connected to or changed.

## Security Rules

- Secret values are never read into the review, printed, summarized,
  hashed for comparison or repeated back. Compare secrets by presence
  (`set` / `missing`) and, where a person states it, by kind (sandbox key
  versus live key), never by value.
- An export or file found to contain a secret value is not read further.
  Say which file, name the variable, and hand the exposure to
  `secrets-identity-hardener` *(manual-only)*; do not copy the value into
  the finding.
- Startup error messages in the specification name the missing or
  malformed setting and the rule it broke, never the value, so logs do not
  become a secret store.
- A difference that weakens a security control in production (debug mode
  on, a permissive allowed-origin list, an auth callback on an
  unregistered host) is ranked first and handed to
  `cloud-security-baseline-reviewer` for account-level controls or the
  environment owner for app settings.
- This skill connects to no environment, database, provider or platform.
  Evidence comes only from the repository and exports a person supplies.

## Gotchas

- Sandbox in staging and live in production is the most common difference
  and usually right, but "usually" is not evidence. Leave it UNKNOWN until
  a document says so; the one time it is wrong, staging charges real cards.
- A variable present in every environment can still differ in shape: a
  trailing slash on a base URL, `http` versus `https`, a region code in
  one place and a region name in another. Compare shape, not just
  presence.
- Database extensions and collation drift silently: a query or index that
  relies on an extension enabled only in staging fails in production at
  the worst time. Check the extension list, not only the engine version.
- Time zone and locale differences surface as off-by-one-day bugs in
  reports and billing. CI often runs in UTC while a developer machine does
  not.
- Preview deployments frequently share a staging database or a single
  auth callback allow-list; both are parity problems that only appear
  under parallel previews.
- A flag defaulted on in staging and off in production makes staging
  tests prove nothing about production. Report the default difference;
  the defaults policy belongs to `feature-flag-architect`.
- Masked platform exports sometimes mask only part of a value. Treat any
  visible fragment of a secret as a secret value.

## Stop Conditions

- Asked to paste, show, compare or print secret values ("paste the
  production secrets so we can compare them") → refuse; compare by
  variable NAME and presence only, and offer the name-only matrix.
- A supplied file or export contains secret values → stop reading it,
  name the file and variable without the value, and hand the exposure to
  `secrets-identity-hardener` *(manual-only)*.
- Asked to call a difference INTENDED with no documented reason → refuse;
  keep it UNKNOWN and ask the owner for the reason or a document.
- Asked to connect to an environment, query a database, call a provider
  or read a live platform setting → refuse; ask the person for an export
  with secret values masked.
- Asked to change a setting, template, IaC file or flag to fix a
  difference → out of scope; report the fix and its owner and change
  nothing.
- No evidence exists for any environment beyond one → stop; a parity
  review needs at least two environments to compare. Ask for the second
  environment's template or export.
- The question is IaC-to-runtime drift or an IaC diff's safety → route to
  `iac-reviewer`.

## Supporting Files

- [references/parity-matrix-sheet.md](references/parity-matrix-sheet.md)
  — the parity dimensions with where to find each and what to compare,
  the INTENDED / ACCIDENTAL / UNKNOWN rules with examples, and the
  manifest and startup-validation entry templates.
- `evals/evals.json` — behavior cases: the missing-variable and
  database-extension happy path, the sandbox-versus-live case that is
  INTENDED only when documented, the refusal to compare secret values,
  the refusal to connect to production, and three should-not-trigger
  cases.
- `evals/trigger-evals.json` — discrimination against `iac-reviewer`
  ("our Terraform drifted"), `vite-build-qa-engineer` ("works in dev, not
  in build"), `local-ci-mirror-preflight` ("passes locally, fails in CI")
  and `feature-flag-architect`.
