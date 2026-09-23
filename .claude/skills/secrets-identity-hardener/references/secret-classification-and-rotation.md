# Secret Classification & Rotation

Progressive-disclosure detail for `secrets-identity-hardener`. Operate on
secret NAMES and LOCATIONS; never print secret values.

**Use:** This reference supports the [manual-only secrets and identity
workflow](../SKILL.md); reading it does not authorize rotation, live-account
changes, or inspection of real secret values. API means application
programming interface; URL means uniform resource locator; DB means database;
CI means continuous integration; CRA means Create React App; KMS means key
management service; RLS means row-level security; XSS means cross-site
scripting; CSRF means cross-site request forgery; and BFG names the BFG
Repo-Cleaner history-rewrite tool. Public-name prefixes
are clues to review, while the built client artifact is the exposure proof.

## Environment-variable classification rubric

| Class | Definition | May ship to client? | Example |
|---|---|---|---|
| public | Intended to be visible in the browser | yes | public API base URL, publishable key |
| server-only | Grants access; must never reach the client | no | DB password, service-role key, signing secret |
| CI-only | Used by pipelines, not runtime | no | deploy token, registry password |
| deploy-only | Injected at deploy, not in repo/build | no | prod DB URL, KMS key id |

Rule: if a variable is server-only but reachable by the client bundle, it is a
finding. Classification is per variable and written down.

## Client-bundle exposure checks (verify the ARTIFACT, not the convention)

- **Vite:** `VITE_` is the default client-exposed environment prefix; inspect
  `envPrefix`, `define`, plugins, and code paths for other injections. Check
  the built `dist/` for server-secret name/value patterns; assert absent. A
  server secret must NOT carry an exposed prefix.
- **Next.js:** `NEXT_PUBLIC_` marks client-exposed environment variables;
  inspect client bundles for other injected values too, not just `.env`.
- **CRA:** `REACT_APP_` marks client-exposed variables; inspect the built
  artifact for other injection paths with the same discipline.
- **Generic:** build the client, then search the output bundle for known
  server-secret names; the proving test fails if found.

Turn this into an automated check (test or CI step) so it stays enforced.

## Rotation procedure

1. Identify every consumer of the credential before rotating (rotation can
   break other services).
2. Get approval (`human-approval-boundary`) — rotation touches live systems.
3. Issue a new credential in the provider/secret manager.
4. Update the secret store / deploy config to the new value.
5. Verify the app works on the new credential; verify the OLD credential is
   rejected where testable.
6. Revoke the old credential.
7. If the old secret is in git history, treat history purge (BFG/filter-repo)
   as a SEPARATE approval-gated action — rotation is what actually restores
   secrecy; purge is cleanup.

## Least-privilege service accounts

- Enumerate what each machine identity currently CAN do vs what it NEEDS.
- Remove unused scopes/roles; record each removal and why.
- One identity per workload where practical; avoid shared "does everything"
  keys reachable from user-facing request paths.
- Service-role / BYPASSRLS credentials belong to trusted server jobs only —
  DB specifics are `rls-policy-auditor`'s domain; coordinate.

## Session/token hardening

- Prefer `HttpOnly`, `Secure`, `SameSite` cookies over localStorage tokens
  (localStorage is XSS-readable).
- Set sane expiry; implement refresh with rotation on privilege change.
- Provide server-side revocation (logout, compromise response).
- Moving storage model changes CSRF posture — add CSRF defense when moving to
  cookies. Add tests for flags, expiry, and revocation.

## Evidence to capture

- The classification table.
- The red→green bundle-exposure check output (secret absent from client).
- Rotation status per credential (rotated w/ approval, or pending ops).
- Least-privilege diffs (grants removed).
- Never the secret values themselves.
