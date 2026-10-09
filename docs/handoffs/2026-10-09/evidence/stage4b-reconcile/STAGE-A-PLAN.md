# STAGE4B-RECONCILE-1 — Stage A plan

Status: SD-A: COMPLETE — submitted for independent Stage B audit; no Stage B verdict claimed.

Item: source-only reconciliation of issue #101 Stage 4B and package-7 dependencies.
Planner: /root/issue101_hostproof.
Start: 2026-10-09 16:46:20 UTC, captured with clock.curr_time.
Initial estimate: 20–30 active-work minutes for this Stage A assignment. Active time is not measured.
Source baseline M: 625fc66711eaf7b3ee788cbc2dff98f05f147c1c, live GitHub main read in this assignment.
Repository: ModernNomad-98/Project-Aegis, source-library Role A.
Scratch root: C:/src/Codex Projects/Project Aegis/stage4b-reconcile/.

## 1. Request, purpose and authority

The owner asked, "do it" and "add max agents to work on backlogs" in the current conversation. The coordinator subsequently assigned this agent a finite Stage A task: "Stage A source-only reconciliation plan for issue #101 / Stage 4B", owning only this scratch plan and evidence below the scratch root. This is authority to prepare this plan. It does not specify or authorize a provider execution.

The change will give the next maintainer one current, source-backed account of what is known, what is missing, and which role can resolve each gap. Existing documents span a historical SDK 0.3.281 source snapshot, APR-108's recorded SDK 0.3.283 tranche, and today's SDK 0.3.287 package declaration. Their scopes must remain distinct.

The proposed source change is one documentary increment, with three source paths. It neither completes nor grants a host run. It carries no new execution manifest, fixture bytes, register entry, installation instruction or owner approval. Later source implementation requires the separate Stage C assignment following independent Stage B acceptance.

Applicable skills read and applied:

- phased-work-handoff-designer: decision carry-forward, scope, evidence and continuation contract; references/handoff-sheet.md also read.
- change-classification-gate: docs-only classification and the file-set lock.
- The delivery workflow expressly records no installed skill as owner of writing a single change's plan. Stage A is therefore procedurally enforced by docs/delivery-workflow.md; the handoff skill is a partial fit, not a claimed Stage A authority.

Local Role A was re-observed in route002/impl: README first heading "# Project Aegis"; docs/skills-catalog.md, scripts/validate-skills.py, and artifacts/audits/skill-contract-audit-baseline.json all exist. That local clone is not asserted to be current main. Current-source findings below come from pinned GitHub reads.

## 2. Classification, blast radius and exact file scope

Governing class: docs-only. No startup instruction, skill trigger, executable, runtime dependency, gate, approval policy or tool grant changes. Approval-sensitive subject matter is described without changing its requirements. If that boundary changes, stop for reclassification and re-planning.

Stage A writes only:

1. This file: stage4b-reconcile/STAGE-A-PLAN.md.
2. Evidence and write-verification receipts under stage4b-reconcile/evidence/.

Proposed Stage C source allowlist, relative to a separately assigned source checkout:

1. NEW docs/evidence/setup/issue-101-stage4b-readiness-reconciliation-2026-10-09.md.
2. docs/roadmaps/aegis-setup-routing-plan.md — one short dated pointer near its current Stage 4B discussion.
3. docs/roadmaps/aegis-setup-package-4b-preflight-draft.md — one short dated pointer after its opening historical-status explanation.

The new note is an explanatory evidence record, not a new authority record or competing protocol. Its title/date must accurately describe the observation being published; if implementation occurs on another date, changing the path/date requires a recorded plan amendment and re-audit before source edits.

Blast radius: maintainer navigation and understanding of held work. No user-facing setup choice, runtime behavior, provider destination or release visibility is changed.

Intentionally NOT touched:

- docs/approvals/APPROVAL_REGISTER.md, including APR-108's historical text and later entries.
- The Stage 4B host-proof protocol, manifest template and synthetic fixture draft.
- tools/aegis_setup/, package.json, package-lock.json, bridge code and tests.
- AGENTS.md, CLAUDE.md, .claude/, .github/, scripts/, delivery workflow, forecast, owner-decision register and all other source paths.
- Original STAGE-4B-PREFLIGHT-DRAFT.md and STAGE-4B-FIRST-TRANCHE-GRANT-DRAFT.md, whose original bytes are unrecovered.
- Host settings, process environment, credentials, accounts, billing, VMs, private cases, holdouts and all external-system state.

No cleanup, formatting sweep or transitive documentation update is included. A newly found contradiction outside the allowlist becomes a separate finding.

## 3. Captured evidence and its limits

Machine-readable source capture: evidence/source-snapshot.json. It contains pinned URLs, source blob IDs, selected full source excerpts, the later lifecycle scan and local role evidence. A blob SHA is a Git object identity, not a SHA-256 file digest. The evidence capture is a new scratch artifact; it is not either missing historical draft.

Read-only source commands used:

- GitHub GET /repos/ModernNomad-98/Project-Aegis/branches/main returned M.
- github_fetch_file(repository_full_name=ModernNomad-98/Project-Aegis, ref=M, path=<source>) returned the source blobs recorded below.
- PowerShell Get-Content of route002/impl/README.md and Test-Path on each Role A landmark returned the heading and three True values.
- Full-register text was scanned after APR-108 with pattern AEGIS-APR-108|APR-108|Stage 4B|first.tranche: zero matches; subsequent headings run APR-110 through APR-121. This proves no matching later lifecycle text in that pinned register, not absence of a later instruction outside it.

Principal source bindings:

| Source at M | Blob SHA |
| --- | --- |
| AGENTS.md | 116450fd754c8040130b73d9816c373bba02d24b |
| CONTRIBUTING.md | dc7fefbd9842167e8225bae2f3f6d50f4dd2acd5 |
| docs/delivery-workflow.md | 720a858083f67a4fb91648517a0a918c68cd1d4b |
| docs/approvals/APPROVAL_REGISTER.md | 7ee0e822398382101900c79aea9962b540a86c57 |
| docs/roadmaps/aegis-setup-routing-plan.md | 2b2bbe497b0557029af30f5638aa39e58a13ca3b |
| docs/roadmaps/aegis-setup-package-4b-preflight-draft.md | 66240809a49f97fc486980176fbffa2e62f394bb |
| docs/roadmaps/aegis-setup-package-4b-preflight-manifest-template.md | 68ce3d962526bcc477cf121e48fd52fedcf5ea3a |
| docs/roadmaps/aegis-setup-package-4b-host-proof-protocol.md | 252bb2f5cab710a220eaa4bc7ba7a4081d65e055 |
| docs/roadmaps/aegis-setup-package-4b-synthetic-case-fixtures.md | 5cba1ca0126e083cbed0e8a788cf95accc5bd280 |
| tools/aegis_setup/host_bridge/package.json | 83541407e4fca04b3874fc6b60d969a3c3bf608d |

Reference URLs and exact APR-108 excerpts are in the evidence JSON. Required further reads for implementer/reviewer: the entire then-current register and its preamble, then-current AGENTS.md, CONTRIBUTING.md, docs/delivery-workflow.md and docs/offline-ci.md. Refresh live main and compare source identities before relying on M.

Historical-draft recovery is limited:

- Prior bounded planner filename search under the old source artifacts and current coordinator directory did not recover either draft.
- The coordinator reported a whole-current-workspace filename search with zero matches; that is relayed evidence and must be labeled as such if retained.
- No global absence claim is made. No original bytes, original file size or original digest were independently re-derived.
- Do not recover secrets, session credentials, private BER cases or sealed holdouts while locating public planning material.

Preserve these as register-attributed original SHA-256 values, explicitly NOT RE-DERIVED:

| Named original | APR-108 recorded SHA-256 |
| --- | --- |
| STAGE-4B-PREFLIGHT-DRAFT.md | 2148226e26d4653c4f23c68d99c81550b2d691a2bb2e6b1a8f3687ad2b493bfa |
| STAGE-4B-FIRST-TRANCHE-GRANT-DRAFT.md | 7fc600faa59dabdcc418fa8e7575909b2971d5ab08442129c3ff998c54d62c71 |

Never create a file under either historical original name, claim reconstruction, replace its recorded hash, infer missing owner wording, or promote this source capture into that missing evidence.

## 4. Content contract for the new source note

Use concise prose for the conclusion and tables for the facts below. Explain SDK, provider request, host, tranche, frozen preflight and NOT RUN in plain terms on first use. The new note must be understandable without reading this scratch plan.

### 4.1 Opening conclusion and version distinction

Opening conclusion: source-only reconciliation; first-tranche execution remains blocked under APR-108; full host proof, helper comparison and package-7 release are unfinished.

| Record | What is established | What is not established |
| --- | --- | --- |
| Historical 2026-09-26 preflight source snapshot, source merge 658fa22edbfde2c953f7d21678d08baa79b75052 | Declared SDK 0.3.281, API SDK 0.94.0, MCP SDK 1.30.1, Zod 4.6.5 and its source hashes | Current installed runtime or runtime selection |
| APR-108 recorded first tranche | Pinned SDK 0.3.283 and exact returned model identity claude-sonnet-5-5; operative authority expressly unestablished | Start permission, model acceptance, current binary availability or host compatibility |
| Package declaration at M | SDK 0.3.287, API SDK 0.94.0, MCP SDK 1.32.0, Zod 4.6.5; Node range >=24 <25 | Runtime installation, successful loading, a replacement execution grant or actual-host proof |

The historical draft is explicitly a historical snapshot; do not call its values an erroneous current claim. Do not silently upgrade or downgrade a runtime to align the records. A later runtime/profile choice and its authority belong to a separately reviewed forward decision.

### 4.2 APR-108 prerequisite map

Every row must cite APR-108 and show current fact, missing evidence and resolving role. Row identifiers below are local evidence-map keys, not new approval-register IDs.

| Key | Current source-backed fact | Missing evidence / permitted next resolution | Responsible role |
| --- | --- | --- | --- |
| P1 — authorizing act | Scope and ceiling provenance is recoverable in APR-108; a dated owner-authored tranche instruction is not established there. Authority unestablished is not authority revoked or denied. | A current direct owner decision answering APR-108's prospective request, or a verified recoverable owner-authored source. Do not fabricate wording or treat a generic backlog instruction as the exact provider grant. | Owner; later separately assigned recorder preserves the actual decision forward. |
| P2 — run host and agent instance | APR-108 cites historical owner-decision aliases win-agent-host-01 and stage4b-operator-01, but explicitly keeps prerequisite 2 open. The drafting host is not the run host. | Owner disposition identifying/designating the actual run host and operator instance; authorized capture of applicable host facts later. No host probing in this batch. | Owner and later authorized agent-operator; independent reviewer checks binding. |
| P3 — source revision | M is a current source observation; it is not a run-source selection. The three SDK versions above differ. | A source/profile revision frozen for the proposed run; re-measured source/lock/script digests if main moves. Any runtime substitution needs an explicit forward scope disposition. | Later packet maintainer and independent reviewer; owner where scope changes. |
| P4 — fixture identity | >=99 variations remain proposals; the repository eight-case draft is not the frozen variation set. Original wider drafts are unrecovered here. | New or recovered exact fixture bytes, frozen exact required-attempt count N and verified digests before any run. New work must be labeled a new revision; this batch creates no fixtures and asserts no historical equivalence. | Separately assigned fixture author and independent reviewer. |
| P5 — allowed paths | Invented synthetic checkout and immediately outside sentinel are required; no actual path is established. | Separately authorized creation/binding and path identity. This batch may document fields, never create a run checkout or sentinel. | Later authorized operator and packet maintainer. |
| P6 — frozen preflight | APR-108 explicitly says incomplete; fixture digest and signing roles are unresolved. Its binding includes provider/endpoint, credential custody, price/allowance, abort margin/meter, persistence, settings/tools and signoffs. | Complete reviewed profile binding all fields, named signing roles and fixture digests. Keep UNKNOWN fields visible. Record a new draft only under its own identity; do not assert a frozen ready manifest. | Packet maintainer, independent reviewer, owner/account holder for account facts; later authorized operator for effective observations. |
| M7 — per-request counts | UNKNOWN, explicitly measured by the tranche rather than awaited in advance. | Authorized observation of actual provider requests, retries and subagent counts; missing counts undermine the procedural ledger and require the recorded stop response. | Later authorized operator; reviewer evaluates evidence. |
| M8 — concurrency | UNKNOWN, explicitly measured by the tranche; the ceiling includes subagents. | Authorized observation that concurrency can be constrained to one; do not invent enforcement. | Later authorized operator; reviewer evaluates evidence. |
| U1 — network discrimination | Loopback/external discrimination is an accepted unknown in APR-108; T1–T5 do not test it and network probes are excluded. | Remains unknown in this batch and tranche; any later boundary proof needs its own scope. | Later separately authorized boundary-proof owner. |
| U2 — ZDR and retention | Zero-data-retention status is unknown; APR-108 records default retention with exceptions, not a guarantee. Account access is forbidden by the tranche. | Owner/account evidence under separate authority if required later. Do not visit account/billing pages or make a fresh policy/pricing claim from historical text. | Owner/account holder and independent privacy reviewer. |

Do not resolve P2 merely from the two historical aliases. Do not turn M7/M8 into impossible preconditions. Do not turn U1/U2 into verified capability or silently add new run scope.

### 4.3 Scope, budget and entitlement distinction

The note should summarize the recorded shape with citations, explicitly subordinate to APR-108. It creates no second normative budget register.

- First tranche: T1–T5 only, up to 10 attempts, at most 40 actual provider requests, US$6, 1,500,000 input tokens, 200,000 output tokens, 60 elapsed minutes, 25 active minutes and five minutes per attempt. Concurrency is one including subagents.
- T1's second attempt is allowed only after an exact claude-sonnet-5-5 first response and no stop event. A different identity, alias, suffix, missing identity or refusal stops the tranche; no confirmation retry repairs it.
- The larger recorded whole-experiment ceiling is 220 actual provider requests and US$50. This tranche cannot spend the remaining 180 requests/US$44. The larger scope is not authorized by this note or automatically released by successful observations.
- Required coverage is >=99 proposed variations, not 198 mandatory runs. Exact N remains unfrozen. The budget multiplier threshold is 220/N, not a constant; T1–T5 contribute zero credited host-proof coverage.
- The record acknowledges no runtime/provider hard cap. Reservation bookkeeping and procedural stop rules are not automatically enforced limits. Do not claim a hard cap or reliable request meter already exists.
- No account entitlement, available balance, fresh price, installed runtime or remaining allowance has been verified by this batch. A numerical ceiling is not evidence of access, affordability or spend already consumed.
- The owner sets the API key in the host-process environment. The operator never receives, reads, requests, records or transmits the secret. The note must not include a credential lookup, environment dump or request for the key.
- No full variation run, case-08 path enumeration, second tranche, install, dependency change, VM, private BER input, account/billing lookup, live provider check or external retrieval is part of this reconciliation.

Use the source's exact limitations. Where a detailed stop rule is needed, link to APR-108 rather than restating a new exhaustive rule list.

### 4.4 Dependency order and package 7

Show this order as a compact numbered list, preserving distinct outcomes:

1. This source-only reconciliation and independent documentary review.
2. Resolve the operative owner act and remaining P2–P6 facts through separately assigned/authorized work.
3. A complete unchanged frozen preflight plus applicable authority before any first-tranche attempt.
4. Authorized T1–T5 observation and independent interpretation of B3/model identity and request multiplier; zero full-proof coverage credited.
5. Separate reviewed scope and authority for full Stage 4B host proof; no automatic second tranche.
6. Later approved predeclared comparison and selection using Aegis and deterministic-rule baselines and the retained candidate shortlist.
7. Conditional package-5/6 integration only if selected and separately authorized.
8. Exact-release package-7 validation, supported host/OS evidence and independent UX/security/authority review.

Aegis-only may win the comparison; it is not an automatic shortcut past the owning plan's package-7 gates. APR-102's one-integration-at-a-time and tested-profile support policies remain binding. No change is proposed to normal setup choices in this batch.

End with the exact unresolved owner question from APR-108's prospective request, framed as a future decision after the documentary packet is reviewable. Do not ask again for already recoverable ceiling choices or invent a grant. An affirmative authorizing-act answer alone leaves P2–P6 open.

### 4.5 Two pointer edits

- Setup plan: add a dated paragraph linking the new reconciliation note and APR-108, stating that it records a blocked first tranche and no host proof/release completion. Preserve historical delivery narrative, readiness matrix and all existing scope statements.
- Historical preflight draft: add a dated paragraph linking the note for current source/record distinctions. Preserve its original historical source commit, values and hashes unchanged.
- Use clear relative repository links. No output date, budget or unknown status should silently replace historical text.

## 5. Acceptance criteria for this documentary change

All criteria below are assessed at Stage D against Stage C's immutable base, head, resolved tree and handoff evidence. For AC8, an explicit UNRUN record with its concrete resolution is evidence that a check was not run, never a pass or a completed Stage E disposition. No criterion requires later-stage evidence or a live run, or declares runtime success. Live observations are out of this change's scope, not silently covered by local checks.

| ID | Checkable criterion | Required evidence |
| --- | --- | --- |
| AC1 | Exactly the three source paths in section 2 change; other source paths and all original historical content outside the two new pointer insertions remain unchanged. | Exact base/head diff name list and unified diff; before/after unchanged historical excerpts. |
| AC2 | The note binds its source observation to one exact commit, distinguishes .281 historical / .283 recorded tranche / .287 current-at-M declarations, and makes no installed-runtime or substitution claim. | Source values and blob identities independently checked at the cited commit; per-record table reviewed. |
| AC3 | All P1–P6, M7–M8 and U1–U2 rows carry source-backed fact, missing evidence and role; M7/M8 remain measured-by-tranche and U1/U2 stay unknown. No unresolved field is called complete. | Independent row-by-row comparison against APR-108 and the template; no missing row. |
| AC4 | Both unrecovered original hashes are reproduced exactly as register-attributed/not-rederived, bounded recovery limitations are explicit, and no original reconstruction or invented owner words are presented. | Exact string comparison with APR-108; filenames and note content inspection. |
| AC5 | First-tranche subceilings, parent-ceiling distinction, exact T1 identity stop, zero coverage credit, >=99 versus frozen N, no hard-cap claim and credential custody match APR-108. | Reviewer checklist keyed to the cited APR-108 clauses; any mismatch is a revision finding. |
| AC6 | Dependency order preserves separate actual-host proof, approved comparison/selection, conditional helpers and package-7 review; Aegis-only is not presented as bypass; APR-102 policy unchanged. | Comparison with setup plan package-7 section and APR-102; no release/savings/support claim added. |
| AC7 | Both pointer links resolve to the new note; note links/anchors resolve; prose/tables render readably and define unfamiliar terms. The note remains evidence-only and clearly names execution/readiness gaps. | Link resolution and rendering sanity receipt plus independent prose review. |
| AC8 | At Stage C/D, the handoff records C's immutable base/head/tree, command journal, local check results or explicit UNRUN records with concrete resolutions, and evidence that implementation stayed within the authorized documentary scope; no provider/VM/account action, install, grant issuance or settings change occurs in this batch. | Base B and candidate H commit identities with H's resolved tree, changed-path diff, command journal, and each local check's command/result/output or an explicit UNRUN entry stating what resolves it. Stage D verifies these records and scope evidence; skipped/unrun is never labeled pass. |

Plan-declared criteria not verifiable at Stage D against the candidate and C handoff: none. AC8 assesses the completeness and truth of C's local evidence, including explicit UNRUN records and their resolutions; it does not require Stage E to have run. Stage E owns its validation disposition. Subsequent applicable exact-head CI, final-review and merge evidence are forward duties of their respective holders under docs/delivery-workflow.md, not prerequisites for Stage D acceptance. Those later duties remain required. Actual-host behavior, entitlement, spend availability, runtime installation, full-case proof and release readiness are explicitly outside these documentary acceptance criteria and remain UNKNOWN/NOT RUN as applicable.

## 6. Proportionate validation plan and hard stops

Stage A: read current sources, persist this plan and its evidence within the assigned scratch directory, then read back and compute file SHA-256. Author write-integrity checks are not a Stage B audit.

Stage C/E validation for the later three-file source candidate:

- Read-only git status and exact base/head changed-path enumeration; git diff --check.
- Human comparison of the new note's tables against pinned sources, including all hashes/numbers and the current lifecycle scan.
- Resolve every new relative link and anchor locally; inspect Markdown rendering or an equivalent parsed preview. Do not publish a site or execute embedded content.
- Required checks from CONTRIBUTING.md: python scripts/validate-skills.py and python scripts/tests/test_validator.py, with command, exit code and output retained. Use an already available compatible runtime; no dependency installation is authorized by this plan.
- Re-read docs/offline-ci.md and the exact candidate workflow for applicable CI coverage. Do not infer host proof from any repository check. Record actual path-filter skips and unrun local checks with their resolution; no broad optional runtime testing for a prose-only change.
- Distinct Stage D and F reviewers apply AC1–AC8 and the existing workflow. No self-review or same-agent stage reuse.
- Any required command blocked by the environment is recorded UNRUN with a concrete resolution under the existing workflow; no workaround install or scope expansion.

Stop this documentary lane and return for re-plan/re-audit if:

- A current owner instruction or later lifecycle event conflicts with the captured state.
- The proposed writing would change a grant, policy, mandatory precondition, runtime version, fixture set or user-facing integration behavior.
- Source paths expand beyond the three-file allowlist.
- Original drafts are found but fail their recorded hashes, or owner text cannot be established; record the finding without treating it as authority.
- A tool requests host/provider/account/credential/VM activity, installation, or external retrieval beyond the explicitly allowed read-only Project Aegis source-repository evidence.
- A materially moved main changes the facts this plan records. Do not simply relabel M. Re-derive affected evidence and revise the plan for a new independent B verdict.

No source execution or public publication is part of this Stage A assignment. A future C–G assignment uses the repository's existing authority and gate rules; this plan grants none.

## 7. Carry-forward and continuation contract

Binding source decisions carried forward, without new authority:

| Binding ID | Still binding | Pointer / effect in this plan |
| --- | --- | --- |
| AEGIS-APR-108 | yes, as the recorded held shape | No operative authority claimed; P1–P6 open, M7/M8 measured later; historical text untouched. |
| AEGIS-APR-102 | yes | Gradual integration and release visibility policy; proof and release remain separate. |
| SD-A through SD-G | yes | docs/delivery-workflow.md owns the stage rules; this plan changes none. |
| MG1 through MG5 | yes | Existing delivery-workflow merge-gate IDs; no condition changed or waived. |

This plan's AC and P/M/U keys are local labels only. They are not owner decisions, register allocations or competing governance definitions.

Per-stage handoff must carry:

- The accepted plan revision/hash and its independent B verdict.
- Exact source base/head/tree and the identities of stage holders.
- Changed-files and intentionally not-touched lists.
- Each command/tool invocation and its distinctive observed result.
- Explicit deviations; any material deviation goes back through plan/audit.
- Unrun checks, unresolved live facts and the next stage's entry evidence.

Stage A changed files: this scratch plan and evidence under its owned directory.
Stage A not touched: every source checkout, Git state, remote issue/PR/settings, original draft and live system listed in section 2.
Stage A deviations: none.
Stage A completed evidence is source observation and an authored plan only. No independent ACCEPT verdict, host result, release result or final validation is claimed.

Next stage: a different agent audits the exact captured SHA-256 of this plan, using its own current-source checks and the evidence snapshot. If ACCEPT, the coordinator assigns a different Stage C holder in a suitable isolated checkout. The planner must not hold B, C, D, E, F or G for this change.

The measured finish time, wall duration and this file's final SHA-256 are recorded separately under evidence/ to avoid a self-referential file digest. Active time remains unavailable; the elapsed wall time is an imperfect comparison with the initial 20–30-minute active-work estimate.
