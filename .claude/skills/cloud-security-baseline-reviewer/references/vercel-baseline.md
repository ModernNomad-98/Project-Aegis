# Vercel Baseline Reference

Detail file for [cloud-security-baseline-reviewer](../SKILL.md). Loaded on
demand. Vercel hosts web front ends and serverless functions. A preview
deployment is the temporary site built for each branch or pull request;
SSO is single sign-on; MFA is multi-factor authentication; HTTPS is the
encrypted form of HTTP, the web's request protocol; a URL is a web address;
CLI is the command-line interface (`vercel`).

**Verification rule.** Vercel features and their plan tiers change often.
Every feature name, setting and plan limit below is a verification item:
confirm it against current Vercel documentation and the team's plan before
citing it. A control the plan does not offer is a GAP with the plan named.
The user supplies every screen or listing; this skill runs nothing.

## Published baselines to name

- Vercel publishes security guidance but no numbered benchmark; name the
  document and its date if the team uses one.
- A team's own baseline, named and versioned in the repository.
- Otherwise: the Aegis minimum baseline below, labelled as such.

## Aegis minimum baseline, by control family

| Family | Control | Evidence the user supplies | GAP signal |
| --- | --- | --- | --- |
| Identity | Team members and roles reviewed; owners few | Team members settings screen | former staff present; many Owners |
| Identity | SSO or MFA required for the team, where the plan allows | Team security settings screen | not enforced (name the plan if unavailable) |
| Secrets | Server-only secrets are not exposed to the browser | `vercel env ls` (lists names and targets, not values) plus the framework's public prefix rule | a service, admin or secret key under a public prefix such as `NEXT_PUBLIC_` |
| Secrets | Production secrets are not available to preview deployments | `vercel env ls` targets column | production database or payment keys scoped to Preview |
| Network | Preview deployments are protected from the public | Deployment Protection settings screen | previews public while they reach real data |
| Network | Forked pull requests cannot reach secrets | Git integration settings screen | fork builds receive environment variables |
| Encryption | Custom domains served over HTTPS only | Domains screen | certificate errors or HTTP-only domains |
| Audit logging | Team audit log or log drains retained, where the plan allows | Audit log or log drain settings screen | none (name the plan if unavailable) |
| Guardrails | Access tokens scoped and expiring | Account tokens screen | full-scope tokens without expiry; unknown owners |
| Posture | Firewall or bot protection rules reviewed, where the plan allows | Firewall settings screen | none on a public login or signup route |
| Incident readiness | A named owner can roll back and rotate keys; runbook exists | The runbook path | no owner; no runbook (hand to `incident-response-runbook`) |

## Gotchas

- `vercel env pull` writes secret values to a local file. Never ask for it;
  `vercel env ls` is enough.
- A public prefix is a build-time rule of the framework, not a Vercel
  setting; the leak is in the browser bundle whatever the dashboard says.
- Preview deployments often run against the production database by
  accident; check which database URL name each target uses.
