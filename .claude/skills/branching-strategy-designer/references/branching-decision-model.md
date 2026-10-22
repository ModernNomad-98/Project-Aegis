# Branching decision model: branching-strategy-designer artifact

## 1. Decision record

| Item | Value |
| --- | --- |
| Context | team size, release cadence, hotfix needs, CI gates |
| Chosen model | trunk-based with short-lived branches / release branches / hybrid |
| Alternatives considered | <option + why rejected> |
| Migration risk | <open branches, release freeze, queue changes> |
| Decision owner | <named human owner> |

## 2. Rule table

| Rule | Specification | Enforcement | Owner |
| --- | --- | --- | --- |
| Branch naming | type/issue-slug, short-lived | CI/name check | <owner> |
| Protection | main requires PR + review + green aggregate | repo settings (owner action) | <owner> |
| Review | 1-2 reviewers by change class | contribution guide | <owner> |
| Merge method | squash for feature PRs; merge commits for release syncs | merge queue/policy | <owner> |
| Hotfix | branch from release tag, cherry-pick to main, re-tag | release runbook | <owner> |
| Release | tag from main or release branch by cadence | release readiness gate | <owner> |

## 3. Alternatives and rejected options

| Option | Fit | Why rejected/accepted |
| --- | --- | --- |
| Trunk-based + short-lived branches | one deployable main, fast feedback | accepted when CI is fast and feature flags exist |
| Release branches | regulated/versioned releases | rejected if no long support windows, adds sync overhead |
| GitFlow | heavy release trains | rejected for small teams; merge burden |

## 4. Migration and completion

- [ ] Migration steps ordered (announce, adapt protection, migrate open branches, enable queue).
- [ ] Rollback of the process change stated.
- [ ] Risks/open constraints recorded.
- [ ] No settings changed by this skill; owner executes.
