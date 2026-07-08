# Merge-Is-Deploy Governance Doc — Template & Mechanics

Companion to `merge-is-deploy-governance`. Placeholders (`<owner>/<repo>`,
`<branch>`) are filled per repo; nothing here is product-specific.

## Governance doc template

```markdown
# Deployment Reality & Pipeline Governance — <repo>

_Adopted <YYYY-MM-DD>; changes to this doc ride reviewed PRs._

## 1. Reality (verified <date>)
Merging to `<branch>` auto-deploys **<app / functions / site>** to
**<environment>** via <platform> with no human step between.
Evidence: <platform config file / project setting — cited>.
**Not auto-deployed:** <e.g. database migrations — applied by an operator
via the gated deployment procedure>. Ordering hazard: code that requires an
unapplied migration must not merge before the migration is applied —
see <gated deployment doc>.

## 2. Authoritative gate = PR-time validation
Required checks (exact names): `<check-1>`, `<check-2>`.
These are the LAST validation before production. Anything not validated
here is validated in production. Known gaps: <list → routed>.

## 3. Post-merge = verification, never a gate
Signals: <smoke check / health endpoint / deploy status>, expected within
<latency>. A post-merge failure is an incident-class signal → rollback
(§5) or fix-forward decision. It does not retroactively become a gate.

## 4. Branch protection (recorded <date>, source: <API | human-dictated>)
- Protected branch: `<branch>`
- Required status checks: `<exact names>` (strict up-to-date: <yes/no> — <why>)
- Required reviews: <n>; enforce admins: <yes/no>
- Merge strategy allowed: <squash/merge/rebase>
- WHO MAY CHANGE PROTECTION: <named human role> — never agents, never
  "temporarily". Every change lands as a dated diff to this section.
- Drift check: on <cadence>, compare live config to this record
  (`gh api repos/<owner>/<repo>/branches/<branch>/protection` — admin
  scope; or `gh api repos/<owner>/<repo>/rulesets`). Mismatch = incident-
  class finding: either the doc or the protection was changed ungoverned.

## 5. Rollback primitive: revert-PR-then-auto-redeploy
1. Identify the bad mainline commit: `git log --oneline <branch>`.
2. Revert per merge strategy (§6), open the revert PR.
3. The revert PR passes the SAME required checks (§2) — the gate is not
   bypassed for rollbacks; if the platform offers an instant
   previous-deploy alias flip, that is a mitigation step, not the rollback.
4. Human merges → platform auto-redeploys the reverted state.
5. Verify via §3 signals.
**Revert does NOT undo:** applied migrations, external registrations,
queued jobs, emitted webhooks — the executable runbook for those lives
with rollback-runbook-author's artifact: <link>.

## 6. Revert mechanics by merge strategy
| Strategy | Mainline commit type | Command |
| --- | --- | --- |
| squash | ordinary commit | `git revert <sha>` (no -m; `-m 1` here FAILS) |
| merge commit | merge commit | `git revert -m 1 <sha>` |
| rebase | series of ordinary commits | `git revert <newest-sha>..<oldest-sha>` range or per-commit, newest first |

## 7. Accepted-risk exposure window
From merge to verified deploy: ≈ <duration> (deploy latency + §3 signal
latency). During it, <blast radius: which users/tenants/surfaces> are
exposed to any defect PR validation missed.
Accepted by <named human> on <date>. Revisit when latency or blast radius
changes materially.
```

## Notes on verification commands

- `gh api repos/<owner>/<repo>/branches/<branch>/protection` returns 404
  both for "no protection" and "no admin scope" — distinguish by checking
  scope first (`gh auth status`); label the record's source honestly.
- Deploy trigger evidence beats platform folklore: the project's own config
  (framework config file, GitOps `Application` spec, platform dashboard
  setting the human screenshots) is citable; "the platform usually…" is not.
- Where auto-merge auditing matters (armed state converts green CI into a
  deploy), the PR timeline's enable event is strategy-specific:
  `auto_merge_enabled`, `auto_squash_enabled`, or `auto_rebase_enabled` —
  query via `gh api repos/<owner>/<repo>/issues/<n>/timeline` and check the
  armed state with `gh pr view <n> --json autoMergeRequest`.

## The exposure-window conversation

The window is not a defect to hide; it is the price of merge==deploy, and
the governance's honesty test. State it as: duration × blast radius ×
who accepted. Three healthy responses exist: shrink the duration (faster
verification signals), shrink the radius (flags, canaries — route to the
pipeline/release skills), or accept it in writing. The unhealthy response —
leaving it unstated — is the one this doc forbids.
