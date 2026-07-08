# Contribution Guide Sheet

Detail for `contribution-guide-author`. Read on demand.

## Zero-to-merged section skeleton

```
# Contributing to <project>

## Ways to contribute
<code, docs, triage, issues — set the scope>

## Find something to work on
<good-first-issues; issue labels; ask before big changes>

## Set up locally
<clone / install / build / run / test — exact, verified, prereqs stated>

## Make your change
<branch/fork model; keep up to date; small focused changes>

## Run checks before pushing
<lint/format command; test command; what CI will run>

## Open a pull request
<PR title/description conventions; link the issue; what a good PR looks like>

## Review & merge
<who reviews; realistic turnaround; how feedback works; accept/decline criteria; who merges>

## Governance
<code of conduct; license; CLA/DCO sign-off; SECURITY: report privately>
```

## Setup-verification checklist

- [ ] Steps run on a CLEAN environment (no hidden local state).
- [ ] Prerequisites (language/tool versions) stated up front.
- [ ] Build succeeds; app/tests run with the documented commands.
- [ ] Common setup errors + fixes noted.

Broken setup is the #1 contribution killer — verify like a quickstart.

## Automate the standard

| Instead of prose… | Point at… |
|---|---|
| "Use 2 spaces, sort imports…" | formatter/linter + `run: <cmd>` |
| "Write tests" | required test check + `run: <cmd>` |
| "Format commits like…" | commit lint / template |

Contributors run a command; they don't memorize prose. Tell them how to
pass CI before pushing.

## Expectation-setting patterns

- State realistic review turnaround ("we aim to respond within a week").
- Say what gets accepted vs declined (scope, roadmap fit, quality bar).
- For OSS: note maintainers may be volunteers; be kind about latency.
- Encourage discussing large changes BEFORE building them.

## Governance pointers (link, don't inline)

- Code of Conduct.
- License + any CLA/DCO sign-off requirement (e.g. `Signed-off-by`).
- **Security disclosure: report privately** (security policy/contact) —
  NEVER a public issue for a vulnerability.

## Product-agnostic

Use placeholders (`<project>`, `<cmd>`, `<chat>`), single-source commands,
and keep the guide matched to the project's REAL process. A stale
CONTRIBUTING is worse than none.
