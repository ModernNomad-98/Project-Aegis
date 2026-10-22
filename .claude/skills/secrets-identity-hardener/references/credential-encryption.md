# Credential encryption: stored-secret hash/KDF and the migration residual

Reference for the `secrets-identity-hardener` skill (extension-only bundle; #104 stays SHIPPED in this batch).

## Stored credentials

- Passwords: **memory-hard KDF preferred - Argon2id** (or scrypt) with per-record salt, stated cost parameters and a rehash-on-login upgrade path. **bcrypt is CPU-hard, not memory-hard** (small fixed memory footprint); accept bcrypt only as a legacy/compatibility choice with an explicit cost factor and an upgrade plan, and never describe it as memory-hard.
- API keys/tokens: store a keyed hash or encrypted envelope, never reversible plaintext; show only once at creation and keep a fingerprint for support.
- Encryption at rest is a second layer, not a substitute for hashing secrets that should never be recoverable.
- Rotation: keep two active versions with an expiry, record which records use which version, and re-wrap/rotate before disabling a version.

## Migration residual (explicit)

- A residual exists when legacy rows use a weaker hash/algorithm or no envelope: name the count, the migration path, the dual-read window and the completion check.
- Do not claim migration complete until the completion check shows zero legacy rows; an unfinished migration is an accepted residual with an owner.
- Never log the secret, the hash input or the derived key.

## Boundaries

- This reference does not perform the code change, run a migration or audit the RLS policies; `appsec-implementer` (manual-only) implements, `secure-migration-reviewer` reviews migration safety.
- No coverage-map status change is claimed by this bundle.
