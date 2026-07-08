# Local CI Mirror Preflight — Procedure Detail

Companion to `local-ci-mirror-preflight`. Commands shown are for a
GitHub-Actions repo; adapt the derivation source for other CI systems.

## 1. Derivation table

Read every workflow that triggers on `pull_request` (mind `paths:` filters —
a path-filtered job that your diff doesn't trigger is out of scope and says
so in the table). For each job:

| CI job (workflow) | What CI runs | Local equivalent | Gap |
| --- | --- | --- | --- |
| `validate` (ci.yml) | `python scripts/validate.py` on 3.x | same command, local Python | version matrix reduced to one |
| `unit` (ci.yml) | `npm run test:ci` with coverage gate | `npm run test:ci` | none |
| `e2e` (e2e.yml) | Playwright vs preview deploy | `npm run e2e` vs local server | env differs — record as partial mirror |
| `secret-scan` (sec.yml) | vendor action w/ org token | none derivable | `cannot-determine-locally` |

Rules:

- The workflow file is the contract. Where a local script and the workflow
  disagree, mirror the workflow and flag the divergence.
- REQUIRED checks (branch protection) get priority; optional jobs are still
  derived but marked optional.
- A job you cannot derive is RECORDED (`cannot-determine-locally`), never
  dropped from the table.

## 2. Mainline baseline (separate worktree — non-negotiable when shared)

```bash
git fetch origin
git worktree add "<scratch>/mainline-baseline" origin/main   # detached at origin/main
cd "<scratch>/mainline-baseline"
# install deps if the checks need them, then run the derived checks
cd -
git worktree remove "<scratch>/mainline-baseline"            # add --force only if artifacts dirtied it
```

- Use a scratch location OUTSIDE the primary checkout.
- Never `git checkout main` in a checkout that another session may be using
  — shared-worktree flips are a documented collision source.
- Record per-check result + duration on the baseline before running the
  work's pass, so the comparison is honest (same commands, same env, same
  day).
- If main's CI is visibly red for a check (`gh run list --branch main`),
  expect the local baseline to reproduce it — if it doesn't, note the
  divergence (env-dependent failure ⇒ lean `CI-infrastructure`).

## 3. Work pass

Run the identical derived list against the tree state you intend to commit
(stash nothing silently — what you test must be what you commit). Capture
observable output per check; "ran clean" with no output recorded is not
evidence.

## 4. Failure classification — evidence standards

| Class | Minimum evidence | Action |
| --- | --- | --- |
| `PR-caused` | fails on work, passes on baseline (both runs cited) | fix before commit — blocking |
| `pre-existing-on-main` | fails on baseline with same signature | report it; do NOT fix inside this PR (scope drift) — route to its own task/issue |
| `CI-infrastructure` | cause is env/runner/network/tooling (evidence: works on retry with no code change, missing local service, rate limit) | note; not blocking; expect real CI to differ |
| `cannot-determine-locally` | no faithful local equivalent (secrets, vendor actions, matrix) | carry as named residual risk to real CI |

Timeouts: record expected vs observed duration; a run killed by timeout is
not an assertion failure. Remediate with the smallest safe fix (split the
run, reduce setup, rerun once) — never raise a timeout ceiling just to
convert red to green, and never let a timeout masquerade as `PR-caused`
without a reproducing assertion.

## 5. Docs-only lightweight path

Take it only when the diff meets the repo's docs-only definition — typically:
all changed files are documentation/content, AND none appear on the
never-docs-only list (workflows, scripts, schema, lockfiles, agent
instruction files). `risk-tiered-validation-selector` owns the definition
where it exists; otherwise the workflow `paths:` filters are the best
in-repo signal. The path is: docs-scoped CI jobs (if any) + link/reference
sanity + an explicit statement in the preflight record:
`Docs-only path taken: <definition matched>`. Silence is not a path.

## 6. Worked example (abbreviated record)

```
LOCAL CI MIRROR PREFLIGHT — feat/orders-cache @ ab12cd3 (vs origin/main @ 99ee001)
| job → local | baseline | work | duration | gap |
| validate → python scripts/validate.py | PASS | PASS | 4s/4s | none |
| unit → npm run test:ci | PASS | FAIL (2 assertions, orders.spec) | 92s/95s | none |
| e2e → npm run e2e (local server) | FAIL (login flake) | FAIL (same signature) | 6m | env differs |
| secret-scan → none | — | — | — | cannot-determine-locally |
Classified:
  unit — PR-caused (passes baseline, fails work) → fixing before commit
  e2e — pre-existing-on-main (same failure signature on baseline; also red on
        main's last 3 CI runs) → reported, routed to issue; NOT fixed here
  secret-scan — cannot-determine-locally → residual to real CI
Verdict: BLOCKED until unit green; then COMMIT with e2e/pre-existing +
secret-scan residual disclosed.
```

## 7. Post-push cross-check (optional but cheap)

After pushing, `gh pr checks <n> --watch` confirms the mirror held. A CI
failure in a check the mirror passed is a derivation gap — update the
derivation table, don't shrug; the mirror is only as good as its last
calibration.
