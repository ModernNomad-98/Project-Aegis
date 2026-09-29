# Supabase Baseline Reference

Detail file for [cloud-security-baseline-reviewer](../SKILL.md). Loaded on
demand. Supabase hosts a Postgres database with sign-in (Auth), file
storage and an automatic web API (application programming interface) over
the database; a URL is a web address. RLS is Postgres
row-level security, which decides which rows each caller may read or
change. The anon (or publishable) key is meant for browsers; the
service_role (or secret) key bypasses RLS and must stay on servers. MFA is
multi-factor authentication; SSL and TLS mean encrypted connections.

**Verification rule.** Supabase key names, dashboard screens, advisor
checks and plan features change. Every item below is a verification item:
confirm it against current Supabase documentation and the project's plan
before citing it. The user supplies every screen, export or lint result;
this skill connects to nothing.

## Published baselines to name

- Supabase's production checklist and Security Advisor checks (the dashboard's built-in configuration checker; name the
  date they were read).
- A team's own baseline, named and versioned in the repository.
- Otherwise: the Aegis minimum baseline below, labelled as such.

## Aegis minimum baseline, by control family

Data access (RLS and the schemas the web API exposes) is a Supabase-only
family; report it after encryption and public storage.

| Family | Control | Evidence the user supplies | GAP signal |
| --- | --- | --- | --- |
| Identity | Organization members reviewed; MFA required for members | Organization members and security screens | former staff present; MFA not required |
| Secrets | The service_role or secret key never reaches a browser or a public repository | Client environment files, the front-end build config and repository search results (key NAMES only) | the service key in a client env file or under a public prefix: CRITICAL; hand rotation to `secrets-identity-hardener` *(manual-only)* |
| Secrets | Database password is strong and not shared in code | Where the connection string lives (name and location only) | connection string with password committed to the repository |
| Network | Database network restrictions and SSL enforcement set as the baseline expects | Database settings screen | open to all addresses and SSL not enforced, without a reason |
| Encryption | Storage buckets are private unless intended | Storage bucket list with the public flag | a public bucket holding user uploads |
| Data access | RLS enabled on every table in exposed schemas | Security Advisor output or a lint export | a table with RLS disabled in an exposed schema; policy content goes to `rls-policy-auditor` |
| Data access | Only intended schemas are exposed through the web API | API settings screen | internal schemas exposed |
| Audit logging | Auth and API logs retained for the baseline period | Logs settings screen and plan | retention shorter than the baseline (name the plan) |
| Guardrails | Auth redirect URLs are exact, not wildcards; sign-up and rate limits set | Auth URL configuration and rate-limit screens | wildcard redirect on a production domain; open sign-up that should be invite-only |
| Posture | Security Advisor findings reviewed and triaged | Security Advisor output with its date | open ERROR-level findings with no owner |
| Incident readiness | A named owner can rotate keys and pause the project; runbook exists | The runbook path | no owner; no runbook (hand to `incident-response-runbook`) |

## Gotchas

- An RLS-enabled table with no policies denies everything through the web
  API but not to the service key; a table without RLS is readable with the
  anon key.
- A leaked service key is exposed from the moment it shipped. Report it by
  name and location, never by value, and say it must be rotated.
- Backups and point-in-time recovery are outside this review; note them as
  out of scope rather than MET.
