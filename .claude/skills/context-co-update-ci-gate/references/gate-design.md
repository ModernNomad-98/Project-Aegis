# Context Co-Update Gate — Reference Design

Companion to `context-co-update-ci-gate`. Shapes below are reference designs
to hand to `ci-pipeline-architect` or a human for installation — this skill
does not edit pipeline files.

## Check logic (pseudocode)

```
changed  = files changed in PR vs base          # e.g. git diff --name-only origin/<base>...HEAD
IMPORTANT = [ globs from the design ]           # e.g. src/api/**, **/migrations/**, .github/workflows/**, AGENTS.md
CONTEXT   = [ docs/REPO_CONTEXT_MAP.md, docs/context/** ]   # the protected artifacts

if error computing changed:            FAIL     # fail closed
touches_important = any(changed matches IMPORTANT)
updates_context   = any(changed matches CONTEXT)
declared_noop     = PR body contains marker line
                    "Context-Update: none — <reason>"      # reviewable claim

if touches_important and not (updates_context or declared_noop):
    FAIL with instructive message
else:
    PASS
```

Notes:

- The marker line must carry a REASON; a bare "Context-Update: none" fails.
- A PR whose only changes ARE the context artifacts passes trivially (the
  map may be updated on its own).
- Renames/deletes of important paths count as touching them.

## GitHub Actions shape (reference)

```yaml
# reference shape — installed via ci-pipeline-architect / human review
name: context-map-gate
on:
  pull_request:
    branches: [<base>]
jobs:
  context-co-update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<pinned>
        with: { fetch-depth: 0 }
      - name: enforce co-update
        run: |
          # compare against the PR base, not HEAD~1 (multi-commit PRs)
          git diff --name-only "origin/${{ github.base_ref }}"...HEAD > changed.txt
          # ... apply the pseudocode above; exit 1 on FAIL
```

Placement rule: where the repo runs a single **aggregate required check**
(see `sharded-validation-with-resume`), this job feeds the aggregate instead
of registering its own required name — one more required job name is one
more thing conditional skips can strand.

## Failure message template

```
❌ Context co-update required.

This PR changes important paths:
  <matched files>

but does not update the context map (<map path>) or notes (<notes dir>),
and declares no exception.

To satisfy this gate, do ONE of:
  1. Update the context map/notes in this PR (protocol: <protocol doc path>
     — date + commit SHA + evidence-cited status moves).
  2. Add to the PR description:  Context-Update: none — <why no update is needed>
     (reviewers may reject the claim).
```

An instructive failure is part of the design: a gate that says only "failed"
teaches people to fight the gate, not maintain the map.

## Update protocol (full text to adopt into the repo)

1. **Stamp every update.** Each map/notes edit records the date and the
   commit SHA the update was verified against:
   `_Updated 2026-07-07 against <sha> — <one-line what changed>_`.
   An undated update poisons every later freshness judgment.
2. **Status moves need evidence.** A section may move (e.g.
   `UNVERIFIED → VERIFIED`, `RISK → RESOLVED`) only with the verifying
   artifact cited inline (PR #, commit SHA, test run). No artifact, no move.
3. **Risk notes are never deleted while unresolved.** Resolution = replace
   the note with the proof (what resolved it, where). "Stale, removing" is
   drift with a commit message.
4. **Surgical updates only inside feature PRs.** Rewriting the map's
   structure rides its own PR where reviewers can see it; a feature PR
   amends the sections its change touches.
5. **Certainty labels** (house convention worth adopting): mark claims
   `confirmed` (evidence linked) vs `inferred` vs `unknown` — the map should
   never present an inference as a verified fact.

## Important-paths starter list (calibrate per repo)

| Glob | Why |
| --- | --- |
| `src/**` API/route/service roots | The map's architecture sections describe them. |
| `**/migrations/**`, schema files | Schema drift is the most expensive kind. |
| `.github/workflows/**` | Pipeline behavior is context; also self-protects this gate. |
| Agent-instruction files (`CLAUDE.md`, `AGENTS.md`, etc.) | Sessions act on them; stale ones steer agents wrong. |
| Auth/RLS/policy paths | Security posture claims in the map must track them. |

Keep the list short enough that a triggered gate is nearly always RIGHT —
the gate's authority comes from its precision, not its coverage.
