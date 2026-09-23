# Check your app before you trust it

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** you built something — maybe with artificial intelligence
(AI) writing most of the code — and you
want to know if it's safe before real users and real data depend on it. You don't need to
know what any of the skill names below mean; each one is a specialist that explains itself
when it runs.

**How to run it:** open your project in your agent tool (Claude Code, Codex
command-line interface (CLI), or any Agent
Skills tool) and take the steps top to bottom. For most steps, asking for what the step
describes in plain words is enough — the named skill selects itself. (Auto-selection quality
varies by tool — see the README's [tools section](../../README.md#using-aegis-with-codex-cli-and-other-agent-skills-tools).)
Start with: **"In this product repository, use the full-codebase-auditor skill
to inventory what was built and list evidence-backed risks before we invite
users."** Any **manual-only** step requires you to name its skill explicitly.
For example: **"Use the secrets-identity-hardener skill to inspect credential
exposure; report any approval needed before rotation."** If your app uses Vite,
say: **"Use the vite-build-qa-engineer skill to check the production bundle
for secret exposure."**

Steps marked *"If…"* are conditional — skip them honestly when the condition doesn't apply
to your app.

## The order

1. **Map what was actually built —
   [`full-codebase-auditor`](../../.claude/skills/full-codebase-auditor/SKILL.md).**
   Yields an honest inventory of the codebase's real state, risks, and technical debt — the
   map every later step works from. Handoff: keep its risk list open; each step below picks
   up its findings.

2. **Stop the urgent leaks —
   [`secrets-identity-hardener`](../../.claude/skills/secrets-identity-hardener/SKILL.md)**
   *(manual-only — name it explicitly: it acts on secrets, so it never auto-fires).*
   Reports any leaked or hardcoded credentials and the needed containment.
   Moving or rotating a credential requires the applicable human approval;
   pending rotations stay visible, never reported as complete. Handoff: any
   identity findings feed the isolation work in step 3.

   *If your app is built with Vite, a frontend build tool:* also name
   [`vite-build-qa-engineer`](../../.claude/skills/vite-build-qa-engineer/SKILL.md)
   *(manual-only — name it explicitly)*. Reports the inspected build and mode,
   searched values and patterns, findings, and gaps in coverage. A result of
   "none found by this method" does not prove the browser bundle is free of
   every secret; source fixes and credential rotation may still be pending.

3. ***If your app has multiple users or customers*** *(most software-as-a-service
   (SaaS) apps do)* — prove they
   can't see each other:

   - **Find every leak surface —
     [`tenant-isolation-reviewer`](../../.claude/skills/tenant-isolation-reviewer/SKILL.md).**
     Yields every place one customer's data could reach another. Handoff: its findings
     drive the two skills below.
   - **Audit and fix the database rules —
     [`rls-policy-auditor`](../../.claude/skills/rls-policy-auditor/SKILL.md).**
     Yields a row-level security audit and negative-test plan. If a policy fix
     is requested, it authors a reviewable migration for separate safety
     review; it does not apply a live database change.
   - **Check for covered regressions —
     [`multi-tenant-security-tester`](../../.claude/skills/multi-tenant-security-tester/SKILL.md).** **Manual-only.**
     Turns isolation findings into negative tests. Run them after relevant
     changes; they catch the cases they cover, not every possible leak.

4. **Scan the whole repository —
   [`security-scan-orchestrator`](../../.claude/skills/security-scan-orchestrator/SKILL.md).**
   Yields one aggregated security-scan report across the codebase. Handoff: hand the report
   to [`static-analysis-reviewer`](../../.claude/skills/static-analysis-reviewer/SKILL.md),
   which yields the findings triaged into real-versus-noise, and to
   [`supply-chain-security-reviewer`](../../.claude/skills/supply-chain-security-reviewer/SKILL.md),
   which yields a judgment on the dependency tree your app inherited.

5. **Check what happens when it fails —
   [`error-handling-security-reviewer`](../../.claude/skills/error-handling-security-reviewer/SKILL.md).**
   Reports fail-open paths — the catch-the-error-and-continue class of error —
   with recommended fixes. The review does not apply a fix or accept a risk;
   keep open findings on the step-7 evidence list for an authorized decision.

6. ***If your app has AI features*** *(a chatbot, an assistant, anything that calls a
   model)*: branch to **[Add AI features safely](add-ai-safely.md)** and run that path,
   then come back here for the close.

7. **The go/no-go —
   [`release-readiness-reviewer`](../../.claude/skills/release-readiness-reviewer/SKILL.md).**
   Yields an evidence-based GO (ready to ship) or NO-GO (blocked from shipping)
   decision, built from what the
   steps above actually found — not from anyone's assurance that it's probably fine. This
   is the close of the path. A GO is an advisory readiness result, not release
   authorization; a human approval or applicable standing grant still governs
   any launch.

## What this is — and isn't

This is a guided order, not a guarantee. Each skill's own output is the evidence: what it
found, what it fixed, what it left open. If a step reports findings you don't understand,
ask Claude Code to explain them in plain words before moving on — an unexplained finding is
not a cleared one.
