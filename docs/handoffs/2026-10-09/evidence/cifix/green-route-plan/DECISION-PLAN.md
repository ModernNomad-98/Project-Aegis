# CIFIX-GREEN-ROUTE — Stage A decision plan

**SD-A: COMPLETE for the decision packet only.** This packet is ready for an independent Stage B audit of its captured SHA-256. It is not an implementation plan accepted for Stage C, an owner policy selection, a settings-change grant, or a merge verdict.

Item: PR #682 CIFIX-GREEN-ROUTE. Holder: `/root/pr682_policy_plan`, Stage A only. Initial ETA: 20–30 active minutes. The actual work-start timestamp was not captured; the first measured checkpoint was **2026-10-09 14:44:43 UTC**. `TIMING.txt` records completion and elapsed time from that checkpoint. Active time was not separately measured. No subagent was spawned.

## 1. Decision in one read

**PROVEN: the unchanged #682 head cannot satisfy the current all-green condition using the present guard.** Its sole changed path is protected, and the guard deliberately exits 1. Neither the approved fixture repair, the documentary #683, nor a rerun supplies an input that changes this predicate.

**No safe all-green bootstrap is established today.** A repository-only amendment that lets its own candidate workflow recognize approval has no independent enforcement root. A potentially sound alternative is to introduce an external, independently controlled authorization check before allowing any candidate workflow policy change. That is a new security system with new configuration authority and operating cost. This packet specifies the trust contract, staging, and falsification tests for that option; it does not claim an installed controller, executable prototype, or successful live bootstrap.

Recommendation: retain the green-only hold and the accepted fixture repair. After independent B scrutiny, present one concrete choice: keep the hold with no additional investment, or authorize the bounded external-controller feasibility package in section 8. The latter initially permits only offline scratch work and independent review, at **4–8 aggregate active hours**, with no live configuration, publication, dispatch, credential use, provider purchase, or merge. A separately reviewable operator plan is required before any live step. Do not offer the already rejected red-check merge as the recommended solution.

## 2. Verified facts and bindings

Fresh read-only GitHub REST observations and pinned contents reads are retained beside this file. The source clone `cifix/pfix-repo` was read using `git -C ... --no-optional-locks status --porcelain=v1`, `remote -v`, and `rev-parse HEAD`: empty porcelain; the ModernNomad-98/Project-Aegis origin; H below. README and all three source-package landmarks establish Role A. This planner changed no source, Git configuration, refs, index, PR, settings, check, or workflow.

| Fact | Observed value / evidence |
| --- | --- |
| Current main M | `2c68df263c99cdb66d6ea4c76cd480f0bf19b5b5`; `GET git/ref/heads/main`, `main.json` |
| #682 H | `a33aa2a620589d2e0412521e6a0ee1ba3594c97f`; OPEN, mergeable true, blocked; `pr682.json` |
| #682 B / tree | B `5228977920ee479e1fe1ec6b8d56f8fc24c14947`; tree `490c47ed280e488a63427302decf09b024ea2724`; PR API and `git rev-parse H^{tree}` |
| Actual repair diff | `git diff --numstat B...H` → `28 0 scripts/tests/test_offline_ci.py` |
| #682 checks | `checks682.json`: changes SUCCESS, validate-skills SUCCESS, gate-guard FAILURE; tools-tests-linux, windows-offline-checks, tools-tests-windows SKIPPED |
| Failed check identity | `113518470282`, H, App ID `15368`, slug `github-actions`; original workflow run `37837581461` from accepted audit/log |
| #683 | OPEN, blocked, H `abc49113a83a5fce54ce525912416b79859ba232`, no merged_at; `pr683.json` |
| Main register | 119 headings, max 119, zero duplicate IDs; SHA-256 `1a35c8c84de597319952a75d7ee5545a74829f0f07a7c12287e1fe43f6368970`; `main-register.txt` |
| #683 register | 121 headings, max 121, zero duplicate IDs; SHA-256 `d3dfd86df8ad6441938a3df788fd0bc1f1efa70e6cf1df2fde3d1061a567380e`; complete APR120/121 read in `record-register.txt` |
| Current workflow | Blob `66cca67d0390e739190939abccae99125cb56543`, SHA-256 `38fddc4c66bea51e466b6cabbe9a27e5e8a9d8a0bfc94e20b93a6c720a8e4a0e`; `main-workflow.txt` |
| Classic branch protection | `branch-protection.json`: required `gate-guard` and `validate-skills`, both App ID 15368; strict false; enforce_admins false; one approving review; stale-dismissal/last-push/code-owner flags false |
| Rules endpoint | `GET rules/branches/main` → `[]`, retained as `rules.json`; this does **not** mean classic protection is absent |
| Independent green-route audit | Remeasured SHA-256 `d550e55cab06e62aa9149d86e0b4f1e27742adbca826df8ad2c46be51b57e15e`; `../green-route-audit/AUDIT.md` |

The pinned workflow's `gate_pattern` includes `scripts/` and `.github/workflows/`. Extracted case-insensitive regex checks returned True for the fixture path, True for the workflow path, False for the register path. The shell counts protected NUL-delimited paths from `git diff --no-renames --name-only -z origin/BASE...HEAD`; a nonempty count leads directly to exit 1. It does not authenticate owner decisions or parse the register. The independent audit retained the actual job log naming the fixture path and exit 1.

Accepted A–F artifacts were read for scope, authority, criteria, and limitations; all six hashes were remeasured:

| Artifact | SHA-256 | Meaning carried forward |
| --- | --- | --- |
| PLAN-rev3.md | `97c09c154034b050e80e996a55fceb1c22439cc32f44d62c34ed3536fe3fb487` | One-file fixture fix; workflow/policy/settings outside scope; changed policy scope-lock paths return to A |
| PLAN-AUDIT-rev3.md | `cb9c1b1fe011f448eed3bbf5f54b8c720619a523811d87ab020b66a43a4ebe39` | B ACCEPT for that plan, not this policy proposal |
| IMPL-HANDOFF.md | `17c9d5948dc0aadb590773420ccdf3fe522e0410586ff9b165938c144a6cfd12` | C exact H, +28/−0 and retained local matrix |
| IMPL-AUDIT-1.md | `505b348a0a15b66dea4a026a8f0c650746d5f5e0a8d8bac5902ac983a5e38405` | D ACCEPT, 12 MET; AC-F11 explained the intended failure rather than requiring green |
| VALIDATE-1.md | `d499c749762e09607fb40474c9f89748df577df7169c600bdaee8773088b02b1` | E INCOMPLETE — UNRUN LISTED, five named coverage/resolution rows |
| FINAL-REVIEW-1.md | `e0e100935d9c352dd3b682cb52afb34e4dfe40e6c11f946b3df44999cb901db8` | F ACCEPT at H, with explicit green-only hold |

Posted D/E/F receipt identities and prior runtime conclusions are corroborating evidence from the independent audit; this planner did not rerun those suites or independently republish/rebind the PR body. No current G readiness is claimed. Provider-suite applicability remains unresolved: queued suites with zero runs do not establish a pass. The prospective route must resolve every actual applicable check, not merely GitHub's required pair.

## 3. Authority and classification

APR120 documents a one-use red-guard exception for the exact H/path/size, requiring its register record on main. It explicitly excludes workflow/pattern/settings changes. APR121 documents the later selection **“Keep green-only hold (recommended)”** after the complete question explained that reruns and #683 cannot make the unchanged predicate pass. It leaves the earlier record intact and supplies no policy-work grant. Its direct owner choice already governs before #683 merges.

The complete relevant entries and lifecycle references were inspected: APR002 concerns the admin mechanism; APR048/100 preserve green conditions and require separately authorized work; APR047 is a four-BER-file exception excluding this guard/test/workflow scope; APR091/106 were consumed by APR092/107. None authorizes the external controller or bootstrap below. The current brief authorizes this scratch decision plan, not those changes. The register is explicitly documentary, not a tamper-proof authorization service or concurrency lock.

This deliverable is Stage A planning with security design and read-only investigation. Its only permitted writes are `cifix/green-route-plan/` scratch evidence, plan, hashes and timing. Stage A itself is procedurally enforced under `docs/delivery-workflow.md`.

Any later selected implementation is **cloud-iac + rls-security (authorization/trust behavior) + qa-test-only**, plus docs-only explanation and ai-agentic if delivery instructions change. Workflow/scripts force **FULL** validation. Expected Aegis paths for a later captured implementation plan are:

- `.github/workflows/validate-skills.yml` — preserve protected set and replace unconditional protected rejection only with independently authorized decision handling.
- `scripts/ci/check-protected-authorization.py` — proposed protected verifier, if a separate module is selected; no file is created here.
- `scripts/tests/test_protected_authorization.py` — proposed denial and receipt tests, if the separate module is selected.
- `scripts/tests/test_offline_ci.py` — keep existing protections and add integration/mutation cases. Any overlap with #682 requires explicit re-plan and new head evidence.
- `docs/offline-ci.md` and, only for actual changed policy statements, `docs/delivery-workflow.md` and its AGENTS summary/pointers — reconcile semantics and preserve MG/SD governance.
- `docs/approvals/APPROVAL_REGISTER.md` — a separate, correctly authorized record PR; preserve APR120/121 historical bytes and append actual later decisions only.

The external controller's exact repository, deployment artifact, operator identity and settings delta are **UNVERIFIED and unselected**. They must be named and frozen before an implementation-plan B ACCEPT or any live authorization. These expected paths are design constraints, not permission to edit them. A new path/class requires reclassification.

## 4. Finite options

| Option | Outcome and tradeoff | Authority, cost and status |
| --- | --- | --- |
| **A. Keep the existing hold** | Preserves the current rule and accepted repair; the fixture race repair remains unmerged. | Available now. No new service or task-controlled spend; no new delivery ETA. The old intermittent risk remains. |
| **B. Investigate an external authorization controller** | Could provide a real independent acceptance root for an all-green policy transition and later protected edits. Adds a credentialed service, availability dependency, policy maintenance and explicit settings work. | Recommended next investment only if green delivery of protected changes is worth this overhead. Offline feasibility timebox 4–8 aggregate active hours. Implementation/live delivery and cash cost unestimated until operator/hosting/permissions are selected; no purchase authorized. Conditional architecture, not a proven route. |
| **C. Change only the candidate workflow to recognize an APR, label, approval comment, or its own verifier** | Does not establish independent enforcement of the policy change. A malicious candidate can replace the verifier or its identity pin along with the guard. | Reject as a bootstrap. Even an owner-authenticated comment does not make candidate execution the trusted authority for its own acceptance. |

Rerunning the unchanged guard, moving/renaming the repair, excluding scripts/tests, allowing `continue-on-error`, treating skips as successes, injecting a duplicate green `gate-guard`, or cherry-picking directly to main are not acceptable solutions. A new external check must have its own identity and must never overwrite or counterfeit the old failure. Historical failures remain recorded. A changed candidate may obtain real success under a separately approved policy; that is a different claim.

GitHub documents that reruns retain the original SHA/ref, so a rerun must not be represented as executing a newly trusted policy. [GitHub rerun documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)

## 5. Candidate policy and independent trust root for option B

The proposed rule is: an unprotected diff passes the existing path policy; a protected diff fails unless a trusted external controller verifies an active exact-candidate authorization and emits its own successful required check. The Actions guard additionally verifies the controller decision and exact binding, then reports its real outcome. Missing, invalid, stale, revoked, expired or unavailable authority fails closed. A protection match is never removed to obtain success.

The controller must be governed outside the PR's writable tree and outside its workflow execution. Its code and configuration are independently reviewed and pinned; it never executes candidate code, imports candidate modules, follows candidate symlinks, or reads a candidate-supplied network endpoint. Candidate data is parsed as inert input. Its signing/App credentials never enter the PR runner. Its grant store is owner-controlled and independent of candidate-authored register text.

Proposed minimum grant fields: repository numeric ID and full name, PR number, head H, base B, resulting candidate/merge tree T, full changed-path manifest including deletions and modes, raw content hashes, policy/controller revision, authority-record ID, owner identity, issued-at, explicit validity/expiry, revocation state, and one merge use. These are new proposed safeguards, not claims that APR120 already contains them. Distinguish PR head from synthetic merge revision. Do not normalize away path case, Unicode, modes, symlinks, or line endings when binding bytes.

Proposed minimal controller permissions: repository contents/metadata/pull-request reads and checks write for its uniquely named result. Repository settings changes are performed separately by an authorized operator; the runtime does not receive administration, contents write, workflow write, merge, deployment or production credentials. Exact GitHub permission requirements, hosting and owner authentication must be proven during feasibility. A GitHub App is a program identity that can emit a check; this design proposes using that identity as a required check source, not trusting a label any writer can copy.

GitHub supports required status checks bound to an expected App source. Its branch-protection API exposes the check's `app_id`; the live repository already pins both required checks to GitHub Actions. These are platform capabilities, not evidence that the proposed controller is installed. [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [branch-protection REST API](https://docs.github.com/en/rest/branches/branch-protection)

The controller uses its own proposed check name, for example `aegis-protected-authorization`, pinned to its actual App ID in server-side protection. Existing `gate-guard` and `validate-skills` requirements remain. The controller must emit genuine authorization decisions; a synthetic success posted to satisfy a name is prohibited. GitHub's Checks API supports App-produced check runs with checks write permission. [Checks API guide](https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-checks)

### Bootstrap sequence and why its order matters

1. **No candidate-policy execution is authority.** First build/audit the external controller and its immutable trust configuration in a separately authorized scope, with offline fixtures. The exact operator and authenticated owner grant channel must be named. There is no circular dependence on merging Aegis workflow changes to install that authority.
2. **Prove platform enforcement separately.** In an explicitly authorized disposable GitHub repository, demonstrate the full bootstrap: the server requires the external App's check; a candidate can fake its own Actions result but still cannot satisfy the external requirement; a wrong App with the same name fails; missing/controller-failure cases block. This entails future GitHub writes and is not authorized by this packet or the proposed offline-only first decision.
3. **Install the independent requirement before publishing a policy candidate.** Only after an exact operator plan, offline/hosted proof, independent security review and explicit live authorization: install the controller and add its App-bound required check, while keeping the old pair. Capture before/after configuration and readback. First enable controller denial/no protected grants. Resolve the existing admin-bypass setting explicitly: this route requires the new external check to be enforced for the intended merger; do not rely on a bypass-capable account's intent as mechanical proof. Any setting change that applies admin enforcement may also expose the existing human-review requirement and must be included in the finite owner-visible delta.
4. **Publish a separately authorized policy PR P-POL at immutable H-POL.** The owner then authenticates the exact reviewed policy candidate externally. The controller independently verifies its exact bytes and owner-authorized scope under the bootstrap policy; G separately verifies the delivery stages and review provenance. An agent's name typed into a receipt does not mechanically prove independent identity. Any proposed automatic stage-validation feature needs its own design and proof and is outside this minimum controller. The new candidate guard may consume that controller's receipt, but the independently required external check remains the acceptance root. A candidate which changes its own verifier to unconditional success remains blocked by that external check. A check on one SHA cannot satisfy another.
5. **G confirms real all-green and merges P-POL pinned to H-POL.** Both existing Actions checks and the added external check must genuinely succeed; all other applicable checks must be resolved under the owner's condition. No failed check is waived. In particular the bootstrap's Actions guard is green because the independently reviewed new policy executed, not because the old deterministic rule somehow passed. Validate that distinction in hosted evidence.
6. **Re-plan #682 after P-POL is on main.** Refresh base/tree and obtain the owner's required changed-head decision before publishing an updated repair candidate H2. This is a deliberate head change, not a rerun of H. Preserve the repair's intended bytes, renewed scope/criteria and independent D/E/F; issue a new exact-H2 authorization through the trusted controller if selected. APR120's old head is not reused. Merge #683 only under its own complete gates and preserve its historical facts; its record is not the new controller's permission store.

This ordering is a **design hypothesis**, not a proof that the platform, owner's chosen controls, and existing workflow tests all compose successfully. If step 2 cannot demonstrate an all-green transition while the independent check is already enforced, option B fails feasibility and the disposition remains hold. In particular, do not silently substitute a direct push, red merge, duplicate status, or trust in candidate code.

### Freshness, races and lifecycle

The controller must reject any H/B/T/path/policy drift and serialize use of a one-use grant. A retry of the same evaluation may be idempotent; it does not grant a second merge. An evaluation receipt is distinct from consumption, which occurs on the actual pinned merge and is recorded with its resulting commit. Revocation must invalidate eligibility before merge. A failed merge must not be reported as consumption; an unknown outcome requires reconciliation before retry.

An App check is not intrinsically a cryptographic lock on the current base or a guarantee of instant revocation. The live snapshot has `strict=false`. Feasibility must demonstrate how strict base freshness, event handling, controller state and G's same-turn verification prevent stale success, including a competing main update between check and merge. A check-name match or head-only merge pin does not settle this race. If server-side checks plus a bounded merge reservation cannot guarantee the selected invariant, no live bootstrap is authorized: report the residual race for an explicit owner design decision. Do not present eventual invalidation as atomic enforcement.

## 6. Threat model and validation contract

Assets: the authority to merge protected code, owner identity, controller keys, correct source/test history, and accurate check evidence. Actors: owner, independent C/D/E/F/G holders, an authenticated repository writer, a fork author, a compromised dependency/runner, and the controller operator. A compromised repository administrator can change server-side controls and is outside what a required check alone can prevent; operator access and configuration audit are explicit trust assumptions, not an eliminated threat. This is one repository, with no SaaS tenant data path; repository/PR identity isolation is the corresponding cross-object boundary.

Trust boundaries: **B1** candidate bytes → external verifier; **B2** owner → authenticated grant store; **B3** controller → GitHub check/protection; **B4** check/receipt → Actions guard and merger; **B5** controller code/keys → deployment operator. Threat consequences are HIGH where unauthorized merge/key exposure is possible; availability-only failures are MEDIUM. The current deterministic rejection is proven; the proposed attack paths and controls below are hypotheses to validate, not claims of a live exploit.

| ID / boundary | Concrete abuse or failure | Required control and falsification test |
| --- | --- | --- |
| T1 B1: tampering/elevation | Writer changes candidate guard/verifier/key pin to return success without approval. | External service reads independent policy and raw Git objects; App-bound required check must remain absent/failing. Hosted mutation test must show merge denial even with green candidate Actions. |
| T2 B2: spoofing/repudiation | Writer adds APR text, copies an owner name/label, edits a comment, or supplies a grant for another repo/PR. | Authenticated owner channel and immutable binding independent of candidate content; deny wrong identity, repo ID, PR, malformed/duplicate fields and forged grant. Retain attributable issue/revoke/use audit. |
| T3 B4: replay | Old green receipt reused at H2, changed base/tree, changed path mode, extra protected file, deleted file or changed policy. | Exact full binding; deny each single-field mutation and same receipt on a second PR. Positive exactly-matching fixture must pass to prove the verifier is live. |
| T4 B3: spoofing | Another App or Actions posts the same check name or a green legacy status. | Source-bound required check; hosted wrong-App/name-collision experiment must leave merge blocked. Never overwrite the old gate result. |
| T5 B4: race | Main advances, grant expires/revokes, controller dies, or two mergers race after a green result. | Fail closed, freshness/reservation design and one-use ledger; adversarial scheduling tests must demonstrate the selected invariant at merge. Unknown atomicity is a hard stop. |
| T6 B1/B5: code execution/disclosure | Candidate import, symlink, archive traversal or network endpoint causes verifier to run/exfiltrate with App credentials. | Never execute candidate, safe raw-object parsing, fixed endpoints, minimal permission/key isolation; denial tests for traversal, oversized payload, symlinks, shell interpolation and candidate module shadowing. Keys absent from logs and PR job environment. |
| T7 B1: path bypass | Rename/delete/case/newline/Unicode name avoids protected classification. | Preserve full existing protected regex semantics and no-renames/NUL handling; run current protected cases, additions/deletions/modes, aliases and near-miss positive cases. |
| T8 B5: operational failure | Bad controller deploy or unavailable auth service silently permits protected changes. | Independently pinned version, explicit fail-closed outcomes, incident rollback to deny protected changes; outage and bad-version rehearsal must block, retain diagnostic evidence and recover without accepting forged success. |

No threat is accepted by this packet. A future independent security reviewer must assess B1–B5, with the operator accountable for B2/B5. This is an explicit design review requirement; it does not widen MG5 beyond outside contributions.

Existing source tests that must survive include all `ProtectedFileGuardTests`, `ImportPathIsolationTests`, gate/tools separation, all workflow mutation probes, pinned-action/hash-locked dependency requirements and Windows current-directory executable isolation. The unauthenticated fixture stays rejected; an authorized positive fixture is separate. Do not weaken an existing assertion to accommodate an untrusted executable path. `gate_pattern` protection of scripts and workflows remains byte-identical unless a separately audited, explicitly selected design says otherwise; this proposal selects no weakening.

The future FULL validation inventory must include `scripts/validate-skills.py`, `scripts/tests/test_validator.py`, `scripts/tests/test_audit_skill_contracts.py`, `scripts/tests/test_markdown_links.py`, complete `scripts/tests/test_offline_ci.py`, new verifier unit/adversarial tests, repository link checks, dependency integrity and DCO, plus the actual applicable Linux/Windows/offline hosted jobs. The implementation plan must specify exact commands/environment for each. Reserved BER/VM/provider/evaluation operations require their own active authorization; ordinary existing hosted results may be read. Record every local UNRUN with named exact-head CI coverage or precise resolution. A skipped job is never a pass.

#682's race proof remains non-vacuous: positive fetch Trace2 liveness, no maintenance children, two-line negative control, POSIX Git 2.55.0/2.43.0 and proportional forced/natural cases. Reuse retained H evidence only as historical evidence. New H2 and changed workflow must have renewed focused and full integration proof. Do not repeat unchanged stress merely to fill an elapsed-time target.

## 7. Delivery dependencies, failure and rollback

Every source change follows A → independent B → C → independent D → E → independent F → separate G, with seven distinct holders. This Stage A holder cannot audit this packet or implement/review/merge its later change. The coordinator assigns roles and verifies handoffs; no two agents hold the same PR. Each implementation artifact has immutable H/T/B and a frozen plan hash before independent audit. F binds actual PR fields; G rederives MG1–MG5 and owner authority in the same turn. P-POL, external-controller delivery, settings application and updated #682 have explicit separate scopes and dependencies; do not hide all actions inside one approval.

Required order: packet A/B → owner's selected finite feasibility scope → independently built/audited offline prototype → exact implementation/hosted-test/operator plans → authorized isolated platform proof → independently authorized controller install and source-bound requirement → P-POL C–G → #682 re-plan/new head/renewed authority and D–G. Documentary #683 may continue only through its own established lane and gates; its merger must verify current prerequisites, not infer readiness from this packet.

Stop and return to A/B for new scope, changed trust assumptions, candidate drift, main policy drift, failed negative test, unresolved App identity/source enforcement, a setting change not in the operator delta, credential exposure, inability to prove the merge freshness invariant, or mismatch between expected and actual check inventory. A protected denial caused by unavailable authorization is a correct safety outcome, not grounds to retry until green.

Rollback is **restore denial first**. Before P-POL merges, the original guard remains rejecting and no protected grant is issued on error. After P-POL, a controller outage blocks protected changes; do not remove the external required check to regain throughput. Revoke the affected authorization, stop the merge lane, preserve evidence, and use a separately reviewed exact-head revert under the still-enforced external authority when the controller is healthy. If that cannot run safely, remain held and require a separately prepared owner recovery decision. Restoring earlier branch settings is never automatic: that could remove the independent trust root while the new guard remains deployed. The owner-visible operator plan must specify the exact revert ordering, allowed outage, and recovery actor before installation. No emergency red merge or direct push is preapproved here.

## 8. Proposed next owner decision and finite feasibility work

After B accepts this packet, the coordinator can present this single decision:

> Keep #682 held, or authorize a 4–8 active-hour offline feasibility package for an external, independently enforced approval check? The package produces a scratch prototype, adversarial test results, and an independently reviewed installation/rollback proposal. It makes no repository, PR, settings, credential, provider, purchase, dispatch, or merge changes. Live introduction would be a separate exact proposal and decision.

The **recommended next action is this bounded feasibility package only if the owner wants to invest in green delivery for protected changes**. Otherwise option A is the complete safe disposition. The present task's permission to plan does not select option B.

| Feasibility deliverable | Bound / proposed holder | Observable exit |
| --- | --- | --- |
| External trust protocol and deployment choices | 60–120 active min, designer | Exact data contract, owner-auth channel candidates, threat/permissions table, operator/root selection gaps |
| Offline scratch reference prototype | 90–180 active min, implementer separate from reviewer | Synthetic positive case and T1–T8 negative matrix, no network writes, raw test logs, artifact hashes |
| Independent design/prototype scrutiny | 60–120 active min, independent reviewer | Each criterion MET/NOT MET/UNRUN; bootstrap and freshness verdict; cannot label hosted proof MET |
| Finite operator proposal | 30–60 active min, planner/assigned operator | Exact proposed App/permissions, costs or quotes, settings delta, disposable-test plan, installation/recovery order, explicit hard stops |

Aggregate estimate **4–8 active hours**; elapsed time includes unbounded owner/reviewer waits. Estimates are planning judgment, not historical measurements or a promise. Stop the package at 8 active hours and deliver unresolved findings; any extension is a new scope decision. No new cash spending is authorized. Hosting, plan eligibility, key storage, App maintenance, Actions/API usage and operator support costs are **unknown** until a deployment option is selected; do not advertise $0 operating cost. Actual implementation/live delivery ETA is **not derivable yet**. The repository's earlier `docs/roadmaps/gate-guard-friction-decision.md` also treated a trusted approval check as separate discovery/design work and left implementation unestimated.

Decision-packet acceptance criteria for Stage B:

1. **DP1:** All decisive present facts have pinned source/API evidence and no current-green claim; hashes and H/B/T agree.
2. **DP2:** APR120/121 precedence and existing scope limits are preserved; no implied implementation, settings, provider or red-merge grant.
3. **DP3:** At least one concrete conditional policy is specified, with independent trust established before candidate policy execution; any circular dependency or unproven atomicity remains a named hard stop.
4. **DP4:** Every proposed trust boundary has a falsification test, and existing protected-path/isolation tests and seven-stage identities are retained.
5. **DP5:** Ordering, changed-head handling, rollback, cost, timebox and one owner choice are concrete; UNVERIFIED live capabilities remain labeled.

Not verifiable at this Stage A head: prototype behavior, hosted wrong-App enforcement, live deployment/permissions, key handling, atomic freshness/revocation, bootstrap success, new candidate all-green checks, current provider applicability, owner selection and future merge readiness. These are explicitly UNVERIFIED and have future gates above; none is an SD-A result.

## 9. Skills actually used and final evidence limits

| Skill | Agent / item | Actual application | Result / limit |
| --- | --- | --- | --- |
| human-approval-boundary | /root/pr682_policy_plan / CIFIX-GREEN-ROUTE Stage A | Read source skill; matched protected-policy/settings proposal to current task scope and complete relevant grants/lifecycle. | Planning allowed; live controller and policy changes need new scope authority. No risky action performed. |
| scoped-approval-register | same | Read skill and register-format reference; read preamble, relevant full grant/lifecycle records and complete APR120/121; checked pinned register counts/hashes. | Later green-only hold retained; documentary entry is not a runtime authorization service. No register edit. |
| change-classification-gate | same | Read skill/classification matrix and actual workflow/test paths; set prospective classes and scope expansion triggers. | Workflow/security plus FULL test implications declared; expected paths do not authorize implementation. |
| risk-tiered-validation-selector | same | Read skill and actual CI/test inventory; selected FULL validation for prospective scripts/workflow/auth changes. | Named existing checks, targeted adversarial cases and UNRUN boundaries; ran no suite. |
| threat-modeler | same | Read skill and threat-catalog; modeled the external-controller proposal against existing guard/isolation code, B1–B5 and T1–T8. | Design hypotheses and concrete tests produced; no live exploit or successful defense claimed. |

Read-only tooling: `gh api` GET endpoints named in section 2 and pinned `contents/PATH?ref=SHA`; Git read-only inspection; file reads/hashes/regex census; primary GitHub documentation browsing. Only scratch plan/evidence/timing files were written. Initial command helper startup failed; the authorized reads succeeded with `login:false` and sandbox escalation. A PowerShell brace-list parse error occurred before execution and was corrected. Large combined reads were output-truncated; decisive source sections were read in smaller targeted blocks and material bindings were remeasured. No tests, remote writes, provider settings, dispatches, comments, pushes or merges were performed.

Memory supplied only general stage-separation/exact-head guidance (`MEMORY.md:267–268`); current material findings are supported by the source and API evidence above. The final handoff must report this plan hash, measured checkpoint-to-finish wall time and active time unavailable. Independent Stage B remains outstanding.
