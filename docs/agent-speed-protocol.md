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

Repeated skill additions use the same 11-15-file pattern. Generate
registration, coverage, reconciliation, manifest and baselines from one
config, with tooling outside protected paths in a planning branch or workspace
until a grant exists, then review the generated diff.

## Measurement

Per PR, record plan-audit rounds, candidate count, Codex findings by class, and
wall-clock time from branch to merge. Target: at most two plan audits, two
candidates, two Codex cycles, and the heavy suite once.

The protocol was applied once, to the design-orchestrator lane (the design
workstream), including a recorded cap deviation; that application is history,
not a standing rule.
