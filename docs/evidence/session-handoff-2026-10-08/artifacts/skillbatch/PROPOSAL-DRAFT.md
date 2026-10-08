# Unselected skill expansion batch: scope proposal

> **Status:** Proposal only, waiting for an owner decision. This page grants no
> authority and builds nothing. No skill, evaluation file, catalog row or
> decision-log row was created or changed by the pull request that adds it.

Prepared 2026-10-08 from `ModernNomad-98/Project-Aegis` `origin/main` at
`52289779`, where `python -B scripts/validate-skills.py` reported 195 valid skills.

This page is for the owner, who decides which batch of the remaining skill
candidates to build next, and for the maintainers and reviewers who would
build it. On 2026-10-08 the owner asked for planning of "A batch from the
unselected skill expansion" and said "make sure you store these plans in the
repo's backlog". This page is that plan. It checks every remaining candidate in the
six groups of the
[backlog forecast's unselected skill expansion](aegis-backlog-forecast.md#start-here--current-reading)
against the 195 shipped skills, records an outcome for each, recommends one
batch and names three alternatives. The
[open-decisions index](aegis-open-decisions-2026-09-23.md#owner-requested-backlog-items)
lists it as an owner-requested backlog item.

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
- A **manual-only** skill carries `disable-model-invocation: true`, so the
  assistant never picks it on its own; a person must name it. The
  [skill generation standard, section 5](../skill-generation-standard.md#5-least-privilege--side-effects)
  requires this for a skill that writes, calls a network, deploys or spends.
  A skill that only reads and reports stays **auto-invocable**.
- An **extension** adds a bounded piece of work to an existing skill instead
  of creating a new one. A **drop** records that shipped skills already cover
  a candidate, so nothing is built.
- A **candidate group** is one row of the forecast's unselected-expansion
  table. This page calls the six remaining rows G1 to G6 (listed under
  [Disposition of every candidate](#disposition-of-every-candidate)).
- **P0**, **P1** and **P2** are the planning tiers of the
  [skills roadmap](../skills/03-saas-security-rls.md) (foundation, high-value
  follow-on, later expansion). Its legend says "A priority does not state
  whether a row shipped"; a tier is not evidence that anyone needs the skill.
- A **D-number** (for example D8, D10, D30 or D74) is an entry in the
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
- **Active hours** count only hands-on agent work, excluding review waits,
  continuous-integration (CI) queue time and time waiting for the owner. Every
  figure here is an agent estimate. **No earlier batch estimate has been
  measured against actual active time**, so all of them have low confidence.
- The **seven-stage workflow** is the
  [delivery workflow](../delivery-workflow.md) every pull request (PR) now
  follows: plan, independent plan audit, implement, independent implementation
  audit, validate, final independent review, merge, each stage held by a
  different agent. It was adopted as D72 on 2026-10-03, after the four earlier
  batches were built.

## Decision in one read

The six groups hold 34 distinct named candidates or topics, plus 19 untiered
rows of roadmap category 06 (quality assurance), one of which (#235) is the
`qa-closeout-reporter` candidate. Checked against the shipped
skills, 11 named candidates are already covered and should be dropped, 6 fit
best as extensions of shipped skills, and the other 17 are real gaps of very
different strength. One shipped skill routes storage-policy audits to a skill
with no storage content; that defect is fixed first in every option below.

**Recommended batch: "recorded boundary priorities".** It takes the defect fix
plus the three items the repository itself already recorded as a priority or
as an open gap, and nothing whose only support is a planning tier.

| Item (roadmap rows) | Recommendation | Manual-only? | Active hours (provisional) |
| --- | --- | --- | ---: |
| 1. `rls-policy-auditor`: storage-object policies and SQL built inside database functions (#115, #112) | **EXTEND**; fixes a shipped routing defect | not applicable (stays auto-invocable) | 1–2 |
| 2. `command-gateway-architect`: the rest of idempotency-first design (#17, #144; D30's top pull-forward) | **EXTEND** | not applicable (stays auto-invocable) | 1–2 |
| 3. `product-spec-writer`: repeated-request behavior in every spec (#17's spec half; acceptance-test findings AEGIS-013 and AEGIS-028) | **EXTEND** | not applicable (stays auto-invocable) | 0.75–1.5 |
| 4. `browser-boundary-reviewer` (#110, #111, #120; D8's open A02 residue) | **BUILD** | No, it reads only what it is given | 3–5 |
| Batch overhead (registration, decision row, reciprocity edits, census, reviews) | — | — | 1.5–2.5 |
| **Total** | **1 new skill, 3 extensions** | | **7.25–13** |
| Optional: record every covered verdict from all six groups in the same decision row | — | — | +0.5–3.75 |
| Seven-stage allowance, 4 pull requests at 1–2 hours each (very low confidence) | — | — | +4–8 |

The library would go from 195 to 196 skills. In forecast terms the batch
consumes three candidates: idempotency-first design from the Phase 2 group,
and storage-policy review and the cross-site deep-dives from the Phase 4
group. At the forecast's flat average of 2–4 hours per candidate that is 6–12
hours, against 7.25–13 here before the seven-stage allowance.

**Alternatives,** each detailed under [Alternatives](#alternatives):

| Alternative | Items | Active hours, before / with the seven-stage allowance | Skills after |
| --- | --- | ---: | ---: |
| Smaller: correctness only | items 1–3 | 3.75–7.5 / 6.75–13.5 | 195 |
| Larger: full request boundary | items 1–4, `authentication-session-reviewer`, and extensions of `change-classification-gate` (#127) and `authorization-matrix-designer` (#59) | 12.25–22 / 19.25–36 | 197 |
| Different emphasis: QA Tier 2 | item 1, `visual-regression-test-designer`, `exploratory-charter-designer`, `mobile-journey-test-designer`, and a `qa-automation-architect` extension (#213) | 11.25–20 / 16.25–30 | 198 |

**Other findings recorded here:** a second shipped pointer to a skill with no
content for its subject (visual regression); a candidate counted twice in the forecast
(#127); 11 covered candidates still priced in the forecast; and scope the
forecast does not price at all. See
[Defects found in shipped skills](#defects-found-in-shipped-skills) and
[Findings about the forecast](#findings-about-the-forecast).

## How the candidates were checked

- **Base.** Every file was read at `52289779`. Six research reports covered
  the groups, delivery mechanics and demand; the planner then re-checked their
  load-bearing claims against the repository and corrected two of them (see
  item 2 and the validation-boundary row under G3).
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
- **Demand.** The repository has one GitHub issue ever (#101, about setup), no
  usage data, and a route graph that by construction records only edges to
  skills that exist. The only observed failure that names a candidate's topic
  is the VolunteerFlow acceptance test's idempotency finding. So demand is
  not used to rank anything else; "no demand signal" is not "no demand".
- **Estimates.** Per-item ranges reuse the four earlier proposals' estimates:
  new skills 2–5 hours, extensions 0.75–2, drops 0–0.25, batch overhead
  1–3.5. None of those has been scored against measured active time. The
  seven-stage allowance of 1–2 hours per pull request rests on one measured
  documentation pull request (#680), so it has very low confidence; it is
  shown separately and may overlap the review share of the batch overhead.

**The selection rule for the recommended batch.** First, the protected lane:
a shipped skill that routes storage-policy audits to a skill with no storage
content (item 1). Then the items the repository itself recorded as a priority or an
open gap: D30's "TOP pull-forward" for idempotency (items 2 and 3), the
VolunteerFlow defects AEGIS-013 and AEGIS-028 (item 3), and D8's "open
residue" for security headers and CORS (item 4). Planning tiers alone did not
qualify an item. The rule is a judgment, and its strongest objection is under
[Self-scrutiny](#self-scrutiny).

## Item 1: `rls-policy-auditor` extension for storage policies and database-function SQL (#115, #112)

**Roadmap text.** #115 Storage Access Policy Review (P0): "Validate bucket
policies, signed URL expiry, path naming, ownership checks, and public asset
boundaries." #112 SQL Injection Defense Review (P0): "Check dynamic SQL,
filters, RPCs, search, sorting, and migration scripts for injection risks."
(RPCs are remote procedure calls.) Both are in
[category 03](../skills/03-saas-security-rls.md).

**The defect this fixes.**
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
no storage content: `grep -ciE 'storage|bucket'` returns 0 for its
`SKILL.md`, 0 for `references/rls-audit-checklist.md` and 0 for
`evals/evals.json`; the one hit in its `trigger-evals.json` (line 41) is a
whole-app leak prompt routed elsewhere. The route sits on the main path:
`project-orchestrator`'s Stage 4, "Make it safe", names
`file-upload-storage-architect` (`SKILL.md:242-245`).

**What shipped skills already do.**

- `rls-policy-auditor` audits PostgreSQL row-level security per table and per
  command (SELECT, INSERT, UPDATE, DELETE), `SECURITY DEFINER` helpers,
  grants and service-role leakage, and always writes a negative-test plan. Its
  per-table method covers the prompt's "row-level rules for our object
  metadata" half, but nothing in it covers bucket policies, path prefixes,
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
- For SQL built at run time inside database functions, neither
  `rls-policy-auditor` nor `secure-migration-reviewer` has any content:
  `grep -ciE 'dynamic sql|\bEXECUTE\b|format\(|inject'` returns 0 in both
  skills' `SKILL.md` and checklists. Injection in application code is covered
  in a diff by `security-pr-reviewer`.

**The gap.** A policy-level audit of storage access: which storage tables or
buckets hold tenant files, whether every policy ties the bucket and path
prefix to the caller's tenant, public buckets and public URLs, who mints
signed URLs and with which role, service-role use in upload handlers, and
per-command negative tests for objects. Plus run-time-built SQL in callable
database functions, which can bypass tenant scope when it concatenates input.

**Recommendation: EXTEND.** Check 3's extension test fits: a new surface that
keeps the base skill's verdict shape (findings plus per-command negative
tests). A separate storage auditor would collide with `rls-policy-auditor` on
"audit our policies" and contradict the pinned trigger-eval case above.

- **Cheaper alternative considered:** repoint the hand-off to
  `tenant-isolation-reviewer` (about 0.5–1 hour). Rejected because that skill
  covers storage in one checklist row and #115 asks for policy-level checks.
- **Fallback:** if the build-time check 6 finds that run-time SQL makes the
  skill do two jobs, ship storage only (0.75–1.5 hours) and keep #112's
  residue deferred.
- **Manual-only:** not applicable; the base stays auto-invocable. It delivers
  policies as migrations for review and never runs DDL against a live
  database, which the quality checklist names as its posture.
- **Draft description:** 1,015 characters measured with `yaml.safe_load`
  (9 to spare). It adds "storage-object policies included (bucket/prefix
  scope, public buckets, signed-URL minting)", "dynamic SQL in functions" and
  "(including those file-upload-storage-architect hands off)", and keeps every
  existing trigger and exclusion.
- **ROUTE-002:** naming `file-upload-storage-architect` clears the existing
  one-way finding `file-upload-storage-architect → rls-policy-auditor`, which
  is in `artifacts/audits/skill-contract-audit-baseline.json` today; no new
  exclusion is added, so no new finding is predicted.
- **Evals:** behavior cases for a prefix policy that ignores the tenant, a
  public bucket holding uploads, and run-time SQL in a `SECURITY DEFINER`
  function; trigger cases against `cloud-security-baseline-reviewer` (account
  posture) and `tenant-isolation-reviewer` (whole-app review). The existing
  `file-upload-storage-architect` case must stay true.
- **Build note:** the build PR answers **Yes** to the security-surface
  question if it edits the skill's Security Rules or Stop Conditions
  ([CONTRIBUTING](../../CONTRIBUTING.md#external-contributions)).
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

**The gap.** `grep -niE 'fingerprint|different payload|payload hash|in[- ]flight|in progress'`
finds nothing in the gateway skill. Unstated today: the response when a
reused key arrives with a different payload (the skill asks what "same
request" means but not what to return when it is not); a duplicate that
arrives while the first request is still running; carrying the key to
third-party side effects such as payment or email providers, with an outbox
for at-least-once external effects (the skill's only outbox is for audit
records, `:159`, `:175`); and a path for a small app with one endpoint and no
command bus yet.

**Recommendation: EXTEND.** A standalone `idempotency-first-designer` would
fire on the gateway's own "Use when" at lines 40-41, a check 2 failure.

- **Manual-only:** not applicable; the base stays auto-invocable.
- **Description:** unchanged (944 characters). The body, its references and
  its evals change, which leaves the description's 80 spare characters for a
  later reciprocity edit.
- **Evals:** cases for a key reused with a different payload and for an
  in-flight duplicate; trigger cases against
  `background-job-orchestration-architect`, `streaming-event-architect` and
  `api-event-architect`.
- **ROUTE-002:** none predicted (no description change).
- **Correction to the research input:** the Phase 2 research said the "same
  request" question was absent; the skill does ask it, so the residual is the
  mismatch response, not the definition.
- **Estimate:** 1–2 active hours (precedent extension range).

## Item 3: `product-spec-writer` repeated-request extension (#17, spec half)

**Why it is here.** This is the only item in the plan backed by an observed
failure. The
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

**The gap and the recommendation: EXTEND.** Every state-changing action in a
spec states its observable outcome on a retry, a double submit, a second tab
and a stale request, and whether duplicate events are possible. The mechanism
stays with item 2 and `tech-spec-writer`; the spec states only the outcome.
This is the bounded slice of AEGIS-013 and AEGIS-028, not the full
state-transition matrix that AEGIS-014 proposes.

- **Scope note:** `product-spec-writer` is not a named expansion candidate.
  The item is the spec-time half of candidate #17, and leaving it out would
  leave that candidate's only observed failure unfixed. The owner may drop it
  (question 3 below).
- **Not covered:** the handoff report also asks for a fresh-session
  regression run proving the behavior; this extension adds eval cases only.
- **Manual-only:** not applicable. **Description:** unchanged (961
  characters). **ROUTE-002:** none predicted.
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

**The gap.** An auto-invocable review of an existing web app's browser trust
boundary, with no diff in hand: CSRF on cookie-authenticated mutations, XSS
sinks, CSP and other security headers, CORS with credentials, framing and
cookie scope, producing findings and one header and CSRF policy.

**Recommendation: BUILD.**

- **One job, not four:** the output is one boundary review (per-surface
  findings plus one policy). If the build-time check 6 calls it a catch-all,
  the fallback is to drop the XSS sinks, which the diff review already
  covers, and keep CSRF, headers and CORS.
- **Not input validation:** validating input is not an XSS or CSRF defense;
  where validation should live is a separate, deferred candidate
  (`validation-boundary-designer`).
- **Manual-only:** No. It reads the code, configuration and captured response
  headers it is given and fetches nothing live; testing a running app belongs
  to [`dast-safety-harness-designer`](../../.claude/skills/dast-safety-harness-designer/SKILL.md).
- **Name:** avoid `browser-security-reviewer`, which contains the reserved
  bundled name `security-review` (`scripts/validate-skills.py:147-163`).
- **Draft description:** 941 characters measured with `yaml.safe_load`: it
  front-loads "Review a web app's browser trust boundary as a whole, not one
  diff", and excludes `security-pr-reviewer`, `llm-output-safety-reviewer`,
  `appsec-implementer`, `caching-strategy-designer` and
  `dast-safety-harness-designer`.
- **Trigger evals pin against** the same five; a case that expects the
  manual-only `appsec-implementer` must start `Explicitly invoke
  appsec-implementer. ` (standard section 6).
- **ROUTE-002:** two to four one-way findings predicted, not measured: toward
  `llm-output-safety-reviewer` (1,018 characters, no room) and
  `caching-strategy-designer` (999), and toward `security-pr-reviewer` (962)
  and `dast-safety-harness-designer` (948) if no reciprocal phrase fits.
  `appsec-implementer` (675) has room for one.
- **Wiring:** `project-orchestrator`'s Stage 4 names no browser-boundary
  reviewer today; a route would be a separate, unestimated pull request, as
  #384 was for the feature-flag skill.
- **Build note:** the build PR answers **Yes** to the security-surface
  question, because it adds a skill's invocation posture, Security Rules and
  Stop Conditions.
- **Estimate:** 3–5 active hours, the range of the earlier new review skills
  with five or more neighbors.

## Alternatives

Every alternative keeps item 1, because it repairs shipped content.

### Smaller: correctness only

Items 1, 2 and 3: three extensions, no new skill, 195 skills after. Base
3.75–7.5 hours with 1–2 of overhead; 6.75–13.5 with the allowance for three
pull requests. Choose it to repair and complete what ships before adding
skills. It leaves D8's open residue unowned.

### Larger: full request boundary

The recommended batch plus three items, 197 skills after; base 12.25–22 hours
with 2–3.5 of overhead, 19.25–36 with the allowance for seven pull requests:

- **`authentication-session-reviewer`** (#108, #109, both P0; 3–5 hours):
  an auto-invocable review of existing sign-in, sign-out, password reset,
  multi-factor and single sign-on flows, sessions and refresh tokens, without
  a diff. No shipped skill covers password reset beyond an audit event and a
  threat-catalog row, and "step-up" or re-authentication appears nowhere. D8
  marks this OWASP category covered, but by its own rubric "covered" means
  "named in at least one shipped Phase 4 skill contract", not reviewed in
  depth. Its support is planning tier plus these searches, which is why it is
  not in the recommended batch.
- **`change-classification-gate` extension for security impact notes**
  (#127, P0; 0.75–1.5 hours): add a written impact note to the rls-security
  class's validation floor, as the gate already does for schema migrations
  ("explicit rollback; data-loss statement") and infrastructure
  ("blast-radius statement") in `references/classification-matrix.md:18-20`.
- **`authorization-matrix-designer` extension** (#59, P0; 0.75–1.5 hours):
  role-assignment rules with a grant ceiling (no one grants a role above
  their own), role and resource inheritance, and tenant-defined custom roles.
  The catalog already attributes #59 to this skill, but its body mentions
  inheritance only for machine actors.

### Different emphasis: QA Tier 2

Item 1 plus the quality assurance Tier 2 core, 198 skills after; base
11.25–20 hours with 1.5–3 of overhead, 16.25–30 with the allowance for five
pull requests. D10 ordered Tier 2 after Tier 1, and Tier 1 was built under
D68.

- **`visual-regression-test-designer`** (#203, promoted by D10 "because UI
  drift is otherwise invisible"; 3.25–5 hours), absorbing #202's snapshot
  rule and the fixture-mode part of #189. It also repairs the second empty
  pointer under [Defects found in shipped skills](#defects-found-in-shipped-skills).
- **`exploratory-charter-designer`** (#228, renamed; 2–3.5 hours).
- **`mobile-journey-test-designer`** (#230, renamed because
  `mobile-viewport-qa` is one word from the shipped `mobile-viewport-craft`;
  2.5–4 hours).
- **`qa-automation-architect` extension** for per-layer timeout policy (#213;
  1–2 hours).

The narrowed `role-coverage-test-designer` (#229) would follow the
`authorization-matrix-designer` extension. A tenant-lifecycle batch
(`tenant-provisioning-designer`, `membership-invitation-designer` and the
#59 extension, with item 1: 8.75–15 hours base) is also coherent; its rows
are P0 but nothing beyond the tier and the gap searches supports them.

## Overlaps between groups

These are the places where two groups claim the same ground. Each resolution
applies whenever the items are built, in this batch or later.

| Overlap | Resolution |
| --- | --- |
| Role coverage testing (G1 #229) and authorization design (G4 #59) both touch `authorization-matrix-designer` | Build the #59 extension first: it changes the matrix that role-coverage tests use as their oracle. Role coverage then plans allowed-path and interface checks only, and delegates denial proofs to `authorization-matrix-designer` and `multi-tenant-security-tester`. `membership-invitation-designer` consumes the grant ceiling from #59. |
| Validation placement (G3 #37) against the browser boundary (G5 #110/#111) and SQL injection (G5 #112) | Three owners: where input is accepted and checked per layer is `validation-boundary-designer` (deferred); output encoding, CSRF, headers and CORS are item 4; SQL built inside database functions is item 1, and SQL in application code stays with `security-pr-reviewer` in a diff. Item 4 must say that input validation is not an XSS defense. |
| Idempotency (G3 #17/#144), inbound webhooks (G5 #116), the VolunteerFlow findings and tenant provisioning (G4 #57) | Write-path design is item 2; spec-time outcomes are item 3; receiving third-party webhooks (signatures, replay window, event-id dedup, tenant mapping) is the deferred `inbound-webhook-security-designer`, which should consume item 2's dedup contract; a provisioning designer would compose that contract rather than restate it; public-API retry windows stay with `api-event-architect`. |
| Shared file `command-gateway-architect` (item 2; later, `validation-boundary-designer`'s reciprocity edit) | Item 2 changes the body only and leaves the description's spare room for the later edit; the later build re-reads the extended file. |
| Shared file `rls-policy-auditor` (G5 storage and SQL; a minor G6 note that backup-gated validation does not name storage-policy changes) | One lane: item 1. |
| Logging redaction (G3 #22 observability-by-design and G5 #124) | Both deferred. Proposed seam: the "never log this" catalog and the leak review go to `log-redaction-reviewer`; the telemetry contract in `observability-by-design` consumes it; the manual-only `observability-operator` implements it. Build them together, or the reviewer first. |
| Security impact notes (#127, listed in both G4 and G5) | Judged once, in G5: an extension of `change-classification-gate`. `threat-modeler` was the other proposed home, but its description says "Do NOT use when: reviewing an implemented diff" (`SKILL.md:37`), and an impact note is written for a concrete change. |
| Rate limits (G5 #117), brute force in authentication review, and invitation spam (G4 #58) | Deferred. D30's wording, "general per-tenant/plan API rate limits + noisy-neighbor defense", is already met by `api-event-architect` step 4 (`SKILL.md:95-98`), present since 2026-07-06, two days before D30. The residual is limits by abuse category, which a later `rate-limit-architect` would own; an authentication reviewer checks that flows are throttled, and an invitation designer consumes the limits. |
| Quality assurance shared files (`qa-automation-architect`, `test-coverage-mapper`, `test-plan-designer`) and a defect-report skill (G6 #224/#225) against exploratory charters (G1 #228) | Plan all quality assurance items in one lane. The #213 and #202 rows go to the G1 plan, not G6. An exploratory debrief hands defects to the defect-report skill if both are built. |

## Disposition of every candidate

Outcomes: **BUILD** (new skill), **EXTEND** (into the named skill), **DROP**
(covered; record it), **DEFER** (a real gap, not in the recommended batch).
"Rec." marks the recommended batch; S, L and Q mark the smaller, larger and
QA alternatives. Hours are the research estimates (low confidence); evidence
is at `52289779`.

### G1 — QA expansion Tier 2 (forecast 12–24 hours)

| Candidate (rows, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `visual-regression-test-designer` (#203 P2; absorbs #179, #202 and part of #189) | BUILD | Q | 3.25–5 | No shipped skill designs visual baselines; `screenshot-evidence-planner` points this work at `qa-automation-architect`, which has no visual content. |
| `exploratory-testing-charter` (#228 P1), as `exploratory-charter-designer` | BUILD | Q | 2–3.5 | `qa-strategy-architect:142-144` says strategies that omit manual testing "leave visual, UX, and exploratory risks unowned"; no shipped skill writes charters. |
| `mobile-viewport-qa` (#230 P1), as `mobile-journey-test-designer` | BUILD | Q | 2.5–4 | Layout is `mobile-viewport-craft`'s; journey checks on phones are not ("Deep responsive QA is its own effort", `clickthrough-test-engineer/references/clickthrough-route-catalog.md:31`). |
| `role-based-qa-matrix` (#229 P1), narrowed as `role-coverage-test-designer` | DEFER | — | 2.5–4 | Denials are owned by `authorization-matrix-designer` step 7 and `multi-tenant-security-tester`; allowed paths and interface consistency are not. Build after the #59 extension. |
| `mock-strategy-designer` (#200, #201 P1) | DROP | records | 0–0.25 | Covered by `integration-test-designer` (real or faked seams), `vitest-unit-component-engineer` ("Mock only owned boundaries"), `api-contract-test-designer` ("Keep fakes faithful"), `qa-strategy-architect` and `test-coverage-mapper`. |
| `ci-shard-parallel-isolation` (#211, #212 P1) | DROP | records | 0–0.25 | Covered by `sharded-validation-with-resume` (built after D10), `qa-automation-architect` ("Design isolation & parallelization"), `test-data-architect` and `playwright-e2e-engineer`. |
| #213 test timeout policy (P1; handed over from G6) | EXTEND `qa-automation-architect` | Q | 1–2 | `grep -ci timeout` returns 0 in that skill and its blueprint; classifying timeouts after the fact is `ci-failure-classifier`'s. |

### G2 — QA expansion Tier 3 (forecast 8–16 hours; D10: "build on demand only")

| Candidate (row, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `property-based-test-designer` (#194 P2) | DEFER (on demand) | — | 2.5–4 | A real gap: only a passing debugging mention exists. No demand signal; D10's rule applies. |
| `mutation-testing-reviewer` (#195 P2) | DEFER as an EXTEND of `test-coverage-mapper` | — | 0.75–1.5 | `test-coverage-mapper` already asks "what real bug would make this test fail?"; reading mutation-tool reports is the residual. |
| `soak-test-planner` (#207 P2) | DROP | records | 0–0.25 | `load-test-planner` plans soak tests and two pinned trigger evals route soak prompts to it. Optional 0.25–0.5-hour note on token and session expiry during long runs. |
| `chaos-test-planner` (#208 P2) | DROP | records | 0–0.25 | `resilience-architecture-reviewer` writes "a fault-injection or game-day plan" and runs none. |

### G3 — Phase 2 expansion (forecast 18–36 hours)

| Candidate (rows, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `idempotency-first-designer` (#17, #144 P0) | EXTEND `command-gateway-architect` (item 2) and `product-spec-writer` (item 3) | Rec., S, L | 1–2 and 0.75–1.5 | Item 2 and item 3 above. |
| `validation-boundary-designer` (#37, #38, #141, #157 P0) | DEFER (BUILD later) | — | 3–5 | The gap is design-time placement across layers. It is narrower than first reported: mass assignment is already named by `security-pr-reviewer`, `threat-modeler`'s catalog and `multi-tenant-security-tester`. |
| `observability-by-design` (#22 P0) | DEFER (BUILD later, with log redaction) | — | 3–5 | No auto-invocable skill designs the telemetry contract; `observability-operator` is manual-only. Name is a near miss with `observability-operator`. |
| `api-contract-designer` (#9 P0) | DEFER as an EXTEND of `api-event-architect` | — | 1–2 | Per-operation schema rules are absent; whether first-party APIs fit that skill's "external contracts" scope is unverified. |
| `refactor-safety-planner` (#11 P0) | DEFER | — | 3–4.5 | The catalog calls `code-simplifier` only "adjacent"; decide together with the unlisted `code-quality-auditor`. |
| `dependency-direction-guard` (#6, #7 P0) | DEFER | — | 2.5–4.5 | `architecture-designer`, `code-reviewer` and an agent definition catch common cases; the residual is a CI ratchet. Decide with `code-quality-auditor`. |
| `operational-runbook-author` (#23 P1) | DROP | records | 0–0.25 | Covered by `incident-response-runbook`, `rollback-runbook-author`, `data-migration-runbook-author`, `gated-deployment-prompt-template` and `onboarding-doc-designer`. |
| `system-context-mapper` (#2 P0) | DROP | records | 0–0.25 | `architecture-designer` step 1 and `threat-modeler`'s system map. |
| `bounded-context-identifier` (#4 P0) | DROP | records | 0–0.25 | `domain-modeler` step 4, "Draw bounded contexts". |

### G4 — Phase 3 expansion (forecast 8–16 hours)

| Candidate (row, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `role-permission-architect` (#59 P0) | EXTEND `authorization-matrix-designer` | L | 0.75–1.5 | The catalog attributes #59 to that skill; "assignment" and "inheritance" are absent except for machine actors. |
| `tenant-provisioning-designer` (#57 P0) | DEFER (BUILD in a tenant-lifecycle batch) | — | 3–4.5 | `tenant-modeler` gives lifecycle semantics only ("semantics only", `SKILL.md:139`); nothing designs the creation workflow, first owner or seed data. |
| `membership-invitation-designer` (#58 P0) | DEFER (BUILD narrowed, after #59) | — | 2.5–4 | `tenant-modeler` models invitation states; single-use tokens, identity binding at acceptance, seat checks and invite-spam limits are unowned. |
| `security-impact-note-author` (#127 P0) | Judged once under G5 | — | — | Listed in both groups; see the G5 row. |

### G5 — Phase 4 security topics (forecast 20–40 hours for about ten topics)

| Topic (rows, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| Storage-policy review (#115 P0) with SQL injection residue (#112 P0) | EXTEND `rls-policy-auditor` (item 1) | all | 1–2 | Item 1 above. |
| CSRF/XSS/SQLi deep-dives (#110 P1, #111 P0) with security headers (#120 P1, unlisted) | BUILD `browser-boundary-reviewer` (item 4) | Rec., L | 3–5 | Item 4 above. |
| Authentication and session review (#108, #109 P0) | BUILD `authentication-session-reviewer` | L | 3–5 | See the larger alternative. |
| Security-impact-note authoring (#127 P0) | EXTEND `change-classification-gate` | L | 0.75–1.5 | See the larger alternative. |
| Rate-limit design (#117 P1) | DEFER | — | 3–5 | D30's framing is met by `api-event-architect`; abuse-category limits remain. |
| Logging redaction (#124 P0) | DEFER (with observability-by-design) | — | 2.5–4 | `security-logging-alerting-architect` says safe log content needs "their own audit-log design and operating controls" (`SKILL.md:17-18`). |
| Webhook security (#116 P1), inbound only | DEFER (after item 2) | — | 2.5–4 | Sending webhooks is `api-event-architect`'s; receiving them appears only as a threat-catalog question. An `api-event-architect` extension (1–2 hours) is the cheaper alternative. |
| Security-drift detection (#130 P0) | DEFER (on demand) | — | not estimated | Covered in pieces by six skills; the residual, a scheduled check of documented controls without a diff, is narrow. |
| Compliance-evidence mapping (#128 P1) | DROP | records | 0–0.25 | `compliance-evidence-collector` maps each control to its evidence. |
| Privacy-by-design (#129 P1) | DROP | records | 0–0.25 | `pii-lifecycle-designer` covers minimization, purpose, retention and deletion. |

### G6 — Phase 5 extras (forecast 2–8 hours)

| Candidate (rows, tier) | Outcome | In | Hours | Evidence |
| --- | --- | --- | ---: | --- |
| `e2e-test-architect` (historical roadmap P0) | DROP | records | 0–0.25 | Covered by composition of `qa-strategy-architect`, `test-plan-designer`, `qa-automation-architect`, `regression-suite-curator`, `test-data-architect` and `playwright-e2e-engineer`. |
| `qa-closeout-reporter` (#235 P0) | DROP | records | 0–0.25 | `ai-closeout-reporter` and `release-readiness-reviewer`; a shipped trigger eval already says this candidate "stays in the backlog" because of that overlap. |
| #224 bug report and #225 triage (P1) | DEFER (one new skill in the QA lane) | — | 3–4.5 | Only the manual-only `clickthrough-test-engineer` files defects, inside its own sessions. |
| #188 production-safe smoke testing (P0) | DEFER as an EXTEND of `synthetic-monitoring-architect` | — | 1–2 | That skill owns scheduled probes and their safety contract; no auto-invocable skill designs a one-off post-deploy smoke set. |
| #231 timezone and #232 notification QA (P1) | DEFER as an optional `test-plan-designer` reference | — | 1–1.5 | Per-feature test plans already route to `test-plan-designer`. |
| #202 snapshot governance (P2), #213 timeout policy (P1) | Moved to G1 | Q | — | See the G1 table. |
| #189 fixture-mode E2E (P1) | DROP by split | records | — | Breadth goes to component tests and `clickthrough-test-engineer`; the state-rendering part moves into `visual-regression-test-designer`. |
| #191, #193, #199, #216, #217, #218, #219, #220, #233, #234 | DROP | records | 0.5–1 together | Each maps to a shipped owner: `test-coverage-mapper`, `test-plan-designer`, `test-data-architect`, `release-readiness-reviewer`, `local-ci-mirror-preflight`, `risk-tiered-validation-selector`, `data-migration-runbook-author`, `merge-is-deploy-governance` and `multi-tenant-security-tester`. |

The candidate counts in [Decision in one read](#decision-in-one-read) come
from these tables: 34 distinct named candidates or topics (6, 4, 9, 4, 10 and
2, less #127 counted twice); 11 of them DROP; 6 EXTEND (#17, whose two
extensions count once, #195, #9, #59, #127 and #115); and 17 BUILD now or
later. The untiered category-06 rows are counted separately.

## Defects found in shipped skills

1. **Storage audits routed to a skill with no storage content.** Described
   under item 1; fixed by item 1 in every option. Because it repairs shipped
   content, the owner may approve it on its own before choosing a batch
   (question 2).
2. **Visual regression routed to a skill with no visual content.**
   `screenshot-evidence-planner` says "Do NOT use when: the ask is
   visual-regression pixel-diff tooling — that is automation architecture
   (`qa-automation-architect`)" (`SKILL.md:33-35`), and
   `grep -ciE 'visual|pixel|screenshot baseline|snapshot'` returns 0 for
   `qa-automation-architect`'s `SKILL.md`, blueprint and both eval files. No
   trigger eval pins this route, so it is less severe than defect 1. It is
   fixed by `visual-regression-test-designer` (the QA alternative) or, if
   that waits, by a visual-layer row in `qa-automation-architect`'s
   blueprint.
3. **Catalog attributions that overstate coverage.** The catalog maps #59 to
   `authorization-matrix-designer` (see the G4 table), #189 to
   `playwright-e2e-engineer` (which says "Reject UI-tree crawling"), and #200
   with #211 and #212 to `qa-automation-architect`, whose body mentions fakes
   only in its database-isolation table. The reconciliation log's "partially
   absorbed" list also omits #189.
   Record these as dated notes in the build's decision row, never by
   rewriting the old text.
4. **AEGIS-013 and AEGIS-028 remain open in `product-spec-writer`.** Fixed in
   part by item 3.

## Findings about the forecast

The forecast's "Unselected skill expansion" figure of **68–140** hours is the
sum of the six group ranges (12–24, 8–16, 18–36, 8–16, 20–40 and 2–8),
which re-adds exactly. Four findings change what that figure means. They are
recorded here, not edited into the forecast, because the forecast changes at
its five-merge checkpoints or on a material owner decision
([execution measurements](aegis-execution-metrics.md)), and a proposal is
neither.

1. **#127 is counted twice.** Security-impact-note authoring is in the
   Phase 3 list (`security-impact-note-author`) and again in the Phase 4
   list (`docs/skills-catalog.md` Phase 3 and Phase 4 backlog paragraphs), so
   both forecast rows price it. Each row averages 2–4 hours per candidate;
   removing one count gives about **66–136**. That figure is derived from the
   averages; no forecast line prices a single candidate.
2. **Eleven covered candidates are still priced.** Nine of them sit in groups
   G1 to G5, where each is priced at the 2–4-hour average: **18–36** hours of
   the forecast for work that costs 0–0.25 hours each to record. The other two
   are inside G6's undivided 2–8.
3. **Some scope is not priced at all.** #120 security headers (folded into
   item 4) is in no group; the reconciliation log puts `code-quality-auditor`
   and three other whole-codebase audit skills in "the Phase 2/5 expansion
   backlog" (`step-0-reconciliation-v4.md:200-205`), but the catalog's Phase 2
   list and the forecast omit them; and #105 sensitive column masking was not
   checked.
4. **The process cost is not in it.** The forecast predates the seven-stage
   workflow. Re-summing the research dispositions for every candidate gives
   **65–113.75** hours before any seven-stage allowance (deferred candidates
   and item 3 included, security-drift detection not estimated). That is 27
   build pull requests by the tables above, 17 new skills and 10 extensions,
   plus one decision pull request per batch. At 1–2 hours per pull request
   (very low confidence) the allowance would add 27–54 hours for the build
   pull requests alone. So the triage does not show that the expansion is
   cheaper than forecast; it shows that its make-up is different.

The forecast's own latest five-merge checkpoint is the one after #554;
`git rev-list --first-parent --count e0c9a000..52289779` returns 122 commits
since then. Bringing it current is separate work; these four findings are
inputs for it.

## Batch summary

**Recommended set:** extend `rls-policy-auditor`, `command-gateway-architect`
and `product-spec-writer`; build `browser-boundary-reviewer`. The library would
go from 195 to 196 skills.

**Suggested pull requests**, so each has one reviewable seam:

1. **Decision record:** D74 and the owner's choice in the reconciliation log,
   a "Decided" row in the open-decisions index, the dated notes for the
   catalog attributions (defect 3), and, if the owner chooses, the covered
   records for all six groups. No build merges before it, as with #493 and
   #510 for the earlier batches.
2. **Item 1**, first, because it repairs shipped content.
3. **Items 2 and 3 together:** one theme, two small body extensions.
4. **Item 4**, with its reciprocity edits. Its title should name its count
   ("195 to 196") so a parallel lane cannot collide on the README's count
   marker, as #502 did.

Each new skill needs its catalog row, the README counts inside the
validator-checked markers, both eval files and the other registration steps
in [How to add a skill](../../CONTRIBUTING.md#how-to-add-a-skill).

**Total estimate:** 7.25–13 active hours, provisional, including 1.5–2.5
hours of batch overhead; plus 0.5–3.75 if every covered verdict is recorded
now; plus a seven-stage allowance of 4–8 hours for four pull requests (very
low confidence). With both, 11.75–24.75.

**Review path per pull request:** the seven stages of the
[delivery workflow](../delivery-workflow.md), each held by a different agent;
`skill-quality-reviewer` checks 1–7 on each new or extended skill;
`library-diff-reviewer` at the implementation audit and final review;
`python -B scripts/validate-skills.py` and the CI checks at the exact head;
and a ROUTE-002 before-and-after comparison with
`scripts/audit-skill-contracts.py`, which this work does not change and whose
committed baselines it does not regenerate (that needs a new owner grant).
Merges follow the merge terms the owner sets for the build, re-derived by the
merge agent. Each build pull request should record its start and finish
times so that the next batch can score these estimates, which no batch has
done so far.

**Decision number:** the choice would be recorded as **D74**, provisionally.
D73 is the highest decision number in the reconciliation log at `52289779`,
and no other page mentions D74. Recheck at decision time.

**Expected ROUTE-002 census after the recommended batch:** one existing
one-way finding cleared (`file-upload-storage-architect →
rls-policy-auditor`) and two to four new ones from item 4. Following the D64
owner decision, these stay as census data. They are predicted from the draft
descriptions, not measured.

## Self-scrutiny

**The strongest objection to the recommended batch.** Its selection rule
favors items the repository happened to record over items that may matter
more. Authentication and session review is arguably the most valuable missing
security review for a SaaS builder, and it is left to the larger
alternative. The batch builds one new skill, so the expansion shrinks slowly.
D30's audit cannot be inspected, and D8's residue covers headers and CORS but
not CSRF or XSS, which are half of item 4. If the owner values new
capability over recorded evidence, the larger alternative is the better
choice.

**The least certain claims.** Every hour figure (never scored, and the
seven-stage allowance rests on one documentation pull request); whether item
4 passes the one-job check; how each hosting platform expresses storage
policies (a build-time verification item); every routing claim, because no
trigger eval was run; and every ROUTE-002 prediction.

**What would change the recommendation.** A routing run showing that storage
prompts already land well (item 1 would shrink to a wording fix); a
skill-quality review calling item 4 a catch-all (split or narrow it); demand
evidence for any deferred candidate; measured active times from these builds;
or an owner preference for new skills over repairs (the larger alternative)
or for quality assurance next (the QA alternative).

## What the owner must answer

One reply of "build it as recommended" answers all seven with the recommended
option.

1. **Batch.** Build the recommended batch (one new skill, three extensions)?
   *Recommended: yes*, because every item rests on a recorded defect, decision
   or finding. Alternatives: the smaller "correctness only" (no new skill),
   the larger "full request boundary" (adds the authentication reviewer and
   two cheap P0 extensions), or "QA Tier 2".
2. **Item 1 on its own.** If you want to choose the batch later, may item 1
   be built now? *Recommended: yes*; it repairs shipped content and is in
   every option.
3. **Item 3.** Include the `product-spec-writer` extension, which is outside
   the named candidates? *Recommended: yes*; it is candidate #17's only
   observed failure. Without it the batch is 6.5–11.5 hours.
4. **Name.** Call item 4 `browser-boundary-reviewer`? *Recommended: yes*; it
   names the boundary and avoids the reserved `security-review`.
5. **Posture.** Keep all four items auto-invocable, reading only what they are
   given? *Recommended: yes.* Letting item 4 fetch live headers would be a
   network call and would make it manual-only.
6. **Covered records.** Record all 11 covered candidates and the covered
   untiered rows in the decision row now? *Recommended: yes*; the evidence is
   on this page, and leaving them in the backlog keeps the forecast
   overstated. Alternative: record only the chosen batch's items.
7. **Census findings.** Accept the predicted ROUTE-002 findings as census
   data? *Recommended: yes*, matching D64.

Merge terms for the build pull requests are not asked here; the owner sets
them when choosing. Whether this work counts inside the forecast's bounded
selected subtotal is not asked either; like the earlier batches, it stays
outside unless the owner selects it.

## What this page does not do

This page grants no authority and builds nothing. It creates no skill,
evaluation, catalog row, README count or decision-log row, edits no shipped
skill, and changes no forecast figure. An owner choice would be a new
instruction to record; delivery would then rely on that instruction, the
standing delivery approval in
[AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
and its conditions, as checked by the merge agent. Nothing here waives the
`gate-guard` check (the CI job that fails when a pull request changes a
protected file), authorizes a change to `scripts/audit-skill-contracts.py`
or its baselines, or permits any environment write, provider call or
deployment.

**Checked for this proposal:** the forecast's unselected-expansion table and
arithmetic; the catalog's Phase 2 to 5 backlog paragraphs and attributions;
the reconciliation log's D8, D10, D30 and D31 text and its untiered-row list;
roadmap categories 01 to 04 and 06 for every row named above; the
VolunteerFlow handoff's AEGIS-013, AEGIS-014 and AEGIS-028; the descriptions
of every neighbor named above (lengths measured with `yaml.safe_load`); the
bodies of `rls-policy-auditor`, `file-upload-storage-architect`,
`command-gateway-architect`, `product-spec-writer`, `change-classification-gate`
and its matrix, and the relevant sections of `threat-modeler`,
`api-event-architect`, `authorization-matrix-designer`, `tenant-modeler`,
`tenant-isolation-reviewer`, `screenshot-evidence-planner`,
`qa-automation-architect` and `project-orchestrator`; text searches of all
195 skills for each gap claimed; and the contract-audit baseline's ROUTE-002
rows for these neighbors.

**Not checked:** live routing (no trigger eval was run); the neighbors'
full trigger-eval files; `scripts/audit-skill-contracts.py` output on the
drafts; hosting-platform storage behavior; row #105; the bodies of the
deferred candidates' neighbors beyond the searches cited; and any user
demand beyond the repository's own records. The drafted skills' behavior is
untested, and every estimate is an agent estimate, not a measurement.
