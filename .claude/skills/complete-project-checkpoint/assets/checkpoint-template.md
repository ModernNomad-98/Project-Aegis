# Complete project checkpoint template

Fill every original field below. Keep all headings/fields; use evidence, UNKNOWN or NOT APPLICABLE with a reason. Added tables may link to durable complete supporting records. Do not turn template labels into claimed results. Follow the [checkpoint contract](../references/checkpoint-contract.md) and full [original procedure](../references/owner-prompt-original.md).

## A. CHECKPOINT IDENTITY

- Checkpoint ID:
- Timestamp:
- Project:
- Owner:
- Workspace:
- Repository/system:
- Branch/revision, if applicable:
- Current objective:
- Current milestone:
- Checkpoint location:
- Verification status:

### Added capture identity and scope

- Generation ID and state (PROVISIONAL / FROZEN / SUPERSEDED):
- Capture start / final evidence cutoff / timezone:
- User invocation and authorized destination evidence:
- Source allowlist and exclusions applied before discovery, reading or hashing:
- Project boundaries and last verified safe state:
- Linked manifest location (do not insert a circular self/manifest hash):

## B. AGENT STATUS

- Coordinator:
- Participating agents:
- Current assignments:
- Actual models:
- Agent completion results:
- Final updates:
- Outstanding agent work:
- Blocked/unavailable agents:
- Handoff status:

### Added finite-work roster and final-report reconciliation

| Agent/process ID | Parent and holder | Finite or recurring | Assignment and acceptance conditions | Permissions | Actual model/provider/version/effort or UNKNOWN | Last observation/progress | Terminal evidence | Acceptance disposition | Final report/artifacts | Blocker and exact continuation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

- Initial roster source and timestamp:
- Later-discovered pre-existing children/processes and reconciliation:
- Last mailbox/report check and material late results:
- Reachable RUNNING items still awaited:
- Evidence permitting any terminal incomplete closeout:
- Coordinator capture/write/readback excluded from the pre-existing barrier:

For every final report retain work performed, changed and NOT-touched surfaces, checks actually run, reviews, failures, unfinished items, pending approvals, followups and next action. A terminal receipt is distinct from deliverable acceptance.

## C. CURRENT PROJECT STATE

- Project objectives:
- Current priorities:
- Workstreams:
- Current milestone:
- Architecture/operational state:
- Constraints:
- Current blockers:
- Important dependencies:

### Added purpose and milestone context

- Owner's actual stated mission, strategic/immediate objectives and sources:
- Business/technical purpose and success criteria:
- Scope boundaries and known deadlines (do not infer):
- Completed and future milestones:
- Cross-project/workstream relationships and separate restrictions:

## D. COMPLETE WORK INVENTORY

- Completed items:
- Active items:
- Pending items:
- Not-started items:
- Blocked items:
- Deferred items:
- Rejected items:
- Cancelled items:
- Unknown-status items:
- Backlog source references:

### Added complete work ledger

| Item ID | Objective/workstream | Status | Priority | Holder | Workflow stage | Evidence/outcome | Acceptance criteria | Remaining work or prior attempts | Dependencies/approvals | Next action | Source and observed time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Retain COMPLETED, ACTIVE, BLOCKED, PENDING/READY, NOT STARTED, DEFERRED, REJECTED, CANCELLED and UNKNOWN items. Include completion records/followups for completed work; original requirement, reason and resumption conditions for deferred work; decision/restrictions for rejected/cancelled work. Do not drop older relevant backlog. Use NONE only when absence is supported, otherwise UNKNOWN.

## E. AGENT RULES & MODEL ROUTING

- Agent hierarchy:
- Operating rules:
- Assignment ownership:
- Model-routing policies:
- Actual model assignments:
- Fallback policies:
- Review independence:
- Provider restrictions:
- Concurrency and budget limits:

### Added role, routing and enforcement records

| Role/assignment | Existing holder | Actual observed model/provider/version/effort | Preferred/planned routing | Fallback/switch authority | Tools/context/budget/concurrency/retry limits | Source | Documented versus enforced |
| --- | --- | --- | --- | --- | --- | --- | --- |

- Delegation/communication/escalation/reporting/handoff rules:
- Planning/author/validator/reviewer/approver separation:
- Security/testing/review responsibilities:
- Creation/termination permissions and failure/retry policy:
- Unavailable model metadata and impact:

## F. WORKFLOWS & FRAMEWORKS

- Applicable frameworks:
- Skills and procedures:
- Current workflow stages:
- Completed stages:
- Remaining stages:
- Stage acceptance criteria:
- Required independent reviews:
- Existing validation:
- Workflow exceptions:

### Added per-item workflow evidence

| Item ID | Applicable process/skill and observed version | Current stage | Completed stages with evidence | Remaining gates and criteria | Existing holders | Approved exceptions | Evidence validity limits |
| --- | --- | --- | --- | --- | --- | --- | --- |

- Installed/available versus merely mentioned skills:
- Actual skill use, purpose, invocation/output evidence and limitations:
- Documentation, change-management, security/compliance, release/delivery requirements:

## G. AUTONOMY & APPROVALS

- Standing permissions:
- Conditional permissions:
- Owner-only actions:
- Prohibited operations:
- Merge approvals, if applicable:
- Deployment authorizations, if applicable:
- HOLD/STOP decisions:
- Pending approvals:
- Authorization sources:

### Added authority lifecycle and consumption

| Action | AUTHORIZED / CONDITIONAL / OWNER APPROVAL REQUIRED / PROHIBITED / UNKNOWN | Owner and exact source | Project/repository and scope | Exact head/tree/body/inventory where applicable | Preconditions/restrictions | Expiry/revocation/supersession | Consumed? | Outcome/evidence availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Cover task selection, delegation, implementation, validation, commits/pushes, PRs, reviews/CI, merges, deployment/production, infrastructure/integrations, model/provider changes, spending, destructive operations and scheduling. Preserve STOP/HOLD/GO/NO-GO/escalation records. A consumed one-shot action with missing output remains consumed/result UNKNOWN; it is not replay permission. Source grants do not transfer to consumers.

## H. DECISION REGISTER

- Approved decisions:
- Rejected decisions:
- Deferred decisions:
- Pending decisions:
- Superseded decisions:
- Conflicting instructions:
- Outstanding owner questions:

### Added complete decision provenance

| Decision ID/subject | Options and rationale when known | Actual decision/status | Decision maker/date/source | Affected work | Conditions | Current applicability/supersession/revocation | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |

- Conditional and revoked approvals:
- Conflicts with all source references (no invented resolution):
- Questions: ID / delivered to owner / acknowledgment / substantive answer / execution milestone / next due check, separately:

## I. TECHNICAL / OPERATIONAL EVIDENCE

- Current revisions:
- Work artifacts:
- Test results:
- Review results:
- CI/CD status, if applicable:
- Security findings:
- Operational verification:
- Evidence references:
- Known evidence limitations:

### Added observed technical or equivalent operational state

- Repository/workspace/worktree/branch/base/head/tree observations and times:
- Dirty, untracked, ignored or unsaved material in capture scope:
- Changed and intentionally NOT-touched surfaces; ownership:
- Issues/PRs, full relevant review findings, failed review attempts and dispositions:
- Test/build/CI commands actually run, result receipts and revisions; historical versus fresh:
- Deployment, environment, database/migration and infrastructure state where applicable:
- Known failures, security findings, technical debt and production restrictions:
- Non-software equivalent systems/artifacts/approvals or NOT APPLICABLE reasons:

No automatic Git mutations or production reads/writes are implied by capture.

## J. SCHEDULED AGENT WORK

- Active schedules:
- Recurring monitoring:
- Agent reminders:
- Deferred follow-ups:
- Failed schedules:
- Blocked schedules:
- Next known execution:
- Scheduling mechanism:
- Session-persistence status:
- Recovery instructions:

### Added schedule identity and persistence ledger

| ID/title | Purpose/owner/model | Host/session/mechanism | Config location and observed config | Schedule/timezone/trigger | State | Last verified execution/delivery | Next run with evidence or UNKNOWN | Outstanding work/dependencies/approvals | Notification intent | Session persistence evidence | Restoration instruction/authority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

- SCHEDULED / REMINDER / PLANNED / WAITING / COMPLETED / FAILED / CANCELLED / UNKNOWN distinctions:
- Recurring/unowned activity still ACTIVE or UNKNOWN:
- Any separately authorized schedule change and before/after list receipts:
- Duplicate-prevention identity/intent checks:

No default pause/delete/recreate/retarget/rearm. Historical schedule timing is not current configuration. Missing scheduler access is UNKNOWN, not permission to create another watch.

## K. RISKS & UNKNOWNS

- Open failures:
- Current blockers:
- Material risks:
- Missing evidence:
- Inaccessible information:
- Conflicting records:
- Unresolved dependencies:
- Unknown status items:

### Added risk and recovery gap ledger

| ID | Description/impact | Evidence/status | Owner | Required resolution | Next action | Capability/access needed |
| --- | --- | --- | --- | --- | --- | --- |

Retain incomplete criteria, missing approvals, stale/conflicting information, inaccessible artifacts and owner questions. Do not fabricate resolutions to make a save appear complete.

## L. ARTIFACT MANIFEST

- Project plans:
- Architecture/design documents:
- Task and backlog records:
- Agent work records:
- Source/change artifacts:
- Reviews/audits:
- Decision logs:
- Approval records:
- Schedule configurations:
- Previous checkpoint references:
- Supporting checkpoint files:
- Verified storage locations:

### Added authorized source coverage

| Source ID/project | Actual locator | Observed time/revision | FULL / BOUNDED / NOT READ | Material facts captured | Exclusion/access gap and reason | Recovery requirement |
| --- | --- | --- | --- | --- | --- | --- |

### Added artifact identity and portability

| Artifact ID/purpose/task | Actual location | Version/revision | Byte count/SHA-256 when measured | Observed time/read coverage | Storage class | Access/readback evidence | Dependencies | Portable to target host? | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

- Memory/knowledge: documented preferences, conventions, failed approaches, tradeoffs, decisions and next-stage context with source/scope/supersession; no hidden reasoning or permanent-memory edits:
- Unsaved/dirty/untracked content: authorized preserved bytes or proven durable reference, and gaps:
- Excluded sensitive/restricted material: safe locator only, without reading/hash/copy of forbidden content:
- Non-circular manifest scope and excluded later receipt/card components:

### Added verified recovery levels

| Level | VERIFIED / PARTIAL / UNRUN / FAILED | Evidence and limitations |
| --- | --- | --- |
| Checkpoint readable | | |
| Required local artifacts accessible | | |
| Source reconstruction | | |
| Runtime reconstruction | | |
| Off-device recovery | | |

## M. EXACT NEXT ACTIONS

- Highest-priority unfinished objective:
- First executable task:
- Assigned agent:
- Required model/routing:
- Current workflow stage:
- Required inputs:
- Dependencies:
- Existing evidence to reuse:
- Approval requirements:
- Acceptance criteria:
- Next tasks in priority order:
- Deferred or conditional follow-ups:

### Added cold-start continuation

- Resume-card location:
- Ordered required reads with exact identities where available:
- First permitted fresh verification and its existing authority:
- Differences that require affected evidence/review refresh:
- Existing agent/task/schedule identities to reuse and avoid duplicating:
- Last verified safe execution state:
- Held/cancelled/deferred work that must not auto-resume:
- Exact permitted action after verification; separate owner-gated alternatives:

## N. CHECKPOINT VALIDATION

- Agent completion barrier:
- Completeness audit:
- Missing information:
- Persistence verification:
- Supporting-file verification:
- Final checkpoint classification:
- Exact recovery location:
- Additional execution after checkpoint: NONE.

### Added independent status axes and final receipt

- Persistence: VERIFIED / PARTIAL / FAILED, with exact readback evidence:
- Finite-work barrier: SATISFIED / INCOMPLETE / UNKNOWN, with terminal/report evidence:
- Content: COMPLETE_WITHIN_DECLARED_COVERAGE / GAPS / UNVERIFIED:
- Execution per coordinator / finite work / recurring or unowned services: STOPPED / ACTIVE / UNKNOWN:
- Original “Additional execution after checkpoint: NONE.” is this coordinator's no-new-dispatch commitment, not a claim that recurring/unowned services stopped. Their actual states are recorded above and in J.
- Final classification: normal complete save / INCOMPLETE RECOVERY CHECKPOINT / PROVISIONAL, with reason:
- Last late-update check, superseded generations and correction links:
- Master / manifest / resume-card identities, in a separate non-circular final receipt:
- Completion marker/promotion evidence or explicit absence:
- Verification actually run / not run / failures:
- No implementation/delivery/production completion inferred from persistence:

### Full original completeness audit — retained under N

#### 19. MANDATORY CHECKPOINT COMPLETENESS AUDIT

Before finalizing the checkpoint, verify that the following have been addressed:

- [ ] Every known running agent is accounted for.
- [ ] All finishable authorized assignments are complete.
- [ ] Incomplete assignments are accurately classified.
- [ ] Final agent updates have been collected where accessible.
- [ ] Current objectives and owner priorities are captured.
- [ ] Project scope and constraints are captured.
- [ ] All known workstreams are captured.
- [ ] Complete known backlog is captured.
- [ ] All active tasks are captured.
- [ ] All pending, blocked, and deferred tasks are captured.
- [ ] Agent roles and operating rules are captured.
- [ ] Actual models and routing policies are captured.
- [ ] Applicable frameworks, skills, and workflows are captured.
- [ ] Current workflow stages are captured.
- [ ] Autonomous permissions are captured.
- [ ] Approval and merge conditions are captured where applicable.
- [ ] Material decisions and decision history are captured.
- [ ] Known schedules and reminders are captured.
- [ ] Relevant repository/operational state is captured.
- [ ] Existing tests, reviews, and evidence are captured.
- [ ] Relevant artifacts are durably indexed.
- [ ] Risks, blockers, and uncertainties are captured.
- [ ] Next actions and future priorities are captured.
- [ ] Exact recovery instructions are captured.
- [ ] No known material information has been silently omitted.
- [ ] No unsupported completion claims were introduced.
- [ ] No critical checkpoint references depend solely on expiring session data.

For each check, record:

- PASS.
- GAP.
- UNVERIFIED.
- NOT APPLICABLE, with reason.

A category does not pass simply because it contains text.

If a material gap remains, document it and classify checkpoint completeness accordingly.

Do not claim absolute completeness beyond the accessible information reviewed.

### Audit evidence per item

| Original checklist item | PASS / GAP / UNVERIFIED / NOT APPLICABLE | Evidence or reason | Followup/owner |
| --- | --- | --- | --- |

Record one row for each of the 27 original checklist items. Text presence alone is not PASS.
