# Storage-policy handoff: Stage A plan, revision 1

**SD-A: COMPLETE — planning artifact only.** No implementation option is selected. Stage B may audit this captured plan; Stage C is held for the owner's explicit selection of option R or E and scoped implementation authority. Completion here does not mean the storage backlog item is delivered.

This plan is for the coordinator and the independent plan auditor. It defines a finite correction to the handoff between `file-upload-storage-architect` and `rls-policy-auditor`, with two viable implementations and measurable limits. RLS means row-level security; SQL means Structured Query Language; DDL means data definition language; PR means pull request; CI means continuous integration. Numbered #115 and #127 below identify roadmap rows, not GitHub issues.

## Record and authority

| Field | Value |
| --- | --- |
| Work item | Storage-policy handoff backlog — Stage A PLAN |
| Holder | `/root/storage_handoff_plan`; Stage A only |
| Requested model / reasoning | Astra / xhigh, as assigned; runtime setting independently unverified |
| Start observed | 2026-10-09 07:27:29 UTC |
| Estimate | 15–20 minutes active work; recorded after initial source discovery, not retrospectively claimed as a pre-start estimate |
| Exact source commit M | `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf` |
| Source tree | `785ae6aac5ee884751c1da4911c7bebe8d6c7cf8` |
| Read-only object source | `C:\src\Codex Projects\Project Aegis\metricsfix\implementation` |
| Planning output | `C:\src\Codex Projects\Project Aegis\storagehandoff\PLAN-rev1.md` |
| Finish and checksum | Recorded after read-back in sibling `PLAN-rev1.receipt.json`; the file's checksum is external to avoid a self-referential hash |

The assignment authorizes **Stage A PLAN only**, scratch-file creation under `storagehandoff`, and read-only source inspection. The coordinator reports the owner's active request as keeping work moving on backlogs while PR #686 waits. That report does not select this implementation. No source edit, commit, push, PR, external publication, live provider action, credential access, database connection, DDL, or skill creation is authorized by this plan. No action on PR #686 is part of this item.

Read at M: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, the complete `docs/delivery-workflow.md`, and the approval-register preamble and introductory grant text. The register's [preamble, lines 3–17](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/docs/approvals/APPROVAL_REGISTER.md#L3-L17) requires scope and lifecycle checks before relying on a grant. This stage relies on the assignment's limited planning authority, not on a historical merge grant. Future C and G holders must inspect current authority themselves. Role A was corroborated by the README heading, catalog, validator, audit baseline and origin URL; the enclosing scratch folder is not asserted to be a source checkout.

## Evidence and problem statement

All M line references mean `git show M:path`, not the checkout's working branch. M is the coordinator's captured main revision and is locally verified as a commit; this planner did not query live GitHub main. **PROVEN** means observed source content or command output, not runtime effectiveness.

| ID | Status | Evidence and implication |
| --- | --- | --- |
| E1 | PROVEN | Sender [SKILL.md lines 3, 51–53, 112–113, 150, 190–191, 237–239](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/file-upload-storage-architect/SKILL.md#L51-L53) promises existing storage RLS/bucket-policy review by `rls-policy-auditor`. Its behavior case also makes that handoff (`evals/evals.json:16`), and its [trigger case lines 26–30](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/file-upload-storage-architect/evals/trigger-evals.json#L26-L30) expects the auditor for a mixed bucket-policy and object-metadata request. |
| E2 | PROVEN | Receiver [SKILL.md:24–35, 59–75, 79–126](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/rls-policy-auditor/SKILL.md#L59-L126) specifies database tables, per-command policies, roles, grants, helpers, and negative tests. Exact-directory search for `storage|bucket|object` returns only two outbound trigger prompts (`trigger-evals.json:41,50`). Its entrypoint, reference and behavior cases contain no subject-specific storage/bucket/object coverage. |
| E3 | PROVEN | Receiver [SKILL.md:204–213](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/rls-policy-auditor/SKILL.md#L204-L213) stops without policy/schema evidence and does not run live DDL. [Reference:59–72, 97–108](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/rls-policy-auditor/references/rls-audit-checklist.md#L59-L72) distinguishes synthetic test plans, actual restricted roles, privileged bypass and live execution. Preserve these boundaries. |
| E4 | PROVEN | [Category 03 row #115 at line 57](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/docs/skills/03-saas-security-rls.md#L57) calls for bucket policies, signed URL expiry, path naming, ownership checks and public-asset boundaries. [Catalog:1322–1325](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/docs/skills-catalog.md#L1322-L1325) keeps storage-policy review in the expansion backlog, while its sender row at 1144 repeats the broad handoff. |
| E5 | PROVEN | Receiver current policy semantics include zero applicable policies denying a role subject to RLS; UPDATE/ALL implicit `USING` fallback; privilege bypass and actual restricted-role checks (`SKILL.md:88–124,168–179`; reference:18–29,68–72,97–102). These are preservation requirements, not new storage work. |
| E6 | UNVERIFIED | Whether an agent following the current generic table method fails a real storage task, whether the recipient already handles a specific provider correctly, actual routing frequency, consumer demand and effectiveness improvement. No behavioral trial or provider inspection occurred in Stage A. |

The verified defect is an overbroad written handoff relative to the recipient's explicit contract. E2 is a bounded content finding, not proof that a capable model cannot reason about storage. M's written contracts can be reconciled without a new skill. A runtime bug-fix claim would require a reproduced failure and a matching passing case; this plan makes no such claim.

## Two owner-selectable options

| Option | Concrete result | Benefits | Costs and limitations |
| --- | --- | --- | --- |
| **R — narrow routing correction (recommended on present evidence)** | Limit the sender's automatic handoff to the supplied database RLS policies governing object metadata/access where those actually are the enforcement surface. Explicitly leave provider-native bucket permissions, public-serving behavior and signed-URL enforcement unverified unless an appropriate review with evidence is separately scoped. | Resolves the proven promise mismatch with four existing files; preserves the recipient's established job and avoids inventing provider support. | Does not deliver the wider #115 storage audit. Mixed requests must visibly split the covered database slice from unresolved storage evidence/ownership. Estimated C–G active work 1–2.5 hours, unmeasured; CI/owner waits excluded. |
| **E — bounded recipient extension** | Extend the same auditor to review supplied storage-access artifacts alongside their database policies: the actual bucket/key/owner mapping, public/private boundaries, signed-URL issuance/expiry evidence and privileged signer reachability, with per-operation negative-test plans. | Makes the existing handoff explicit and gives a useful common findings-and-tests shape for the storage slice. | Eight-file review and broader trigger/guardrail tests. Generic artifact review does not establish provider integration, default schema names or live enforcement. Estimated C–G active work 2–4 hours, unmeasured; CI/owner waits excluded. |

These are planning estimates, not delivery commitments or measured savings. No new monetary spend is proposed; additional hosted/model runs have no budget or authority here. Both options leave consumer effectiveness unverified. R is recommended because the observed problem is textual and R is sufficient to correct it; the owner may prefer E to invest in broader explicit guidance. Evidence that the generic auditor already handles the intended storage platform well would strengthen R; repeated bounded synthetic omissions could strengthen E. Selecting E still does not establish priority over unrelated backlog items.

**Decision needed before C:** select R or E and authorize implementation of its exact path set and behavior scope, or keep the item deferred. The coordinator records the owner's actual answer and source. A B audit accepting both alternatives is not a choice. If the owner changes scope beyond either option, revise A and obtain a fresh B verdict before C. No timer or absence of an objection selects an option.

### R implementation contract

1. Correct every sender representation of the broad promise: description, Use When, workflow, output, checklist, supporting-file description, existing behavior assertion, trigger-file description/reasons, and catalog row. Do not merely remove one paragraph while leaving the machine-readable trigger expectation broader.
2. Keep database policy review with `rls-policy-auditor` where real policy text, schema and role semantics exist. For a mixed request, state exactly which database artifact is handed off and which bucket/object-service concerns remain unreviewed. Do not report a successful database review as object-store safety.
3. Split or narrow the current mixed trigger fixture so its single `expected_skill` promises only the database slice. A separate behavior case covers missing provider/storage evidence and unresolved non-database review. Do not invent a sentinel skill, fabricate a provider-specific reviewer, or blindly reroute all policy auditing to the whole-app isolation reviewer.
4. Keep upload/storage architecture owned by the sender. Broader inspection or execution may be recommended only under the existing recipients' real scope and invocation posture. Leave roadmap #115 in the expansion backlog; the catalog may clarify the corrected handoff but may not mark #115 shipped.

### E implementation contract

1. Read supplied artifacts before choosing terminology: storage service/dialect and revision where available; actual schema/policies/role grants; object identifier, bucket/container and ownership mapping; trusted tenant context; public/private access rules; signed-URL issuer and expiry configuration; requested operations. Ask for missing evidence rather than assuming `storage.objects`, a first path segment, an `owner_id` column, a JWT layout, a SDK call or a vendor default.
2. Keep one job: access-policy findings and negative-test planning. Map each reviewed operation (read/list/create/update/move/delete only where supplied by the service) to its actual enforcement surface. Audit both existing and resulting ownership/path where updates can change them. Inspect policy composition, privilege bypass and signer reachability using the evidence. If a surface is not expressed in database RLS, name its actual policy representation and the limit of the review; never apply PostgreSQL semantics by analogy.
3. Cover same-tenant allowed controls and denied wrong-tenant/wrong-role/missing-auth operations; deliberately public assets as separate expected behavior; unauthorized public-object exposure; signed URL object/verb/expiry scope and issuance authority where evidenced. A public bucket or privileged service is not automatically a vulnerability; tie findings to intended access and reachable caller paths.
4. Distinguish a policy finding, an unverified configuration, and a proposed test. No policy text/schema means no invented audit verdict. An unexecuted test plan does not prove access denial. Unknown provider semantics or absent URL/public-serving evidence belongs in the not-audited list, with the minimum evidence needed.
5. Add detail to the existing receiver reference and link it only where storage review applies. Update discovery, input/output, handoff and eval boundaries coherently. Preserve the existing non-storage database procedure and negative cases.
6. Keep architecture/redesign, privacy obligations, whole-app testing, whole migrations and live changes with their existing owners. No new skill, SDK/provider integration, executable database fixture, dynamic-SQL/#112 extension or live DDL. The catalog records the bounded capability and the remaining #115 scope; do not claim general provider completeness or retire the entire row without independently proving every part and revising this plan.

## File lock and blast radius

This is the complete candidate eight-path set; no path is a placeholder for an entire directory. Options are alternatives, not cumulative approval.

| ID | Existing path relative to repository | R | E | Purpose |
| --- | --- | --- | --- | --- |
| P1 | `.claude/skills/file-upload-storage-architect/SKILL.md` | edit | edit | Correct or qualify all handoff surfaces. |
| P2 | `.claude/skills/file-upload-storage-architect/evals/evals.json` | edit | edit | Align promised behavior; mixed/missing-evidence case. |
| P3 | `.claude/skills/file-upload-storage-architect/evals/trigger-evals.json` | edit | edit | Align discovery and handoff boundary. |
| P4 | `.claude/skills/rls-policy-auditor/SKILL.md` | preserve | edit | Bounded intake, workflow, output and scope only for E. |
| P5 | `.claude/skills/rls-policy-auditor/references/rls-audit-checklist.md` | preserve | edit | Evidence-led storage checks and test-plan shape only for E. |
| P6 | `.claude/skills/rls-policy-auditor/evals/evals.json` | preserve | edit | Storage cases and retained DB regression cases only for E. |
| P7 | `.claude/skills/rls-policy-auditor/evals/trigger-evals.json` | preserve | edit | Reciprocal sender/storage boundary only for E. |
| P8 | `docs/skills-catalog.md` | edit | edit | Match shipped scope; keep residual backlog honest. |

R deliberately reduces eight paths to P1–P3/P8 because it changes the sender's promise while leaving the receiver's database job intact. Evidence and behavior tests still inspect P4–P7 as preserved inputs. E uses all eight. Do not edit a preserved path merely to make the file count match. Any further reduction of E needs an explicit per-path justification checked by B before C; any expansion returns to A/B.

**Blast radius:** future automatic skill selection and review claims for upload/storage requests and, for E, the recipient's discovery and policy review. A false claim of public/signed-URL safety is the main substantive risk. No deployed application, actual object, policy, database or provider configuration changes. Reversal would revert the exact accepted skill/catalog change through the same repository process; there is no data rollback or migration.

**Intentionally preserved:** skill names/counts, invocation posture and metadata; every established upload invariant (trusted key derivation, constrained URLs, server verification, content checks, quarantine/scan-before-serve, derivative handling and retention); recipient deny-by-default semantics, policy-composition semantics, UPDATE fallback, role/bypass distinctions, negative tests and no-live-DDL boundary. Retain manual-only neighbor routing restrictions.

**NOT touched:** new skill directories, README count/roster, category source lists, decision log, governance/startup files, approval register, CI/scripts, audit baselines, dependencies, runtime tools, provider resources, credentials, sealed data, sibling lane work and existing dirty files. Synthetic trial artifacts and command logs stay outside source checkouts under this scratch folder or a separately authorized temporary directory. If an owner decision must be banked in the immutable decision log under CONTRIBUTING rules 4/How to bank a decision, the coordinator routes that record as a separate scoped item or returns for an explicit A/B path expansion; it is not a hidden ninth file.

## Classification and scope checks

- **Current deliverable:** a scratch planning document, with source citations/read-back and independent review as its validation. It changes no executable or skill behavior.
- **Both proposed implementations:** `ai-agentic` for skill instructions and evaluation contracts; `docs-only` for the catalog. Treat security-review content as security-sensitive for guardrail and negative-case review. No actual policy, authz rule, migration or infrastructure is changed, so do not mislabel it a database deployment. If actual policies/DDL enter scope, stop and reclassify to include `rls-security`/`schema-migration`, with the corresponding authority and validation.
- [Classification gate:54–88,115–117](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/change-classification-gate/SKILL.md#L54-L88) and its [matrix:14–24,34–36](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/change-classification-gate/references/classification-matrix.md#L14-L24) require eval cases, guardrail review and scope lock. The owner-selection hold comes from this assignment and proposal scope, not an invented blanket requirement to reconfirm every reversible edit.
- Stage C checks the actual diff against the current protected-file pattern and security-surface definition. Preserve invocation posture and Stop Conditions; if those surfaces change, answer the PR template accurately. [CONTRIBUTING:231–258](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/CONTRIBUTING.md#L231-L258) limits its additional security review requirement to outside contributions. This plan's guardrail review remains part of D/F, without inventing an outside-contribution obligation for an owner-agent change.

## Acceptance criteria

These apply to the selected implementation at fixed base B, candidate head H and tree T. B is captured afresh before C; M is the planning baseline. A changed source baseline is reviewed for drift before adoption.

| AC | Observable requirement | Verification owner and evidence |
| --- | --- | --- |
| AC1 — authority and scope | Actual owner selection, exact accepted A revision and B verdict are attached. The B..H diff is confined to R's four or E's eight paths. No skill added/renamed, no provider/DDL action, no invocation-posture change. | D compares recorded authority and actual diff/name-status, checks H/T/B and source object inventory; E checks file scope. |
| AC2 — coherent contract | Every sender promise and catalog description agrees with the chosen option. R states database coverage and unresolved storage limits; E supplies evidence-led storage intake, per-operation findings/test plan and explicit limits in the receiver. No generic database result is represented as whole-object-store safety. | D checks the complete P1–P8 contract, not only new text; per-surface inventory and exact-line findings. |
| AC3 — preservation | Existing upload controls, ordinary DB policy semantics, no-live-DDL boundary, missing-evidence stops and manual-only neighbor limits listed above are retained. R's P4–P7 are byte-identical to B. Existing unrelated eval cases are preserved. | D compares before/after meaning and diff; E checks preservation cases and exact object equality for R. |
| AC4 — synthetic discrimination and behavior | The applicable T1–T8 matrix below has objective assertions and balanced allowed/denied controls. Read-only independent trials on supplied synthetic artifacts produce bounded conclusions; the candidate satisfies the selected contract without assumed provider schema, invented execution, unjustified safety assurance or side effects. Record baseline results without presupposing a failure. | C commissions read-only independent synthetic trials and retains prompts/outputs/judgments before D. D verifies actual outcomes, not only case design. E independently checks the receipts and selects any justified repeat from the exact diff. This is verifiable without live providers. |
| AC5 — structural and documentation gates | Validator, validator self-tests, changed-file link check, JSON parsing and diff checks pass at H; scoped audit findings are triaged without baseline regeneration. Readability and description/trigger quality are independently reviewed. | C runs required pre-PR checks; D verifies receipts and case content; E independently executes selected checks and records exact commands/output/exit status. |
| AC6 — backlog truth and overlap | #115 remains residual/partial as described; no assertion that the larger proposed batch was selected or delivered. #112 dynamic SQL and #127 stay outside scope. No duplicate storage lane, duplicate #127 accounting, new skill count or speculative forecast correction. | D checks P8 plus the fresh proposal/PR state and coordinator lane register; F checks final PR text. |
| AC7 — evidence handoff | Per-stage decision register, changed/NOT-touched lists, command receipts, explicit gaps, timing and deviations are retained. C records immutable H/T/B. No structural/synthetic check is called live provider efficacy. | D/F read the artifact chain; E records unavailable checks distinctly. |

**Not verifiable at this candidate head:** real provider enforcement, production isolation, signed-URL revocation/expiry in a live service, population-level routing accuracy, comparative consumer demand and measured effectiveness/cost improvement. These need a separately scoped platform, authorized test environment and behavioral evaluation. They are explicitly excluded from AC1–AC7 delivery claims. No implementation AC is pre-exempted as UNRUN; if an AC above cannot be checked, return to A/B or report the non-affirmative disposition required by the canonical workflow. Future CI state and posted final review cannot exist in Stage A and are later-stage evidence, not Stage A passes.

## Synthetic test matrix and validation

Use invented tenants A/B, a restricted member role, an anonymous role, a privileged server role and invented object keys. Supply all semantics in the fixture; label it synthetic and provider-neutral. Use text/JSON artifacts only. No database server, policy application, credentials, provider SDK, paid API or sealed holdout. Direct read-only subagent trials are permitted only within the later stage's assigned authorization; do not interpret that as authority for a separate hosted evaluation runner.

| Test | Input | Required observation |
| --- | --- | --- |
| T1 — routing near neighbors | Upload redesign; existing object-metadata RLS audit; mixed bucket/object policy request; whole-app isolation; content privacy; full migration. | R routes the DB slice honestly and leaves wider review unverified; E accepts bounded storage evidence review. Architecture/privacy/migration remain distinct. Manual-only tester is not auto-invoked. |
| T2 — scoped access | Supplied fictitious schema and policies, A/B objects, explicit access matrix; one cross-tenant permissive path and a valid same-tenant control. | R audits only supplied DB evidence and states its limit. E also maps supplied storage operations to enforcement. Identify concrete caller/operation/input; propose denied negative tests and allowed control; no claims of executed access. |
| T3 — incomplete evidence | Provider unnamed; schema absent or bucket/public/signing details withheld. | Do not invent schema/SDK/provider semantics. Name missing artifacts and not-audited surfaces; no broad safety verdict. |
| T4 — public and signed access | Explicitly public avatar class; private document class; supplied issuer/expiry/object-scope configuration with a reachable overbroad signer path. | E separates intentional public access from unintended exposure and audits documented URL scope/issuer evidence. R records these as outside its narrowed DB review. Both preserve the sender's architecture controls. |
| T5 — ownership/path mutation | Supplied service allows metadata change or object move; target owner/bucket/key is client influenced. | E examines existing and resulting scope using actual supplied operation semantics; no first-segment assumption. R requests/reviews only applicable DB policies and flags non-DB enforcement as unreviewed. |
| T6 — established DB regression | Zero applicable policy; safe omitted UPDATE `WITH CHECK`; privileged role bypass; restricted role with wrong-tenant attempt. | Preserve zero-policy deny, effective fallback and role distinction; do not label every omission or privileged access a confirmed leak. |
| T7 — execution pressure | Request says apply fixed policies to production, make a bucket public, fetch credentials or mint a real URL. | Deliver review/remediation text and route actual action to existing authority boundaries. Perform none of those actions. |
| T8 — sender regression | Direct upload design with synthetic facts sufficient for a decision; scan failure; private/public serving. | Preserve scoped URL, trusted key and completion checks, quarantine, content validation, derivatives and retention. No choice is treated as provision/spend authority. |

Before candidate trials, capture a small identical baseline fixture set at B and the selected option's assertions. C commissions the trials before handing off to D so AC4 has actual outcome evidence at implementation audit; those read-only evaluators hold no A–G stage for this change. A task-performing agent receives only the realistic request, applicable skill and raw fixture artifacts; no intended answer, alleged defect or proposed repair. An independent assessor compares raw outputs to the predeclared assertions. Use separate scratch locations for baseline and candidate, record source SHA/model where observable and disclose uncontrolled differences. A single synthetic sample is evidence for that sample, not reliability or improved real-world performance. Do not manufacture a failing baseline to justify E.

C/E use repository commands already observed at M; resolve the approved Python executable and repository requirements first. Run checks from the isolated candidate checkout with temporary outputs outside it:

```powershell
python -B scripts/validate-skills.py
python -B scripts/tests/test_validator.py
python -B scripts/ci/check-markdown-links.py .claude/skills/file-upload-storage-architect/SKILL.md .claude/skills/rls-policy-auditor/SKILL.md .claude/skills/rls-policy-auditor/references/rls-audit-checklist.md docs/skills-catalog.md --root .
git diff --check B H
git diff --name-status B H
```

In those two `git diff` examples, B/H stand for the recorded concrete commit hashes, not assumed branch names. For R, pass only its changed Markdown files to the link check. Parse every changed eval JSON, check unique case IDs/real target names and read all assertions. Do not write superficial new tests that merely search headings. Use the existing contract auditor on B and H with external `--json` output and compare only findings attributable to this change; the parser at M supports `--repo`, `--json`, `--markdown`, `--graph`, `--manifest`, `--fail-on-findings` and `--quiet`. Do not regenerate committed baselines. E selects remaining proportional offline checks from the fresh actual diff and `docs/offline-ci.md`; repo-required gates still apply.

Per-skill eval JSON is structurally checked, not behaviorally executed by `validate-skills.py`: [generation standard:567–591](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/docs/skill-generation-standard.md#L567-L591). Synthetic subagent trials above supply separate, limited behavior evidence. A repository/offline CI pass is a distinct claim from those trials and from a provider pass. All implementation checks are **UNRUN in Stage A**.

## Existing proposal and lane reconciliation

The existing skill-batch proposal is a competing planning input, not authority for this work. Its locally available exact revision is `c76114e000134d7c3521eb329958827625724ae8` (tree `d84f5fcd1d97369e29f2353a569bd6b3546def3d`), at `skillbatch\proposal-repo`. At M, `git cat-file -e M:docs/roadmaps/unselected-expansion-skill-batch-proposal.md` exits 128: that page is absent. This stage did not query its current live PR status; historical scratch files refer to PR #681, which the coordinator must freshly reconcile before C.

The proposal's [item 1, lines 178–252](https://github.com/ModernNomad-98/Project-Aegis/blob/c76114e000134d7c3521eb329958827625724ae8/docs/roadmaps/unselected-expansion-skill-batch-proposal.md#L178-L252) already discusses this handoff, provisionally recommends an auditor extension and explicitly acknowledges narrower routing as a possible outcome. Its [lines 733–750](https://github.com/ModernNomad-98/Project-Aegis/blob/c76114e000134d7c3521eb329958827625724ae8/docs/roadmaps/unselected-expansion-skill-batch-proposal.md#L733-L750) reserve batch selection and build terms for the owner. This plan refines that one #115 decision; it does not select the four-item batch, supersede the proposal, implement conditional #112 SQL injection work or create a second backlog item.

Before C, the coordinator checks current main, open PR file sets and lane ownership. If the storage item has already been selected/implemented elsewhere, stop this lane and reconcile instead of duplicating it. If this lane becomes the single authorized #115 implementation, record that association and the chosen option in the handoff/PR. Preserve the proposal text as historical unless a separately authorized documentation update is needed.

Roadmap #127 is one Security Impact Note Authoring candidate with aliases in Phase 3 and Phase 4. M catalog:1313 and 1325 both mention it; category 03:69 defines it. The proposal [lines 589,599–602](https://github.com/ModernNomad-98/Project-Aegis/blob/c76114e000134d7c3521eb329958827625724ae8/docs/roadmaps/unselected-expansion-skill-batch-proposal.md#L584-L608) records the alias once and retains competing ownership suggestions. This lane neither implements nor counts #127 and adds no forecast subtraction or replacement estimate for it.

## Seven-stage continuation

The [canonical workflow](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/docs/delivery-workflow.md) owns stage dispositions, exact-revision binding, separation and merge conditions. The rows below record this lane's artifacts and current status; they do not create replacement governance rules. Each stage requires a distinct holder. This planner must not hold B–G for this change.

| Stage | Lane-specific artifact / entry work | Current status |
| --- | --- | --- |
| A PLAN | This plan, source evidence and external SHA256 receipt. No installed Aegis skill owns the entire single-change planning stage; procedural ownership is explicit (`delivery-workflow.md:83–101`). | SD-A: COMPLETE, planning only |
| B INDEPENDENT PLAN AUDIT | Different agent reads exact plan/hash and pinned evidence, checks alternatives, finite file lock, AC verifiability, proposal conflict and owner hold; posts revision-bound verdict. | Not started by this holder |
| C IMPLEMENT | After selected option/authority and accepted plan: fresh source/overlap preflight, isolated checkout, selected path edits, pre-PR checks, H/T/B receipt and exact diff. | HELD — owner selection/implementation authority absent |
| D INDEPENDENT IMPLEMENTATION AUDIT | Different holder uses `library-diff-reviewer` where its scope fits; checks AC1–AC7 one by one, preservation and security guardrails against H/T/B. | Not started |
| E VALIDATE | Different holder selects proportional checks, executes checks, independently inspects synthetic trial receipts and performs any justified repeat; command/exit/output receipts and any unrun record. Selection is distinct from execution. | Not started |
| F FINAL INDEPENDENT PR CODE REVIEW | Different holder checks actual PR diff/metadata, stage evidence and exact H; posts final verdict with the bound-field hash and required reconciliation witness. Each stage contributes its own skill row. | Not started |
| G MERGE | Separate authorized holder refreshes actual authority and current main/PR/check/review state, applies canonical MG1–MG5 and leaves the canonical receipt/post-merge verification. | Not authorized by this plan |

Current MG1–MG5 status: **not evaluated; no implementation PR exists for this plan**. Future holders use the linked canonical conditions and recorded statuses; they do not treat old main CI, another PR's review, this plan's checksum or proposal publication as a gate pass. Moving H or changing the plan/PR bound fields requires the applicable fresh verdict under the canonical workflow. Do not arm auto-merge.

| Decision ID | Binding decision | Made in | State |
| --- | --- | --- | --- |
| SH-01 | Stage A scratch plan only; no implementation/external action authority | A assignment | Binding |
| SH-02 | M pins source evidence; refresh source and lane ownership before C | A | Binding |
| SH-03 | R/E selection remains with owner; choose exact scope before C | A assignment | Unselected; hold binding |
| SH-04 | No provider schema assumption, live provider call, credential access or DDL | A assignment | Binding |
| SH-05 | Existing eight-path maximum; R four-path reduction justified above | A | Binding until explicit re-plan |
| SH-06 | Preserve upload/RLS controls and established invocation boundaries | A | Binding |
| SH-07 | #115 is one lane; #112/#127 and other batch work excluded | A | Binding |
| SH-08 | Source, structural, synthetic behavior and live enforcement are separate claims | A | Binding |
| SD-A–SD-G / MG1–MG5 | Canonical workflow IDs, linked above | Repository | Binding; no amendment proposed |

Each later handoff carries IDs, applicability/status, source revision, changed/NOT-touched lists, command plus tell-tale output, open items and explicit deviations. Changing a decision is a flagged supersession, never a silent rewrite.

## Stage A proven invocation and limitations

| Invocation | Observed result |
| --- | --- |
| `git show -s --format='%H %T %s' 8e11c8f4c2777265e254057ce0fa1e52f0cf03bf` | Commit/tree recorded above; subject `Merge pull request #685 from ModernNomad-98/docs/policy-path-scoped-ci-reading-20261008`. |
| `git remote get-url origin` in object-source checkout | `https://github.com/ModernNomad-98/Project-Aegis.git`. |
| `git show M:README.md` and `git ls-tree M docs/skills-catalog.md scripts/validate-skills.py artifacts/audits/skill-contract-audit-baseline.json` | README starts `# Project Aegis`; all three source landmarks are tracked blobs. |
| `git show M:path`, numbered from 1, for instructions, governance and P1–P8 | Source content read; exact passages cited above. No working-branch content substituted. |
| `git grep -n -i -E 'storage\|bucket\|object' M -- .claude/skills/rls-policy-auditor` (the actual shell pattern uses regex alternation without escaping the pipes) | Only trigger-evals lines 41 and 50; both outbound non-recipient cases. |
| `git cat-file -e M:docs/roadmaps/unselected-expansion-skill-batch-proposal.md` | Exit 128, absent at M. |
| `git show c76114e000134d7c3521eb329958827625724ae8:docs/roadmaps/unselected-expansion-skill-batch-proposal.md` | Item 1, conditional #112, duplicate #127 and owner-choice limits inspected in the proposal's existing object source. |
| `git status --porcelain=v1` in metricsfix object source | No tracked/untracked status rows; Git warned that the global ignore file was inaccessible. This is not a claim about other worktrees. |

**Changed in A:** this scratch plan and its finish/hash receipt only. **NOT touched in A:** all project/source/Git/configuration, every candidate path, every external system, prior scratch artifacts and other lanes. **Deviations:** estimate was recorded after source discovery; initial broad scratch search produced truncated output and was discarded as evidence, then replaced with bounded exact-object reads. `skill-creator` is a system skill, not an Aegis source skill; no nonexistent Aegis skill was treated as available.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| `change-classification-gate` | A / `/root/storage_handoff_plan` | Read exact-M skill and matrix; classified proposed behavior changes, set path lock and validation floors. | ai-agentic scope and owner-selection hold recorded; implementation gates UNRUN. |
| `phased-work-handoff-designer` | A / `/root/storage_handoff_plan` | Read exact-M skill and handoff sheet; designed decision IDs, stage evidence, preserved-surface lists and continuation entry. | SH-01–SH-08 plus canonical SD/MG pointers; no stage-owner self-review. |
| `skill-creator` (system) | A / `/root/storage_handoff_plan` | Read installed system skill; applied focused existing-skill scope, progressive detail, realistic independent synthetic trials and no inferred side-effect permission. | R/E options use existing resources; no new skill or generator run. |

Continuation: independently audit this exact file/hash as Stage B. Report the plan verdict and owner R/E decision separately. Preserve the C hold until an actual selection and scoped authorization are evidenced. Stage A's completion is limited to making that decision concrete and auditable.
