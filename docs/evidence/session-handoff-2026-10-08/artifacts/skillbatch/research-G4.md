# Research G4: Phase 3 expansion, planning helper report (Stage A support only)

Helper: P34 research helper (G4 only). Writes no repository files, makes no commits and no GitHub writes.
Started 2026-10-08T17:11:40Z (`date -u`). The finish time is in the report handed back to the caller.

**Aegis skills used (dogfood rule).** `skill-quality-reviewer` (auto-invocable). I applied its check 2
(trigger collision, SKILL.md:79), check 3 (duplication or extension, :85), check 6 (scope, :101) and
check 7 (invocation posture, :103) to each candidate's *scope*. The fit is partial: the skill is written
for a drafted skill, and none of these four is drafted yet. I also used the library's own
standalone-versus-extension test from D31/D32, which calls a candidate a near-duplicate when it is less
than about 40% distinct (reconciliation log :1350, :1397). I read `prioritization-frame-picker`
but did not apply it: with no demand data, a scoring frame would be false rigor, and the
DEMAND helper owns demand. I used no MANUAL-ONLY skill.

**Base state, re-observed this turn.**
- `git ls-remote origin refs/heads/main` returned `5228977920ee479e1fe1ec6b8d56f8fc24c14947`, both at start
  and at 17:25:34Z.
- The local checkout is detached at `c060a7cb`, which is NOT the base. I therefore exported `git archive 52289779`
  to `$S/skillbatch/g4-tree`. `diff -rq` against the earlier helper's `p34-tree` returned no differences.
- `python3 -B scripts/validate-skills.py` on that tree reported `OK: 195 skill(s) valid, 0 warning(s)`.
  `.claude/skills/` has 196 entries; the extra entry is `_template`.
- Exact names: an `ls .claude/skills | grep` for tenant, provision, member, invit, role, permission,
  impact and note returned none of the four candidate names.
- I extracted all descriptions with `yaml.safe_load` (script `$S/skillbatch/g4-scripts/desc.py`; output
  `$S/skillbatch/g4-desc-all.txt`). Every length below comes from that output.

Paths below are relative to the base tree. "cat-02" means `docs/skills/02-saas-platform-architecture.md`, "cat-03" means
`docs/skills/03-saas-security-rls.md`, and "recon" means `docs/reconciliation/step-0-reconciliation-v4.md`.

---

## 0. Duplication flag: `security-impact-note-author` is listed twice

**Facts.**
- The candidate appears in the Phase 3 expansion list: catalog :1311-1314 and recon :135-137. That list
  comes from the historical execution plan's Phase 3 list:
  `docs/prompts/senior-principal-claude-skills-execution-plan.md:402`, item 14, and :741.
- The same capability appears again among the Phase 4 expansion topics: catalog :1322-1325, which ends
  "...security-drift detection, security-impact-note authoring". There it is cat-03 row #127,
  "Security Impact Note Authoring | P0" (cat-03:69).
- Both forecast rows include it:
  - `aegis-backlog-forecast.md:729` "Phase 3 expansion (four skills) | 8–16".
  - `:730` "Phase 4 expansion (about ten security topics) | 20–40". The catalog's list at :1322-1325
    has 10 topics, counted with `sed -n 1322,1325p | tr , "\n" | nl`, and #127 is the tenth.

**Consequence.** The 68–140 total for the unselected expansion counts this one capability twice. The
forecast does not give hours per skill. Its group averages are 8–16/4 and 20–40/10, so the double count
is about **2–4 agent-hours**. That figure is derived from the averages; no forecast line states it.

**My view.** Evaluate #127 **once, under G5**:
- Its source row is cat-03, the security category.
- Every close neighbor is a security or approval skill (§4 below).
- It appears in the Phase 3 list only because the execution plan's Phase 3 mixed SaaS and security
  skills (execution plan :383-402 lists `threat-modeler` and `appsec-implementer` there too).
- Treat G4 as **three** candidates. §4 records my overlap analysis so that the SEC helper or the
  coordinator can reconcile one verdict.

---

## 1. `tenant-provisioning-designer`

**(1) Source and priority.**
- cat-02:26, row #57 "Tenant Provisioning Workflow | **P0** | Design tenant creation, initial admin
  setup, defaults, seed data, and post-provision verification."
- Execution plan :390 and :729. Moved to the Phase 3 expansion by recon :135-137 and catalog :1311-1314.

**(2) Overlap verdict: PARTIAL, with a large gap.** What the shipped skills already cover:
- `tenant-modeler` (description 974 chars) covers "the full tenant lifecycle from provisioning
  through suspension to offboarding and purge". Its body gives *semantics only*:
  - The lifecycle state machine, where each state declares access, data, billing and jobs posture
    (SKILL.md:91-97).
  - The provisioning row "None (or admin-only setup) | Seeding | Not started / trial clock pending |
    Setup jobs only" (`references/tenant-lifecycle-catalog.md:9`).
  - The checklist line "No tables designed, no policies written — semantics only" (:139).
- `saas-platform-architect` (815) covers the platform level only:
  - "Define platform-level tenant flows: onboard (provision → verify → activate) ... delegating
    detailed lifecycle semantics to `tenant-modeler`" (SKILL.md:81-83).
  - Every siloed component "names its provisioning and upgrade story" (:72-73).
  - A capability-inventory line "Tenant management: provision, suspend, offboard, purge" that is
    marked present, partial or missing (`references/platform-deployment-models.md:22`).
  - "No implementation performed" (:137).
- `cell-based-architecture-designer` (932) covers the placement policy for new tenants (SKILL.md:103-105).
- `background-job-orchestration-architect` (871) covers the generic job execution model: idempotency,
  resumability, retry and a dead-letter queue.
- `audit-log-architect` covers the "Tenant lifecycle | Provision ..." audit event
  (`references/audit-event-taxonomy.md:17`).
- `plan-entitlement-architect` covers the "Trial start | Signup" plan transition
  (`references/entitlement-matrix-template.md:45`).
- `test-tenant-provisioner` (manual-only, `disable-model-invocation: true` at SKILL.md:4) covers *test*
  tenants in a NON-PRODUCTION environment only (description; catalog :536).

**The gap.** No shipped skill designs the provisioning *workflow* itself:
- the ordered steps across systems;
- an idempotency key per request;
- compensate-or-resume after a partial failure;
- the first owner or initial admin;
- defaults versus seed data;
- post-provision verification;
- abuse controls on self-serve signup.

Searches backing this:
- A grep of `.claude/skills` for `provision` found only the lines above, plus unrelated
  "provisional" hits.
- A grep for `first admin|initial admin|first owner|seed data|default settings` found nothing
  relevant.
- `default|seed` in `saas-platform-architect` and `tenant-modeler` matched only "do not pick a default silently".

**Distinctness.** By judgment, using the D32 method, about 70–80% of the surface is distinct (not
measured). That is well above the ~40% duplicate threshold.

**Extension rejected.**
- `tenant-modeler` declares itself semantics only (:139) and has 50 characters of description room
  (974 of 1024).
- `saas-platform-architect` is a structure skill. Adding a multi-system workflow would make it a
  second job, which fails check 6.

**(3) Invocation posture: model-invocable.**
- It designs and creates nothing. Standard §5 at `docs/skill-generation-standard.md:270-275` reads "Default to read-only".
  Only write, network, deploy or spend behavior needs `disable-model-invocation: true`.
- Its peers are all model-invocable: catalog :413 says "None has side effects, so all are
  model-invocable", and D64's posture is "Design only ... → model-invocable" (recon :3291-3293).
- Its Stop Conditions must refuse to create real tenants or run provisioning scripts. A request for
  test tenants goes to `test-tenant-provisioner`, which is manual-only, so the user must name it.

**(4) Estimate: 3–4.5 active hours, provisional, low confidence.** Basis:
- Precedent estimates for design-only single-skill builds: 2.5–4 for `ai-task-decomposer`
  (ai-sdlc :66), `ci-failure-classifier` (qa-tier1 :62) and `environment-parity-reviewer`
  (phase6 :78). 3–4.5 for `resilience-architecture-reviewer` (phase6 :76). 3–5 for
  `ai-human-in-the-loop-designer` (phase7 :68).
- I put this one in the upper band because it needs a reference file: the step catalog and the
  compensation patterns.
- No measured active time exists for any precedent. The metrics page records "active time not
  measured" for skill PR #383 (`aegis-execution-metrics.md:377`), and the checkpoint text says "No
  active, review, CI or waiting split was measured" (:15).
- Wall time from the first authored commit to merge, for six D68–D71 skill PRs, is context only. I
  took the author date of the first branch commit and the merge commit from `git log` and computed the
  span in Python:

  | PR | Wall time |
  | --- | --- |
  | #502 | 4h16m02s |
  | #517 | 2h37m15s |
  | #521 | 16h17m23s |
  | #522 | 3h43m32s |
  | #523 | 2h37m12s |
  | #526 | 3h18m09s |

  These spans include review, CI and waiting, and exclude authoring before the first commit, so they
  cannot calibrate active hours.

**(5) Value and dependencies.**
- The row is P0.
- `project-orchestrator` Stage 3 sends a SaaS or multi-customer product through
  `saas-platform-architect`, then `tenant-modeler` → `multi-tenant-data-architect`, then
  `authorization-matrix-designer` (project-orchestrator SKILL.md:239-240). No skill on that route
  designs how a tenant is created.
- Actual user demand is **unverified**; the DEMAND helper owns it.
- It depends only on shipped skills, which it consumes: `tenant-modeler`, `saas-platform-architect`,
  `plan-entitlement-architect`, `audit-log-architect`, `cell-based-architecture-designer` and
  `background-job-orchestration-architect`.
- Cross-group seam: G3's candidate `idempotency-first-designer`, if built, would be composed rather
  than re-derived.

**(6) Trigger boundary.**
- **Use when:** designing what happens between "sign up" or "sales closes a deal" and a working
  tenant; fixing tenants left half-created; adding operator-led enterprise provisioning.
- **Not when:**
  - what a tenant *is*, or its lifecycle states → `tenant-modeler`;
  - pooled versus siloed structure → `saas-platform-architect`;
  - test accounts → `test-tenant-provisioner`;
  - running the jobs → `background-job-orchestration-architect`.
- **Trigger evals pin against:** `tenant-modeler`, `saas-platform-architect`, `test-tenant-provisioner`
  (a manual-only neighbor, so positive prompts must name it) and `background-job-orchestration-architect`.
- No existing trigger eval contests a provisioning prompt. The `tenant-modeler` and
  `saas-platform-architect` trigger-eval prompts are about semantics and pooled versus siloed; a grep of
  their evals for `invit|provision` found only a "provisioning story" assertion in
  saas-platform-architect `evals.json:14`, :43.

---

## 2. `membership-invitation-designer`

**(1) Source and priority.**
- cat-02:27, row #58 "Membership and Invitation Design | **P0** | Handle invites, acceptance,
  expiration, revocation, role assignment, and auditability."
- Execution plan :391 and :730. Recon :136; catalog :1312.

**(2) Overlap verdict: PARTIAL.** The semantics are covered; the flow mechanics and their security are not.

Covered:
- `tenant-modeler`'s description names "user-to-tenant membership (roles attached to membership,
  invitations, users in multiple tenants)" and "a membership + invitation model". Its body models:
  - invitations as their own lifecycle, "including re-invite, domain-capture, and who may invite" (:86-87);
  - ownership and the last-owner guard (:88-90);
  - the state machine draft → sent → accepted, expired or revoked, where revocation wins over a
    concurrent accept;
  - "Invitations carry the role they grant";
  - "Who may invite is a permission ... invite volume is a plan limit candidate" (catalog reference :37-51).
- `authorization-matrix-designer` has `invite:member` in its template (`references/...-template.md:24`) and a
  "Revocation" negative test (:50-51).
- `audit-log-architect` has "invitation sent/accepted/revoked, ownership transfer" events (taxonomy :12).
- `authority-invalidation-architect` diagnoses access changes that did not take effect, including an
  invited member's stale claims (SKILL.md:304-308).
- `share-link-access-architect` designs bearer tokens with entropy, expiry, revocation and
  enumeration defense, but **explicitly for non-members**: "ephemeral guest sessions (not
  memberships)" (description) and "Do NOT use when ... MEMBER roles" (SKILL.md:39-47).

Not covered, by grep of `.claude/skills` for `invit`, `scim|domain capture|deprovision` and
`higher role|own role|role ceiling`:
- the invite token as a single-use, hashed, expiring credential that mints a *membership*;
- binding acceptance to the invited identity (email mismatch, unverified email, tenants that enforce
  single sign-on);
- the new-account versus existing-account accept path;
- idempotent acceptance;
- seat or plan-limit checks at acceptance (`plan-entitlement-architect` never says "seat": `grep -c` returns 0);
- spam and enumeration limits on invites, and responses that do not reveal whether an account exists;
- retention of invitee email addresses;
- a role-grant ceiling, so no inviter can grant a role above their own (no skill states this rule;
  `multi-tenant-security-tester` tests only "role self-upgrade", SKILL.md:89).

**Distinctness.** By judgment, about 60–65% distinct from `tenant-modeler` (not measured). Roughly 6
shared elements (states, expiry, revoke race, role carried, who may invite, audit events) against about
10 distinct ones. That is above the ~40% threshold.

**Extension into `tenant-modeler` rejected.** It is "semantics only" (:139), its Stop Conditions hand off
implementation (:174-175), and its description has 50 characters of room.

**Extension into `share-link-access-architect` rejected.** D32 resolved that skill STANDALONE precisely
on the line between a capability (a link) and member access control (recon :1399-1408). Merging
membership invitations into it would blur that line.

The role-grant ceiling belongs in `authorization-matrix-designer`; see §3. This candidate consumes it.

**(3) Invocation posture: model-invocable.** It designs only and sends no email; the same basis as §1(3).

**(4) Estimate: 2.5–4 active hours, provisional, low confidence.** Same precedent basis as §1(4). Plus one
reference file: a token and acceptance checklist with a negative-test catalog.

**(5) Value and dependencies.**
- The row is P0.
- Invitations are the library's own canonical worked example of a SaaS feature, in five shipped
  skills:
  - `ai-task-decomposer/assets/task-plan-template.md:79-105`;
  - `test-plan-designer/references/test-plan-template.md:29`;
  - `manual-test-case-creator/references/manual-case-template.md:47-54`;
  - `acceptance-criteria-reviewer/references/criteria-review-sheet.md:69-79`;
  - `integration-test-designer/references/boundary-catalog.md:39`.

  That shows the feature recurs in the library's material. It is **not** evidence of user demand,
  which is unverified.
- It depends on `tenant-modeler` (semantics) and is best built after the §3 extension (the grant
  ceiling).
- Cross-group seams with G5's topics: authentication and session review (accept when single sign-on
  is enforced) and rate-limit design (invite spam).

**(6) Trigger boundary.**
- **Use when:** designing team invitations or joining by domain; fixing invites that never expire,
  can be replayed, or grant too much.
- **Not when:**
  - what membership means → `tenant-modeler`;
  - the role matrix → `authorization-matrix-designer`;
  - anyone-with-the-link access → `share-link-access-architect`;
  - access that survives a removal → `authority-invalidation-architect`.
- **Trigger evals pin against:** `tenant-modeler` (highest collision risk, because its description says
  "invitations"), `share-link-access-architect` and `authorization-matrix-designer`.

---

## 3. `role-permission-architect`

**(1) Source and priority.**
- cat-02:28, row #59 "Role and Permission Architecture | **P0** | Design roles, permissions,
  assignment tables, inheritance rules, and least-privilege checks."
- Execution plan :392 and :731. Recon :136; catalog :1313.

**(2) Overlap verdict: COVERED by the catalog's own attribution, with a small residual gap.**
- Catalog :425 is the `authorization-matrix-designer` row, and its source column says "**cat 02 #59**".
  The shipped skill already stands for this row.
- The cat-03 sibling row #106 "Authorization Matrix Design" (cat-03:48) carries the same name.
- Its description (493 chars) reads: "Design authorization ... as an explicit roles × permissions × resources
  matrix ... deny-by-default ... Use when roles or permissions need design or repair." That is the
  candidate's exact trigger. A new skill would collide on its core case, which is a check 2 FAIL
  (SKILL.md:79-84).
- Residual gap, from a body grep for `inherit|hierarch|custom role|assignment|ReBAC`: the only hits are
  "Machine actors ... inheriting a human's role" (:180) and "service accounts don't inherit human roles"
  (template :55). That leaves three things unowned:
  - row #59's "assignment tables" (the storage shape for assignments, and who may assign which role,
    with a grant ceiling);
  - its "inheritance rules" (role hierarchy, and permissions cascading down a resource hierarchy, with
    precedence);
  - guardrails for custom roles defined by a tenant.

  None of these appears in any shipped skill.
- Recommend **MERGE** them as an extension. Check 3's preferred pattern is "a scoped additive diff"
  (SKILL.md:85-90). Its precedents: #192 into `test-plan-designer` (qa-tier1 :60) and #277 into
  `code-reviewer` (ai-sdlc :68).
- The extension fits:
  - The description has 531 characters of room. My draft extended description measures 828 with
    `yaml.safe_load` (Appendix A).
  - The body is 208 lines (`wc -l`), well under the 500-line cap.
- **Alternative: DROP** and record #59 as covered, at 0–0.25 hours. I reject it because §2 needs the
  grant-ceiling rule to live in the authorization skill. Otherwise the invitation skill would author
  authorization policy, which is an overlap.

**(3) Invocation posture.** Not applicable; the base skill stays model-invocable (catalog :425 "yes").

**(4) Estimate: 0.75–1.5 active hours, provisional.** Precedents: the test-plan-designer and code-reviewer
extensions, both 0.75–1.5 (qa-tier1 :60; ai-sdlc :68).

**(5) Value and dependencies.** It closes the two words in the P0 row that no skill covers, with no new
trigger. `membership-invitation-designer` (§2) consumes it.

**(6) Trigger boundary.**
- Existing trigger, plus "inherited or custom roles grant more than intended".
- **Not when:** a filter axis below the tenant → `intra-tenant-scope-architect`; plan gating →
  `plan-entitlement-architect`.
- **New trigger-eval cases:** against `intra-tenant-scope-architect` (resource-hierarchy inheritance
  versus a row-filter scope, a boundary that SKILL.md:46-50 already draws) and against
  `membership-invitation-designer` once it exists.

---

## 4. `security-impact-note-author` (for reconciliation with G5; see §0)

**(1) Source and priority.**
- cat-03:69, row #127 "Security Impact Note Authoring | **P0** | Document impact, risks, mitigations,
  tests, rollback, and approval needs for security-sensitive changes."
- Execution plan :402 and :741; recon :136; catalog :1313 and :1325.

**(2) Overlap verdict: PARTIAL, a thin gap that is mostly composition.** Each part of the row has a
shipped owner:

| Part of #127 | Shipped owner | Evidence |
| --- | --- | --- |
| Impact, risks, mitigations, validation, residual threats | `threat-modeler` (917) | Its inputs include "the existing code and schema of the surface being extended" (Inputs 1); the output has Mitigations, Accepted/deferred threats and a Validation plan. |
| Blast radius, reversibility, approval needs | `human-approval-boundary` (893) | Output fields Blast radius, Reversibility, Options |
| Approval path for the change class | `change-classification-gate` (669) | Output field "Approval path" |
| Rollback | `rollback-runbook-author` (997) | — |
| Control changes and tests at review time | `security-pr-reviewer` (962) | Output fields "Control changes" and "Tests" |
| Author's note for one implemented control | `appsec-implementer` (manual-only) | Output carries "Closes", "Change class — approval", the negative test before and after, and "Does NOT cover: <residual risk>" |
| Risks and skipped checks at PR opening | `ai-closeout-reporter` (1015) | Sections 6–7 |

Two greps support the gap:
- `security impact|impact note` across `.claude/skills` matched only `human-approval-boundary` evals
  :76 and `hidden-context-exposure-reviewer`.
- The only skill eval that mentions security impact is `human-approval-boundary` "stop-unclear-security-impact".

**The gap.** No skill produces one author-side, change-scoped record for *any* security-sensitive change.
By judgment it is about 25–35% distinct (not measured), which is below the ~40% threshold. That points
to an **extension**, not a new skill.

A standalone skill would collide with:
- `threat-modeler` on "what is the security impact of this change";
- `security-pr-reviewer` on "security-check this PR".

**Candidate bases.**
- (a) **`threat-modeler`**: a change-scoped "impact note" output mode. Its 107 characters of description
  room are enough for one phrase. It is uncertain whether that clashes with its "designs and systems,
  not hunks" boundary (Use When, "Do NOT use when: reviewing an implemented diff").
- (b) **`ai-closeout-reporter`**: a conditional "Security impact" section when the change is in the
  security class. Its description is full (1015 of 1024), so the change would be body-only. Precedent:
  migration proof went "in the body, not the description, to fit" (ai-sdlc :279-280).

My leaning is (a), and it is **unverified**. The G5 helper should decide with the security neighbors in view.

**(3) Invocation posture: model-invocable.** It drafts a document. Writing it into the repository falls under
Exception 1 (`docs/skill-generation-standard.md:291-297`). Posting it to GitHub is an external write that stays
with a human or a manual-only path.

**(4) Estimate if merged: 1–2 hours, provisional.** Precedents: the ai-closeout-reporter extension at 1–2
(ai-sdlc :67) and the model-context-designer extension at 1–1.5 (phase7 :67). If built standalone, 2.5–4
by the §1(4) basis, which I do not recommend.

**(5) Value.** The row is P0. It reduces review friction, but every one of its parts already exists.
Demand is unverified.

**(6) Trigger boundary.**
- **Use when:** "write the security impact note for this change before approval".
- **Not when:** reviewing the diff → `security-pr-reviewer`; a design-time threat model →
  `threat-modeler`; a halt for one risky action → `human-approval-boundary`.
- **Trigger evals pin against:** `threat-modeler`, `security-pr-reviewer` and `human-approval-boundary`.

---

## 5. Summary table

| Candidate (row, priority) | Verdict | Distinct vs nearest shipped (judgment) | Posture | Recommendation | Active h (provisional) |
| --- | --- | --- | --- | --- | ---: |
| `tenant-provisioning-designer` (#57, P0) | PARTIAL: `tenant-modeler` semantics + `saas-platform-architect` platform flow | ~70–80% | model-invocable (design only) | **BUILD** | 3–4.5 |
| `membership-invitation-designer` (#58, P0) | PARTIAL: `tenant-modeler` invitation semantics; flow mechanics and security unowned | ~60–65% | model-invocable | **BUILD, narrowed to flow mechanics** | 2.5–4 |
| `role-permission-architect` (#59, P0) | COVERED: catalog :425 attributes #59 to `authorization-matrix-designer`; residual assignment, inheritance and custom roles | <40% | n/a (base stays model-invocable) | **MERGE** as an extension (alternative: DROP) | 0.75–1.5 |
| `security-impact-note-author` (#127, P0) | PARTIAL: composition of `threat-modeler`, `human-approval-boundary`, `security-pr-reviewer`, `rollback-runbook-author` | ~25–35% | model-invocable | **Evaluate once in G5**; leaning MERGE (`threat-modeler`) | 1–2 if merged |
| Batch overhead (registration, decision row, reciprocity edits, reviews) | — | — | — | — | 1.5–3 |

**Basis for the overhead row.** The precedent overheads are 1.5–3 (qa-tier1 :64), 2–3.5 (phase6 :80),
1.5–2.5 (phase7 :71) and 1–2 (ai-sdlc :70). All of them predate D72 (2026-10-03, recon :3685), the
seven-stage delivery workflow that puts a separate agent on every stage of every PR. The effect of D72
on these hours is **unverified**; the MECH helper's measured costs should replace this row.

## 6. Recommendation: one coherent sub-batch of 3 ("G4-A: how tenants and members come into existence")

1. **EXTEND `authorization-matrix-designer`** with the #59 residual: role-assignment rules with a grant
   ceiling, role and resource-hierarchy inheritance with precedence, the shape of assignment storage, and
   bounded tenant-defined custom roles. #59 is recorded as covered, so no separate skill is built.
2. **BUILD `tenant-provisioning-designer`** (#57), model-invocable.
3. **BUILD `membership-invitation-designer`** (#58), model-invocable, narrowed to flow mechanics. It
   consumes `tenant-modeler`'s invitation states and the grant ceiling from item 1.

#127 leaves G4 and is evaluated once in G5 (§0).

**Effect.** The library goes from 195 to 197 skills.
- Total: **7.75–13 active hours**, provisional, low confidence. That is 0.75–1.5 + 3–4.5 + 2.5–4 + 1.5–3.
- The forecast row for G4 is 8–16 for four candidates. Moving #127 out removes its roughly 2–4 hours
  from G4's share.

**Why this set is coherent.**
- All three share one neighbor cluster: `tenant-modeler`, `authorization-matrix-designer`,
  `share-link-access-architect` and `saas-platform-architect`. One trigger-eval seam design covers all
  of them.
- The `tenant-modeler` reciprocity rewrite is done once. My draft names both new skills at 995 characters
  (Appendix A).
- Item 1 is a precondition of item 3.

**Suggested PR order and mechanics.**
- PR1 = item 1 plus the decision row, so a new D-number. D73 is the highest on `main`: a grep for
  `D7[4-9]|D[89][0-9]` in `docs` returned 0 matches. Recheck at build time.
- PR2 = item 2 plus the reciprocity edit in `saas-platform-architect`. Its description has 209
  characters of room.
- PR3 = item 3 plus the reciprocity edit in `share-link-access-architect`, which has 102 characters of
  room. PR3 also does the one `tenant-modeler` rewrite, once both new skills are on disk.
- **Order matters.** The contract audit flags trigger evals that name a skill not yet on disk. Evidence:
  commit `cf4c6908`, "keep trigger-evals to skills on disk ... the seam is pinned once that skill
  exists", and the follow-up `fa9e05b9`.
- Expect two one-way ROUTE-002 findings to remain as census data, following D64 (recon :3283-3290):
  toward `test-tenant-provisioner` (1006 characters, so no room to reciprocate) and
  `background-job-orchestration-architect`. This is predicted, not measured.
- A `project-orchestrator` Stage 3 route for the two new skills (SKILL.md:239-240) is optional. D64 needed
  a separate PR, #384 (metrics :717), so decide at build time.
- Each build PR answers "Yes" on "Security-relevant surface?", because the list includes any skill's
  Stop Conditions and Security Rules (CONTRIBUTING.md:247-249). The additional review applies to outside
  contributions only (CONTRIBUTING.md:233-236; AGENTS.md).

**Alternatives.**
- **Smaller: items 1 and 2 only**, deferring #58. Estimate 4.75–8, using the 1–2 overhead of the
  one-skill ai-sdlc precedent. This leaves the invitation-security gap open.
- **Combined: one new `tenant-onboarding-flow-designer` covering #57 and #58, plus item 1.** Estimate
  5.75–9.5. The single-skill figure of 3.5–5.5 inside that is my judgment. A stranger would count two
  jobs (tenant creation and member invitations), so it risks a check 6 CONCERN (skill-quality-reviewer
  SKILL.md:101-102). I do not recommend it.
- **None**, if the DEMAND helper finds no evidence of demand for SaaS tenancy flows and other groups
  carry stronger demand.

## 7. Self-scrutiny

**Strongest counter-argument.** `tenant-modeler` already claims "invitations" in its description. The
library's last four batches dropped or merged most of their candidates: the decision tables in
qa-tier1 :57-65, ai-sdlc :66-71 and phase7 :64-72. A capable generalist using `tenant-modeler`,
`share-link-access-architect`, `authorization-matrix-designer` and `audit-log-architect` might handle
invitation flows well enough. On that view, building `membership-invitation-designer` adds a real risk
of trigger collision with `tenant-modeler` for a modest gain. The same argument, more weakly, says
provisioning could be a scoped addition to `saas-platform-architect`'s step 6.

**Least certain claims.**
- (a) The distinctness percentages. They are judgment, exactly as D31 and D32 used them, and not measured.
- (b) The estimates. No precedent has a measured active time, and the overhead predates D72.
- (c) Whether new skills reduce routing errors or create them. No trigger eval has been run.
- (d) The leaning toward `threat-modeler` as the home for #127 (§4).
- (e) Value. No user-demand data was read; the DEMAND helper owns it.

**Evidence that would change the recommendation.**
- A trigger-eval dry run showing `tenant-modeler` reliably wins invitation-flow prompts *and* covers
  token, binding and ceiling behavior. That would turn item 3 into a body extension or a DROP.
- DEMAND evidence that no consumer has built multi-member tenants. That would cut the batch to item 1,
  or to none.
- MECH measurements showing D72 overhead per PR far above the precedent. That would favor fewer PRs, and
  so the combined alternative.
- An owner preference for fewer skills.

## 8. Not done, unverified, open

**Not done.**
- No `scripts/audit-skill-contracts.py` run, so the ROUTE-002 predictions are unmeasured.
- No reading of neighbor trigger-eval files beyond the prompt lists for `tenant-modeler` and
  `authorization-matrix-designer`.
- No demand research, which belongs to the DEMAND helper.
- No evaluation of G5's other topics.
- No check of the SCIM/directory-sync gap: no shipped skill or source row covers it, by grep of
  `.claude/skills` and `docs/skills`. It is noted here only and is **not** used to support the
  recommendation.
- No reading of adjacent cat-02 rows that no skill owns (#66 settings, #82 onboarding, #83 offboarding).
  They are outside G4 and do not support the recommendation.

**Unverified items:** see §7, "Least certain claims".

**Open question for the coordinator.** Confirm with the SEC helper that #127 is evaluated once in G5.

## Appendix A: draft descriptions

These are measured, untested drafts for the builder; the builder owns the final wording. File:
`$S/skillbatch/g4-drafts/drafts.yaml`. Measured with
`python3 -I -c "yaml.safe_load(...)"`; no value contains a newline.

| Draft | Characters |
| --- | ---: |
| `tenant-provisioning-designer` | 1002 |
| `membership-invitation-designer` | 1001 |
| `authorization-matrix-designer`, extended (from 493) | 828 |
| `tenant-modeler` reciprocal rewrite (from 974) | 995 |

The `tenant-modeler` rewrite keeps every "Use when" and excluded neighbor from the current description,
in shorter wording. The builder must confirm that no meaning of a trigger is lost.
