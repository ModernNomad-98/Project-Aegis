# Agent speed protocol

**Status.** Adopted by the owner on 2026-11-16 and recorded as decision D-19
(the owner's decision to adopt this protocol); published 2026-11-20. The caps
below are defaults: a deviation is recorded in the PR body, and a material
deviation that changes a gate is recorded in the owner approval register.

These caps are a working agreement between the people and agents doing the
work. They are not machine-enforced: no check fails when a cap is exceeded, and
none is claimed to.

## Caps

- **Plan audits.** One independent audit per capture. A blocking or major
  finding means a new capture and a full re-audit. A minor or nit finding is
  fixed by the author and verified by the same auditor as a delta check of the
  capture diff, not a new full cycle.
- **Candidates.** At most two per PR. After the last candidate, every remaining
  P2/P3 finding (medium or low severity) gets an audited disposition and a
  follow-up issue, while a real P1 (the highest severity, still blocking) still
  blocks.
- **Codex review cycles.** At most two reviews. Known false-positive classes
  are answered with the recorded evidence template.
- **Local blind review.** One pass at the final candidate head; the fix
  re-check is a delta review, not a new full review.
- **Heavy validators.** The local pre-push gate is fast: skill validation,
  targeted validator checks, the markdown link check, the commit sign-off
  check, and the gate pattern. The full validator suite runs once at the final
  head in CI. Local full-suite runs are optional and never repeated per
  candidate.

### Delta re-audits
When a minor or nit finding is fixed after the plan audit, the same auditor checks only the delta:
- **Inputs:** the original capture hash, the fix diff, and the changed-lines context.
- **Check:** the fix addresses the finding, the agreed scope is unchanged, and no new risk was introduced.
- **Verdict:** `DELTA PASS` or `DELTA REVISE`, recorded in the PR body (or the run log); a `DELTA REVISE` returns to the author for another delta check; no full re-audit and no new full audit cycle.

A blocking or major finding still requires a new capture and a full re-audit.

## Scope freeze

The captured plan is the scope. Anything requested after capture becomes (a) a
new plan revision explicitly scheduled, or (b) the next PR. It is never a
silent addition to the running candidate.

## Evidence, not prose re-measurement

Each plan and candidate carries a generated evidence block: counts, file
identities, line anchors, closure commands with their base outputs, manifest
ancestry, and gate-pattern matches. Auditors verify the block against the
repository mechanically; a stale number is treated as a plan defect.

## Base freeze and one re-base

Freeze the base at capture. If a merge moves it, run one re-base pass (refresh
the evidence and flag only the facts that changed) and continue; do not re-plan
from scratch.

## Known false-positive classes

Record the evidence, then continue.

- **Manifest source-revision ancestry.** A synthetic or squash review commit
  reports a sibling. Evidence: the branch's parent chain, an ancestor test from
  the recorded source revision to the head returning exit 0, and required
  skill validation and targeted validator checks green. A fresh audit at that
  head refutes it.
- **Audit-engine route findings on prose route names.** For example, a written
  walkthrough referred to by a route-like label. Dispose with a follow-up
  issue.
- **A refused-action negation quoted by the semantic audit.** Dispose as a
  false positive, quoting the sentence.

## Owner-only work stays out of PR lanes

Grants, protected paths, pins and re-pins, live runs, personal or secret
material, and other repositories: park, record, continue. Batch them, and
decide analogues from the owner approval register and prior PR receipts.

## Scaffolding

Skill additions use `scripts/scaffold-skill.py` (APR-140 tooling; no
`.github/` change) with one JSON config: `name`, `description`, `purpose`,
`use_when`, `inputs`, `workflow`, `output_format`,
`validation_checklist`, `gotchas`, `stop_conditions`, `supporting_files`,
`positive_prompt`, `negative_prompt`, `overlaps_with`, and optional
`trigger_note`. Unknown keys are rejected, the name cannot shadow a reserved
bundled skill, and every overlap must resolve to an installed
`.claude/skills/<name>/SKILL.md`.

The generator emits exactly three files under `.claude/skills/<name>/`:

- `SKILL.md` — strict frontmatter (`name` plus a single-quoted `description`
  with internal apostrophes doubled) and the nine sections in canonical order:
  Purpose, Use When, Inputs to Inspect, Workflow (numbered), Output Format,
  Validation Checklist (checkboxes), Gotchas, Stop Conditions, Supporting
  Files (bullets, or "- None yet.").
- `evals/evals.json` — `$schema`, `skill`, an eval-suite `description`,
  and two cases: one `should_trigger` built from the config's positive prompt
  with assertions derived from its workflow and checklist, and one
  `should_not_trigger` built from the negative prompt that names the first
  overlap as the owner.
- `evals/trigger-evals.json` — `skill`, `description`, `overlaps_with`, and
  the matching positive/negative discrimination cases; the positive expects
  this skill and forbids the overlaps, the negative expects the first overlap
  and forbids this skill.

The default is a dry run that writes nothing and prints each file plus the
closure list:

```
python -P scripts/scaffold-skill.py --config <config.json> --repo-root .
python -P scripts/scaffold-skill.py --config <config.json> --repo-root . --apply
```

`--apply` refuses an existing skill directory unless `--force` is given;
`--force` overwrites only the three generated files and leaves other files in
the directory alone. Output is deterministic, contains no timestamp, and an
invalid argument or config exits 2 with one line of error text.

Registration, README counts, the manifest and the audit baseline keep their
owning tools — the generator never edits them. Its printed closures are, in
order:

1. Review the generated text and replace the placeholder assertions with
   checks specific to this skill.
2. Add the `docs/skills-catalog.md` row and the README selected/coverage
   entry, and hand-bump the README family-roster count by one. Do not run
   `--write-readme-counts` yet: it fails closed until the manifest matches
   disk.
3. Commit the skill, then run
   `python -P scripts/validate-skills.py --refresh-skills-manifest --manifest-ref=<content-commit>`
   and commit the manifest. That refresh exits 1 because the README count is
   still stale, but it writes the manifest before that check; the failure is
   expected.
4. Run `python -P scripts/validate-skills.py --write-readme-counts` and
   commit the result.
5. Run `python -P scripts/validate-skills.py`, then
   `python -P scripts/tests/test_audit_skill_contracts.py`.
6. Regenerate the baseline with
   `python -P scripts/audit-skill-contracts.py --json artifacts/audits/skill-contract-audit-baseline.json`
   and review the diff.

## Measurement

Per PR, record plan-audit rounds, candidate count, Codex findings by class, and
wall-clock time from branch to merge. Target: at most two plan audits, two
candidates, two Codex cycles, and the heavy suite once.

### Per-PR cycle metrics
Copy this block into the PR body (or the run log) before merge:

| Metric | This PR |
| --- | --- |
| Plan-audit rounds | `<n>` — target at most 2; one per capture, with a delta check for minor/nit fixes |
| Candidates | `<n>` (cap: 2) |
| Codex review cycles | `<n>` (cap: 2) |
| Local blind-review passes | `<n>` (cap: 1, at the final candidate) |
| Heavy-suite runs | `<n>` (cap: 1, at the final head via CI) |
| Codex findings by class | `<P1/P2/P3 with disposition>` |
| Wall clock, branch to merge | `<hh:mm>` |
| Cap exceeded? | no — or yes, with the recorded deviation and the follow-up issue |

If a cap is exceeded, record the deviation in the PR body and a follow-up issue
(or an explicitly scheduled plan revision); do not extend the running PR. A real
P1 still blocks regardless.

The protocol was applied once, to the design-orchestrator lane (the design
workstream), including a recorded cap deviation; that application is history,
not a standing rule.
