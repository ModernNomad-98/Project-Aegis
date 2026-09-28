# Environment parity sheet

Reference for `environment-parity-reviewer`. Read it while building the
parity matrix (Workflow step 2), classifying differences (step 3) and
drafting the manifest and startup validation (steps 5 and 6).

## 1. Parity dimensions

Check every row. Where a dimension does not apply (no database, no
third-party provider), say so in the report instead of dropping the row.

| Dimension | Where to look (repository or supplied export) | What to compare | Typical failure when it differs |
| --- | --- | --- | --- |
| Language runtime | `.nvmrc`, `.python-version`, `.tool-versions`, `engines` field, container base image, CI setup step | Major and minor version | A syntax or library feature exists in one runtime and not the other |
| Dependency versions | Lockfile committed? Same lockfile used by CI and the deploy build? | Lockfile presence and install mode (frozen or not) | A floating dependency resolves to a newer, breaking release in one place |
| Environment-variable names | `.env.example` and per-environment templates, platform variable export (values masked), the code's config reads | Present or missing per environment | Missing variable: crash or silent fallback to a default |
| Non-secret values | Same sources; only values that are not secrets (base URLs, modes, region codes, log levels) | Exact value and shape (scheme, trailing slash, casing) | Wrong host, mixed `http`/`https`, a region name where a code is expected |
| Secret variables | Same sources | `set` or `missing` only; kind (sandbox or live) only when a person states it | Missing secret: a feature fails at first use, not at boot |
| Feature-flag defaults | Flag service per-environment export, code-level defaults | Default and targeting per environment | Staging tests exercise a path production never runs |
| Database engine and version | IaC, platform export, migration tooling config | Engine, major and minor version | A function or syntax available in one version only |
| Database extensions | Migration history, platform export | Extension list and versions | A query or index needs an extension enabled only in staging |
| Database settings | Platform export | Collation, encoding, time zone | Sort order or date boundaries differ |
| Migration version | Migration table export or tooling status output supplied by a person | Latest applied migration per environment | Code expects a column one environment does not have yet |
| Third-party modes | Provider dashboard export or screenshot, mode variables | Sandbox or live per provider (payments, email, messaging, maps) | Real charges or emails from a non-production environment, or test keys in production |
| Auth callbacks and origins | Identity provider export, allowed-origin config | Registered callback addresses, allowed origins, cookie domain | Sign-in fails on preview hosts, or a permissive origin list in production |
| Build mode | Build scripts, CI workflow, platform build settings | Production or development mode, source maps, minification | Debug code or verbose errors shipped, or a bug that only minified output shows |
| Region | IaC, platform export | Hosting region per service | Latency, data-residency obligations, a provider feature missing in one region |
| Time zone and locale | Container and CI settings, platform export | Process time zone, default locale | Off-by-one-day reports, number or date formatting differences |
| Data shape | Seed scripts, supplied row counts, tenant list | Volume, seed versus real data, number of tenants, oldest record | A query that is fast on seed data times out on real volume; a code path only real tenants reach |

## 2. Classification rules

Every difference gets exactly one class.

| Class | Rule | Example |
| --- | --- | --- |
| **INTENDED** | A document in the inputs (decision record, runbook, README section, config comment) states the reason. Cite its path. | "Staging uses the payment sandbox — see `docs/runbooks/payments.md`, section Environments." |
| **ACCIDENTAL** | No documented reason, and the difference can change behavior. | `STRIPE_WEBHOOK_SECRET` is in the staging template but not in production's variable export. |
| **UNKNOWN** | The evidence cannot settle it: no document, and the difference may or may not be deliberate, or one side's value is not visible. Pair it with one owner question. | Production shows live payment mode, staging shows sandbox mode, and nothing documents why. Question: "Is sandbox-in-staging the intended policy? If yes, where should that be written down?" |

Rules of thumb:

- "Obviously intended" is not a class. A difference with no document is
  UNKNOWN even when it looks deliberate.
- A missing value on one side is ACCIDENTAL when the code reads it
  unconditionally; UNKNOWN when the code has a guarded default.
- A difference that weakens a security control in production is ranked
  first regardless of class.

## 3. Required-configuration manifest entry

One entry per setting the code reads.

```
Name:          PAYMENT_MODE
Required in:   staging, production (preview: optional)
Secret?:       no
Allowed shape: one of "sandbox" | "live"
Default:       none (must be set)
Consistency:   "live" only in production
Owner:         payments team
Source:        src/config/payments.ts:12 (read); .env.example:8 (template)
```

A secret entry shows `Secret?: yes` and never an example value; its
allowed shape describes the format only ("starts with a provider prefix,
40 characters").

A setting the code reads but no template lists is a finding of its own:
the manifest entry is drafted and the gap is reported as ACCIDENTAL.

## 4. Startup validation entry

One entry per manifest row the app cannot run correctly without.

```
Name:     PAYMENT_MODE
Check:    present; value in {"sandbox", "live"}; "live" refused when
          APP_ENV is not "production"
Error:    "PAYMENT_MODE must be 'sandbox' or 'live' (got an unsupported
          value); 'live' is allowed only in production."
On fail:  stop — the app does not start
```

Rules for the specification:

- The error names the setting and the rule broken; it never includes the
  value, even for non-secret settings, so the rule is uniform.
- Stop on anything that would corrupt data, charge money, send messages
  or weaken security; warn only on settings with a safe default.
- Validate everything first, then report all failures together, so one
  deploy attempt shows every missing setting instead of one per restart.
- The specification is handed to the implementing engineer. Exposing the
  result through a health or readiness check is `observability-operator`
  work *(manual-only)*.

## 5. Worked example (short)

Inputs: `.env.staging.example` and `.env.production.example`, a staging
migration history, and a production extension list exported by the
database owner.

| Dimension | staging | production | Class |
| --- | --- | --- | --- |
| `SEARCH_API_URL` name | present | missing | ACCIDENTAL: the search client reads it unconditionally |
| Extension `pg_trgm` | enabled | not enabled | ACCIDENTAL: migration `0042_fuzzy_search` creates a trigram index |
| `PAYMENT_MODE` value | sandbox | live | UNKNOWN: no document; one owner question |

Manifest and startup validation gain an entry for `SEARCH_API_URL`
(present, `https` URL, stop on failure). The extension finding goes to
the database owner, and to `iac-reviewer` if the database is defined in
IaC.
