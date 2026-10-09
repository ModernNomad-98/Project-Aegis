# CIFIX-1 — independent Stage B audit of PLAN-rev3

**SD-B: ACCEPT** for the P-FIX and P-REG plans at SHA-256 **97c09c154034b050e80e996a55fceb1c22439cc32f44d62c34ed3536fe3fb487**. Required plan changes: **none**.

This accepts the plan's design, authority treatment, criteria, and ordering. It does not report implementation, runtime validation, hosted success, or merge readiness. No Stage C–G work was performed by this auditor.

## 1. Binding and audit scope

- Item: CIFIX-1 Stage B INDEPENDENT PLAN AUDIT.
- Holder: /root/cifix_plan_audit, Stage B only, independent of /root/cifix_plan. This holder may hold no other stage of either change.
- Assigned start: 2026-10-08 19:01:17 UTC; announced active-work estimate: 25–40 minutes. Active time is not separately measured.
- Audited file: C:\src\Codex Projects\Project Aegis\cifix\PLAN-rev3.md.
- Source clone read only: C:\src\Project Aegis\Project-Aegis.
- M: 5228977920ee479e1fe1ec6b8d56f8fc24c14947.
- S: 32f5ae25780c4802184a63d4063507fcf31b3a37.
- Snapshot prefix at S: docs/evidence/session-handoff-2026-10-08/.
- Only file written: C:\src\Codex Projects\Project Aegis\cifix\PLAN-AUDIT-rev3.md.

The first Get-FileHash SHA256 read matched the assigned hash. A separate Python hashlib read and the 19:07:22 UTC checkpoint matched it again. The final binding check is recorded in the closing handoff below. Any subsequent plan edit voids this ACCEPT; it is not an acceptance of a future revision.

Policy and source were read from M using git show. The clone's checked-out HEAD is f7c48212bce508512fac4d45f3aa2e43c05b59a4, so reading its working files as though they were M would have been wrong. git rev-parse --verify independently resolved both assigned refs to M and S. git remote -v resolved origin to https://github.com/ModernNomad-98/Project-Aegis.git. The README at M begins "# Project Aegis"; git ls-tree found docs/skills-catalog.md, scripts/validate-skills.py, and artifacts/audits/skill-contract-audit-baseline.json. These corroborate Role A.

The source clone had two existing untracked directories, artifacts/recovery/ and artifacts/reviews/. git --no-optional-locks status --porcelain also warned that the user ignore file was inaccessible. No clone file, branch, ref, index, configuration, or remote state was changed by this auditor.

## 2. Instructions and Aegis skills used

Read at M: AGENTS.md, CLAUDE.md, CONTRIBUTING.md, docs/delivery-workflow.md, the approval-register preamble, relevant grant records and references, the PR template, the complete target test file, and the relevant CI workflow sections. Compared the saved rev1 and rev2 audits including RC1–RC16, rev2's design/criteria/register draft/sequence, BRIEF.md, the Q2–Q4 JSON, owner answer and message records, HANDOFF.md, REDACTIONS.md, BRIEF-COMMON.md, and diagnosis/residual evidence.

The current delivery workflow says no installed skill owns the plan-level ACCEPT/REVISE decision. This decision and the captured-revision binding are procedural. The following non-manual skills were read and applied only within their actual scope:

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [.claude/skills/acceptance-criteria-reviewer/SKILL.md](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/acceptance-criteria-reviewer/SKILL.md) | B / cifix_plan_audit | Reviewed every numbered criterion for outcome, threshold, and evidence; used its criteria-review-sheet completeness classes. | 20 TESTABLE, 0 NEEDS-REWRITE, 0 UNTESTABLE; detailed table in §6 and exact criterion text in Appendix A. This skill supplies no work-completion verdict. |
| [.claude/skills/change-classification-gate/SKILL.md](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/change-classification-gate/SKILL.md) | B / cifix_plan_audit | Matched actual paths and proposed behavior to classification-matrix floors and the scope lock. | P-FIX bug-fix plus qa-test-only, protected and security-relevant; reproduction/flip/regression required. P-REG is documentary grant transcription on a security-relevant governance surface. |
| [.claude/skills/scoped-approval-register/SKILL.md](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/scoped-approval-register/SKILL.md) | B / cifix_plan_audit | Applied its register-format source/proposal, immutable-record, effective-status, and factual-lifecycle checks to the draft and contingencies. | Complete selected wording is preserved; recording creates no authority; EOF append and lifecycle requirements are checkable. |
| [.claude/skills/human-approval-boundary/SKILL.md](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/human-approval-boundary/SKILL.md) | B / cifix_plan_audit | Checked the one-time red-guard merge, separate register vehicle, size disclosure, and changed-head procedure against actual owner selections. | Q2 is the vehicle grant; Q4 requires a fresh answer after recording; OQ-C supplies the explicit main-merge boundary; disclosure is not assent. |
| [.claude/skills/risk-tiered-validation-selector/SKILL.md](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/risk-tiered-validation-selector/SKILL.md) | B / cifix_plan_audit | Used classifier-rules to check scripts/ full-tier treatment, documentary checks, actual CI inventory, and named limits. | P-FIX cannot use a docs-only shortcut. Local core checks, focused race evidence, hosted checks, and explicit unavailable coverage are distinguished. No tier was executed. |

No MANUAL-ONLY skill was invoked. The memory quick pass supplied the general reminder to bind workflow conclusions to current source; all CIFIX facts and authority conclusions here were independently derived from the assigned artifacts and current local Git objects.

## 3. Evidence checks performed in this audit

These are read-only artifact/source inspections, not repository validation or a rerun of the old prototype.

| Check | Observed output |
| --- | --- |
| Get-FileHash -Algorithm SHA256 on PLAN-rev3.md, plus Python hashlib over its raw bytes | 97c09c154034b050e80e996a55fceb1c22439cc32f44d62c34ed3536fe3fb487 |
| git rev-parse --verify origin/main and origin/claude/sharp-lovelace-urgxpz | M and S exactly |
| git diff --quiet c060a7cb origin/main -- scripts/tests/test_offline_ci.py .github/workflows/ scripts/ci/record-check.py scripts/validate-skills.py | Exit 0 |
| hashlib.sha256 over git show M:scripts/tests/test_offline_ci.py raw bytes | 4fa62a8b03bf2d72ded776a73881dfbd18a1c6434e0ca4d9aef2e8de07d3a022 |
| raw.count of LF bytes, plus Python AST counting direct test methods by class | 750 newlines; RecorderTests 6, ProtectedFileGuardTests 10, ImportPathIsolationTests 3, GateJobIsolationTests 13, HashLockTests 6; total 38 |
| Hash and heading-regex census of the complete M register blob | SHA-256 1a35c8c84de597319952a75d7ee5545a74829f0f07a7c12287e1fe43f6368970; 119 headings, maximum 119, duplicate IDs [] |
| Case-insensitive match against the extracted workflow gate_pattern | test path True; register path False |
| Current workflow tools/offline path expressions applied to the two proposed paths | Both false for both paths |
| Numbered-criterion regex over the exact plan | F1–F12 and R1–R8, with no missing numbered criterion |
| Case-insensitive scan for the forbidden automated-reviewer invocation string, assembled without writing the string | 0 in the plan |

Actual S blob hashes were recomputed with subprocess.check_output of git show and hashlib.sha256; no working-tree newline conversion was used:

| Snapshot input | SHA-256 |
| --- | --- |
| HANDOFF.md | 46cfef81a5f24b5d25b1f96623abf67ad18407720644f031c7c90a8cd2ddf16b |
| owner-messages.md | 443f791038c41f7bffabc0bb6841b1aa9191f351bfc52c8e31b8f2ef7392b061 |
| owner-askuserquestion-answers.md | a4c4524fe069e8a7347d180f24c2e9e2ebaf5b73982c26b034705a620e45b255 |
| artifacts/cifix/BRIEF.md | 682eb1cf401efda27a51c59ca006fa97812df13a259664ccd227653f13f37364 |
| artifacts/cifix/PLAN-rev2.md | 6ef9a2aee2ba612d842643ed7246734c544c736bc09554fb715eedc39127498c |
| artifacts/cifix/PLAN-AUDIT-rev1.md | 26609843ae2940c42cb93dc7813703b3397ff27a3e497926f0df62264c6941e0 |
| artifacts/cifix/PLAN-AUDIT-rev2.md | 4bd41cb236a2361afddbfbdfa9bdae255dec1104e857368d3682ce32963f1846 |
| artifacts/cifix/owner-q2-q4-verbatim.json | 74c8cd5a559b1398fe411d6d75f4da1be23fe788b0845cdb59dcfb09bc82f1c2 |
| artifacts/ci-diag/DIAGNOSIS.md | 522ea312e15f7d7f7b930f20e508c632b2fb54cfbf783c8734fe5d1710c09cfb |

The rev2 plan/audit scratch hashes differ from the saved redacted copies where REDACTIONS.md explains the copy changes. Rev3 correctly binds actual saved bytes and does not pretend the original scratch hashes are hashes of these copies.

### Owner quotation fidelity

I extracted the single Markdown register draft in rev3 §7 and compared its lines to the selected source fields. All 15 required strings occur on a single physical line in that draft. This comparison preserves Unicode punctuation and performs no whitespace normalization.

| Source string | Character count | SHA-256 first 16 where measured | Single-line occurrences |
| --- | --- | --- | --- |
| Grant question | 588 | 87eee772606974b1 | 1 |
| Grant option | 255 | 95826ec00af9e24e | 1 |
| Grant selected label | — | — | 1 |
| Q2 question | 412 | 51235c50902a464f | 1 |
| Q2 selected label | 29 | 85a773618067eb64 | 1 |
| Q2 option description | 178 | ff4684325e17732f | 1 |
| Q3 question | 213 | 31c08a19b4ec1923 | 1 |
| Q3 selected label | 28 | 17f23d40ac940559 | 1 |
| Q3 option description | 199 | 9938d0d37743b726 | 1 |
| Q4 question | 195 | b67305a3d3f25d42 | 1 |
| Q4 selected label | 26 | c9485ac41f06fece | 1 |
| Q4 option description | 186 | c07b81c3c8476558 | 1 |
| OQ-C question | 221 | 51562fcda67d7d1b | 1 |
| OQ-C selected label | — | — | 1 |
| OQ-C option description | 147 | — | 1 |

The six Q2–Q4 question/description fields plus three chosen labels are nine selected JSON fields. The prior audit's eight-row quotation table comprised those six question/description fields plus the two original BRIEF strings; rev3's explicit correction of the historical "eight JSON strings" wording is justified by the actual JSON.

The recorded owner selections are corroborated by owner-askuserquestion-answers.md at 15:26:38.922Z, 16:01:08.352Z, and 17:51:48.809Z on 2026-10-08. The scrutiny instruction is present in owner-messages.md at 16:23:20.186Z. The coordinator's later BRIEF transcription times are separately identified. No extraction timestamp is invented for the Q2–Q4 JSON.

Audit instrument correction: my first grant-option extraction selected the older wrapped fragment in BRIEF and printed length 119. I corrected the selector to the complete quoted single-line source, then obtained 255 characters, hash16 95826ec00af9e24e, and exactly one draft occurrence. The 119-character read is not relied on as a full-option fidelity check.

Fidelity to the archived source is proven by these reads. Fidelity of those archived transcriptions to the unavailable original conversation remains the prior coordinator's attestation; no independent transcript authentication is claimed.

## 4. Prior required changes

| Prior item | Verdict | Independent basis in rev3 |
| --- | --- | --- |
| RC1 — Q2 and P-REG authority | Resolved | §7 quotes the full proposal, selected label, and option; §§2/8 rest authority on Q2, with APR-100/048/050 supporting delivery mechanics only. |
| RC2 — consumption batching | Resolved | §9 removes a CIFIX P-CONS task, preserves the next-register-PR choice with APR-119, allocates the later ID then, and requires the merge receipt facts. |
| RC3 — head-move procedure | Resolved | §8.3 distinguishes before/after main merge, voids head-bound evidence, and requires a fresh question naming H2 after recording. |
| RC4 — P-REG C versus future evidence | Resolved | §8.1 requires P-FIX D ACCEPT plus completed H checks before P-REG C; §7 cites D and logs, not a future F comment. |
| RC5 — settled P-FIX F/MG3 before P-REG G | Resolved | AC-R7 and §8.1 require the identified final verdict, exact H/hash, automated result or explicit unavailability at H, finding triage, and time ordering. |
| RC6 — complete source/proposal and correct attribution | Resolved | All selected source text is supplied and mechanically matched; draft explains selections versus owner-authored prose and narrows independent D/log evidence to technical facts. |
| RC7 — true EOF append | Resolved | AC-R1 combines raw byte-prefix equality, positive append, both trailing LF checks, sole-path zero deletions, and one EOF hunk. |
| RC8 — cross-PR separation | Resolved | §8 prohibits P-FIX G from every P-REG stage; P-REG C is independent of P-FIX C/G. Shared A/B does not undermine that prohibition. |
| RC9 — current base and historical attribution | Resolved | M, scope identity, register count/hash, and source-role landmarks were independently checked. §8.1 properly attributes APR-105 wording and APR-106's quotation of a D audit. |
| RC10 — concrete commands | Resolved | F3 includes AST/counter recipes, F5 exact two-line removal, F12 empty TMPDIR plus preserved dirty source, R2 enumerates/ref-resolves other PRs, and R4 defines the entry boundary and measured values. |
| RC11(a/b) — inputs, OQ-A/B, scrutiny | Resolved | Actual S hashes match; the JSON closes OQ-A; §4 makes size disclosure a record rather than consent, removes the arbitrary 40-line allowance, and holds P-REG C on a size difference. |
| RC11(c) — historical request to keep OQ-C open | Superseded by later owner answer | BRIEF and the 17:51:48.809Z owner selection explicitly confirm merged on main; preserving an open question would contradict the later evidence. |
| RC12 — fillable draft | Resolved | Only future measured placeholders remain; all owner labels/text are on one line; JSON provenance and missing extraction time are honest; D/log evidence does not authenticate owner words. |
| RC13 — five incorrect/incomplete criteria | Resolved | R2 excludes P-REG in the query; R7 uses F's comment ID and reads its actual disposition; R8 enumerates actual source fields; F11 supplies log retrieval and anchored parsing; F9/full suites require real clones. |
| RC14 — merge mechanism and main advance | Resolved | §8.2 distinguishes REST sha and MCP expectedHeadSha, labels current admin-bypass capability unknown, requires fresh capability evidence, stops on refusal, forbids branch update after recording, and checks main's changed paths. |
| RC15 — precise Q4 and expiry when no regrant | Resolved | §8.3 requires an answer to a SHA-naming question; a factual EXPIRED event is owed with or without replacement approval; Q3 is not extended to expiry timing. |
| RC16 — recommendation scrutiny and estimates | Resolved | §§3/4/8/9/11 state counterarguments and change-of-mind evidence. Runtime/merge/ETA unknowns remain unverified and do not justify bypassing gates. |

## 5. Technical, authority, and ordering assessment

**Technical design.** At M, the fixture initializes its repository at test-file line 157, commits at lines 166 and 183, and launches the extracted guard with cwd=repo at lines 184–186. The current guard fetch is workflow line 493. The proposed local config calls therefore precede both fixture commits and the guard fetch. Other temporary fixtures in the complete file do not create a temporary repository with those maintenance-triggering calls. This supports the proposed location without changing the real guard or workflow.

The independent historical audits report mechanism trace, forced reproduction, and deterministic flip evidence on two Git versions. Those reports support selecting the design. They are not fresh candidate evidence: the raw historical traces, prototype, and stress harnesses are absent from this snapshot. Rev3 restores executable recipes and requires fresh exact-revision results before later affirmative stages. Its counterfactual test removes only the two config lines and requires the maintenance assertion itself to fail, preventing an unrelated setup/cleanup failure from being misreported as the flip.

The new regression checks the existing guard outcome, trace liveness, and absence of maintenance child processes. The external census covers the existing fixture calls while the new method owns its separate trace. Natural and forced runs measure bounded success, not an impossible promise that the race can never recur. The plan's acknowledged high-precedence environment and packaged-build limits remain real.

**Coverage/classification.** This is bug-fix plus qa-test-only on scripts/, so full-tier treatment and reproduce/flip/regression evidence are appropriate. The documentation grant is a transcription of authority already given, not a new permission control; its explicit security-relevant answer and register audit remain required. The class decorator at test-file line 137 makes the new method POSIX-only. The workflow runs the file at lines 153–154 and 309–310, but the Windows job's path condition at 275 skips for these two proposed paths. Rev3 reports that boundary honestly. Reading calibration constants through AST in the existing test is not executing the reserved calibration package.

**Authority.** The grant question plus selected option authorize the one-file repair and a one-time exact-head guard exception; Q2 authorizes the separate recording PR on all seven stages/all checks green/admin-merge terms. The archived proposal described two config lines, while the file-scoped selected option and bug-fix floor support keeping the regression. Rev3 explicitly discloses the approximately 28-line total, records actual numstat, and does not turn lack of objection into approval.

APR-047 explicitly excludes guard scripts/tests, so it is not this repair's exception. APR-100/048/050 provide no missing work grant and no substitute for Q2. APR-106/107 are consumed historical examples only; their mechanics do not grant this change. APR-033/034 support the distinction between recording a factual expiry and obtaining a fresh answer to a question naming the replacement head.

BRIEF-COMMON's default against a register edit is overcome for this specific P-REG by the express one-time grant, the separate Q2 vehicle choice, and OQ-C. This audit accepts that specific override; it does not broaden the default for other work.

**Sequence.** There is no circular dependency in the planned path:

1. Shared A/B covers both explicitly named PRs.
2. P-FIX C produces immutable H/tree/B and required local evidence; D audits it.
3. P-REG C waits for D ACCEPT and completed, explained H checks, allowing it to record real D/log facts.
4. P-FIX E/F and P-REG D/E/F use distinct holders; P-REG G waits for settled P-FIX F and MG3 at H.
5. P-REG merges under its own Q2 authority. P-FIX G then reads the entry on main, repeats its own gates, keeps H unchanged, and uses a pinned merge.

The explicit OQ-C answer resolves the recorded-versus-drafted boundary. After P-REG merges, updating P-FIX to main is forbidden because it would move the approved H. Before the merge call, main changes are checked against the scope lock, other changes/conflicts/lifecycle effects are reviewed, and current main is rechecked. A moved bound field also requires a new F verdict even if H has not moved. This preserves the repository's procedural exact-head rules.

**Merge semantics.** I independently read the current [GitHub REST merge documentation](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request): its sha parameter binds the PR head, and HTTP 409 reports a mismatch. That establishes the documented pin semantics, not whether today's actor can bypass a failed required guard. Rev3 keeps that capability unverified, requires current read-only evidence, and stops if the pinned call is refused. An ambiguous response requires a state read before any further action. The snapshot's old GraphQL restriction is not misrepresented as a current Codex restriction.

**Reserved scope.** The plan authorizes no new skill build, evaluation/rehearsal repair, VM/ISO work, Stage 4B execution, provider call/spend, credential access, or reserved manual package execution. Existing hosted CI may be observed. Local full-tier steps outside the authorized scope are explicitly unavailable coverage, not a reason to run reserved scripts. No reserved pin, fixture, budget, or flag was copied into this audit.

## 6. Acceptance-criteria review

Summary: **20 TESTABLE; 0 NEEDS-REWRITE; 0 UNTESTABLE.** These are testability verdicts, not claims that any criterion has passed on a future candidate. The compound subconditions are retained within their original numbered criteria; the exact text and command blocks appear in Appendix A.

| Criterion | Verdict | Observable threshold and evidence |
| --- | --- | --- |
| AC-F1 | TESTABLE | Git sole-path numstat must have zero deletions and actual a additions; diff positions match the design. A different a triggers the stated disclosure hold before P-REG C. |
| AC-F2 | TESTABLE | No prohibited added construct in the case-insensitive diff scan, plus independent assertion/behavior review. A textual hit is investigated rather than silently discarded. |
| AC-F3 | TESTABLE | AST name-set delta is exactly the named one test, none removed; class 10→11 and fixture calls 88→89 with no guard skips. The runtime counter preserves original run_guard and assertions. Fresh baseline mismatch stops reconciliation. |
| AC-F4 | TESTABLE | Both selected Gits, live base trace, and H zero maintenance/gc-auto child/start events with positive upload-pack evidence and 11 successful class tests. Separate trace ownership is explained. |
| AC-F5 | TESTABLE | R0 differs by only two exact removed lines; each Git produces five maintenance-assertion failures in R0 and five unskipped successes at H. Logs distinguish required failure from incidental cleanup error. |
| AC-F6 | TESTABLE | Git 2.55 forced baseline has at least one Errno 39 cleanup failure in three runs; H succeeds 10/10 with zero such errors and no fixture/trace leftovers. The forced setting is explicit. |
| AC-F7 | TESTABLE | Twenty full-file natural runs in the real H clone all exit 0, report 39 tests and the one expected POSIX skip, with no Errno 39 or fixture leftovers. No retry-until-green interpretation. |
| AC-F8 | TESTABLE | Real H clone, one full-file run per selected Git, exit 0, 39 tests, only the identified Windows-specific skip. |
| AC-F9 | TESTABLE | Four explicitly listed core repository commands in a real H clone exit 0 with remeasured B summaries. Other full-tier unavailable coverage must be named by E; it is not silently folded into success. |
| AC-F10 | TESTABLE | Scope-lock paths unchanged; every commit in B..H enumerated and independently checked for a valid DCO trailer. No artificial one-commit requirement. |
| AC-F11 | TESTABLE after publication | Paginated checks/statuses plus mapped run/job IDs, logs, sole protected path, actual new method success, correct ci-tests summary, and verified advisory skips. Declared unavailable before publication; unavailable log is not an empty success. |
| AC-F12 | TESTABLE | Clean isolated candidate and byte-preserved existing source status; each H TMPDIR empty. B failures are retained separately. |
| AC-R1 | TESTABLE | REG only, zero deletions, raw base prefix intact, positive EOF append, both trailing newlines, one EOF hunk, and an ancestor base. This detects insertion inside an old record. |
| AC-R2 | TESTABLE | Main and other open-PR register headings have no duplicates; P-REG explicitly excluded; new N=K+1 at authoring and G. Failed fetch/missing blob is an investigation stop. |
| AC-R3 | TESTABLE | Complete 255-character original option appears exactly once on one line in the extracted new entry. Verified on the present draft. |
| AC-R4 | TESTABLE | Exact entry boundary, live H/tree/B/merge-base/path/numstat and check IDs agree. Presence checks are accompanied by equality to fresh measured values. |
| AC-R5 | TESTABLE | Three named commands at HR exit 0, zero broken/dead links, and rendered paragraphs/one-line source strings remain legible and faithful. |
| AC-R6 | TESTABLE after publication | Complete HR checks/status/run evidence; changes/validator/guard success, explained advisory skips, and no unexplained failing actual check. No P-REG exception is supplied. |
| AC-R7 | TESTABLE at P-REG G | The handoff's F comment ID identifies the actual ACCEPT at H/hash; MG3 result/unavailability and finding triage are timestamped; H is rechecked; HR's merge occurs afterward and is verified. Its future merge-time evidence is explicitly UNRUN at D. |
| AC-R8 | TESTABLE | Every one of the 15 enumerated selected source strings occurs intact in the new entry; values are parsed from the sources. All 15 are present in the current draft. |

### Completeness and unavailable coverage

- Negative cases: unfixed negative control, absent/lifeless trace, prohibited weakening, duplicate IDs, unreadable remote evidence, and unexpected checks are covered.
- Boundary cases: exact file/size, no deletions, one EOF append, main drift, pre/post recording head movement, and stale body hash are covered.
- Permission cases: P-REG cannot authorize itself; the one-time grant cannot cover another head/path/check; stage holders are separated; outside-contribution provenance triggers re-evaluation of MG5.
- Error/recovery cases: failed pinned call stops, uncertain merge outcome is read before retry, expired unused grant is recorded with or without regrant, and failures are retained.
- Timing/state cases: published checks and merge-time R7 are assigned to the stages that can actually observe them; P-REG's final merge follows P-FIX F/MG3 and precedes P-FIX G.

No uncovered class requires a new owner product decision for this bounded plan. Environment readiness remains an execution prerequisite: POSIX bash, the selected Git versions, and available Python/dependencies must be established before SD-C COMPLETE. A skipped Windows guard class is not a substitute. This is an existing plan gate, not an additional approval request from the audit.

## 7. Self-scrutiny and residual limits

**Strongest counterargument to ACCEPT:** this is still a proposed fix supported partly by archived reports. The old raw traces/harnesses are unavailable, this auditor ran no prototype, the execution environment is not yet established, and present admin-bypass capability is unverified. An acceptance that treated those historical numbers as current proof would be unsound.

I accept the plan because it does not do that. It has explicit fresh reproduction, liveness, flip, two-Git, forced/natural, repository, and hosted evidence gates; immutable head/tree/base and source-text checks; and a stop on unsupported execution or merge outcomes. The unresolved questions concern later observations, not missing acceptance properties or uncovered present scope. Acceptance is of this executable plan, while later stages must independently establish their own facts.

Evidence that would change this verdict: any changed plan hash; a different current implementation base without reconciliation; evidence the owner limited the entire repair to two lines; a fresh unfixed negative control without the required maintenance assertion; trace liveness failure or residual H maintenance; an unavailable required bug-fix floor treated as passed; an actual sequencing cycle; or an uncovered replacement vehicle/merge action treated as authorized.

Two execution cautions remain within the existing plan and do not require revision:

1. The complete source environment is more than the CI YAML. A passing static YAML check cannot prove absence of inherited runner config; keep the isolated negative control and actual candidate CI regression evidence.
2. A future replacement-register PR must have applicable authority for its actual vehicle and merge. Section 8.3 already requires that; the new owner question should make the complete replacement proposal reviewable. Q3 supplies consumption timing only.

The draft's root-cause sentence should be read with §3's explicit historical-inference limit. The original hosted leftover process was not captured. Subsequent reports should retain that limitation and describe fresh mechanism evidence as such.

**Intentionally not done:** implementation; any code/test changes; prototype or harness execution; repository test/validator runs; provider calls; credential/holdout access; reserved execution; new skill building; Git writes; fetch; commit; push; PR/comment creation; workflow dispatch/rerun; merge; settings changes. The sole network read was the public GitHub REST documentation, not the repository API. Current remote main, open PR membership, branch-protection/rules/actor capability, future PR IDs/heads/checks/reviews, and actual runtime results were not independently queried or executed in this Stage B audit.

## Appendix A — exact audited acceptance criteria

The following section is copied verbatim from the captured plan, with its original numbering and command blocks. The main audit above applies to the entire quoted criterion, including every compound clause.


Set `R=ModernNomad-98/Project-Aegis`, `F=scripts/tests/test_offline_ci.py`, and `REG=docs/approvals/APPROVAL_REGISTER.md`. B/H are P-FIX base/head; BR/HR are P-REG base/head; PF/PR are their integer PR numbers; N is the allocated approval ID (candidate 120). Variables are assigned verified values before commands run. Every candidate check uses the same immutable head/tree/base.

### P-FIX

**AC-F1 — One additive file with disclosed size.** `git diff --numstat "$B...$H"` returns exactly `a 0 scripts/tests/test_offline_ci.py`; `git diff --name-only "$B...$H"` has that sole path. The numstat deletion column, including deleted blank lines, governs. Report a; 28 is the disclosed prototype size, not an upper bound. Apply §4's notification/hold if different. Review diff positions against §3–§4.

**AC-F2 — No weakening.** `git diff "$B...$H" -- "$F" | grep -inE '^\+.*(skip|expectedFailure|ignore_cleanup_errors|retry|sleep|timeout)'` has no output (grep exit 1); an independent diff read confirms no assertion change, removal, retry, quarantine or suppression. A match requires investigation, not an automatic removal of the check.

**AC-F3 — Exactly one regression and one fixture call added.** Run this in the clone; it reads Git blobs without checking out or importing candidate code:

```bash
python3 -I -B - "$B" "$H" "$F" <<'PY'
import ast, subprocess, sys
def names(rev):
    raw = subprocess.check_output(['git', 'show', rev + ':' + sys.argv[3]])
    return {c.name + '.' + m.name for c in ast.parse(raw).body if isinstance(c, ast.ClassDef)
            for m in c.body if isinstance(m, ast.FunctionDef) and m.name.startswith('test_')}
b, h = names(sys.argv[1]), names(sys.argv[2])
print('added:', sorted(h-b), 'removed:', sorted(b-h), 'base=', len(b), 'head=', len(h))
raise SystemExit(not (h-b == {'ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance'} and not b-h and len(h) == len(b)+1))
PY
```

Expected counts 38→39 at M. Run §5's counter at B/H: fixture calls 88→89, class tests 10→11, no skipped guard tests. If measured baseline differs, stop for reconciliation rather than adjusting an expected value silently.

**AC-F4 — No maintenance spawn on any fixture path.** For each selected Git, in T(B) and T(H): `GIT_TRACE2_EVENT="$TRACE" python3 -B -P scripts/tests/test_offline_ci.py ProtectedFileGuardTests > "$LOG" 2>&1`, recording exit before parsing. Parse `child_start` and `start` events as §5 specifies; fresh base must exhibit maintenance and live upload-pack traces; H must show zero maintenance children, zero `gc --auto` children, zero maintenance starts, positive upload-pack count and 11 successful class tests. Historical base count 264 is corroboration, not a fabricated new observation. The regression owns its separate trace; the external class trace covers the other fixture calls and its own assertion covers its one call.

**AC-F5 — Deterministic flip.** Make a second exported H tree R0 and remove only the exact two config call lines using `sed -i '/git("config", "maintenance.auto", "false")/d; /git("config", "gc.auto", "0")/d' "$R0/$F"`. Raw newline count must drop exactly 2; diff must contain only those removals. In R0 then unmodified T(H), execute the new method five times per Git using `python3 -B -P scripts/tests/test_offline_ci.py ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance`. R0 must show the assertion failing for maintenance argv five times; a secondary cleanup error does not replace that required assertion evidence. H must exit 0 five times with no skip. Retain every invocation log.

**AC-F6 — Forced reproduction and removal.** For Git 2.55.0 only, use the forced environment in §5 and run the guard class three times on B and ten on H. B: at least one failure with Errno 39 through `run_guard` cleanup; also record any second-commit exit 128. H: ten successes, zero Errno 39, zero leftover fixture/trace directories under each dedicated TMPDIR. This is a bounded stress test, never a retry-until-green merge strategy.

**AC-F7 — Natural stress.** In the real clone at H, without forced config, run `python3 -B -P scripts/tests/test_offline_ci.py` 20 times with Git 2.55.0. All 20 must exit 0, report 39 tests and `OK (skipped=1)` on POSIX, with zero Errno 39 and no fixture leftovers. Preserve failures; do not discard early failures and report only later passes.

**AC-F8 — Full target file on both Gits.** In the real clone at H, run `python3 -B -P scripts/tests/test_offline_ci.py` once per selected Git. Expected exit 0, 39 tests, `OK (skipped=1)` on POSIX. The one skip must be the Windows-specific test. A Windows run's different skip count cannot substitute.

**AC-F9 — Core repository checks.** In the real clone at H, run the first four §5 baseline commands; each exits 0 with the same baseline summary as B. The offline-file command is AC-F8; fixture counting is AC-F3. Never run these repository checks in T(H). Additional full-tier CI steps and any UNRUN local steps are recorded by E with exact coverage; do not invoke reserved execution scripts to fill a gap.

**AC-F10 — Scope and DCO.** `git diff --quiet "$B...$H" -- .github/` exits 0, as do equivalent unchanged-file checks for the other scope-lock paths. Enumerate `git rev-list "$B..$H"`; for each commit inspect `git show -s --format=%B "$commit"` for its valid `Signed-off-by:` trailer. Report commit count and sign-off evidence per commit. Do not require a force-push merely to force count 1.

**AC-F11 — Published checks/logs bind to H.** Retrieve and retain:

```bash
gh api --paginate "repos/$R/commits/$H/check-runs?per_page=100" --jq '.check_runs[] | {id,name,status,conclusion,head_sha,details_url}'
gh api "repos/$R/commits/$H/status" --jq '{state,statuses}'
gh api "repos/$R/actions/runs/$RUN" --jq '{id,head_sha,event,status,conclusion,run_attempt}'
gh api --paginate "repos/$R/actions/runs/$RUN/jobs?per_page=100" --jq '.jobs[] | {id,name,status,conclusion,steps}'
gh api "repos/$R/actions/jobs/$GG_JOB/logs" > "$OUT/gg.log"
gh api "repos/$R/actions/jobs/$VS_JOB/logs" > "$OUT/vs.log"
awk '/Z Gate files touched:\r?$/{f=1;next} /Z This PR modifies the merge gate/{f=0} f' "$OUT/gg.log" | sed -E 's/^[^ ]+ +//; s/\r$//'
grep -nE 'Z (Ran [0-9]+ tests|OK \(skipped=[0-9]+\)|CHECK ci-tests: exit)' "$OUT/vs.log"
```

Resolve RUN from the check details URL/API and job IDs from the run's jobs list; verify mapping instead of assuming ID equivalence. The prior audit observed check-run ID=job ID, but that is historical. Log fetch failure is unavailable evidence, not an empty successful check. The anchored guard extractor must return exactly `scripts/tests/test_offline_ci.py`; the `Z` anchor avoids the echoed shell source. Validator log must show the added method passing, `Ran 39 tests`, `OK (skipped=1)`, and `CHECK ci-tests: exit 0` together in that step. Other suite summaries such as the historical `OK (skipped=5)` are identified by step, not mistaken for ci-tests coverage.

Expected job conclusions: `changes`/`validate-skills` success; `gate-guard` failure solely for the one protected path; `windows-offline-checks`/`tools-tests-linux`/`tools-tests-windows` skipped due to the successful path filter's `tools=false`/`offline=false`. Save the changes job log/output evidence too. Inspect every check and legacy status at H, not just required checks; any unexpected failing/cancelled/incomplete actual check stops progression. A queued external suite with zero check runs is recorded as such, not a green job. Use run-level completion/conclusions to resolve the documented job-status stale `in_progress` case; do not classify an otherwise complete successful run as pending solely from that stale field. An unexpected shape is investigated, never waived by the expected table.

**AC-F12 — Isolation.** Record `git status --porcelain` before/after in the actual implementation clone and any source checkout observed. Clean implementation candidate expected; pre-existing dirty source output is preserved byte-for-byte, not forced empty. Each H run's dedicated TMPDIR must be empty (`find "$TMPDIR" -mindepth 1 -print` on POSIX). Retained logs outside it are intentional. Preserve failing B fixtures as evidence; they are not H leftovers. Any cleanup later uses verified absolute scratch paths in one native shell.

### P-REG

**AC-R1 — Pure EOF append.** `git diff --numstat "$BR...$HR"` names REG only, zero deletions. Execute:

```bash
python3 -I -B - "$BR" "$HR" "$REG" <<'PY'
import subprocess, sys
b, h = [subprocess.check_output(['git', 'show', rev + ':' + sys.argv[3]]) for rev in sys.argv[1:3]]
ok = h.startswith(b) and len(h) > len(b) and b.endswith(b'\n') and h.endswith(b'\n')
print('byte_prefix=', h.startswith(b), 'base_newlines=', b.count(b'\n'), 'appended_newlines=', h[len(b):].count(b'\n'), 'both_end_newline=', b.endswith(b'\n') and h.endswith(b'\n'))
raise SystemExit(not ok)
PY
git diff -U0 "$BR" "$HR" -- "$REG" | grep '^@@'
```

Expected prefix True, exit0, and exactly one hunk whose prefix is `@@ -L,0 +L+1,n @@`, where L is the base blob's newline count and n the appended newline count; allow Git's trailing context after the second `@@`. No earlier byte may change. The three-dot numstat and direct BR/HR proof must refer to the same ancestor base; verify BR is the merge base first.

**AC-R2 — Unique next ID, excluding this PR.** Re-run at writing and at P-REG G. First count headings and duplicate IDs from current main and HR; zero duplicates. Enumerate open PRs using the actual P-REG number (before creation, PR=0 excludes none):

```bash
gh api --paginate "repos/$R/pulls?state=open&per_page=100" --jq ".[] | select(.number != $PR) | .number"
```

For each returned number n, in P-REG's isolated clone: `git fetch origin "pull/$n/head:refs/cifix/approval-collision/$n"`; read that ref's REG blob and extract `^### AEGIS-APR-[0-9]+:` headings. A failed fetch or missing/unreadable register requires investigation, not treating its maximum as zero. Let K be the maximum ID across main and those other PRs. N must equal K+1, and HR contains N exactly once as the appended grant. Main at writing has maximum119 and the coordinator observed zero open PRs, so N=120 is a candidate, never reserved permanently. A collision returns to the coordinator for allocation and renewed head-bound stages.

**AC-R3 — Original option intact.** In the extracted new entry e.md, `grep -cF -- "$GRANT_OPTION" e.md` returns 1 for the exact 255-character string in §7. Quotation stays on a single physical line.

**AC-R4 — Measured binding.** Extract e.md by its exact heading `### AEGIS-APR-$N:` through the next `### AEGIS-APR-` heading, or EOF, excluding the following heading. Compare H, `git rev-parse "$H^{tree}"`, B/`git merge-base "$B" "$H"`, sole path and `+a/−0` with fresh Git/API results. Each fixed value has `grep -cF` count ≥1 in e.md. Entry also gives actual check-run/workflow-run IDs, conclusions, and D audit comment URL; no prefilled future F comment.

**AC-R5 — Repository/docs checks.** In the real clone at HR: `python3 -B -P scripts/validate-skills.py`; `python3 -B -P scripts/tests/test_validator.py`; `python3 -B -P scripts/ci/check-markdown-links.py docs/approvals/APPROVAL_REGISTER.md`. All exit0; links report broken0/dead0. Link counts may increase. Read the rendered Markdown to confirm owner paragraphs remain legible and one-line source strings were not wrapped or typographically rewritten.

**AC-R6 — Published HR checks.** Reuse AC-F11's paginated check/status/run retrieval at HR. `changes`, `validate-skills`, `gate-guard` success; advisory three skipped by verified path scope. Any actual additional check must pass if applicable; record other status honestly. No guard exception for P-REG is authorized or expected.

**AC-R7 — Settled P-FIX state before P-REG merge.** P-REG G obtains the immutable Stage F comment ID F_COMMENT from F's handoff, not search results, and retains its exact body/time:

```bash
gh api "repos/$R/issues/comments/$F_COMMENT" --jq '{id,created_at,updated_at,body}'
gh api --paginate "repos/$R/pulls/$PF/reviews?per_page=100" --jq '.[] | {id,user:.user.login,commit_id,submitted_at,state,body}'
gh api --paginate "repos/$R/pulls/$PF/comments?per_page=100" --jq '.[] | {id,original_commit_id,created_at,updated_at,body}'
gh api --paginate "repos/$R/issues/$PF/comments?per_page=100" --jq '.[] | {id,created_at,updated_at,body}'
gh api "repos/$R/pulls/$PF" --jq '{head:.head.sha,body,updated_at}'
```

Read that identified F verdict's actual disposition line: it must be `SD-F: ACCEPT`, name H and the current bound-field hash, with author identity independent and no later superseding REVISE. A text search merely containing the token is invalid; the prior audit found that token inside a REVISE comment. Verify MG3 from exact-head automated result or an explicit unavailable-for-H notice; relate P0–P2 findings by `original_commit_id`, and retain each triage comment/commit and timestamp. An issue comment can be the unavailability record. No result for an earlier head and no silence substitutes. Recompute bound fields and confirm live head=H. Store verification UTC plus evidence IDs and timestamps. After merge, `gh api "repos/$R/pulls/$PR" --jq '{merged,merged_at,merge_commit_sha,head:.head.sha}'` proves P-REG merged; its `merged_at` must be later than the relevant F, automated result/unavailability, final triage and premerge verification times. Check HR is the candidate actually merged. The live observations are repeated immediately before the merge; re-check PF after it as well and use §8 if it moved.

**AC-R8 — Every owner source string present.** In e.md use `grep -cF -- "$text" e.md` once for each: the 588-character grant question and 255-character grant option from BRIEF; all six JSON question/description strings (the three `questions[*].question` fields and three chosen `options[0].description` fields); all four selected labels (the grant label plus the three JSON `options[0].label` values); and the OQ-C question, label, and description from the later BRIEF. Each count ≥1. Obtain strings by JSON parsing/the one-line brief source, not retyping or whitespace-normalizing them. Preserve UTF-8 punctuation. If a source string is absent or wrapped, repair the unmerged entry; no fallback assertion of equivalent meaning. **Explicit RC13(c) count correction, confirmed by the coordinator in this planning turn:** the audit's eight-row quotation table comprises two BRIEF strings plus six JSON question/description strings; they are not eight JSON strings. Including the three JSON labels gives nine selected JSON fields. This enumeration corrects that label without dropping coverage. Text matching proves transcription only, not owner authority; the complete question/selection/provenance provides that context.


## Final Stage B handoff

- **Decision IDs retained:** SD-A through SD-G and MG1 through MG5, unchanged. This audit changes no owner grant, lifecycle event, gate, classification floor, or reserved boundary.
- **Final plan binding:** Get-FileHash / hashlib before and after the audit both resolve to 97c09c154034b050e80e996a55fceb1c22439cc32f44d62c34ed3536fe3fb487. The final read also independently re-resolved M/S and the source HEAD above.
- **Final read-only check outputs:** source status still contains exactly the two pre-existing untracked directories recorded in §1. Exit 0. No source or persistent Git state/configuration mutation was performed.
- **Read failure and recovery:** the first finalization script, launched from the scratch workspace, stopped on Git exit 128 (dubious ownership under the sandbox user) before writing its handoff. It was repeated using per-command -c safe.directory for this verified clone only; ref/status reads then succeeded. No global or local Git configuration was written.
- **Artifact read-back:** exact Appendix A equality to the captured plan; 20 original numbered criteria and 20 testability rows; forbidden reviewer invocation string count 0; trailing LF present. Exit 0. These inspect the audit artifact only and are not repository test runs.
- **Touched files:** this audit artifact only. PLAN-rev3.md, the source checkout, S, and every external system were left unchanged.
- **Unknowns:** original-transcript authentication; future execution-host/runtime availability and actual reproduction results; current remote drift, PR membership, protection/rules/actor capability; future H/HR/PR/check/review/merge outcomes. No historical test report is promoted to current proof.
- **Continuation:** the coordinator may hand this unchanged plan and audit to separate Stage C holders under the plan's entry conditions. Establish the required execution environment and refresh main before implementation; any different base follows the plan's reconciliation rule. No implementation on rev2; no new plan revision is covered by this verdict. This Stage B holder holds no later stage and will not audit another revision without a new assignment.
- **Timing:** start 2026-10-08 19:01:17 UTC; finish 2026-10-08 19:17:22 UTC; measured elapsed wall time 16 minutes 5 seconds. Active time was not measured. The 25–40-minute initial estimate was for active work, so this shorter wall time is only an imperfect comparison.

**SD-B: ACCEPT — P-FIX and P-REG, PLAN-rev3 SHA-256 97c09c154034b050e80e996a55fceb1c22439cc32f44d62c34ed3536fe3fb487, source M 5228977920ee479e1fe1ec6b8d56f8fc24c14947, handoff S 32f5ae25780c4802184a63d4063507fcf31b3a37. Required changes: none.**
