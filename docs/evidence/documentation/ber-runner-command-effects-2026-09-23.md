# Behavioral Eval Runner command effects

## Current reading — 2026-09-24

This note helps maintainers verify the runner guide's offline command effects.
The premerge estimate and guard wording below are historical. [Pull request (PR) #197](https://github.com/ModernNomad-98/Project-Aegis/pull/197)
merged as `ebaba9362e3eedba2f419a9072c6477f3ce23024` after Linux and Windows
passed and the owner approved its one-time protected guard exception, now
consumed by [approval-register entry APR-017](../../approvals/APPROVAL_REGISTER.md#aegis-apr-017-consumption-of-pr-197-exception).

Date: 2026-09-23. This documentation correction follows the first
Behavioral Eval Runner guide review. The earlier deep screen was estimated at
2–4 active hours; this correction was estimated at 1–3 active hours. The
selected backlog estimate at work start was 175–394 active hours. Estimates
describe active effort, while the merge report will measure elapsed wall time.

The [runner guide](../../../tools/behavioral_eval_runner/README.md) now explains
what each offline workflow command reads, prints, or writes. In particular,
its `census --out census.json` example creates or replaces a file in the
current directory. The guide defines manifest, fixture, hash, and JavaScript
Object Notation before the workflow and explains canonical output beside the
example. It says that `schedule` does not dispatch work. This
changes documentation only; it grants no permission for provider calls, real
inputs, or host activation.

The command options were checked against the local `cli.py` handlers and
`census --help`, `materialize --help`, and `verify-evidence --help`. Independent
review and continuous integration results belong to the pull request. Because
the guide is a protected path, a failed `gate-guard` requires an explicit
pull-request-specific owner disposition before merge.
