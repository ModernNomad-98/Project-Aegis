# Readiness Evidence Reference

Detail file for the owning [Release Readiness Reviewer](../SKILL.md).
Loaded on demand. For an auto-deploying merge, the pre-merge gate uses the
exact PR head or merge-queue candidate; verify the final merged commit and
artifact afterward. Unknown on a blocking dimension remains NO-GO.
CI means continuous integration; PR means pull request; SHA denotes a
commit hash; API means application programming interface; UI means user
interface; CODEOWNERS is the repository file assigning code review owners.

## Evidence table template — pass/blocking criteria per dimension

| Dimension | Passing evidence looks like | Blocking when |
| --- | --- | --- |
| CI on gated tree | every required check ran on the exact shipping SHA, or on the exact PR/merge-queue candidate before auto-deploying merge, with result + run link and final-commit follow-up | required check missing/failed/not-run on the gated tree; evidence only from an unrelated branch tip |
| Artifact provenance | shipping artifact stamped with commit + run id and deploy consumes it; before an auto-deploying merge, verified build/provenance contract with actual artifact checked afterward | untracked rebuild-at-deploy; unstamped artifact; provenance chain broken |
| Test signal | suites that ran exercise the changed surface (coverage-mapper cross-check) | green suites that never touch the changed module; retried-to-green on release-relevant checks unexplained |
| Migrations | `secure-migration-reviewer` output for every migration in scope | any unreviewed migration; review found blockers unresolved |
| Rollback path | runbook for THIS release shape: primitive named, migration posture covered, rehearsal status stated | no runbook; "revert the commit" without deploy/data story; runbook assumptions broken by this scope |
| Feature flags | new behavior behind flags with recorded default decisions; kill-switch coverage for risky paths | flag defaulted ON without a recorded decision; no kill switch on a high-risk path |
| Docs/changelog | user-facing changes documented; breaking changes called out | breaking change undocumented |
| Observability | dashboard/alert coverage for the new surface; on-call staffed for the release window | new surface invisible; nobody watching the window |
| Approvals | change-class approvals recorded (per `change-classification-gate` mapping) | required approval absent or granted for a different scope |

## Verdict rules

- Any blocking cell → **NO-GO**. Unknown/unverifiable on a blocking
  dimension → **NO-GO** (unknown ≠ pass).
- Blocking items must each carry the exact evidence that would flip them —
  the gate's output is an evidence request list, not a mood.
- Ship-with-awareness risks (non-blocking) each need a monitoring plan and
  an owner, otherwise they escalate to blocking.
- Overrides are human decisions routed through `human-approval-boundary`
  and recorded as overrides — the gate never relabels a NO-GO.

## Common evidence sources

- Branch protection / pipeline config → the required-check list
  (`ci-pipeline-architect` design).
- CI run API/UI filtered to the exact gated tree SHA → check states + links;
  verify the final shipping SHA after an auto-deploying merge.
- Artifact registry metadata → provenance fields.
- Migration PR + `secure-migration-reviewer` report.
- `rollback-runbook-author` artifact + rehearsal log.
- Flag-management system → flag states, defaults, owners.
- Dashboards/alert definitions → observability coverage
  (`observability-operator` / `slo-reliability-architect`).
- PR approvals / CODEOWNERS log → approval records.
