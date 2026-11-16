# OWNER DECISION TABLE ADDENDUM — new items from task-11 (2026-11-10)

Adds the newly identified unresolved items to OWNER-DECISION-TABLE-2026-11-10.md (45553dde...). No authority claimed; no repo/settings/host action.

| # | Decision | Known facts (task-11 evidence) | Why not resolvable internally | Recommendation |
| --- | --- | --- | --- | --- |
| T12 | Missing Stage-B plan audits for historical Experience items 3, 4, 8 (PRs #962/#963/#967) | All three delivered/merged; Stage B marked UNRUN or absent; a retrospective audit cannot retroactively certify a pre-merge gate | Governance/process disposition is owner-held; cannot convert historical UNRUN to PASS | Record the three as historical process defects; do not re-open/re-merge; if desired, commission a clearly-labelled retrospective review that does not cure the gate |
| T13 | Programme-level closure disposition for Experience items 3 and 4 | Acceptance evidence exists at delivered heads; closure gating acts missing (Stage-B, at-head delta applicability, closure entries) | Closure disposition is owner-held | Keep delivered-but-not-closed until at-head applicability task and a closure entry exist; do not claim closed items 3/4 |
| T14 | Hosted proof for Experience item 8 (acceptance row P3-08-01) | Delivery complete; hosted schema-only PR proof UNRUN; schema/workflow unchanged since #967; local routing proof is supporting only | Requires an authorized schema-only PR hosted run (repo/CI action) | Authorize one bounded schema-only PR later; do not substitute local evidence |

Also noted for planning (not owner decisions): the task-11 item labels did not match the package's actual bindings; the re-derivation used the A-ROWS work-item definitions (item 3 = permission-test omissions, item 4 = starter-selector checks, item 8 = schema-only contract tests). The programme execution plan's Experience descriptions will be corrected in the next planning edit.

Recorded by: Lead (DeepSeek Harness; route deepseek-flash). Local record only.