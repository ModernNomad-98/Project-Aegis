# Quality assurance Tier 1 skill batch: scope proposal

> **Status:** Proposal only, waiting for an owner decision. This page grants no
> authority and builds nothing. No skill, evaluation file, catalog row or
> decision-log row was created or changed by the pull request that adds it.

Prepared 2026-09-28 from `ModernNomad-98/Project-Aegis` `origin/main` at
`ebf210c6`, where the validator reported 186 valid skills.

This page is for the owner, who decides whether and how to build the five
remaining quality assurance (QA) Tier 1 candidates, and for the maintainers
and reviewers who would build them. It follows the
[feature-flag skill proposal](feature-flag-architect-skill-proposal.md): it
records scope, boundaries and an estimate, and builds nothing.

## Terms used on this page

- **Quality assurance (QA)** is the work of checking that software does what
  it should before users rely on it.
- **Tier 1** is the "build first" group in the prioritized QA expansion
  backlog, recorded by decision D10 in the
  [reconciliation log, section 3](../reconciliation/step-0-reconciliation-v4.md#phase-5-qa-expansion-backlog--prioritized-d10).
  A **D-number** (for example D10 or D68) is a numbered entry in that log's
  [recorded decisions](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions).
- A **skill** is a folder under `.claude/skills/` whose `SKILL.md` tells an
  AI assistant how to do one job. Its **description** is the text the
  assistant reads when choosing a skill; the library caps it at 1,024
  characters.
- A **manual-only** skill carries `disable-model-invocation: true`, so the
  assistant never picks it on its own; a person must name it. The
  [skill generation standard, section 5](../skill-generation-standard.md#5-least-privilege--side-effects)
  requires this for any skill that writes, calls a network, deploys or spends.
  A skill that only reads and reports stays **auto-invocable**.
- An **extension** adds a scoped piece of work to an existing skill instead of
  creating a new one.
- **Continuous integration (CI)** is the automated build-and-test run on each
  change. **End-to-end (E2E)** tests drive the whole product like a user.
  **Row-level security (RLS)** is database rules that limit which rows each
  tenant (customer account) can read or write.
- **Behavior evals** (`evals/evals.json`) describe prompts and the behavior a
  skill should show. **Trigger evals** (`evals/trigger-evals.json`) check that
  the right skill, and not a neighbor, is chosen for a prompt.
- **ROUTE-002** is a census finding from `scripts/audit-skill-contracts.py`:
  skill A's description says "Do NOT use for X (skill B)", but skill B's
  description never names A. It is information, not a failure; widely used
  "hub" skills cannot name every skill that points at them.
- **Active hours** count only hands-on agent work, excluding review waits, CI
  queue time and time waiting for the owner. They are agent estimates, not
  measurements.

## Decision in one read

The five candidates are not five equal gaps. Checking each against the 186
shipped skills shows that one is already covered, one fits best as a small
extension, and three are real gaps.

| Candidate (roadmap row) | Recommendation | Manual-only? | Active hours (provisional) |
| --- | --- | --- | ---: |
| `regression-first-bug-fixer` (#190) | **DROP**: already owned by `tdd-engineer`, `systematic-debugger` and `regression-suite-curator` | not applicable | 0–0.25 |
| `negative-path-test-mapper` (#192) | **MERGE** into `test-plan-designer` as an extension | not applicable (base stays auto-invocable) | 0.75–1.5 |
| `test-tenant-provisioner` (#198) | **BUILD** | **Yes**, it writes to an environment | 3–5 |
| `ci-failure-classifier` (#214 + #215) | **BUILD** | No, read-only over logs it is given | 2.5–4 |
| `acceptance-criteria-tester` (#226 + #227) | **BUILD, narrowed to #226 and renamed** `acceptance-criteria-reviewer` | No, read-only review | 2–3.5 |
| Batch overhead (registration, decision row, reciprocity edits, reviews) | — | — | 1.5–3 |
| **Total** | **3 new skills, 1 extension, 1 drop** | | **9.75–17.25** |

The [backlog forecast](aegis-backlog-forecast.md) carries this group as "QA
expansion Tier 1 (five skills)" at 10–20 agent-estimated hours. The
recommended set lands slightly lower because two candidates do not become new
skills.

Roadmap row numbers refer to
[category 06 of the skills roadmap](../skills/06-qa-test-engineering.md). All
five rows are priority P0 (highest) there.

## Candidate 1: `regression-first-bug-fixer` (#190)

**Roadmap text:** "Write a failing test that reproduces the bug before
implementing the fix."

**Purpose as proposed.** When a bug is reported, first write a test that
fails because of the bug, confirm it fails for the right reason, then fix the
code and show the same test passing. The test stays as a guard against the bug
returning.

**Claimed gap.** The D10 note says `regression-suite-curator` owns suite
membership, not the fix workflow, and that `tdd-engineer` "owns new behavior,
not bug reproduction".

**What the shipped skills already do.** The D10 note on `tdd-engineer` is out
of date:

- [`tdd-engineer`](../../.claude/skills/tdd-engineer/SKILL.md) (manual-only)
  lists "Use when: fixing a bug — the reproduction becomes the regression
  test, red before the fix, green after", and its description includes "when
  fixing a bug that should get a regression test proving the fix". Its core
  rule, confirm the test fails for the intended reason before changing code,
  is exactly the #190 discipline.
- [`systematic-debugger`](../../.claude/skills/systematic-debugger/SKILL.md)
  (manual-only) handles bugs whose cause is unknown; its step 6, "Prevent",
  adds the reproduction as the regression test and hands it to
  `tdd-engineer`.
- [`regression-suite-curator`](../../.claude/skills/regression-suite-curator/SKILL.md)
  decides which fixed-bug tests are promoted into which suite tier and cites
  catalog item 190 by number.

| Boundary | Owner today |
| --- | --- |
| Cause unknown: reproduce, reduce, isolate, prove the root cause | `systematic-debugger` |
| Cause known: failing test first, minimal fix, green run, transcript | `tdd-engineer` |
| Whether the new test joins the smoke, pull-request or nightly tier | `regression-suite-curator` |
| An intermittent failure rather than a consistent bug | `flaky-test-detective` |

A new skill would sit exactly on `tdd-engineer`'s "fixing a bug" trigger and
fail check 2 (trigger collision) of
[`skill-quality-reviewer`](../../.claude/skills/skill-quality-reviewer/SKILL.md).

**Recommendation: DROP.** Record #190 in the "Already covered" table of the
D10 backlog as owned by `tdd-engineer`, with `systematic-debugger` and
`regression-suite-curator` as the neighbors above, and correct the stale D10
note in the same decision row.

- **Manual-only:** not applicable; nothing is built. The owning skills are
  already manual-only because they write test and source files and run suites.
- **Draft description:** none; nothing new to route.
- **ROUTE-002 edits:** none.
- **Evals:** none new. Optional, if the owner wants proof of coverage: one
  trigger-eval case in `tdd-engineer` for "a customer reported the export
  drops the last row; write the failing test before the fix" (0.25 hours).
- **Estimate:** 0–0.25 active hours, mostly the covered-table row.

## Candidate 2: `negative-path-test-mapper` (#192)

**Roadmap text:** "Test unauthorized, invalid, expired, missing, duplicated,
conflicting, and out-of-order scenarios."

**Purpose as proposed.** For each surface of a product (an endpoint, a form, a
background job, a webhook), list systematically how it should behave when the
input or situation is wrong, so that tests cover more than the happy path.

**What the shipped skills already do.**

- [`test-plan-designer`](../../.claude/skills/test-plan-designer/SKILL.md)
  already derives "happy path, negative path, boundary" behaviors for every
  risk (workflow step 2). Its
  [plan template](../../.claude/skills/test-plan-designer/references/test-plan-template.md)
  lists the negative paths as "unauthorized, invalid input, expired, missing,
  duplicate, conflicting, out-of-order": the same seven classes as #192.
- [`manual-test-case-creator`](../../.claude/skills/manual-test-case-creator/SKILL.md)
  requires happy, negative and boundary cases per behavior.
- [`integration-test-designer`](../../.claude/skills/integration-test-designer/SKILL.md)
  requires per-boundary negative cases.
- [`multi-tenant-security-tester`](../../.claude/skills/multi-tenant-security-tester/SKILL.md)
  (manual-only) owns security negatives: cross-tenant access, wrong role,
  privilege escalation.
- [`test-coverage-mapper`](../../.claude/skills/test-coverage-mapper/SKILL.md)
  finds existing gaps but has no negative-path class of its own.

**The real gap is small.** The seven classes appear as a catalog in a
reference file, but nothing requires them to be walked **per surface** or
recorded as a matrix, so a plan can list "negative paths" and still skip
"expired" or "out-of-order" silently. A standalone skill would compete with
`test-plan-designer` for every "what should we test for this change?" prompt.

| Boundary | Owner after the extension |
| --- | --- |
| Per-surface negative-path matrix for one change or release | `test-plan-designer` (extended) |
| Cross-tenant, wrong-role and privilege-escalation negatives | `multi-tenant-security-tester` |
| Real-boundary negative cases in integration suites | `integration-test-designer` |
| Negative steps in manual cases | `manual-test-case-creator` |
| Which negatives are missing from existing tests | `test-coverage-mapper` |
| Error codes and envelopes the negatives should return | `error-taxonomy-designer` |

**Recommendation: MERGE** into `test-plan-designer` as an extension, the
pattern `skill-quality-reviewer` check 3 prefers when new content fits as a
scoped addition. The extension:

1. makes step 2 produce a negative-path matrix: rows are the surfaces the
   change touches, columns are the seven classes, and each cell is a planned
   item, "not applicable because …", or a delegation to
   `multi-tenant-security-tester`;
2. adds a matrix block to the output template and one checklist line ("every
   touched surface has all seven classes answered");
3. updates the description (draft below).

**Manual-only:** no. `test-plan-designer` designs and writes nothing; the
extension keeps it auto-invocable.

**Draft replacement description for `test-plan-designer`**, 961 characters
measured with Python `yaml.safe_load` (limit 1,024). It adds the matrix and a
reciprocal exclusion toward `acceptance-criteria-reviewer` (candidate 5); every
existing "Use when" phrase and excluded neighbor stays.

```yaml
description: 'Design the concrete test plan for ONE feature, change, or release — the requirement/risk being verified, in-scope and out-of-scope items, the test-layer split for THIS change (what is automated at which layer, what is manual), a negative-path matrix per surface (unauthorized, invalid, expired, missing, duplicate, conflicting, out-of-order), test data needs, environment assumptions, entry/exit criteria, named artifacts, and CI placement. Every planned test traces to a requirement or risk. Use when asked to write a test plan for a feature/release/bugfix, to decide what testing a specific change needs before it ships, or to turn acceptance criteria into a verification plan. Do NOT use for the product-wide QA strategy (qa-strategy-architect), auditing existing coverage (test-coverage-mapper), checking criteria are testable (acceptance-criteria-reviewer), writing manual case steps (manual-test-case-creator), or implementing tests (the engineer skills).'
```

To make room, the sentence "the plan is executable by someone who didn't
write it" moves from the description into the skill body, where the same rule
already appears as the plan-item quality bar.

**ROUTE-002 edits:** none new from the matrix. The exclusion toward
`acceptance-criteria-reviewer` is reciprocated by that skill's own description.

**Eval plan.**

- Behavior: one new case where a change touches an invite endpoint and a
  webhook; the plan must show all seven classes for both surfaces, mark any
  "not applicable" with a reason, and delegate the cross-tenant cell rather
  than specifying it.
- Behavior: one refusal-edge case where the user asks for "just the happy
  path"; the plan may narrow scope but must list the skipped negative classes
  as out of scope, never omit them silently.
- Trigger: two cases pinning "map every negative path for this API change" to
  `test-plan-designer` against `multi-tenant-security-tester` and
  `integration-test-designer`.

**Estimate:** 0.75–1.5 active hours.

## Candidate 3: `test-tenant-provisioner` (#198)

**Roadmap text:** "Create test tenants and users for repeatable auth, RLS,
integration, and E2E validation." D10 broadened it with: a marker on every
test row and a rule never to change unmarked rows; separate validate-only and
apply modes; credentials referenced by environment-variable name only;
capability grants that need a backup and carry an inline rollback; and a
static check that QA automation cannot reach production.

**Purpose.** Create, repair and check the named test tenants, users, roles and
memberships that auth, RLS, integration and E2E runs depend on, in a named
non-production environment, so every run starts from the same known accounts
instead of hand-made ones that drift.

**The gap.** Designing test data is owned; **making the accounts exist and
proving they still match** is not:

- [`test-data-architect`](../../.claude/skills/test-data-architect/SKILL.md)
  designs the persona and baseline catalog ("owner/admin/member per tenant"),
  seeds and isolation rules. It produces a design and hands wiring to the
  engineer skills. It never touches an environment.
- `multi-tenant-security-tester` (manual-only) specifies seeded two-tenant
  fixtures for its security suites, but does not create or repair them.
- [`tenant-modeler`](../../.claude/skills/tenant-modeler/SKILL.md) defines
  what a tenant is in the product, including real tenant provisioning, not
  test accounts.
- [`secrets-identity-hardener`](../../.claude/skills/secrets-identity-hardener/SKILL.md)
  (manual-only) stores and rotates credentials; the provisioner only refers to
  them by name.

| Boundary | Owner |
| --- | --- |
| Which personas, tenants and roles exist, and their stable identifiers | `test-data-architect` |
| Creating, repairing and checking those accounts in a test environment | `test-tenant-provisioner` (new) |
| The two-tenant security fixtures' required shape | `multi-tenant-security-tester` |
| What a tenant is and its product lifecycle | `tenant-modeler` |
| Where the test credentials live and how they rotate | `secrets-identity-hardener` |
| Whether the RLS policies those accounts exercise are correct | `rls-policy-auditor` |

Merging into `test-data-architect` was considered and rejected: the apply mode
writes to an environment, which would force that auto-invocable design skill
to become manual-only and lose automatic routing for every fixture-design
question.

**Recommendation: BUILD, manual-only.** Validate-only is the default mode;
apply mode needs a named non-production environment and explicit human
approval. Stop Conditions refuse production, refuse to change or delete an
unmarked row, refuse to print or store a credential value, and stop when no
persona catalog exists (hand off to `test-data-architect` first).

**Draft description**, 1,006 characters measured with `yaml.safe_load`:

```yaml
description: 'MANUAL-ONLY; never auto-invoke. Provision and verify repeatable test tenants and users in a named NON-PRODUCTION environment for auth, row-level-security (RLS), integration and end-to-end (E2E) runs. Every created row carries a test marker and unmarked rows are never mutated; validate-only mode (the default) reports drift against the persona catalog, apply mode creates or repairs only marked tenants, users and memberships; credentials are referenced by environment-variable NAME only; capability grants are backup-gated with an inline rollback; a static lint flags test automation that could reach production. WRITES to an environment, so manual invocation only. Use when test tenants or users are missing, drifted or hand-made, or runs fail on stale auth fixtures. Do NOT use to design the persona and data catalog (test-data-architect), write cross-tenant security tests (multi-tenant-security-tester), define the tenant model (tenant-modeler), or store or rotate secrets (secrets-identity-hardener).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `test-data-architect` | 999 | Reciprocate; needs about 50 characters of rewording elsewhere to fit a "provisioning the accounts (test-tenant-provisioner)" exclusion |
| `multi-tenant-security-tester` | 831 | Reciprocate; room exists |
| `tenant-modeler` | 974 | Leave one-way (census) |
| `secrets-identity-hardener` | 846 | Leave one-way (census); room exists, but it is a security hub that many skills point at |

**Eval plan.** Every positive prompt names the skill, because the
[standard, section 6](../skill-generation-standard.md#6-evaluations) requires
it for manual-only skills; trigger-eval cases use the prefix
`Explicitly invoke test-tenant-provisioner. `.

- Behavior, happy path: validate-only run against a staging catalog of two
  tenants and six personas; reports one missing membership and one drifted
  role, changes nothing.
- Behavior, apply: repairs only marked rows, shows the backup reference and
  rollback step before a capability grant, names credentials by variable name.
- Behavior, refusal: "seed the demo tenant in production" is refused.
- Behavior, refusal: an unmarked row blocks the repair; the skill reports it
  and does not touch it.
- Behavior, edge: no persona catalog exists; the skill stops and hands off to
  `test-data-architect`.
- Behavior: the static lint flags a test config whose base URL resolves to the
  production host.
- Trigger: about 8 cases against `test-data-architect`,
  `multi-tenant-security-tester` and `tenant-modeler`, in both directions.

**Estimate:** 3–5 active hours. It is the largest item because of the two
modes, the marker rule, the lint and the refusal cases. The pull request that
builds it will likely answer "Yes" to the security-relevant-surface question,
because it handles credentials and environment writes.

## Candidate 4: `ci-failure-classifier` (#214 + #215)

**Roadmap text:** #214 "Scan logs for console errors, unhandled rejections,
skipped tests, auth failures, and hidden runtime failures"; #215 "Classify
failure as product bug, test bug, missing secret, timeout-only, infra failure,
or skipped runtime." D10 merged them into one skill and added: duration as
first-class evidence, a timeout class never confused with a regression,
resume instead of rerun after timeout-only interruptions, and no hiding real
failures by raising timeouts.

**Purpose.** Given a CI run's logs and reports, give every failed or
suspicious job exactly one cause class, and scan passing runs for problems the
green result hides, so the next step goes to the right owner instead of a
blind rerun.

**The gap.** Several shipped skills touch CI results, but none answers "why is
this CI run red, and is this green run really green?":

- [`local-ci-mirror-preflight`](../../.claude/skills/local-ci-mirror-preflight/SKILL.md)
  (manual-only) runs the checks locally before push and classifies failures by
  **origin**: caused by this change, already failing on main, CI
  infrastructure, or not determinable locally. It does not classify a remote
  run by **cause type** or scan green runs.
- [`flaky-test-detective`](../../.claude/skills/flaky-test-detective/SKILL.md)
  (manual-only) finds the root cause of one intermittent test.
- `systematic-debugger` (manual-only) finds the root cause of a product bug.
- [`sharded-validation-with-resume`](../../.claude/skills/sharded-validation-with-resume/SKILL.md)
  designs how interrupted runs resume.
- [`ci-pipeline-architect`](../../.claude/skills/ci-pipeline-architect/SKILL.md)
  (manual-only) designs and edits the pipeline itself.

| Boundary | Owner |
| --- | --- |
| Cause class of each failure in an existing CI run; hidden markers in green runs | `ci-failure-classifier` (new) |
| Running checks locally before push; origin classification | `local-ci-mirror-preflight` |
| Root cause of an intermittent test | `flaky-test-detective` |
| Root cause of a product bug | `systematic-debugger` |
| Resuming only unfinished shards after a timeout | `sharded-validation-with-resume` |
| A missing CI secret's governance | `ci-pipeline-architect` |
| Pipeline stages, retries and gates | `ci-pipeline-architect`, `qa-automation-architect` |

Extending `local-ci-mirror-preflight` was considered and rejected: that skill
is manual-only because it runs checks, so "why did CI fail?" would never route
to it automatically, and its job is pre-push verification, not diagnosis of a
run that already happened.

**Recommendation: BUILD, auto-invocable.** It reads logs and reports the user
supplies or that are already on disk, and reports. It fetches nothing from a
CI provider, reruns nothing and edits nothing, so section 5 of the standard
keeps it auto-invocable. Stop Conditions refuse to raise a timeout or add a
retry to turn red into green, and refuse to call a run "passed" when a
required job was skipped.

**Draft description**, 1,013 characters measured with `yaml.safe_load`:

```yaml
description: 'Classify a CI run''s failures and hidden problems from its logs and reports: each failed or suspicious job gets exactly one class (product bug, test bug, missing secret or config, timeout-only, infrastructure, skipped-runtime where a skip hides the real result, or indeterminate), with duration as first-class evidence and timeouts never conflated with regressions; GREEN runs are scanned for hidden runtime markers (console errors, unhandled rejections, unexpected skips, auth failures). Reads logs supplied or already on disk; fetches and reruns nothing. Refuses to mask a failure by raising a timeout or adding a retry. Use when CI is red and the cause is unclear, a pass looks suspicious, or a timeout must be told apart from a failure. Do NOT use to root-cause an intermittent test (flaky-test-detective), debug a product bug (systematic-debugger), mirror CI locally before push (local-ci-mirror-preflight), design shard resume (sharded-validation-with-resume), or design the pipeline (ci-pipeline-architect).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `local-ci-mirror-preflight` | 715 | Reciprocate; room exists |
| `systematic-debugger` | 710 | Reciprocate; room exists |
| `flaky-test-detective` | 1,012 | Leave one-way (census); no room |
| `sharded-validation-with-resume` | 1,009 | Leave one-way (census); no room |
| `ci-pipeline-architect` | 1,016 | Leave one-way (census); already a hub under D64 |

**Eval plan.**

- Behavior, happy path: a red run with an assertion failure in one job and a
  runner disconnect in another gets two different classes with the log lines
  that justify each.
- Behavior: a job that timed out at its 30-minute ceiling with no failed
  assertion is TIMEOUT, not a regression; the hand-off names
  `sharded-validation-with-resume`.
- Behavior: a green run whose logs contain an unhandled promise rejection and
  12 unexpectedly skipped tests is reported as green-with-findings.
- Behavior, refusal: "just bump the timeout so it passes" is refused with the
  reason.
- Behavior, edge: logs are truncated; affected jobs are INDETERMINATE with the
  evidence that would settle them.
- Trigger: about 10 cases in both directions against `flaky-test-detective`
  ("fails one run in five"), `systematic-debugger`,
  `local-ci-mirror-preflight` ("before I push") and
  `sharded-validation-with-resume`.

**Estimate:** 2.5–4 active hours.

## Candidate 5: `acceptance-criteria-tester` (#226 + #227)

**Roadmap text:** #226 "Verify requirements are testable, complete,
unambiguous, and tied to validation evidence"; #227 "Check code, tests, docs,
security, migration, CI, screenshots, and closeout before marking done." D10
merged them and noted the candidate was already deferred once.

**Purpose as proposed.** Before work starts or is tested, check that the
acceptance criteria (the conditions a feature must meet to count as done) can
actually be checked, and that the definition of done (DoD) is met before work
is marked finished.

**What the shipped skills already do.**

- [`product-spec-writer`](../../.claude/skills/product-spec-writer/SKILL.md)
  **writes** specifications with testable acceptance criteria and names the
  anti-pattern of criteria that restate the requirement. It does not review
  criteria written elsewhere, such as a ticket or user story.
- [`requirements-gathering-facilitator`](../../.claude/skills/requirements-gathering-facilitator/SKILL.md)
  draws out unclear requirements before a specification exists.
- `test-plan-designer` **turns** criteria into a verification plan and
  assumes they are testable.
- [`release-readiness-reviewer`](../../.claude/skills/release-readiness-reviewer/SKILL.md)
  already gates a release, merge or risky change on evidence per dimension:
  CI on the exact candidate, tests, migration review, rollback, flags, docs,
  observability and approvals. That is the #227 checklist.
  [`ai-closeout-reporter`](../../.claude/skills/ai-closeout-reporter/SKILL.md)
  writes the closeout and
  [`agent-governance-audit`](../../.claude/skills/agent-governance-audit/SKILL.md)
  verifies afterward that the process was followed.

**The gap.** #226 is real: nothing reviews criteria someone else wrote and
returns a per-criterion verdict before a plan is built on them. #227 is
covered by the three skills above, and a new DoD gate would collide with
`release-readiness-reviewer` on "is this ready to mark done?".

| Boundary | Owner |
| --- | --- |
| Writing a specification and its criteria | `product-spec-writer` |
| Drawing out unclear requirements | `requirements-gathering-facilitator` |
| Reviewing existing criteria for testability, completeness and ambiguity | `acceptance-criteria-reviewer` (new) |
| Turning checked criteria into a test plan | `test-plan-designer` |
| Writing manual cases from the criteria | `manual-test-case-creator` |
| The definition-of-done evidence gate (#227) | `release-readiness-reviewer`, with `ai-closeout-reporter` and `agent-governance-audit` |

**Recommendation: BUILD, narrowed to #226, and rename it
`acceptance-criteria-reviewer`.** The skill reviews criteria; it does not run
tests, so "tester" would mislead both users and routing. The `-reviewer`
suffix matches library usage for read-only verdict skills (for example
`release-readiness-reviewer` and `tenant-isolation-reviewer`). Record #227 as
covered in the D10 table.

**Manual-only:** no. It reads and reports; suggested rewrites are shown for
the author to accept and are never applied silently.

**Draft description**, 1,000 characters measured with `yaml.safe_load`:

```yaml
description: 'Review acceptance criteria that already exist, in a spec, ticket or user story, for testability, completeness and ambiguity: each criterion must name an observable outcome, a pass or fail threshold and the evidence that will prove it; missing negative, boundary and permission cases are listed; vague words ("fast", "works", "user-friendly") are flagged with a suggested concrete rewrite for the author to accept. Per-criterion verdict TESTABLE, NEEDS-REWRITE or UNTESTABLE, with one question to the owner where intent is unclear; rewrites nothing silently and invents no requirement. Use when a story or spec arrives for build or test and nobody has checked that its criteria can be verified, or before turning criteria into a test plan. Do NOT use to write the spec (product-spec-writer), elicit unclear requirements (requirements-gathering-facilitator), plan the tests (test-plan-designer), write manual cases (manual-test-case-creator), or gate a release on evidence (release-readiness-reviewer).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `test-plan-designer` | 868 (961 after candidate 2) | Reciprocated by the candidate 2 description above |
| `product-spec-writer` | 895 | Reciprocate; room exists |
| `requirements-gathering-facilitator` | 993 | Leave one-way (census); no room |
| `manual-test-case-creator` | 983 | Leave one-way (census); little room |
| `release-readiness-reviewer` | 819 | Leave one-way (census); gate hub |

**Eval plan.**

- Behavior, happy path: a five-criterion ticket with one "should load fast"
  criterion; that one is NEEDS-REWRITE with a measurable suggestion, the rest
  TESTABLE with the evidence named.
- Behavior: a criterion list with no failure or permission cases; the missing
  classes are listed as gaps, not invented as requirements.
- Behavior, refusal: "just fix the criteria in the ticket" produces suggested
  rewrites for the author and changes nothing.
- Behavior, edge: criteria that contradict each other get one owner question,
  not a guess.
- Trigger: about 8 cases in both directions against `product-spec-writer`
  (write vs review), `test-plan-designer` (review vs plan) and
  `release-readiness-reviewer` ("is this story done?").

**Estimate:** 2–3.5 active hours.

## Batch summary

**Recommended set:** build `test-tenant-provisioner`, `ci-failure-classifier`
and `acceptance-criteria-reviewer`; extend `test-plan-designer` with the
negative-path matrix; drop `regression-first-bug-fixer` and
`acceptance-criteria-tester`'s #227 half as already covered. The library
would go from 186 to 189 skills.

**Suggested pull requests**, so each has one reviewable seam:

1. `test-plan-designer` extension, `acceptance-criteria-reviewer`, the
   `product-spec-writer` reciprocity edit, the D10 covered-table rows for #190
   and #227, and the D68 decision row.
2. `ci-failure-classifier` with the `local-ci-mirror-preflight` and
   `systematic-debugger` reciprocity edits.
3. `test-tenant-provisioner` with the `test-data-architect` and
   `multi-tenant-security-tester` reciprocity edits.

Each new skill needs its catalog row (the
[skills catalog](../skills-catalog.md) Phase 5 section), the README counts
inside the validator-checked markers, both eval files, and the registration
steps in
[How to add a skill](../../CONTRIBUTING.md#how-to-add-a-skill).

**Total estimate:** 9.75–17.25 active hours, provisional, including 1.5–3
hours of batch overhead (registration, decision row, reciprocity edits,
contract-audit comparison and reviews). No project-orchestrator route is
proposed; confirm at build time that no stage needs one.

**Review path per pull request**, as in the feature-flag precedent:
`python -B scripts/validate-skills.py`; `skill-quality-reviewer` checks 1–7
on each new or extended skill in a fresh session; a ROUTE-002 before-and-after
comparison with `scripts/audit-skill-contracts.py` (a protected script that
this work does not change, and whose frozen baseline is not regenerated);
`library-diff-reviewer` on the whole pull request; then a merge under the
standing conditions of
[AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green),
[AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
and
[AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review).

**Decision number:** the build would be recorded as **D68**. D67 was the
highest decision number in the reconciliation log at `ebf210c6`, and no other
page on `main` mentions D68. Recheck at build time.

**Expected ROUTE-002 census after the batch:** eight new one-way findings
would remain, toward `tenant-modeler`, `secrets-identity-hardener`,
`flaky-test-detective`, `sharded-validation-with-resume`,
`ci-pipeline-architect`, `requirements-gathering-facilitator`,
`manual-test-case-creator` and `release-readiness-reviewer`. Following the
D64 owner decision, these would stay as census data rather than trigger
rewrites of full or hub descriptions.

## What the owner must answer

One reply of "build it as recommended" answers all four with the recommended
option.

1. **Build set.** Approve building the recommended set (three new skills, one
   extension, one drop)? *Recommended: yes.* Alternative: build all five as
   separate skills, which adds roughly 3–6 hours and two trigger collisions
   (`tdd-engineer` and `test-plan-designer`).
2. **Name.** Rename `acceptance-criteria-tester` to
   `acceptance-criteria-reviewer`? *Recommended: yes*, because it reviews and
   runs no tests.
3. **`ci-failure-classifier` posture.** Keep it auto-invocable and reading
   only logs it is given? *Recommended: yes.* The alternative, letting it fetch
   logs from the CI provider itself, is a network call and would make it
   manual-only, so "why is CI red?" would no longer route to it automatically.
4. **Census findings.** Accept the eight one-way ROUTE-002 findings listed
   above as census data? *Recommended: yes*, matching D64.

Whether this work counts inside the bounded selected planning subtotal in the
[backlog forecast](aegis-backlog-forecast.md) is not asked; like the
feature-flag work, it stays outside unless the owner selects it.

## What this page does not do

This page grants no authority and builds nothing. It creates no skill,
evaluation, catalog row, README count or decision-log row, and it edits no
shipped skill. An owner "build it" answer would be a new instruction to record;
delivery would then rely on the standing delivery approval in
[AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
and its conditions. Nothing here waives a protected `gate-guard` check,
authorizes a change to `scripts/audit-skill-contracts.py` or its frozen
baseline, or permits any environment write, provider call or deployment.

**Checked for this proposal:** the D10 Tier 1 table, the catalog's Phase 5
section, roadmap rows #190, #192, #198, #214, #215, #226 and #227, the
descriptions of every neighbor named above (lengths measured with
`yaml.safe_load`), and the relevant body
sections of `tdd-engineer`, `systematic-debugger`, `regression-suite-curator`,
`test-plan-designer` and its template, `test-data-architect`,
`local-ci-mirror-preflight` and `product-spec-writer`.

**Not checked:** the neighbors' existing trigger-eval files (the build must
add cases to them where reciprocity edits land), the project-orchestrator
stage map, and `scripts/audit-skill-contracts.py` output; the expected
ROUTE-002 findings above are predicted from the draft descriptions, not
measured. The behavior of the drafted skills is untested; the estimates are
agent estimates, not measurements.
