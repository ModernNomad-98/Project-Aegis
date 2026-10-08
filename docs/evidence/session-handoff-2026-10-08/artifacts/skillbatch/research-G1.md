# Research G1 — QA Tier 2 candidates (skill-batch planning, Stage A support)

- **Helper:** QA-A research helper, group G1 only. Planning research; writes no repository file.
- **Base read:** `origin/main` = `5228977920ee479e1fe1ec6b8d56f8fc24c14947`
  (`git ls-remote origin refs/heads/main` → `5228977920ee479e1fe1ec6b8d56f8fc24c14947 refs/heads/main`).
  The local checkout was detached at `c060a7cb`, so every file was read from a fresh
  `git archive 52289779 | tar -x` copy at `$S/skillbatch/g1-tree/`. Earlier helpers' working files were not used.
- **Role:** Role A (source library). The four landmarks exist in the base tree: `README.md` starts `# Project Aegis`,
  plus `docs/skills-catalog.md`, `scripts/validate-skills.py` and `artifacts/audits/skill-contract-audit-baseline.json`.
- **Library state:** `python3 -B scripts/validate-skills.py` on the base copy → `OK: 195 skill(s) valid, 0 warning(s)`.
  There are 196 directories under `.claude/skills/`, counting `_template`. Of those, 30 have
  `disable-model-invocation: true` in frontmatter, all with the `MANUAL-ONLY; never auto-invoke.` sentinel
  (counted by parsing frontmatter, not by grep).
- **Start:** 2026-10-08T17:11:40Z (`date -u`). **Finish:** see the end of this file.
- **Skills used (dogfood rule):**
  - `skill-quality-reviewer` supplied the method: check 2 (trigger collision, sweeping the whole corpus), check 3
    (extension or new skill), check 7 (invocation posture) and the near-miss-name rule, from
    `references/quality-review-checklist.md:57-106,170-184`. It was **not invoked as a review**. Its stop condition
    is "the target skill's directory or SKILL.md is missing … stop" (`SKILL.md` Stop Conditions), and none of these
    candidates exists yet.
  - `prioritization-frame-picker` supplied the ranking method: a coarse value-versus-effort cut, ranges instead of
    decimals, and a check that the order still holds if an input is off by 2× (`SKILL.md` Workflow steps 2–4).
  - Neither skill is MANUAL-ONLY (0 sentinel matches in either file).

Terms: **QA** is quality assurance. **CI** is continuous integration. **E2E** is end-to-end.
**Auto-invocable** means the assistant may pick the skill on its own. **MANUAL-ONLY** means a person must name it.
**ROUTE-002** is the contract-audit census note that skill A routes to skill B but B never names A
(information only; D64 keeps such one-way findings as census data,
`docs/reconciliation/step-0-reconciliation-v4.md:3283-3290`).

---

## Summary table

| Candidate (roadmap rows, priority) | Verdict | Shape recommended | Manual-only? | Active hours (provisional, low confidence) |
| --- | --- | --- | --- | ---: |
| `visual-regression-test-designer` (cat 06 #203 P2; also absorbs cat 05 #179 P2, #202 P2 snapshot selection, and the fixture-mode slice of #189 P1) | **NEW** (no shipped owner) | **BUILD** | No (design only) | 3.25–5 |
| `exploratory-testing-charter` (#228 P1) | **NEW** (no shipped owner) | **BUILD**, renamed `exploratory-charter-designer` | No (design + debrief only) | 2–3.5 |
| `mobile-viewport-qa` (#230 P1) | **PARTIAL**: design is owned by `mobile-viewport-craft`; journey verification on mobile is unowned | **BUILD**, renamed `mobile-journey-test-designer` (the proposed name is a near-miss) | No (design only) | 2.5–4 |
| `role-based-qa-matrix` (#229 P1) | **PARTIAL**: denials are owned by `authorization-matrix-designer` and `multi-tenant-security-tester`; the allowed side, UI consistency and role changes are unowned | **BUILD, narrowed**, renamed `role-coverage-test-designer` (the one to defer if the batch must shrink) | No (design only) | 2.5–4 |
| `mock-strategy-designer` (#200 + #201, both P1) | **COVERED** across five shipped skills | **DROP**; add a covered-table row | not applicable | 0–0.25 |
| `ci-shard-parallel-isolation` (#211 + #212, both P1) | **COVERED** by `sharded-validation-with-resume`, `qa-automation-architect`, `test-data-architect` and `playwright-e2e-engineer` | **DROP**; add a covered-table row | not applicable | 0–0.25 |
| E1: `qa-automation-architect` extension (hand-off #213 P1 timeout policy, plus the optional #200 and #212 residuals) | **PARTIAL (minor)**: setting timeouts is unowned; classifying them is owned by `ci-failure-classifier` | **EXTEND** (one lane only) | not applicable (base stays auto-invocable) | 1–2 |
| #189 record (hand-off; fixture-mode slice goes to candidate 1) | **COVERED by split** | record plus a dated note on the v4 absorbed list | not applicable | in the drops' 0–0.5 |
| Batch overhead (registration ×4, decision row, reciprocity body edits, optional Stage 7 wiring, reviews) | — | — | — | 2–3.5 |
| **Total** | **4 new skills, 1 extension, 2 drops (+ #189 record)** | | | **13.25–22.5** |

The forecast carries G1 as "QA expansion Tier 2 (six skills) | 12–24 | Ideally after Tier 1"
(`docs/roadmaps/aegis-backlog-forecast.md:726`). It also says "All ranges are agent estimates with low confidence" (:721).
Tier 1 was delivered under D68 (`docs/reconciliation/step-0-reconciliation-v4.md:3385`). The recommended set comes in
inside the forecast range, although two candidates do not become skills, because it also absorbs three hand-off rows
(#202, #213 and part of #189) that the forecast counted under "Phase 5 extras" (`aegis-backlog-forecast.md:731`).

---

## Shared evidence: what D10 did and did not see

D10, the decision that tiered this backlog, was merged in PR #17 at **2026-07-07T07:15:13Z**
(`gh api repos/ModernNomad-98/Project-Aegis/pulls/17` → `17 2026-07-07T07:10:02Z 2026-07-07T07:15:13Z`). Its audit
baseline was "the 16 shipped Phase 5 skills … plus QA coverage living cross-phase" (`step-0-reconciliation-v4.md:983-996`).

- **Shipped after D10:** `sharded-validation-with-resume` (first commit `27d2a216`, 2026-07-07T18:42:14-07:00 =
  2026-07-08T01:42Z, PR #32) and `mobile-viewport-craft` (`e58cd162`, 2026-07-08T00:00:28-07:00 = 2026-07-08T07:00Z,
  PR #35) (`git log --diff-filter=A … -- .claude/skills/<name>/SKILL.md`). D10 could not account for either one. That
  matters for #211 and #230.
- **Shipped before D10:** the decisive mock and parallel-isolation content was already there at D10's baseline commit
  `f00948df`. `git show f00948df:<file> | grep -cF` returned 1 for each of these strings:
  - "FAKED seam" and "Faked seams drift" in `integration-test-designer`;
  - "Mock only owned boundaries" in `vitest-unit-component-engineer`;
  - "Keep fakes faithful" and the "fake drifted" eval in `api-contract-test-designer`;
  - "Design isolation & parallelization" in `qa-automation-architect`;
  - "Design parallel isolation" in `test-data-architect`;
  - "Asserting against the mock" in `test-coverage-mapper`;
  - `--shard` in `playwright-e2e-engineer`.

  So for #200/#201 and #212, my COVERED verdicts **disagree with D10's judgment of the same content**, not with a gap
  D10 failed to see. I explain why under each candidate. The QA Tier 1 proposal set the precedent for correcting a D10
  note forward (`docs/roadmaps/qa-tier1-skill-batch-proposal.md:90-121`, the #190 drop).
- **Demand:** I found no recorded demand for any G1 topic. A repo-scoped listing of all 680 issues and PRs
  (`gh api repos/…/issues?state=all&page=1..9`; only issue #101 is a true issue) matched only PR #17 (the D10 backlog
  itself) for every G1 keyword. The single "exploratory" hit, PR #183, refers to the VolunteerFlow handoff, an
  exploratory test of Aegis itself. Its one role-related finding, AEGIS-009, is spec-level
  (`docs/audits/volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md:311-320`) and is recorded
  "Symptom corrected" (:1001). **The only priority signal is the roadmap and reconciliation tiering.** Value claims
  below are limited to coverage-gap evidence.

---

## Candidate 1 — `visual-regression-test-designer` (#203)

**(1) Source rows.**
- Cat 06 #203 "Visual Regression Test Design | P2 | Capture critical UI states with stable data, deterministic viewport,
  and reviewable diffs." (`docs/skills/06-qa-test-engineering.md:49`).
- D10 placed it in Tier 2 "plus #203 promoted because UI drift is otherwise invisible to the shipped suite"
  (`step-0-reconciliation-v4.md:251-252,256`).
- Related unmapped row: cat 05 #179 "Visual Regression Readiness | P2 | Identify stable screens and states suitable for
  screenshots or visual diff testing." (`docs/skills/05-frontend-ux-engineering.md:44`). It has no catalog source
  mapping (`grep -nE '(#|\b)179\b' docs/skills-catalog.md step-0-reconciliation-v4.md` → only skill-count text).

**(2) Overlap verdict: NEW.**
- Corpus sweep `grep -rniE 'visual[- ]regression|visual diff|toHaveScreenshot|pixel|screenshot (diff|comparison|baseline)|snapshot (diff|baseline)|golden image|percy|chromatic|applitools|baseline image' .claude/skills`
  found exactly one relevant line, the pointer in `screenshot-evidence-planner/SKILL.md:33-35`: "Do NOT use when: the
  ask is visual-regression pixel-diff tooling — that is automation architecture (`qa-automation-architect`) with this
  policy as input." The other hits are unrelated (prompt-injection pixels, masking, CSS pixel units).
- That pointer lands on a skill with no visual content. `qa-automation-architect`'s default stack table
  (`references/automation-blueprint.md:8-17`) lists unit, integration, contract, E2E, a11y and build QA, with no visual
  layer, and its SKILL.md never mentions visual diffs (read in full, 166 lines).
- `qa-strategy-architect` routes "visual/judgment checks → manual + screenshot evidence" (`SKILL.md:67-68`).
  Automated visual diffing therefore has no owner anywhere.
- Neighbors own adjacent slices:
  - `screenshot-evidence-planner` owns evidence capture-quality rules ("deterministic viewport(s), stable/seeded data",
    `SKILL.md:100-102`), naming, masking and storage. Visual baselines must follow its masking rule.
  - `test-coverage-mapper` treats "Snapshot-everything tests nobody reviews on update" as test theater
    (`references/coverage-mapping-method.md:30`).
  - `code-reviewer` flags "snapshots regenerated without a reason" (`references/severity-rubric.md:64-65`).
  - `playwright-e2e-engineer` (manual-only) would implement the specs.
- The genuinely new content is: risk-ranked state inventory, capture determinism (fonts, animation, time, data),
  dynamic-region masking, diff thresholds, baselines per browser and OS, human-reviewed baseline updates, CI tier
  placement, and the owner's tool choice.
- **Extension or new?** The checklist says a separate skill is right when "the output artifact differs in kind, or the
  base skill would need a new Output Format" (`quality-review-checklist.md:104-106`). Library structure points the same
  way: each layer row in the blueprint points to its own designer skill, for example "A11y automated | … | harness per
  `accessibility-test-harness`" (`automation-blueprint.md:16`). So the shape is a new skill plus one new blueprint row.
- Lexical check: TF-IDF cosine of the draft description against all 195 shipped descriptions, with parenthetical skill
  names removed. The highest score was 0.113 (`cloud-security-baseline-reviewer`), then `playwright-e2e-engineer` 0.109.
  No strong lexical neighbor exists, which is consistent with NEW. This is a crude signal and is not used as proof.

**(3) Posture: auto-invocable.** It designs and reports, and it writes no tests and updates no baselines.
- Rule: "Any write/network/deploy/spend behavior requires … `disable-model-invocation: true`" (`docs/skill-generation-standard.md:271-275`);
  pure design stays auto-invocable (`quality-review-checklist.md:176`).
- It must teach the hosted-service versus self-hosted tool choice under the AGENTS.md build-choice rule. The choice
  authorizes no spending.
- Stop Condition to write: a request to run the suite or accept baselines is an implementation step and goes to the
  manual-only engineer skills. If the owner wants the skill itself to update baselines, the posture flips to MANUAL-ONLY.

**(4) Estimate: 3–4.5 h for #203 alone; 3.25–5 h with the hand-off absorptions (#202 selection rule, #189
fixture-mode slice; see "Hand-off rows" below).**
- Basis: the closest precedents are design skills that teach an owner spend or tool choice, estimated at 3–5
  (`ai-human-in-the-loop-designer`, `phase7-ai-engineering-skill-batch-proposal.md` table row) and 3–4.5
  (`resilience-architecture-reviewer`, `phase6-reliability-skill-batch-proposal.md` table row).
- Reciprocity is mostly body edits: `screenshot-evidence-planner` (description 999 characters; change the body pointer
  at :33-35), `qa-automation-architect` (903; add the blueprint row), and `qa-strategy-architect` (832; add an
  automated-visual option at :67-68).
- No active-time measurements exist (see "Estimate basis" below). **Low confidence.**

**(5) Value and dependencies.**
- Value: closes the only UI-regression class with no automated owner. That gap is evidenced above; how much it matters
  to users is unverified.
- Depends only on shipped skills: `screenshot-evidence-planner`, `qa-automation-architect`, `test-data-architect`
  (stable data), `playwright-e2e-engineer` (implementation) and `mobile-viewport-craft` (breakpoints).
- Seam with candidate 3: both use a viewport matrix. Visual baselines per viewport belong here; functional mobile
  checks belong to candidate 3.

**(6) Trigger boundary.**
- **Use when:** UI changes ship unnoticed; snapshot or visual tests are noisy or rubber-stamped; before adopting a
  visual-diff tool; when choosing which states deserve baselines.
- **Not when:** setting the evidence-screenshot policy (`screenshot-evidence-planner`), designing the whole framework
  (`qa-automation-architect`), writing specs (`playwright-e2e-engineer`, manual-only), or designing the responsive
  layout (`mobile-viewport-craft`).
- **Trigger-evals must pin against:** `screenshot-evidence-planner` (the main collider: "what screenshots do we need"
  versus "diff baselines"), `qa-automation-architect` (tooling and CI), and `playwright-e2e-engineer` (cases must use
  `Explicitly invoke playwright-e2e-engineer. `, per `skill-generation-standard.md:574-576`).
- Draft description: 973 characters measured with `yaml.safe_load` (see appendix).

## Candidate 2 — `exploratory-testing-charter` (#228) → `exploratory-charter-designer`

**(1) Source row.** Cat 06 #228 "Exploratory Testing Charter | P1 | Define mission, risks, personas, data, paths, and
timebox for exploratory testing." (`06-qa-test-engineering.md:74`); D10 Tier 2 (`step-0-reconciliation-v4.md:259`).
Historical note: the superseded July proposal put "exploratory charters" inside `test-plan-designer`
(`docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md:144`; status "Historical proposal … v4 reconciliation
supersedes", :3-5). The shipped `test-plan-designer` has 0 matches for `exploratory|charter` (grep -c on SKILL.md and
its template).

**(2) Overlap verdict: NEW.**
- `grep -rniE 'exploratory|charter|session-based|time-?box' .claude/skills` returns no exploratory-testing owner. The
  only exploratory-related lines are:
  - `clickthrough-test-engineer/SKILL.md:19-20`: "systematic verification-by-driving, not a permanent test suite and
    not exploratory wandering";
  - `qa-strategy-architect/SKILL.md:142-144`: "Strategies that omit manual/judgment testing entirely leave visual, UX,
    and exploratory risks unowned".
- `manual-test-case-creator` writes scripted cases with "ONE observable expected result per step" (description), which
  is the opposite of a charter.
- **Extension or new?** An extension into `test-plan-designer` was considered and rejected on evidence:
  - a charter set plus a session debrief is a different artifact from a per-change test plan, and would need a new
    Output Format block (checklist rule, `quality-review-checklist.md:104-106`);
  - `test-plan-designer`'s description is already 961/1,024 characters (measured), so an exploratory trigger phrase
    would push out existing text.
- Lexical nearest neighbors: `test-plan-designer` 0.219, `manual-test-case-creator` 0.183, `qa-strategy-architect` 0.143.

**(3) Posture: auto-invocable.** It writes charters and turns supplied notes into a debrief, and runs no session.
Running a chartered session in a live app drives a browser, which belongs to a human or to the manual-only
`clickthrough-test-engineer`. Stop Condition to write: "explore the app now" is refused or handed off.

**(4) Estimate: 2–3.5 h.** Basis: the closest precedent is `acceptance-criteria-reviewer`, a document-shaped, read-only
skill with 4–5 neighbors, estimated at 2–3.5 (`qa-tier1-skill-batch-proposal.md:63,489`). Reciprocity is body-level:
`clickthrough-test-engineer` (1,008 characters, no room) at :19-20, and `qa-strategy-architect` (832, room exists) at
:142-144. **Low confidence.**

**(5) Value and dependencies.** It fills a gap that `qa-strategy-architect` itself names as a risk. It is the cheapest
candidate. It depends on shipped skills only: `qa-strategy-architect` (risk inventory), `test-data-architect`
(personas and data), `screenshot-evidence-planner` (session evidence) and `manual-test-case-creator` (scripting what is
worth keeping). No demand evidence beyond the P1 label.

**(6) Trigger boundary.**
- **Use when:** a feature needs human exploration beyond scripted cases; before a release or bug bash; when the QA
  strategy leaves exploratory risk unowned; when debriefing session notes.
- **Not when:** writing scripted cases (`manual-test-case-creator`), running a planned walkthrough
  (`clickthrough-test-engineer`, manual-only), writing the per-change plan (`test-plan-designer`), or setting product
  strategy (`qa-strategy-architect`).
- **Pin against:** `test-plan-designer`, `manual-test-case-creator`, and `clickthrough-test-engineer` (with the
  "Explicitly invoke" prefix).
- Draft description: 912 characters.

## Candidate 3 — `mobile-viewport-qa` (#230) → `mobile-journey-test-designer`

**(1) Source row.** Cat 06 #230 "Mobile Viewport QA | P1 | Verify critical journeys on mobile breakpoints, touch
interactions, dialogs, and navigation." (`06-qa-test-engineering.md:76`); D10 Tier 2 (`step-0-reconciliation-v4.md:258`).

**(2) Overlap verdict: PARTIAL.**
- **Design is owned.** `mobile-viewport-craft` (shipped after D10) owns "layout/touch/viewport CORRECTNESS"
  (description; `SKILL.md:30-31`). Its workflow covers breakpoints, touch targets, safe areas, viewport units, keyboard,
  hover and reflow (:77-116). Its output is a craft **spec** (:133-148). It routes only accessibility verification
  onward, to `accessibility-test-harness` (:52-55, 208-211). Its trigger-evals overlap only `frontend-perf-engineer`,
  `edge-state-ux-designer` and `accessibility-test-harness` (`evals/trigger-evals.json` `overlaps_with`).
- **Journey verification on mobile is unowned.**
  - `clickthrough-test-engineer`'s route catalog says: "Default: desktop 1280×800 + one mobile width (375×812) on
    customer-facing routes. Deep responsive QA is its own effort" (`references/clickthrough-route-catalog.md:30-32`).
  - `playwright-e2e-engineer` has 0 mobile, device or viewport matches in SKILL.md
    (`grep -ciE 'mobile|device|viewport|touch'`). The single hit in its patterns file is "touching a real application".
  - `accessibility-test-harness` checks zoom and reflow at 200%/400% (`SKILL.md:103`; `references/a11y-checklists.md:30`)
    but not touch, dialogs or navigation journeys.
- **Extension or new?** A verification design is a different artifact from a craft spec, and the library already pairs
  design skills with verification skills. Example: `frontend-perf-engineer`'s trigger-evals route "Set up the lab
  measurement that runs our key pages on a throttled mobile profile … fails CI on regression" to
  `performance-test-harness` (`frontend-perf-engineer/evals/trigger-evals.json:21`).
- **Name:** `mobile-viewport-qa` is one word away from `mobile-viewport-craft`, and the checklist treats a near-miss
  name as "a CONCERN/FAIL by closeness" (`quality-review-checklist.md:86-89`). Proposed rename:
  `mobile-journey-test-designer`, following the `integration-test-designer` / `api-contract-test-designer` pattern.
  The owner decides the final name.
- Lexical nearest neighbor: `mobile-viewport-craft` **0.321**, the strongest collision risk in G1. Trigger-evals must
  discriminate both ways.

**(3) Posture: auto-invocable** (design only). Running emulated or real-device sessions belongs to manual-only skills
or humans. A device-cloud subscription is an owner spend choice to teach, never authorized by this skill. Stop Condition
to write: executing on devices is refused or handed off.

**(4) Estimate: 2.5–4 h.** Basis: comparable to `ci-failure-classifier` 2.5–4 (`qa-tier1-skill-batch-proposal.md:62`)
and `environment-parity-reviewer` 2.5–4 (`phase6-reliability-skill-batch-proposal.md` table). The upper end allows for
the two-sided seam with `mobile-viewport-craft`, whose 993-character description has no room, so its side of the seam
lives in trigger-evals and body text. **Low confidence.**

**(5) Value and dependencies.** It closes the verification half of P1 #230. It consumes the `mobile-viewport-craft`
spec as its oracle, plus `test-data-architect` personas and `screenshot-evidence-planner` evidence. Implementation is
handed to `playwright-e2e-engineer` (manual-only) or to manual passes. It shares the viewport matrix with candidate 1.

**(6) Trigger boundary.**
- **Use when:** a release must be proven on phones or tablets; mobile bugs keep reaching users; choosing emulation
  versus real devices.
- **Not when:** designing or fixing the responsive layout (`mobile-viewport-craft`), mobile performance
  (`frontend-perf-engineer` / `performance-test-harness`), accessibility verification (`accessibility-test-harness`),
  or running the session (`clickthrough-test-engineer`).
- **Pin against:** `mobile-viewport-craft` (the main collider: "fix the overflow on phones" goes there; "prove checkout
  works on phones" comes here), `clickthrough-test-engineer`, and `accessibility-test-harness`.
- Draft description: 959 characters.

## Candidate 4 — `role-based-qa-matrix` (#229) → `role-coverage-test-designer` (narrowed)

**(1) Source row.** Cat 06 #229 "Role-Based QA Matrix | P1 | Test behavior across anonymous, member, manager, admin,
owner, support, and platform roles." (`06-qa-test-engineering.md:75`). D10 note: "QA counterpart to Phase 3
`authorization-matrix-designer`" (`step-0-reconciliation-v4.md:257`).

**(2) Overlap verdict: PARTIAL.**
- **The denial side is owned twice.**
  - `authorization-matrix-designer` step 7 "Define the negative-test plan: for each sensitive permission and each
    privileged role boundary, a test where the disallowed actor attempts the action and the expected result is denial"
    (`SKILL.md:102-105`), with a negative catalog for IDOR, vertical escalation, horizontal reach, revocation,
    impersonation expiry, machine actor and disabled tenant (`references/authorization-matrix-template.md:42-56`).
  - `multi-tenant-security-tester` (manual-only) builds "surface × actor (wrong-tenant, wrong-role, anonymous,
    service-role/job) × operation × expected result (deny…)" (`SKILL.md:76-80`), with a mandatory positive control
    per denial (`SKILL.md:84`; `references/negative-test-matrix.md:64`).
- **The allowed side is unowned.**
  - The authorization design writes every allow down (`authorization-matrix-designer/SKILL.md:18`) but plans tests
    only for denials.
  - Its own enforcement map marks UI hide/disable as "No — UX only" (`authorization-matrix-template.md:35`). Nothing
    verifies that each role sees controls consistent with the server decision, except one-session
    `clickthrough-test-engineer` "Permission-gated controls checked per persona" (`SKILL.md:105`, manual-only).
  - `test-coverage-mapper` is the catalog owner of #191 ("happy paths for each user role"), but its SKILL.md and
    references have 0 matches for `role|persona|golden` (grep).
- **Genuinely new content:** a role-by-journey matrix derived from the authorization matrix; a positive test per allowed
  capability at the cheapest layer; UI-versus-server consistency per role; role-change cases (promotion, demotion,
  removal mid-session, ownership transfer); support and platform modes as functional behavior; per-role evidence.
- **Extension or new?** An extension of `authorization-matrix-designer` (description 493 characters, plenty of room)
  was considered. It fails the checklist's "trigger situations are disjoint / output differs in kind" test: "design
  roles and permissions" is a different situation from "verify the app for every role", and the output is a coverage
  matrix, not an authorization model (`quality-review-checklist.md:101-106`). The narrowing is required. It must
  **delegate, never re-specify**, denial proof, or it collides with both owners on their core cases (check 2 FAIL rule,
  :79-80).
- Lexical nearest neighbors: `test-tenant-provisioner` 0.169, `authorization-matrix-designer` 0.169,
  `multi-tenant-security-tester` 0.161, `qa-strategy-architect` 0.142. It is a three-way neighbor set.

**(3) Posture: auto-invocable** (design only). Creating role accounts belongs to `test-tenant-provisioner`
(manual-only); executing belongs to the engineer skills.

**(4) Estimate: 2.5–4 h.** Basis: comparable to `ai-task-decomposer` 2.5–4 (`ai-sdlc-skill-batch-proposal.md` table).
The upper end reflects three-way trigger-eval discrimination. The reciprocity edit to `authorization-matrix-designer`
fits (493 characters). **Low confidence.**

**(5) Value and dependencies.** Role-specific bugs in multi-tenant SaaS are a plausible class, but I found **no
recorded demand** (AEGIS-009 is spec-level and corrected). It depends on `authorization-matrix-designer` output (the
oracle) and `test-data-architect` / `test-tenant-provisioner` personas.
- *Unverified cross-group risk:* G4's `role-permission-architect` and `membership-invitation-designer` and G6's
  `e2e-test-architect` ("roles, tenants" in E2E journeys, `product-agnostic-skill-and-agent-roadmap.md:147`) may become
  further neighbors. Their verdicts belong to the P34 and QA-B helpers and are not checked here.
- This is the candidate to defer if the owner wants a smaller batch, because its gap is the narrowest of the four
  builds.

**(6) Trigger boundary.**
- **Use when:** asked to test the app for each role; role-specific bugs reach users; after roles or permissions change.
- **Not when:** designing roles and permissions (`authorization-matrix-designer`), proving cross-tenant or wrong-role
  denials (`multi-tenant-security-tester`, manual-only), creating test accounts (`test-tenant-provisioner`,
  manual-only), plan entitlements (`plan-entitlement-architect`), or one change's plan (`test-plan-designer`).
- **Pin against:** `authorization-matrix-designer`, `multi-tenant-security-tester` (with the "Explicitly invoke"
  prefix), and `test-plan-designer`.
- Draft description: 974 characters.

## Candidate 5 — `mock-strategy-designer` (#200 + #201)

**(1) Source rows.** #200 "Mock Strategy Design | P1 | Choose mocks, fakes, stubs, adapters, recordings, or live tests
based on risk and confidence." and #201 "Test Double Contract Review | P1 | Ensure mocks and fakes stay aligned with real
provider and database behavior." (`06-qa-test-engineering.md:46-47`). D10 merged them: "ONE skill … (`api-contract-test-designer`'s
fake-fidelity check is the contract-layer slice of this)" (`step-0-reconciliation-v4.md:260`).

**(2) Overlap verdict: COVERED.** Every clause of the two rows has a shipped owner.

| Roadmap clause | Shipped owner and evidence |
| --- | --- |
| Choose mock / fake / real per dependency (integration layer) | `integration-test-designer` step 1 "Draw the boundary map first … REAL … or FAKED seam … Every fake gets a one-line rationale" (`SKILL.md:70-76`); classification table (`references/boundary-catalog.md:8-19`) |
| Adapters | "fakes live at OWNED adapters … never by patching a vendor SDK's internals" (`boundary-catalog.md:21-22`); unit layer "wrap the library in an owned adapter and mock the adapter" (`vitest-unit-component-engineer/references/vitest-patterns.md:35-37`) |
| Mocks and stubs (unit layer) | `vitest-unit-component-engineer` step 3 "Mock only owned boundaries" (`SKILL.md:64-67`, manual-only) |
| Per-layer fake/real posture (strategy) | `qa-strategy-architect` step 4 "what runs against in-memory fakes, what needs a seeded database, what needs a deployed environment" (`SKILL.md:74-77`); blueprint "In-memory fake … unit only — never call it integration" (`qa-automation-architect/references/automation-blueprint.md:46`) |
| Recordings and live tests | `api-contract-test-designer` recipes: "Recorded fixtures: re-record or re-validate against the provider sandbox on a schedule only when that external execution is authorized" (`references/contract-test-patterns.md:39-48`) |
| #201 fakes stay aligned with the real provider | `api-contract-test-designer` "Use when: our system CONSUMES a third-party provider and fakes/recordings must be proven faithful" (`SKILL.md:33-34`) and step 6 "Keep fakes faithful" (:84-86); pinned eval `edge-consumer-side-fakes`: "Our integration tests fake the payment provider, and last month the fake drifted from the real API. Prevent that." (`evals/evals.json:21-31`) |
| #201 fakes stay aligned with real DB behavior | The DB is never faked at the integration layer: "Database, auth, and permission paths under test are REAL; any mock of them reroutes the spec to unit" (`integration-test-designer/SKILL.md:142-143`); "seed via real migrations + factories so constraint and default behavior is production-shaped" (`boundary-catalog.md:33-35`) |
| Reviewing existing doubles for theater | `test-coverage-mapper`: "Asserting against the mock itself" and "Integration tests where every boundary is mocked: reclassify" (`references/coverage-mapping-method.md:33-36`) |

- **Why I disagree with D10.** D10 credited only the contract-layer slice. All the content above existed at D10's
  baseline (see "Shared evidence"). A new skill would fire on `api-contract-test-designer`'s pinned core case and on
  `integration-test-designer`'s "units are green but wiring keeps breaking — mocks drifted" (`SKILL.md:28-29`). That
  is a check 2 FAIL by the checklist's own rule (:79-80).
- **Residual (optional, not recommended as a skill):** one cross-layer "test-double selection" table, saying which
  double type per layer and when to move up to a recording or live sandbox. It could become a 0.5–1 h reference addition
  to `qa-automation-architect`. That would also make its catalog source citation "cat 06 #200" (`docs/skills-catalog.md:522`)
  match its body, which today mentions fakes only in the DB-isolation table.

**(3) Posture:** not applicable; nothing is built. **(4) Estimate:** 0–0.25 h (covered-table row and dated D-row note),
or 0.5–1 h with the optional reference row. **(5) Value:** a new skill would add no capability. **(6) Trigger
boundary:** none new. Optional proof: one trigger-eval case in `integration-test-designer` for "should we mock the
payment API or hit the sandbox in these tests?".

## Candidate 6 — `ci-shard-parallel-isolation` (#211 + #212)

**(1) Source rows.** #211 "CI Shard Design | P1 | Split large suites into stable shards with run IDs, isolated resources,
and useful artifacts." and #212 "Parallel Test Isolation | P1 | Prevent parallel tests from sharing users, tenants,
records, ports, browser state, or queues unsafely." (`06-qa-test-engineering.md:57-58`). D10: "ONE skill … Extends
`qa-automation-architect`'s blueprint into enforceable rules" (`step-0-reconciliation-v4.md:261`).

**(2) Overlap verdict: COVERED.**

| Roadmap clause | Shipped owner and evidence |
| --- | --- |
| Stable shards | `sharded-validation-with-resume` (shipped **after** D10): "NAMED functional shards … Every existing test/check lands in EXACTLY one shard; balance by measured duration" plus an `uncategorized` catch-shard (`SKILL.md:65-74`); balancing rules (`references/shard-runner-design.md:92-100`) |
| Run IDs | "one persisted record per shard per run-id" (`SKILL.md:75-80`); runner-level `--shard=i/n` "upload `playwright-report/` + traces with the run id" (`playwright-e2e-engineer/references/playwright-patterns.md:68-69`) |
| Useful artifacts | `qa-automation-architect` step 5 "Define reporting & artifacts" (`SKILL.md:83-85`); "JUnit/JSON report per suite + failure traces/screenshots uploaded with run id" (`automation-blueprint.md:59-60`) |
| Sharding plan in CI | `qa-automation-architect` step 6 "sharding plan" (`SKILL.md:86-88`); pinned routes: `ci-pipeline-architect` trigger-evals "Decide which test suites run on PR versus nightly, the sharding, and the retry policy" → `qa-automation-architect` (`ci-pipeline-architect/evals/trigger-evals.json:25`); `regression-suite-curator` trigger-evals "Design the CI tiers, sharding, and retry mechanics" → `qa-automation-architect` (`regression-suite-curator/evals/trigger-evals.json:15`); "Design shards and a resume mechanism" → `sharded-validation-with-resume` (`ci-failure-classifier/evals/trigger-evals.json:81`) |
| Users, tenants, records not shared | `test-data-architect` step 4 "worker-scoped namespacing (prefix/tenant per worker), no test mutates catalog baseline rows" (`SKILL.md:77-80`); checklist "Parallel isolation is structural (namespacing), not conventional" (:118); run + worker + test ID markers (`references/test-data-patterns.md:37-41`); pinned `test-data-design-wins-here` "Our tests share one seeded workspace and collide in parallel" (`test-data-architect/evals/trigger-evals.json:14`) |
| Ports and state | `qa-automation-architect` step 4 "no shared mutable state, port/resource allocation, DB strategy per layer" (`SKILL.md:79-82`); checklist "Isolation rules make parallel runs collision-free (data, ports, state)" (:123); pinned eval `edge-slow-tangled-suite` "can't run in parallel because tests share seed users" (`qa-automation-architect/evals/evals.json:21-31`) |
| Browser state | "Share one login/storage state per persona only when that account's use is parallel-safe. Stateful parallel tests need per-worker or per-test accounts and sessions" (`playwright-patterns.md:51-53`); gotcha "Shared login state across parallel workers causes heisenbugs" (`qa-automation-architect/SKILL.md:139-141`) |
| Queues | Covered only generically ("resource rules", `qa-automation-architect/SKILL.md:107`); integration lists "internal queue/jobs … REAL or in-process driver" (`boundary-catalog.md:16`). **This is the only thin spot.** |
| Diagnosing collisions | `flaky-test-detective` taxonomy "Shared state — data | fails only in parallel" and "port collisions" (`references/flake-taxonomy.md:20,25`, manual-only) |

- **Why I disagree with D10.** D10 predates `sharded-validation-with-resume`. Its "enforceable rules" residual is
  answered by `test-data-architect`'s structural-namespacing rule and `test-tenant-provisioner`'s
  "never-mutate-unmarked rule … prod-safe static lint of QA automation" (D68 broadening, `step-0-reconciliation-v4.md:247`).
- A new skill would fire on the pinned core cases of `qa-automation-architect`, `test-data-architect` and
  `sharded-validation-with-resume` listed above, which is a check 2 FAIL.
- **Residual (optional):** name queues, caches, email/SMS sandboxes, feature flags and the clock in
  `qa-automation-architect`'s isolation resource list (0.25–0.5 h).

**(3) Posture:** not applicable. **(4) Estimate:** 0–0.25 h (covered-table row), or 0.25–0.5 h with the optional list.
**(5) Value:** a new skill would add no capability. **(6) Trigger boundary:** none new.

---

## Hand-off rows from the G2/G6 helper: #213, #202, #189 (verified independently)

The coordinator routed these untiered cat-06 rows to G1 (`$S/skillbatch/research-G2G6.md:299-317,320,383`; read as
data). I re-ran each check on the base tree. My own results:

- **Untiered status.** "Category-06 items neither tiered nor mapped above (#188, #189, …, #202, #213, …)"
  (`step-0-reconciliation-v4.md:274-275`). **Confirmed.**
- **Helper's counts.** `grep -ci timeout` and `grep -ci snapshot` on `qa-automation-architect/SKILL.md` and
  `references/automation-blueprint.md` → `0 0` and `0 0`. **Confirmed.**
- **Documentation inconsistency.** The catalog maps #189 to `playwright-e2e-engineer` ("cat 06 #187/#189",
  `docs/skills-catalog.md:523`), but the v4 "partially absorbed via shipped catalog source mappings" list names only
  #191, #199 and #217 (`step-0-reconciliation-v4.md:276-278`). The list says "Several", so it is **incomplete, not
  contradictory**. **Confirmed.**
- **Further finding (mine):** the #189 mapping also overstates coverage. `playwright-e2e-engineer` explicitly rejects
  breadth: "Reject UI-tree crawling — route breadth to `clickthrough-test-engineer` or component layers"
  (`SKILL.md:61-63`). It treats missing test-only routes as "a separate classified change" (`SKILL.md:157-158`). Its
  SKILL.md and patterns have 0 matches for `page.route|mock|intercept|fixture mode`.

### #213 Test Timeout Policy (P1)

Source: "Set timeouts that distinguish slow failure, infra instability, hidden hangs, and real product problems."
(`06-qa-test-engineering.md:59`).

- **Distinguishing after the fact is owned.** `ci-failure-classifier` has a timeout-only class with "timeouts never
  conflated with regressions" (description), "A timeout with failed assertions before it is classified by those
  assertions" (`SKILL.md:107-108`), "may be a product hang" (:216-218), and refuses "to raise a timeout" (:246).
  `flaky-test-detective` holds the rule "widen timeout silently | masks slow regressions | … widen WITH a named reason"
  (`references/flake-taxonomy.md:57`, manual-only). `code-reviewer` flags "timeouts or retry counts raised"
  (`references/severity-rubric.md:65`).
- **Setting timeouts per layer is not owned.** Word-boundary counts for `timeouts?|hangs?|hung`:
  `qa-automation-architect` 0, `test-plan-designer` 0, `vitest-unit-component-engineer` 0, `regression-suite-curator` 0.
  `ci-pipeline-architect` names a per-stage "timeout" field only (`SKILL.md:83,145`, manual-only).
  `playwright-e2e-engineer` has one gotcha, "keep default timeouts honest" (`SKILL.md:144-145`). The design question is
  per-test, per-assertion and per-job ceilings derived from measured durations with headroom. It sits next to
  `qa-automation-architect`'s own retry policy (step 6, `SKILL.md:86-92`) and is unowned.
- **Verdict: PARTIAL (minor).** Disposition: **extension of `qa-automation-architect`, not a new skill**, and not
  folded into `ci-shard-parallel-isolation` (dropped above). The new content is a bounded policy slice that fits the
  base's Purpose and Output Format line "CI placement: … retry policy" (`SKILL.md:109-110`), which meets the
  checklist's extension rule (`quality-review-checklist.md:101-103`).

### #202 Snapshot Test Governance (P2)

Source: "Use snapshots only for stable, meaningful outputs with explicit update review." (`06-qa-test-engineering.md:48`).

- **The update-review half is owned.**
  - `change-classification-gate`: "Test-only changes can still change effective behavior (snapshot regeneration …)"
    (`SKILL.md:118-119`); "snapshot test update | qa-test-only OR a masked regression | Confirm the behavior change was
    intended before updating snapshots" (`references/classification-matrix.md:46`).
  - `code-reviewer`: "snapshots regenerated without a reason" (`references/severity-rubric.md:65`).
- **The selection half is owned only negatively.** `vitest-unit-component-engineer`: "No snapshot-everything"
  (`SKILL.md:70`, manual-only). `test-coverage-mapper`: "Snapshot-everything tests nobody reviews on update" is theater
  (`references/coverage-mapping-method.md:32`). The positive rule ("when does an output earn a snapshot") has no owner.
- **Verdict: PARTIAL (minor).** Disposition: **absorb into candidate 1**, scoped as "baseline-comparison tests: screenshot
  baselines and serialized snapshots". The selection rule (stable, meaningful outputs only) and the reviewed-update rule
  are the same policy that candidate 1 already defines for screenshot baselines. Cost: +0.25–0.5 h on candidate 1.
- **Fallback if the owner wants candidate 1 kept to screenshots:** record #202 as covered by the four skills above.
- **Collision note:** `vitest-unit-component-engineer` is manual-only and implements the tests, so the design-versus-
  implementation seam matches the existing `playwright-e2e-engineer` seam.

### #189 Fixture Mode E2E Design (P1)

Source: "Use local or test-only routes and deterministic fixtures for broad UI regression coverage."
(`06-qa-test-engineering.md:35`).

- **Breadth is deliberately routed away from E2E.** `playwright-e2e-engineer` routes it to `clickthrough-test-engineer`
  or component layers (`SKILL.md:61-63`). The component layer owns UI in isolation with network fixtures: "mock the
  repo's OWN api-client module, or use an interceptor … at the fetch boundary; add a setup guard that fails on
  unexpected real fetch" (`vitest-unit-component-engineer/references/vitest-patterns.md:30-32`).
- **Deterministic data is owned.** `test-data-architect` description: "per-layer data sources (… API-created fixtures
  for E2E)".
- **Test-only routes are a product change.** `playwright-e2e-engineer/SKILL.md:157-158` treats them as a separate
  classified change.
- **The one unowned slice** is rendering UI states deterministically (fixture mode) so they can be compared broadly.
  That is exactly the capture-determinism part of candidate 1.
- **Verdict: COVERED by split, with one slice absorbed into candidate 1** (its state-rendering step names fixture mode,
  test-only routes and component states as options). Recording cost is in the drops row.
- **Documentation fix to carry in the build's decision row** as a dated note, never a rewrite: add #189 to the v4
  "partially absorbed" list, and note that the catalog :523 mapping covers journey-level fixtures only, with breadth
  owned by the component layer and candidate 1.
- **Relation to `mock-strategy-designer`:** #189's network mocking is covered by the same evidence as #200
  (candidate 5). It does not revive that candidate.

### Effect on the recommendation

- Candidate 1 grows to **3.25–5 h** (#202 + #189 slice).
- A new recommended item, **E1 = `qa-automation-architect` extension (#213 timeout policy)**, adds **1–2 h**. The basis
  is extension precedents of 0.75–1.5 (`qa-tier1-skill-batch-proposal.md:60`) and 1–2 (`ai-sdlc-skill-batch-proposal.md`
  table). The range includes the two optional residuals from candidates 5 and 6 (a test-double selection row; queues,
  caches and sandboxes in the isolation list). Together these make the catalog's "cat 06 #200/#211/#212" citation for
  that skill (`docs/skills-catalog.md:522`) match its body.
- Only one lane should plan E1. The G2/G6 helper says the same: "Two helpers proposing edits to
  `qa-automation-architect` would collide" (`research-G2G6.md:312-313`).

---

## Estimate basis (applies to every row above)

- **No active-time measurement exists for any skill build.** The D68 builds (#498–#502) fall in the window the forecast's
  #554 checkpoint covers (#492–#554). That checkpoint says its interval "is not an active-work measurement"
  (`docs/roadmaps/aegis-backlog-forecast.md:139`). The earlier window states "No active, review, CI or waiting split
  was measured" (`docs/roadmaps/aegis-execution-metrics.md:15`). All per-skill figures are the precedent proposals'
  **agent estimates**:
  - D68: new skills 2–3.5 / 2.5–4 / 3–5; extension 0.75–1.5; drop 0–0.25; overhead 1.5–3
    (`qa-tier1-skill-batch-proposal.md:57-65`).
  - D69: 2.5–4; extensions 0.75–2; overhead 1–2.
  - D70: 3–5; overhead 1.5–2.5.
  - D71: 3–5 / 3–4.5 / 2.5–4 / 3–5; overhead 2–3.5 (each proposal's "Decision in one read" table).
- **Observed wall time only, open-to-merge, D68 build PRs** (`gh api repos/ModernNomad-98/Project-Aegis/pulls/<n>`):
  - #499 `acceptance-criteria-reviewer`: 18:51:11Z → 22:07:13Z = 3h16m02s
  - #500 `test-tenant-provisioner`: 3h45m55s
  - #502 `ci-failure-classifier`: 19:02:58Z → 23:15:34Z = 4h12m36s
  - #498 `test-plan-designer` extension: 3h54m17s

  These ran in parallel and include review, CI and queue time, so they are **not** active time and do not score the
  estimates. Authoring time before each PR opened is not derivable.
- Overhead 2–3.5 follows D71 (4 new skills + 1 extension). It covers 4 registrations (catalog rows, README counts,
  both eval files each), the decision row, about 8 neighbor body or description reciprocity edits, optional Stage 7
  "by evidence" wiring in `project-orchestrator` (`SKILL.md:259-263`), and the review path.

## Recommendation — G1 sub-batch

Ranking method: `prioritization-frame-picker`, a coarse value-versus-effort cut.

- **Value input (evidence):** coverage-gap size from the verdicts above. Roadmap P1/P2 labels are a secondary input.
- **Demand input:** none was found, so it carries **zero weight**.
- **Effort input (guess):** precedent ranges.

| Rank | Candidate | Gap (evidence) | Effort | Note |
| ---: | --- | --- | --- | --- |
| 1 | `visual-regression-test-designer` | whole class unowned; the existing pointer lands on a skill with no content | M (3.25–5) | Tier-2 promoted; absorbs cat 05 #179, #202 selection, #189 fixture-mode slice |
| 2 | `exploratory-charter-designer` | whole class unowned; `qa-strategy-architect` names the risk | S–M (2–3.5) | cheapest |
| 3= | `mobile-journey-test-designer` | verification half of #230 unowned | M (2.5–4) | strongest collider (`mobile-viewport-craft`) |
| 3= | `role-coverage-test-designer` | allowed side and UI consistency unowned; denials owned | M (2.5–4) | narrowest gap; three-way collision |
| E1 | `qa-automation-architect` extension (#213) | per-layer timeout setting unowned; classification owned | S (1–2) | P1 row; also fixes the skill's catalog #200/#211/#212 citation mismatch |
| — | `mock-strategy-designer`, `ci-shard-parallel-isolation`, #189 remainder | covered | ~0 | drop; record as covered |

Sensitivity check: all four builds sit within 2–4.5 h. Doubling any one effort does not move a build below the drops,
and does not reorder ranks 1–2 against 3. Ranks 3= are a judgment tie; I break it toward mobile because #230's gap is
**explicitly acknowledged in shipped text** ("Deep responsive QA is its own effort", `clickthrough-route-catalog.md:31`),
while #229's gap is inferred from absence.

**Recommended sub-batch (4 builds + 1 extension + 2 drops + 1 record, 13.25–22.5 provisional active hours):**
1. Build `visual-regression-test-designer`, `exploratory-charter-designer`, `mobile-journey-test-designer` and
   `role-coverage-test-designer` (narrowed). All four are auto-invocable designers in the Phase 5 "UI/manual" or
   "strategy/plan/coverage" clusters (`docs/skills-catalog.md:539-549`).
2. Drop `mock-strategy-designer` (#200/#201) and `ci-shard-parallel-isolation` (#211/#212). Record them in the D10
   "Already covered" table (`step-0-reconciliation-v4.md:219-237` style) with the owners named above. A dated decision
   row corrects the D10 notes forward; the dated text is not rewritten. The next decision number would be **D74**
   (D73 is the highest at `step-0-reconciliation-v4.md:3735`; recheck at build time).
3. Extend `qa-automation-architect` (E1) with a per-layer timeout policy for #213, and optionally the test-double
   selection row and the wider isolation resource list. Plan it in the G1 lane only.
4. Record #189 as covered by split, with the fixture-mode slice moved into candidate 1. Add #189 to the v4 "partially
   absorbed" list by a dated note. #202 is absorbed into candidate 1, with "record as covered" as the fallback.

The library would go from 195 to 199 skills.

**Smaller alternative (3 builds + E1, about 10.25–18 h):** defer `role-coverage-test-designer`. Recompute: 3.25–5 +
2–3.5 + 2.5–4 + 1–2 (E1) + 0–0.5 (records) + overhead 1.5–3 (D68-like: 3 new + 1 extension) = 10.25–18. Choose this if the owner prefers to wait for G4's
role/membership verdicts before adding a fourth neighbor to that cluster.

**Minimum alternative (2 builds + E1, about 7.75–13.5 h):** visual + exploratory only (the two whole-class gaps) plus
E1. Recompute: 3.25–5 + 2–3.5 + 1–2 + 0–0.5 + 1.5–2.5 = 7.75–13.5. Dropping E1 as well gives 6.75–11.5.

**Suggested PR seams** (each reviewable on its own, following D68):
1. `visual-regression-test-designer` + the `screenshot-evidence-planner` pointer change + the `qa-automation-architect`
   blueprint row + the `qa-strategy-architect` line.
2. `mobile-journey-test-designer` + the `clickthrough-test-engineer` route-catalog pointer + the `mobile-viewport-craft`
   trigger-eval case.
3. `exploratory-charter-designer` + the `qa-strategy-architect` / `clickthrough-test-engineer` body pointers.
4. `role-coverage-test-designer` + the `authorization-matrix-designer` reciprocity + the covered-table rows and decision
   row.
5. E1 `qa-automation-architect` extension (could ride with seam 1, since both touch the blueprint reference).

**Owner questions this implies** (for the plan author; not asked here):
- the build set (4, 3 or 2);
- the three renames;
- the posture (all auto-invocable, design only);
- E1 (#213 timeout policy) and whether it also carries the two optional residuals;
- absorbing #202 into candidate 1, or recording it as covered.

### Self-scrutiny

- **Strongest counter-argument.** The two COVERED verdicts overturn D10, which saw most of the same content and still
  called #200/#201 and #211/#212 gaps. A single "test-double policy" or "parallel-isolation rules" page might be easier
  for a builder to find than evidence spread across five skills. A user who asks "what's our mocking strategy?" might
  get a fragmented answer from `qa-strategy-architect` step 4.
  - **Answer:** the checklist judges collision by request routing, not by discoverability. The pinned evals show today's
    routing already lands each request on a named owner. The optional reference rows address findability at about 1 h,
    without a new trigger.
- **Second counter-argument.** `role-coverage-test-designer` may be too thin once denials are delegated. Allowed-path
  tests could instead be one line added to `authorization-matrix-designer` step 7 ("…and a positive test per allow").
  That is the cheaper extension shape, and it is a defensible alternative I did not choose. I rejected it on the
  "disjoint trigger / different artifact" rule, which is a judgment, not a measurement.
- **Third counter-argument (E1 and the absorptions).** Stacking the #213, #200 and #212 residuals onto
  `qa-automation-architect` risks scope creep in a hub skill. Folding #202 and part of #189 into candidate 1 widens its
  trigger toward `vitest-unit-component-engineer`'s territory.
  - **Answer:** E1 adds policy rows next to the skill's existing retry policy, not a new job (check 6). Candidate 1
    keeps one job, "baseline-comparison test design". Both remain judgments; if the build-time
    `skill-quality-reviewer` check 6 or check 2 objects, #202 falls back to "record as covered" and E1 shrinks to
    #213 alone (0.75–1.5 h).
- **Least certain claims.**
  1. All estimates. No active-time actuals exist for any skill build, so the figures are precedent agent estimates
     with **low confidence**.
  2. Value to SaaS builders. **No demand evidence exists**; the ranking rests on gap size and roadmap labels only.
  3. The mobile-versus-role tie-break.
  4. That draft descriptions of 912–974 characters can keep their yield clauses after review edits. They were measured
     at those lengths, but the evals are untested.
  5. Cross-group overlaps with G4 and G6 are **unverified** here, except the three hand-off rows, which I re-verified.
  6. The "setting timeouts is unowned" claim rests on word-boundary greps across 12 QA/CI skills; a synonym (for
     example "ceiling" or "budget") could hide partial coverage. `sharded-validation-with-resume` has per-shard
     "ceiling" text, which is job-level only.
- **What would change the recommendation.**
  - A shipped skill body I missed that designs visual baselines, exploratory charters or mobile journey verification
    would turn that candidate into a drop or extension. My sweeps were keyword-based (commands above), so a synonym
    could hide one.
  - If G4's helper recommends building `role-permission-architect`, or G6's helper recommends `e2e-test-architect`,
    with role-journey scope, then `role-coverage-test-designer` should merge into or defer behind that skill.
  - Owner-reported demand, such as mobile bugs or UI drift in a consumer product, would raise the corresponding rank.
  - Measured active time from D69–D71 builds (the MECH helper's lane) would replace the precedent ranges.
- **Not inspected:**
  - the full bodies of `accessibility-test-harness`, `edge-state-ux-designer`, `plan-entitlement-architect`,
    `admin-console-architect` and `e2e`-related G6 rows;
  - `scripts/audit-skill-contracts.py` output (the ROUTE-002 effects of the drafts are predicted, not measured);
  - the D69–D71 build PR timings;
  - CONTRIBUTING.md's "How to add a skill" step count (the overhead uses precedent ranges).

---

## Appendix A — draft descriptions (measured with `yaml.safe_load`; drafts only, not reviewed)

File: `$S/skillbatch/g1-scripts/drafts.yaml`. Lengths: visual 973, mobile 959, exploratory 912, role 974. Each starts
with "Design …", so the capability sits in the first ~90 characters (`docs/skill-generation-standard.md:162-166`).

## Appendix B — commands behind the key claims (quoted output abbreviated)

- `git ls-remote origin refs/heads/main` → `52289779… refs/heads/main`
- `python3 -B scripts/validate-skills.py` (base copy) → `OK: 195 skill(s) valid, 0 warning(s)`
- Frontmatter parse (`g1-scripts/desc.py`) → `196 30` (entries, manual-only)
- Visual sweep (Candidate 1 grep) → only `screenshot-evidence-planner/SKILL.md:33` is relevant
- `grep -ciE 'mobile|device|viewport|touch' playwright-e2e-engineer/SKILL.md` → `0`
- `grep -ciE 'exploratory|charter' test-plan-designer/SKILL.md references/test-plan-template.md` → `0`, `0`
- Eval prompt scan (Python over `*/evals/*.json` for G1 keywords) → the pinned cases cited in candidates 5 and 6
- `git show f00948df:<file> | grep -cF '<string>'` → 1 for each of the nine strings listed under "Shared evidence"
- TF-IDF similarity script (inline, parentheticals stripped) → the neighbor scores quoted per candidate
- Issues/PR scan (680 rows) → G1 keywords only in PR #17 (+ #183, unrelated)

---

**Finish:** 2026-10-08T17:32:46Z (`date -u`). Start 2026-10-08T17:11:40Z. Measured wall time is in the report. Active time was not measured separately.
