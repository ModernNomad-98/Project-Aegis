# Issue #101 package 2 review evidence

## Scope and authority

AEGIS-APR-007 in the merged owner approval register grants the ten exact
package-2 files and one signed implementation PR. The branch started from
grant merge `1af342712d27d5e6ea482b3f451106b4dccaf125` in the isolated
`.worktrees/issue101-package2` worktree. Work began 2026-09-23 16:35 UTC.
Previous and current forecasts are both 6–12 active hours; the ceiling is
12 active implementation hours and 1,200 added lines. Selected backlog total
is 191–426 active hours, or 207–466 with both optional helpers. Observed
implementation time and exact added lines are reported in the PR on closeout.

## Delivered and limited

The manual-only `aegis-setup` skill shows four choices and can complete only
Aegis-only setup. The copied skill includes a Windows PowerShell 5.1 state
writer and a state contract. Its JSON record lives in the current user's
local application data, keyed to one physical checkout root. A saved selection
is a preference; it grants no provider or host invocation authority. Local
and online helper routes are unavailable. Other operating systems may use
the conversation but have no tested saved-state support.

No provider/model call, install, credential, customer data, private holdout,
host hook, classifier, deployment or measured token-saving claim is part of
this package. The package-3 offline advisory contract is separate.

## Verification

- Windows PowerShell 5.1: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude/skills/aegis-setup/scripts/test-selection.ps1` exits 0 with `PASS: 21 selection assertions`. Synthetic temporary directories cover fresh selection, later read, overwrite, original/completion timestamps, failed write preserving a prior record, concurrent lock rejection, moved checkout, unsupported version, corrupt and duplicate JSON (including escaped duplicate keys), strict schema-version type, explicit repair, and checkout-local state rejection.
- `python scripts/validate-skills.py` exits 0 with `OK: 185 skill(s) valid, 0 warning(s)`. It checks structure, not behavioral evals.
- `evals/evals.json` and `evals/trigger-evals.json` are manual review prompts for four-choice wording and nearby skill routing. Independent conversation/authority review is required before merge.

## Open gates

Record final test exits, independent audit findings, signed commit and PR,
exact-head GitHub Actions, and observed active time in the PR. Keep the PR
unmerged until the coordinator reconciles the shared routing-plan file and
confirms delivery.
