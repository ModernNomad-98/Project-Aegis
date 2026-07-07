# Evidence Cadence Catalog

Lookup tables for building per-control evidence specs. Everything here is a
design aid; the control catalog (`compliance-control-foundation`) decides
WHAT needs evidence, and the audit window decides the period to cover.

## Evidence types

| Type | Example | Strength notes |
| --- | --- | --- |
| System configuration | RLS policies dump, IAM policy export, branch-protection settings | Strong when extracted by query/API with date; weak as screenshot alone |
| Log/trail extract | audit-log query results for the window (`audit-log-architect` schema) | Strong when population-complete and append-only |
| Test run | CI run on release SHA, `multi-tenant-security-tester` suite result, validator output | Strong; pin to commit/date |
| Screenshot | masked UI state per `screenshot-evidence-planner` (naming, masking, metadata) | Supporting evidence; must carry build/env/date metadata |
| Ticket/record | change tickets, incident postmortems, access-review records | Strong when the system timestamps and enumerates them |
| Review minutes | management review, internal-audit report, vendor assessment | Net-new for most orgs; needs owner + calendar |
| Signed approval | `human-approval-boundary` records, PR approvals, risk acceptances | Strong; dual attribution preferred |
| Process audit | `agent-governance-audit` per-change reports | Reusable as change-management evidence |

## Cadence by operating frequency

| Control operates | Evidence cadence | Window coverage rule |
| --- | --- | --- |
| Continuously (logging, RLS, encryption) | Periodic extracts (monthly/quarterly) + config snapshot at window start/end | Extracts must tile the window with no interval uncovered |
| Per change (review, migration safety, release gate) | Per-occurrence artifact, enumerated by population | Population = ALL occurrences in window (e.g. all merged PRs) |
| Periodically (access review, backup-restore test, vendor review, management review) | One artifact per scheduled occurrence | Missed occurrence = hole; reschedule forward, never backdate |
| On event (incident, DR invocation) | Per-event bundle (timeline, postmortem) | Zero events is fine — prove the monitoring existed, not the event |

## Population patterns

- Changes: merged-PR list on protected branches for the window (`gh` query)
  — the population behind review/change-management sampling.
- Access: identity-provider user/role export at defined dates + change log.
- Incidents: tracker query by severity and window.
- Jobs/backups: scheduler history export.
- Rule: the enumeration method must be re-runnable by the auditor; "we kept
  the important ones" is not a population.

## Retention & integrity postures

| Posture | Meaning | Verdict |
| --- | --- | --- |
| Append-only / WORM | store forbids mutation | strong |
| Versioned | history preserved (git, versioned bucket) | strong |
| Access-controlled mutable | few writers, no history | acceptable, flag |
| Open mutable | shared folder, anyone edits | weak — flag, propose move |

Retention floor: audit window + engagement completion; extend per contract,
regulation, or certification-body expectation (verify with the body).

## Reuse map (shipped artifacts → evidence)

| Shipped source | Evidence it yields |
| --- | --- |
| `screenshot-evidence-planner` | naming/masking/metadata policy all screenshot evidence follows |
| `manual-test-case-creator` | stranger-executable capture steps for periodic manual controls |
| `audit-log-architect` | tenant-scoped trail extracts; population source for data-access evidence |
| CI + `scripts/` validators | per-change test evidence pinned to SHA |
| `agent-governance-audit` | per-change process-compliance reports |
| `ai-closeout-reporter` | closeout records incl. intentionally-not-done |
| `release-readiness-reviewer` | go/no-go evidence bundles |
| `incident-response-runbook` | during-incident evidence capture + postmortems |
