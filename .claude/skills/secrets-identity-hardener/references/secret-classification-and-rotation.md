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

Rule: classify intended use and observed exposure separately. If a variable
is server-only but reachable by the client bundle, it is a finding. A public
variable may still be misused as a credential elsewhere. Record each
variable's lifecycle location, consumers, observed artifact exposure, and
intended class without printing its value.

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

**Role and scope (defined once, before the steps):** the credential owner is the recorded authorization role for
routine rotation; the human incident owner is the accountable role for an incident and may
authorize emergency revocation when the credential owner is unavailable. If both are present,
the incident owner's recorded emergency decision governs the revocation while routine rotation
still needs the credential owner's recorded authorization. BOTH confirmed and suspected
compromise may use the emergency path; for suspected compromise record the basis for suspicion
and complete post-hoc verification.

## Rotation procedure

1. Identify every consumer of the credential before rotating (rotation can
   break other services).
2. Check the complete effective approval record for an applicable active
   grant; obtain missing rotation scope before touching live systems.
3. Issue a new credential in the provider/secret manager.
4. Update the secret store / deploy config to the new value.
5. Migrate every known consumer from the inventory to the new credential and
   verify each consumer works; record each verification. Revocation requires the
   credential owner's recorded authorization (or a recorded owner-approved
   exception); never revoke while any known consumer still uses the old credential,
   except under the emergency/compromise carve-out in step 6.
6. Routine rotation runs a bounded overlap window (no longer than the
   provider's propagation window) and escalates to the credential owner if
   consumers cannot be verified within it, recording risk and residual-consumer
   evidence. Compromise is not routine rotation: the human incident owner may
   authorize immediate revocation before full verification, recording the risk
   and any residual consumers.
7. Revoke the OLD credential under the applicable grant.
8. Prove the OLD credential is rejected where testable, then capture any
   residual consumers/failures as incident evidence and record them. Verifying
   the new credential alone is never proof of revocation.
9. If the old secret is in git history, treat history purge (BFG/filter-repo)
   as a separate action whose scope must be covered by an applicable active
   grant or a new owner decision. Rotation restores credential secrecy; purge
   is cleanup.

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
