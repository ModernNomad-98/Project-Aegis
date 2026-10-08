# Unselected skill expansion batch: scope proposal

> **Status:** Proposal only, waiting for an owner decision. This page grants no
> authority and builds nothing. No skill, evaluation file, catalog row or
> decision-log row was created or changed by the pull request that adds it.

Prepared 2026-10-08 against source commit
`5228977920ee479e1fe1ec6b8d56f8fc24c14947`. The source tree has **195
shipped `SKILL.md` entrypoints**, counted by the paths
`.claude/skills/*/SKILL.md` after excluding `_template`. This is a file count,
not a validator result or a claim that all skills are effective.

This page gives the owner a choice among the six remaining groups in the
[unselected skill expansion](aegis-backlog-forecast.md#start-here--current-reading).
It records provisional dispositions, a four-item recommendation, and three
alternatives. The owner's request to plan and store this proposal is preserved
in the [unmerged, commit-pinned owner messages](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/owner-messages.md#L173-L199).
The open-decisions index does not yet link to this page; discoverability can
be addressed separately if the owner wants an index change.

The [preserved draft](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/PROPOSAL-DRAFT.md)
and [six research reports](#research-provenance-and-limits) are historical,
unmerged planning inputs. The recommendations below use independently checked
text at the source commit where cited. A research conclusion without such
support is identified as unverified and is not a ranking premise.

It follows the four earlier batch proposals: the
[quality assurance Tier 1](qa-tier1-skill-batch-proposal.md),
[AI-assisted development lifecycle](ai-sdlc-skill-batch-proposal.md),
[Phase 7 AI engineering](phase7-ai-engineering-skill-batch-proposal.md) and
[Phase 6 reliability](phase6-reliability-skill-batch-proposal.md) pages. Like
them, it records scope, boundaries and estimates, and builds nothing.

## Terms used on this page

- A **skill** is a folder under `.claude/skills/` whose `SKILL.md` tells an
  artificial intelligence (AI) assistant how to do one job. Its **description** is the text the
  assistant reads when choosing a skill; the library caps it at 1,024
  characters.
- A **manual-only** skill carries `disable-model-invocation: true`, so a person
  must name it. The [skill generation standard, section 5](../skill-generation-standard.md#5-least-privilege--side-effects)
  applies that posture to write, network, deploy and spending actions, subject
  to its stated bounded documentary-write and other exceptions. A proposed
  supplied-input review or design skill may remain **auto-invocable**; a later
  build must assess its exact permissions and workflow.
- **BUILD**, **EXTEND**, **DROP** and **DEFER** are proposed dispositions, not
  selected or delivered states. An extension adds a bounded piece of work to
  an existing skill. A drop proposes no build after an ownership check; it
  does not change the authoritative backlog.
- A **candidate group** is one row of the forecast's unselected-expansion
  table. This page calls the six remaining rows G1 to G6 (listed under
  [Disposition of every candidate](#disposition-of-every-candidate)).
- **P0**, **P1** and **P2** are the planning tiers of the
  [skills roadmap](../skills/03-saas-security-rls.md) (foundation, high-value
  follow-on, later expansion). Its legend says "A priority does not state
  whether a row shipped"; a tier is not evidence that anyone needs the skill.
- A **D-number** (for example D8, D10 or D30) is an entry in the
  [recorded decisions](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions)
  of the reconciliation log.
- **SaaS** is software as a service. **API** is an application programming
  interface. **QA** is quality assurance; **E2E** (end-to-end) tests drive the
  whole product like a user; **UI** is the user interface. **RLS** (row-level
  security) is database rules that limit which rows each tenant (customer
  account) can read or write. **SQL** is the database query language;
  **SQLi** is SQL injection; **DDL** (data definition language) is the SQL
  that changes tables and policies. **CSRF** (cross-site request forgery) tricks a
  signed-in browser into sending a request; **XSS** (cross-site scripting)
  runs an attacker's script in a page; **CORS** (cross-origin resource
  sharing), **CSP** (Content Security Policy) and **HSTS** (HTTP Strict
  Transport Security) are browser rules set by the server's response headers. **OWASP** is the Open Worldwide Application
  Security Project, whose Top 10 lists common web risks; **A02** is its
  security-misconfiguration category.
- **Behavior evals** (`evals/evals.json`) describe prompts and the behavior a
  skill should show. **Trigger evals** (`evals/trigger-evals.json`) check that
  the right skill, and not a neighbor, is chosen for a prompt.
- **ROUTE-002** is a census finding from `scripts/audit-skill-contracts.py`:
  skill A's description says "Do NOT use for X (skill B)", but skill B's
  description never names A. It is information, not a failure.
- **Active hours** count hands-on work; **wall time** includes review, CI and
  owner waits. Figures below are unverified inherited agent estimates. The
  [execution metrics](aegis-execution-metrics.md) do not provide active-time
  splits sufficient to calibrate them; a start and finish timestamp alone
  measure wall time.
- The **seven-stage workflow** is the
  [delivery workflow](../delivery-workflow.md) every pull request (PR) now
  follows: plan, independent plan audit, implement, independent implementation
  audit, validate, final independent review, merge, each stage held by a
  different agent. It was adopted as D72 on 2026-10-03, after the four earlier
  batches were built.

## Decision in one read

The six forecast groups mix named candidates, broad topics and roadmap rows;
they are not interchangeable units or a count of future pull requests. The
tables below preserve all named candidates and the 19 untiered category-06
rows. #127 appears in two groups but has one provisional disposition, and
#235 is both an untiered row and `qa-closeout-reporter`. The strongest
current-main evidence concerns textual coverage and handoff mismatches.
No live routing, effectiveness or demand comparison was run.

**Recommended for the owner's consideration: four boundary items.** The
source names a storage-policy audit handoff, D30 prioritizes idempotency,
the historical VolunteerFlow report exposes a spec-time omission, and D8
records security-header and CORS residue. These support a provisional set,
not a finding that this set has the greatest user demand or measured value.

| Item (roadmap rows) | Recommendation | Manual-only? | Active hours (provisional) |
| --- | --- | --- | ---: |
| 1. `rls-policy-auditor`: storage policies (#115), with dynamic SQL (#112) conditional | **EXTEND** to make the storage handoff explicit | proposed auto-invocable review | 1–2 |
| 2. `command-gateway-architect`: the rest of idempotency-first design (#17, #144; D30's top pull-forward) | **EXTEND** | not applicable (stays auto-invocable) | 1–2 |
| 3. `product-spec-writer`: repeated-request behavior in every spec (#17's spec half; acceptance-test findings AEGIS-013 and AEGIS-028) | **EXTEND** | not applicable (stays auto-invocable) | 0.75–1.5 |
| 4. `browser-boundary-reviewer` (#110, #111; adjacent #120) | **BUILD**, subject to one-job review | proposed supplied-input review | 3–5 |
| Batch overhead (registration, decision row, reciprocity edits, census, reviews) | — | — | 1.5–2.5 |
| **Illustrative base sum** | **1 new skill, 3 extensions** | | **7.25–13** |

The base sum is `1–2 + 1–2 + 0.75–1.5 + 3–5 + 1.5–2.5` active hours.
It is inherited planning arithmetic, not a measured delivery promise. If a
later owner choice adds one new skill and no others, the entrypoint count
would change from 195 to 196; no skill is added by this page. The forecast
uses broader candidate-group averages and is not directly comparable.

**Alternatives,** each detailed under [Alternatives](#alternatives):

| Alternative | Items | Illustrative active-hour range | Main tradeoff |
| --- | --- | ---: | --- |
| Smaller | items 1–3 | 3.75–7.5 | Defers D8's header/CORS residue |
| Larger | items 1–4, authentication/session review, and tentative #127 and #59 extensions | 12.25–22 | Broader overlap and unmeasured review cost |
| QA emphasis | item 1, visual, exploratory and mobile QA design, plus #213 | 11.25–19.5, or 20 with the separate 0–0.5 record allowance | Prioritizes the independently observed visual handoff |

**Other findings recorded here:** a visual-tooling handoff with no
subject-specific text in its named destination; #127 listed twice; partial
coverage of #189; and scope omitted from the group list. See
[Known source mismatches and historical findings](#known-source-mismatches-and-historical-findings) and
[Findings about the forecast](#findings-about-the-forecast).

## How the candidates were checked

- **Base.** The primary file and search observations identified below are
  pinned to `5228977920ee479e1fe1ec6b8d56f8fc24c14947`. The unmerged
  reports are provenance, not current repository authority.
- **Overlap test.** The yardstick is
  [`skill-quality-reviewer`](../../.claude/skills/skill-quality-reviewer/SKILL.md)'s
  check 2 (would the new skill fire on a shipped skill's core case?), check 3
  (extension when the new work is a bounded slice that keeps the base skill's
  verdict shape; a new skill when the trigger or the output differs in kind),
  check 6 (one job) and check 7 (invocation posture). Each candidate still
  needs a real skill-quality review when it is built.
- **Ranking method.**
  [`prioritization-frame-picker`](../../.claude/skills/prioritization-frame-picker/SKILL.md):
  a coarse value-versus-effort cut in ranges, each input marked as evidence or
  guess, and a protected lane for must-do security and correctness items so a
  low score cannot bury them.
- **Demand.** The historical research found no comparative usage or demand
  dataset. No current GitHub issue census or consumer-use measurement was
  made for this page. Missing demand evidence does not imply no need.
- **Estimates.** Per-item ranges and overhead were inherited from the
  [unmerged mechanics report](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-MECH-DEMAND.md#L111-L153).
  Its suggested extra 1–2 hours per pull request uses documentation-PR wall
  time as a proxy and may overlap review overhead. It is not added to any
  delivery promise or used to rank the options.

**Selection rationale.** The source explicitly routes storage audits to item
1's owner, D30 prioritizes the named idempotency candidate, the historical
VolunteerFlow report records the item 3 symptom, and D8 records header/CORS
residue relevant to part of item 4. The private audit behind D30, actual
consumer demand and comparative behavior remain unverified. The set's
strongest objection is under
[Scrutiny of the recommendation](#scrutiny-of-the-recommendation).

## Item 1: `rls-policy-auditor` extension for storage policies (#115; #112 conditional)

**Roadmap text.** #115 Storage Access Policy Review (P0): "Validate bucket
policies, signed URL expiry, path naming, ownership checks, and public asset
boundaries." #112 SQL Injection Defense Review (P0): "Check dynamic SQL,
filters, RPCs, search, sorting, and migration scripts for injection risks."
(RPCs are remote procedure calls.) Both are in
[category 03](../skills/03-saas-security-rls.md).

**The textual handoff mismatch.**
[`file-upload-storage-architect`](../../.claude/skills/file-upload-storage-architect/SKILL.md)
designs storage and hands the audit of existing policies away. Its
description says "Do NOT use … for auditing existing storage RLS/bucket
policies (rls-policy-auditor)", its body repeats the hand-off at lines 52,
113, 150 and 190, and its pinned trigger-eval case
`existing-policy-audit-goes-to-rls-policy-auditor`
(`evals/trigger-evals.json:26-30`) expects `rls-policy-auditor` to win "We
already have storage bucket policies and row-level rules for our object
metadata. Audit them for holes". But
[`rls-policy-auditor`](../../.claude/skills/rls-policy-auditor/SKILL.md) has
no subject-specific storage guidance in a scoped source search:
`git grep -niE 'storage|bucket' 52289779 -- .claude/skills/rls-policy-auditor`
finds only an unrelated whole-app trigger prompt at line 41. This is a
textual mismatch, not a proven routing or behavioral failure. The handoff
appears on the main path:
`project-orchestrator`'s Stage 4, "Make it safe", names
`file-upload-storage-architect` (`SKILL.md:242-245`).

**What shipped skills already do.**

- `rls-policy-auditor` audits PostgreSQL row-level security per table and per
  command (SELECT, INSERT, UPDATE, DELETE), `SECURITY DEFINER` helpers,
  grants and service-role leakage, and always writes a negative-test plan. Its
  per-table method may cover the prompt's "row-level rules for our object
  metadata" half, but does not name bucket policies, path prefixes,
  public buckets or signed URLs. How each hosting platform stores
  object-access rules is a verification item for the build, not a basis for
  this proposal.
- [`tenant-isolation-reviewer`](../../.claude/skills/tenant-isolation-reviewer/SKILL.md)
  has one storage row in its whole-application checklist: "Per-tenant
  prefixes/buckets; signed URLs scoped and expiring"
  (`references/isolation-surface-checklist.md:18`). It does not audit
  individual policies or write per-command negative tests.
- [`cloud-security-baseline-reviewer`](../../.claude/skills/cloud-security-baseline-reviewer/SKILL.md)
  checks account-level bucket exposure, for example "No public bucket unless
  intended" (`references/aws-baseline.md:35`).
- Dynamic SQL inside database functions is an adjacent #112 slice. Its
  platform-specific behavior and fit in the policy-audit job require a later
  scoped check. Injection in application code remains a diff-review concern
  for `security-pr-reviewer`.

**The proposed gap.** A policy-level audit of storage access: which storage tables or
buckets hold tenant files, whether every policy ties the bucket and path
prefix to the caller's tenant, public buckets and public URLs, who mints
signed URLs and with which role, service-role use in upload handlers, and
per-command negative tests for objects. Reviewing run-time-built SQL in
callable functions is conditional on a later one-job check.

**Recommendation: EXTEND, provisionally.** Storage policy review may fit the
base skill's findings and negative-test shape, and the current handoff names
it. The strongest objection is that generic per-table guidance may already
handle the actual storage platform adequately. Evidence of that behavior
would reduce this to wording or routing clarification; a different verdict
shape would favor a separate skill. Neither has been tested here.

- **Alternative:** repoint the handoff to `tenant-isolation-reviewer` if
  later behavior evidence supports its whole-app storage checklist as the
  right audit home. It has one storage row today, so the policy-level #115
  request remains a concern.
- **Fallback:** if the build-time check 6 finds that run-time SQL makes the
  skill do two jobs, ship storage only (0.75–1.5 hours) and keep #112's
  residue deferred.
- **Posture and routing:** propose supplied-input review and design only,
  with no live database command. A later build must check its actual
  side-effect posture, final description, neighboring triggers and ROUTE-002
  census. No final description or census result exists yet.
- **Evals:** behavior cases for a prefix policy that ignores the tenant, a
  public bucket holding uploads, and run-time SQL in a `SECURITY DEFINER`
  function; trigger cases against `cloud-security-baseline-reviewer` (account
  posture) and `tenant-isolation-reviewer` (whole-app review). The existing
  `file-upload-storage-architect` case must stay true.
- **Future build boundary:** derive its security-surface answer from its
  actual diff under [CONTRIBUTING](../../CONTRIBUTING.md#external-contributions).
- **Estimate:** 1–2 active hours, the precedent range for an extension that
  adds one surface.

## Item 2: `command-gateway-architect` idempotency extension (#17, #144)

**Roadmap text.** #17 Idempotency-First Design (P0): "Prevent duplicate side
effects from retries, double-clicks, webhook replays, and automation reruns."
#144 Idempotency Key Middleware (P0): "Support safe retries with request
keys, payload hashes, actor scope, and terminal response replay."
([category 01](../skills/01-software-architecture-engineering.md),
[category 04](../skills/04-backend-api-data-engineering.md)).

**Recorded priority.** D30 (2026-07-08) named `idempotency-first-designer` the
"TOP pull-forward … table-stakes for any mutating API"
(`step-0-reconciliation-v4.md:745-753`). Of D30's three pull-forwards, the
resilience reviewer shipped in D71 and this one remains. The audit behind D30
is private and cannot be inspected; its recorded conclusion can.

**What shipped skills already do.** D31 then built
[`command-gateway-architect`](../../.claude/skills/command-gateway-architect/SKILL.md),
which now owns the core and the trigger: "Use when: retries or double-submits
cause duplicate side effects and the write path has no idempotency contract"
(`SKILL.md:40-41`), and step 4, "Design idempotency concretely": key source,
dedup store and retention, "what 'same request' means", the replayed-key
response, and idempotency versus concurrency control (`:104-108`). Its output
carries `Idempotency: <key source, dedup store, replay response, concurrency
control>` (`:136`). Retried public-API requests belong to
[`api-event-architect`](../../.claude/skills/api-event-architect/SKILL.md);
job reruns, event consumers and offline sync have their own owners.

**The textual residue.** A scoped search for `fingerprint`, `different
payload`, `payload hash`, `in-flight` and `in progress` finds no match in the
gateway skill at the source commit. The gateway **already asks what “same
request” means** (`SKILL.md:104-108`). It does not state the outcome when a
reused key carries a different payload or arrives while the first request is
running. Provider-side effects and a one-endpoint product are later design
questions, not a basis for claiming the current skill fails.

**Recommendation: EXTEND, provisionally.** A standalone
`idempotency-first-designer` would overlap the gateway's own “Use when” at
lines 40–41. The strongest objection is a product with one endpoint and no
command bus. Evidence that the gateway cannot express that small case
without forcing unrelated architecture would favor a narrower new skill and
explicit trigger separation.

- **Posture:** propose design output over supplied inputs; a later build
  assesses the actual side-effect rule.
- **Evals:** cases for a key reused with a different payload and for an
  in-flight duplicate; trigger cases against
  `background-job-orchestration-architect`, `streaming-event-architect` and
  `api-event-architect`.
- **Description and routing:** final text and ROUTE-002 effects require a
  later build and census. The preserved G3 report already recognized the
  “same request” line, so this page claims no new correction to that report.
- **Estimate:** 1–2 active hours (precedent extension range).

## Item 3: `product-spec-writer` repeated-request extension (#17, spec half)

**Why it is here.** A historical acceptance test recorded a symptom. The
[VolunteerFlow acceptance test](../audits/volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md)
recorded AEGIS-013, "Product specification omitted repeated-request and
idempotency behavior" (P1; first observed in `product-spec-writer`; "Required
improvement: Add repeated-request behavior to every state transition"), and
AEGIS-028, "Idempotency was applied only to claim rather than the full state
model". Both are marked "Symptom corrected during test", but the same report's
authority rule says "A same-session correction to VolunteerFlow does not
resolve a Project Aegis repository defect."

**What shipped skills already do.**
[`product-spec-writer`](../../.claude/skills/product-spec-writer/SKILL.md) has
no repeated-request lens: a search for idempotency, retry, duplicate, repeat,
replay, double-click and resubmit finds only unrelated hits (a duplicate name
in an example, and a gotcha about duplicated error copy), and it has no
state-transition or stale-request wording.
[`acceptance-criteria-reviewer`](../../.claude/skills/acceptance-criteria-reviewer/SKILL.md),
built later, asks about "a duplicate submission" among its negative cases
(`references/criteria-review-sheet.md:51`); that is one case, at review time,
after the spec exists.

**The textual gap and recommendation: EXTEND.** Every state-changing action in a
spec states its observable outcome on a retry, a double submit, a second tab
and a stale request, and whether duplicate events are possible. The mechanism
stays with item 2 and `tech-spec-writer`; the spec states only the outcome.
This is a proposed bounded slice of AEGIS-013 and AEGIS-028, not the full
state-transition matrix that AEGIS-014 proposes. The report labels the
symptom corrected during its test; root cause remains unverified. Its own
resolution rule requires a source fix and fresh-session regression.

- **Scope note:** `product-spec-writer` is not a named expansion candidate.
  The item is a spec-time adjunct to candidate #17. The owner must
  explicitly include it in any later build choice.
- **Not covered:** the handoff report also asks for a fresh-session
  regression run proving the behavior; this extension adds eval cases only.
- **Counterargument:** a generic later review may catch duplicate requests,
  and mandatory spec detail could add friction. Fresh-session regression or
  an owner choice to keep the batch strictly to named candidates would narrow
  or remove this adjunct. Final description and census effects are unmeasured.
- **Estimate:** 0.75–1.5 active hours, the range of the earlier
  negative-path extension of `test-plan-designer`.

## Item 4: `browser-boundary-reviewer` (#110, #111, #120)

**Roadmap text** ([category 03](../skills/03-saas-security-rls.md)): #110
CSRF and Browser Boundary Review (P1), "Assess browser-side mutation paths,
cookies, headers, origins, and cross-site risks"; #111 XSS Defense Review
(P0), "Review rendering, markdown, rich text, user content, third-party
widgets, and escaping boundaries"; #120 Security Header Review (P1), "Review
CSP, HSTS, frame, referrer, permissions, and content type headers for browser
apps". #120 is not in the catalog's remaining Phase 4 list; it is added
because D8 records its subject as open.

**Recorded gap.** D8's OWASP audit states: "A02 residue: application/platform
configuration — security headers, CORS, XML-parser hardening (XXE-class),
default accounts, cloud posture — has no Phase 4 owner … the app-config slice
remains open residue" (`step-0-reconciliation-v4.md:174-178`). XXE is XML
external entity injection; this page does not take up that part.

**What shipped skills already do.**
[`security-pr-reviewer`](../../.claude/skills/security-pr-reviewer/SKILL.md)
reviews "an ACTUAL diff" for injection and "broadened CORS";
[`appsec-implementer`](../../.claude/skills/appsec-implementer/SKILL.md)
(manual-only) implements output encoding; `static-analysis-reviewer` triages
scanner findings;
[`llm-output-safety-reviewer`](../../.claude/skills/llm-output-safety-reviewer/SKILL.md)
covers model output only; the manual-only `secrets-identity-hardener` notes,
in a gotcha and a reference line, that cookie changes alter CSRF posture.
Searches of all shipped skills: no description mentions CSRF; no file
mentions HSTS, `X-Frame`, `frame-ancestors`, `Referrer-Policy` or "security
header".

**The proposed gap.** A review of an existing web app's browser trust
boundary, with no diff in hand: CSRF on cookie-authenticated mutations, XSS
sinks, CSP and other security headers, CORS with credentials, framing and
cookie scope, producing findings and one header and CSRF policy.

**Recommendation: BUILD, provisionally.** D8 directly supports header and
CORS residue; CSRF and XSS are adjacent roadmap topics, not proved by D8 to
have the highest consumer demand. The strongest objection is that four
topics may make an oversized reviewer while existing diff and authentication
skills already catch some cases. A one-job and trigger review, or measured
consumer demand, could narrow this to headers/CORS or reorder the batch.

- **One job, not four:** the output is one boundary review (per-surface
  findings plus one policy). If the build-time check 6 calls it a catch-all,
  the fallback is to drop the XSS sinks, which the diff review already
  covers, and keep CSRF, headers and CORS.
- **Not input validation:** validating input is not an XSS or CSRF defense;
  where validation should live is a separate, deferred candidate
  (`validation-boundary-designer`).
- **Posture:** propose reading supplied code, configuration and captured
  headers, with no live fetch; testing a running app belongs
  to [`dast-safety-harness-designer`](../../.claude/skills/dast-safety-harness-designer/SKILL.md).
- **Name:** avoid `browser-security-reviewer`, which contains the reserved
  bundled name `security-review` (`scripts/validate-skills.py:147-163`).
- **Description:** the historical draft is a starting idea. A later build
  must check its final length, trigger and neighbor distinctions.
- **Trigger evals pin against** the same five; a case that expects the
  manual-only `appsec-implementer` must start `Explicitly invoke
  appsec-implementer. ` (standard section 6).
- **ROUTE-002:** predicted one-way findings remain unverified until the
  final wording and census are checked. No baseline changes now.
- **Wiring:** `project-orchestrator`'s Stage 4 names no browser-boundary
  reviewer today; a route would be a separate, unestimated pull request, as
  #384 was for the feature-flag skill.
- **Future build boundary:** any security-surface answer follows that
  build's actual diff.
- **Estimate:** 3–5 active hours, the range of the earlier new review skills
  with five or more neighbors.

## Alternatives

Every alternative includes item 1 because the current source has an explicit
storage-audit handoff without matching subject-specific audit guidance. That
is a proposal choice, subject to later behavior evidence.

### Smaller: correctness only

Items 1, 2 and 3: three proposed extensions and no new skill. Their inherited
base arithmetic is `1–2 + 1–2 + 0.75–1.5 + 1–2 overhead = 3.75–7.5`
active hours. This has the smallest scope, but leaves D8's header/CORS
residue for later. Evidence of demand for a browser review, or an extension
that fails the one-job test, would change the choice.

### Larger: full request boundary

The recommended set plus three proposed items; its inherited base range is
12.25–22 active hours with 2–3.5 of overhead. Its benefit is fuller request
boundary coverage. Its strongest cost is more overlap and review work that
has not been measured:

- **`authentication-session-reviewer`** (#108, #109, both P0; 3–5 hours):
  an auto-invocable review of existing sign-in, sign-out, password reset,
  multi-factor and single sign-on flows, sessions and refresh tokens, without
  a diff. The [historical G5 research](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G5.md#L79-L117)
  reports limited password-reset and step-up coverage, but those negative
  searches have not been independently rerun for this page. The benefit and
  shape are therefore unverified, and this item does not justify the
  recommended set. Confirmed existing ownership could remove it.
- **`change-classification-gate` extension for security impact notes**
  (#127, P0; 0.75–1.5 hours): consider a written impact note. The
  [classification matrix](../../.claude/skills/change-classification-gate/references/classification-matrix.md)
  already has written-note floors for migrations and infrastructure, while
  `threat-modeler` excludes implemented diff review. The gate runs before
  work, however; a change-time note might belong elsewhere. This is a
  tentative home, not a new validation floor.
- **`authorization-matrix-designer` extension** (#59, P0; 0.75–1.5 hours):
  role-assignment rules with a grant ceiling (no one grants a role above
  their own), role and resource inheritance, and tenant-defined custom roles.
  The [catalog](../skills-catalog.md) already attributes #59 to this skill;
  its current inheritance references concern machine actors. The proposed
  role ceiling and custom-role extension needs an owner and one-job check.

### Different emphasis: QA Tier 2

Item 1 plus the quality assurance Tier 2 core. The listed inherited items
sum to **11.25–19.5 active hours** including 1.5–3 overhead:
`1–2 + 3.25–5 + 2–3.5 + 2.5–4 + 1–2 + 1.5–3`.
The earlier draft's 20-hour upper end additionally allowed 0–0.5 hours for
records; that separate allowance is unverified and no records change here.
This option addresses the visual handoff earlier; source-text gaps do not
prove a failed visual test or owner demand. An actual routing/behavior check
or product-specific QA demand could move it ahead of the recommended set.

- **`visual-regression-test-designer`** (#203, promoted by D10; 3.25–5
  hours), with a proposed positive snapshot-selection rule for #202 and the
  deterministic state-rendering residue of #189. Neither slice is shipped
  coverage today. This would address the second textual handoff mismatch.
- **`exploratory-charter-designer`** (#228, renamed; 2–3.5 hours).
- **`mobile-journey-test-designer`** (#230, renamed because
  `mobile-viewport-qa` is one word from the shipped `mobile-viewport-craft`;
  2.5–4 hours).
- **`qa-automation-architect` extension** for per-layer timeout policy (#213;
  1–2 hours).

The narrowed `role-coverage-test-designer` (#229) could follow the
`authorization-matrix-designer` extension. A separate tenant-lifecycle
batch is also plausible, but its comparative demand and cost remain
unverified. No option is selected by this page.

## Overlaps between groups

These are the places where two groups claim the same ground. Each resolution
applies whenever the items are built, in this batch or later.

| Overlap | Resolution |
| --- | --- |
| Role coverage testing (G1 #229) and authorization design (G4 #59) both touch `authorization-matrix-designer` | If both are chosen, design the #59 matrix first, then let role-coverage tests use it as an oracle. This is a proposed dependency, not an authorized sequence. |
| Validation placement (G3 #37) against the browser boundary (G5 #110/#111) and SQL injection (G5 #112) | Proposed seams: layer placement stays deferred; browser boundary review is item 4; database-function dynamic SQL is only a conditional item 1 slice; application-code SQL injection remains with `security-pr-reviewer` for diffs. Input validation alone is not an XSS defense. |
| Idempotency (G3 #17/#144), inbound webhooks (G5 #116), the VolunteerFlow findings and tenant provisioning (G4 #57) | Write-path design is item 2; spec-time outcomes are item 3; receiving third-party webhooks (signatures, replay window, event-id dedup, tenant mapping) is the deferred `inbound-webhook-security-designer`, which should consume item 2's dedup contract; a provisioning designer would compose that contract rather than restate it; public-API retry windows stay with `api-event-architect`. |
| Shared file `command-gateway-architect` (item 2; possible later `validation-boundary-designer` reciprocity edit) | A later build must re-read the then-current description and check its limits; this proposal reserves no description space. |
| Shared file `rls-policy-auditor` (G5 storage and SQL; a minor G6 note that backup-gated validation does not name storage-policy changes) | One lane: item 1. |
| Logging redaction (G3 #22 observability-by-design and G5 #124) | Both deferred. Proposed seam: the "never log this" catalog and the leak review go to `log-redaction-reviewer`; the telemetry contract in `observability-by-design` consumes it; the manual-only `observability-operator` implements it. Build them together, or the reviewer first. |
| Security impact notes (#127, listed in both G4 and G5) | One tentative disposition under G5: consider `change-classification-gate`, with the before-work timing as a serious objection. G4's `threat-modeler` suggestion remains a live alternative, although its current description excludes implemented diff review (`SKILL.md:37-38`). |
| Rate limits (G5 #117), brute force in authentication review, and invitation spam (G4 #58) | Deferred. D30's wording, "general per-tenant/plan API rate limits + noisy-neighbor defense", is already met by `api-event-architect` step 4 (`SKILL.md:95-98`), present since 2026-07-06, two days before D30. The residual is limits by abuse category, which a later `rate-limit-architect` would own; an authentication reviewer checks that flows are throttled, and an invitation designer consumes the limits. |
| Quality assurance shared files (`qa-automation-architect`, `test-coverage-mapper`, `test-plan-designer`) and a defect-report skill (G6 #224/#225) against exploratory charters (G1 #228) | Plan all quality assurance items in one lane. The #213 and #202 rows go to the G1 plan, not G6. An exploratory debrief hands defects to the defect-report skill if both are built. |

## Disposition of every candidate

These are proposal dispositions only. **Rec.** marks the recommended set;
S, L and Q mark the smaller, larger and QA alternatives. Hour ranges are
unverified historical research estimates, excluded from ranking. Each group
links its defining source. A row with a named current owner is still subject
to later behavior and trigger review; “DROP” here does not close backlog.

### G1 — QA expansion Tier 2 (forecast 12–24 hours)

Source: [D10 Tier 2](../reconciliation/step-0-reconciliation-v4.md#phase-5-qa-expansion-backlog--prioritized-d10),
[category 06](../skills/06-qa-test-engineering.md), and
[unmerged G1 research](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G1.md).

| Candidate (rows, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `visual-regression-test-designer` (#203 P2; adjacent #179, #202 and part of #189) | BUILD | Q | 3.25–5 | `screenshot-evidence-planner` points visual tooling at `qa-automation-architect`; a scoped search of that directory for visual/pixel/snapshot terms found no matching guidance. This is a textual mismatch, not a failed route. #202's positive snapshot-selection rule and #189's state-rendering residue are still unbuilt. |
| `exploratory-testing-charter` (#228 P1), as `exploratory-charter-designer` | BUILD | Q | 2–3.5 | `qa-strategy-architect:142-144` says strategies that omit manual testing "leave visual, UX, and exploratory risks unowned"; no shipped skill writes charters. |
| `mobile-viewport-qa` (#230 P1), as `mobile-journey-test-designer` | BUILD | Q | 2.5–4 | Layout is `mobile-viewport-craft`'s; journey checks on phones are not ("Deep responsive QA is its own effort", `clickthrough-test-engineer/references/clickthrough-route-catalog.md:31`). |
| `role-based-qa-matrix` (#229 P1), narrowed as `role-coverage-test-designer` | DEFER | — | 2.5–4 | Denials are owned by `authorization-matrix-designer` step 7 and `multi-tenant-security-tester`; allowed paths and interface consistency are not. Build after the #59 extension. |
| `mock-strategy-designer` (#200, #201 P1) | DROP, tentative | — | 0–0.25 | Existing owners include `integration-test-designer`, `vitest-unit-component-engineer` and `api-contract-test-designer`; the historical coverage judgment needs fresh full-body review before a record is closed. |
| `ci-shard-parallel-isolation` (#211, #212 P1) | DROP, tentative | — | 0–0.25 | `sharded-validation-with-resume` and `qa-automation-architect` name isolation; exact combined ownership needs fresh full-body review. |
| #213 test timeout policy (P1; handed over from G6) | EXTEND `qa-automation-architect`, proposed | Q | 1–2 | Scoped source search found no timeout guidance in its skill or blueprint; `ci-failure-classifier` handles failures after the fact. |

### G2 — QA expansion Tier 3 (forecast 8–16 hours; D10: "build on demand only")

Source: [D10 Tier 3](../reconciliation/step-0-reconciliation-v4.md#phase-5-qa-expansion-backlog--prioritized-d10),
[category 06](../skills/06-qa-test-engineering.md), and
[unmerged G2/G6 research](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G2G6.md).

| Candidate (row, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `property-based-test-designer` (#194 P2) | DEFER (on demand) | — | 2.5–4 | Historical research found only a passing debugging mention. Current demand is unmeasured; D10's specialized/on-demand qualification applies. |
| `mutation-testing-reviewer` (#195 P2) | DEFER as an EXTEND of `test-coverage-mapper` | — | 0.75–1.5 | `test-coverage-mapper` already asks "what real bug would make this test fail?"; reading mutation-tool reports is the residual. |
| `soak-test-planner` (#207 P2) | DROP | records | 0–0.25 | `load-test-planner` plans soak tests and two pinned trigger evals route soak prompts to it. Optional 0.25–0.5-hour note on token and session expiry during long runs. |
| `chaos-test-planner` (#208 P2) | DROP | records | 0–0.25 | `resilience-architecture-reviewer` writes "a fault-injection or game-day plan" and runs none. |

### G3 — Phase 2 expansion (forecast 18–36 hours)

Source: [Phase 2 catalog](../skills-catalog.md#phase-2--core-architecture--engineering-p0),
[roadmap categories 01](../skills/01-software-architecture-engineering.md)
and [04](../skills/04-backend-api-data-engineering.md), and
[unmerged G3 research](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G3.md).

| Candidate (rows, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `idempotency-first-designer` (#17, #144 P0) | EXTEND `command-gateway-architect` (item 2) and `product-spec-writer` (item 3) | Rec., S, L | 1–2 and 0.75–1.5 | Item 2 and item 3 above. |
| `validation-boundary-designer` (#37, #38, #141, #157 P0) | DEFER (possible BUILD) | — | 3–5 | Design-time placement is a research hypothesis. A blanket claim that mass-assignment policy is absent would be false: `security-pr-reviewer`, `threat-modeler`'s catalog and `multi-tenant-security-tester` name it. |
| `observability-by-design` (#22 P0) | DEFER (possible BUILD with log redaction) | — | 3–5 | Historical G3 research reports no auto-invocable telemetry-contract designer; `observability-operator` is manual-only. Current comparative demand and trigger fit need review. |
| `api-contract-designer` (#9 P0) | DEFER as an EXTEND of `api-event-architect` | — | 1–2 | Per-operation schema rules are absent; whether first-party APIs fit that skill's "external contracts" scope is unverified. |
| `refactor-safety-planner` (#11 P0) | DEFER | — | 3–4.5 | The catalog calls `code-simplifier` only "adjacent"; decide together with the unlisted `code-quality-auditor`. |
| `dependency-direction-guard` (#6, #7 P0) | DEFER | — | 2.5–4.5 | `architecture-designer`, `code-reviewer` and an agent definition catch common cases; the residual is a CI ratchet. Decide with `code-quality-auditor`. |
| `operational-runbook-author` (#23 P1) | DROP | records | 0–0.25 | Covered by `incident-response-runbook`, `rollback-runbook-author`, `data-migration-runbook-author`, `gated-deployment-prompt-template` and `onboarding-doc-designer`. |
| `system-context-mapper` (#2 P0) | DROP | records | 0–0.25 | `architecture-designer` step 1 and `threat-modeler`'s system map. |
| `bounded-context-identifier` (#4 P0) | DROP | records | 0–0.25 | `domain-modeler` step 4, "Draw bounded contexts". |

### G4 — Phase 3 expansion (forecast 8–16 hours)

Source: [Phase 3 catalog](../skills-catalog.md#phase-3--saas--tenant-isolation-p0p1),
[category 02](../skills/02-saas-platform-architecture.md), and
[unmerged G4 research](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G4.md).

| Candidate (row, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `role-permission-architect` (#59 P0) | EXTEND `authorization-matrix-designer` | L | 0.75–1.5 | The catalog attributes #59 to that skill; "assignment" and "inheritance" are absent except for machine actors. |
| `tenant-provisioning-designer` (#57 P0) | DEFER (BUILD in a tenant-lifecycle batch) | — | 3–4.5 | `tenant-modeler` gives lifecycle semantics only ("semantics only", `SKILL.md:139`); nothing designs the creation workflow, first owner or seed data. |
| `membership-invitation-designer` (#58 P0) | DEFER (BUILD narrowed, after #59) | — | 2.5–4 | `tenant-modeler` models invitation states; single-use tokens, identity binding at acceptance, seat checks and invite-spam limits are unowned. |
| `security-impact-note-author` (#127 P0) | Cross-reference only; one tentative disposition under G5 | — | — | Both [catalog lists](../skills-catalog.md) include it. G4 research suggests `threat-modeler`; G5 suggests `change-classification-gate`. See the G5 row and the timing objection above. |

### G5 — Phase 4 security topics (forecast 20–40 hours for about ten topics)

Source: [Phase 4 catalog](../skills-catalog.md#phase-4--security-rls--supply-chain-p0p1),
[category 03](../skills/03-saas-security-rls.md), and
[unmerged G5 research](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G5.md).

| Topic (rows, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| Storage-policy review (#115 P0), with conditional dynamic SQL (#112 P0) | EXTEND `rls-policy-auditor` (item 1) | Rec., S, L, Q | 1–2 | Item 1 above; storage-only remains a fallback. |
| CSRF/XSS deep-dives (#110 P1, #111 P0), with adjacent security headers (#120 P1, unlisted) | BUILD `browser-boundary-reviewer` (item 4), tentative | Rec., L | 3–5 | Item 4 above; D8 directly supports headers/CORS only. |
| Authentication and session review (#108, #109 P0) | BUILD `authentication-session-reviewer` | L | 3–5 | See the larger alternative. |
| Security-impact-note authoring (#127 P0; same candidate as G4) | EXTEND `change-classification-gate`, tentative | L | 0.75–1.5 | Written-note precedent in its matrix supports consideration; before-work timing and G4's `threat-modeler` suggestion remain counterarguments. No new floor is imposed. |
| Rate-limit design (#117 P1) | DEFER | — | 3–5 | D30's framing is met by `api-event-architect`; abuse-category limits remain. |
| Logging redaction (#124 P0) | DEFER (with observability-by-design) | — | 2.5–4 | `security-logging-alerting-architect` says safe log content needs "their own audit-log design and operating controls" (`SKILL.md:17-18`). |
| Webhook security (#116 P1), inbound only | DEFER (after item 2) | — | 2.5–4 | Sending webhooks is `api-event-architect`'s; receiving them appears only as a threat-catalog question. An `api-event-architect` extension (1–2 hours) is the cheaper alternative. |
| Security-drift detection (#130 P0) | DEFER (on demand) | — | not estimated | Covered in pieces by six skills; the residual, a scheduled check of documented controls without a diff, is narrow. |
| Compliance-evidence mapping (#128 P1) | DROP | records | 0–0.25 | `compliance-evidence-collector` maps each control to its evidence. |
| Privacy-by-design (#129 P1) | DROP | records | 0–0.25 | `pii-lifecycle-designer` covers minimization, purpose, retention and deletion. |

### G6 — Phase 5 extras (forecast 2–8 hours)

Source: [forecast extras](aegis-backlog-forecast.md),
[D10 untiered rows](../reconciliation/step-0-reconciliation-v4.md#phase-5-qa-expansion-backlog--prioritized-d10),
[category 06](../skills/06-qa-test-engineering.md), and the
[unmerged G2/G6 research](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G2G6.md).

| Candidate (rows, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `e2e-test-architect` (historical roadmap P0) | DROP | records | 0–0.25 | Covered by composition of `qa-strategy-architect`, `test-plan-designer`, `qa-automation-architect`, `regression-suite-curator`, `test-data-architect` and `playwright-e2e-engineer`. |
| `qa-closeout-reporter` (#235 P0) | DROP | records | 0–0.25 | `ai-closeout-reporter` and `release-readiness-reviewer`; a shipped trigger eval already says this candidate "stays in the backlog" because of that overlap. |
| #224 bug report and #225 triage (P1) | DEFER (one new skill in the QA lane) | — | 3–4.5 | Only the manual-only `clickthrough-test-engineer` files defects, inside its own sessions. |
| #188 production-safe smoke testing (P0) | DEFER as an EXTEND of `synthetic-monitoring-architect` | — | 1–2 | That skill owns scheduled probes and their safety contract; no auto-invocable skill designs a one-off post-deploy smoke set. |
| #231 timezone and #232 notification QA (P1) | DEFER as an optional `test-plan-designer` reference | — | 1–1.5 | Per-feature test plans already route to `test-plan-designer`. |
| #202 snapshot governance (P2), #213 timeout policy (P1) | Moved to G1 | Q | — | See the G1 table. |
| #189 fixture-mode E2E (P1) | **PARTIAL/DEFER** | Q for proposed unbuilt residue | — | Journey fixture, component and data portions have existing owners; deterministic state rendering remains a proposed slice of the unbuilt visual skill. It is not fully covered and does not belong in a covered-row record now. |
| #191, #193, #199, #216, #217, #218, #219, #220, #233, #234 | DROP | records | 0.5–1 together | Each maps to a shipped owner: `test-coverage-mapper`, `test-plan-designer`, `test-data-architect`, `release-readiness-reviewer`, `local-ci-mirror-preflight`, `risk-tiered-validation-selector`, `data-migration-runbook-author`, `merge-is-deploy-governance` and `multi-tenant-security-tester`. |

For the untiered category-06 rows, the source set is **19 distinct roadmap
numbers**: #188, #189, #191, #193, #199, #202, #213, #216–#220,
#224–#225, and #231–#235. The preceding G1 and G6 tables account for each by number or a
contiguous range. #235 is also the named `qa-closeout-reporter` candidate;
it is one row. #127 is one topic despite two group listings. These are
roadmap-row counts, not counts of independent builds or all library gaps.

## Known source mismatches and historical findings

1. **Storage audit handoff lacks storage-specific destination text.** Described
   under item 1. A later extension, routing clarification or behavior result
   may resolve it. This page changes no skill.
2. **Visual tooling handoff lacks visual-specific destination text.**
   `screenshot-evidence-planner` says "Do NOT use when: the ask is
   visual-regression pixel-diff tooling — that is automation architecture
   (`qa-automation-architect`)" (`SKILL.md:33-35`), and
   a scoped search for `visual|pixel|screenshot baseline|snapshot` returned
   no match in `qa-automation-architect`'s directory. A proposed visual
   skill or a narrower existing-skill clarification could address it; no
   routing or effectiveness test was run.
3. **Catalog attributions that overstate coverage.** The catalog maps #59 to
   `authorization-matrix-designer` (see the G4 table), #189 to
   `playwright-e2e-engineer`, and #200 with #211/#212 to
   `qa-automation-architect`. The #189 state-rendering residue is not shipped
   coverage. These attribution judgments need a later owner and source
   review; this proposal edits neither catalog nor reconciliation log.
4. **AEGIS-013 and AEGIS-028 are historical symptoms, not resolved source
   findings.** The [VolunteerFlow handoff](../audits/volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md)
   says their symptoms were corrected during the test but requires a source
   fix and fresh-session regression for resolution. Item 3 proposes a
   response to the present textual omission; root cause remains unverified.

## Findings about the forecast

The [current dated reading](aegis-backlog-forecast.md#start-here--current-reading)
uses **68–140 agent-estimated active hours** after delivered groups were
removed. Its six remaining ranges re-add as
`12+8+18+8+20+2 = 68` and `24+16+36+16+40+8 = 140`.
The older [inventory table](aegis-backlog-forecast.md) still displays
**106–220** for a broader pre-delivery set. Neither figure measures actual
work, and this proposal does not update the forecast.

- **Duplicate:** [the catalog](../skills-catalog.md) lists #127 in Phase 3
  and Phase 4. The forecast has no per-item #127 price. Subtracting a group
  average of 2–4 hours and publishing 66–136 would invent a corrected total,
  so this page records the duplication without a replacement estimate.
- **Coverage:** several proposed DROP rows already have named owners, but
  exact remaining work and record cost need later verification. #189 has an
  unbuilt residue and must not enter a fully covered record.
- **Unpriced scope:** #120 security headers is adjacent to the catalog's
  named Phase 4 list. The [reconciliation log](../reconciliation/step-0-reconciliation-v4.md)
  also mentions an unlisted whole-codebase audit overlap. #105 sensitive
  column masking was not checked. No scope is silently added to the forecast.
- **Process cost:** the forecast predates the seven-stage workflow. The
  historical mechanics report's 1–2 hours per pull request uses wall time
  from a documentation change, may overlap batch overhead, and cannot be
  converted into an active-hour allowance for these options.

These findings are inputs for a later authorized forecast and decision review,
not a checkpoint performed by this page.

## Batch summary and later decisions

**Tentative set:** extend `rls-policy-auditor`, `command-gateway-architect`
and `product-spec-writer`; propose `browser-boundary-reviewer`. These are
four design items, not selected work. The base arithmetic is 7.25–13
estimated active hours including 1.5–2.5 overhead, all uncalibrated. A
seven-stage process allowance is unknown because its historical proxy uses
documentation pull-request wall time and may overlap the overhead. No
combined delivery estimate or new skill count is promised.

If the owner chooses a batch later, a separate decision-record change can
record the choice, scoped exclusions and any covered-row decisions. A
possible implementation decomposition would keep storage policy guidance,
idempotency/spec outcomes and browser review in separately reviewable seams.
Each later build must independently check the then-current source, skill
overlap and one-job fit, invocation posture, final description, neighbor
triggers and evaluations, registration surfaces, applicable validation, and
security-surface answer under [CONTRIBUTING](../../CONTRIBUTING.md#how-to-add-a-skill)
and the [delivery workflow](../delivery-workflow.md). This page creates none
of those artifacts or authorities.

At the pinned base, the [reconciliation log](../reconciliation/step-0-reconciliation-v4.md)
has D73. “D74” in historical research is only a provisional next number;
the decision number must be re-observed if and when the owner selects work.
Any ROUTE-002 census change is likewise a prediction until final skill
descriptions are written and measured. Start/finish timestamps on future
work will measure wall time only; active/review/CI/wait splits must be
recorded separately when available.

## Scrutiny of the recommendation

The set favors recorded textual gaps and priorities. Its strongest set-level
objection is that the proposed browser reviewer includes CSRF and XSS beyond
D8's explicit header/CORS residue, while the independently observed visual
tooling handoff remains for the QA alternative. Authentication review may
also be more valuable to some consumers; that comparative value and demand
have not been measured. The private audit behind D30 is unavailable.

Evidence that would change the order includes a genuine storage prompt and
behavior check, a one-job/trigger review of the browser scope, consumer task
or incident frequency, comparative authorized routing tests, and measured
active costs. These are future evidence needs, not hidden prerequisites to
storing this proposal. The alternatives above remain viable owner choices.

## Owner-choice sequence

1. The next decision is **which batch, if any**, to select: the four-item
   proposal, the smaller three-extension set, the larger request-boundary
   set, the QA emphasis, or a different owner priority. No work starts from
   this page alone.
2. If a batch is selected, decide whether the `product-spec-writer` adjunct
   outside the named expansion candidates is included, whether #112 dynamic
   SQL fits item 1, and how narrowly to define the browser reviewer.
3. Only after that scope is set, decide final names, invocation posture,
   records for covered rows, and build/merge terms using fresh evidence.
   #189 remains PARTIAL/DEFER until its unbuilt residue has an actual owner.

These dependent decisions are not answered by one blanket “build it” reply.
The owner has approved storage of a proposal on the stated delivery terms;
that is separate from selecting or building a skill batch, as the
[unmerged, commit-pinned answer](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/owner-askuserquestion-answers.md#L71-L75)
records.

## Research provenance and limits

The preserved, unmerged research inputs are
[G1 QA Tier 2](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G1.md),
[G2 and G6](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G2G6.md),
[G3](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G3.md),
[G4](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G4.md),
[G5](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-G5.md),
and [mechanics/demand](https://github.com/ModernNomad-98/Project-Aegis/blob/32f5ae25780c4802184a63d4063507fcf31b3a37/docs/evidence/session-handoff-2026-10-08/artifacts/skillbatch/research-MECH-DEMAND.md).
They are evidence of earlier investigation, not merged repository policy.

**Checked at the pinned source for load-bearing recommendations:** the
[forecast](aegis-backlog-forecast.md) and six-range arithmetic; [catalog](../skills-catalog.md)
Phase 2–4 candidate lists; [reconciliation](../reconciliation/step-0-reconciliation-v4.md)
D8, D10, D30 and untiered-row text; [category 03](../skills/03-saas-security-rls.md)
and relevant roadmap rows; the `SKILL.md` bodies or cited passages of
`rls-policy-auditor`, `file-upload-storage-architect`,
`command-gateway-architect`, `product-spec-writer`,
`security-pr-reviewer`, `change-classification-gate` and its matrix;
the named storage and visual handoffs and bounded searches stated above;
and the [VolunteerFlow historical finding](../audits/volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md).

**Not checked:** live skill routing or behavior, a real storage platform,
provider effects, comparative consumer demand, final skill descriptions or
ROUTE-002 changes, #105, and full-body ownership for every deferred or
tentatively dropped row. Historical helper estimates and broad negative
searches are not fresh measurements. No skill build or evaluation was run.

## Excluded actions

This page selects and builds nothing. It changes no skill, evaluation,
catalog, README count, decision log, approval register, forecast, backlog
status, readability ledger or index, CI/configuration file, audit baseline,
or script. It does not authorize a migration, provider or database call,
environment write, deployment, VM/ISO work, reserved evaluation/rehearsal,
Stage 4B, BER work, or a protected evidence-pin change. The full plan and
later authority gates govern any subsequent work.
