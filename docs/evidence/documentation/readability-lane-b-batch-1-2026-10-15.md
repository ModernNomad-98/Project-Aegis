# Readability Phase 4 lane B — batch 1 Stage C record, 2026-10-15

- **Lane:** PHASE 4 FULL-PAGE RE-READ, LANE B. **Stage:** C (IMPLEMENT). **Base:**
  `e2a3e20b7c20ef8385b219b39c6405237163406f` (`origin/main` tip, the PR #769 index-rebuild merge).
- **Reader:** `readability-lane-b-implementer-c` — a single Stage C implementer agent, model DeepSeek
  (deepseek-v4-pro), who wrote none of the eight pages below and also writes this lane's ledger
  section. That second clause is the same declared deviation the 2026-10-12 remaining-page record
  states: one agent performed the reader passes and the ledger write, recorded here rather than
  presented as two agents.
- **What this page is.** The lane's tracked batch record. It is the **evidence source** every row this
  lane appends to the ledger's consolidated keeper table cites, so the ledger's `Quote` column can
  hold a verbatim fragment of a tracked page (the column contract), and it **names every row's full
  40-character acceptance revision verbatim** in its own bytes.
- **Acceptance revision bound by all eight rows of this batch:**
  `e2a3e20b7c20ef8385b219b39c6405237163406f`
  That revision resolves to itself and is contained in `refs/remotes/origin/main`
  (`git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main`
  exits 0).
- **The lane changed none of the eight read pages.** So the bytes the reader read are the bytes the
  merge receives, and the acceptance is not voided by the merge.

## 1. The instrument's figures at the base, quoted

```text
python -P -B tools/readability_acceptance/check_index.py --quiet --ref e2a3e20b7c20ef8385b219b39c6405237163406f
{
  "compared_ref": "e2a3e20b7c20ef8385b219b39c6405237163406f",
  "reader_pages_in_tree": 653,
  "accepted_on_recorded_review": 57,
  "provably_pending": 4,
  "no_recorded_acceptance": 586,
  "recorded_acceptance_within_10_lines": 0,
  "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6,
  "official_pending_count": 596
}
```

**This lane publishes no readability count of its own** (ledger "Official-count switch", D84) and
presents the figures above as the instrument's, not as its own measurement.

## 2. Lane derivation and batch selection, by command

- The lane's brief names two of the instrument's buckets as the pending set:
  `no_recorded_acceptance` (586) plus `provably_pending` (4) = **590 paths** at
  `e2a3e20b7c20ef8385b219b39c6405237163406f`, derived from the `--json` output by the same rule the
  checker's own source applies (reader pages minus emitted rows).
- Sorted by repository path, the 590 split into **four quarters of 148**. **Lane B is sorted indices
  148–295**: first `.claude/skills/file-upload-storage-architect/SKILL.md`, last
  `.claude/skills/share-link-access-architect/SKILL.md`. The quarter's actual letter span is **f
  through s inside `.claude/skills/`**, not the brief's "G through N" description; the
  command-derived quarter is authoritative. The sibling lanes' own scratch derivations
  (`_laneA_paths.json` at `wt-laneA-b1`, `_laneD.json` at the main clone) compute the same
  148/148/148/146 split of the same 590 paths, so the four quarters are disjoint and complete.
- The six `cannot_decide` (lost-commit) pages sort inside lane A's quarter region and are in no
  lane's two-bucket list; the programme assigns them separately.
- **Batch 1 = the first eight pages of lane B**, in lane order:

| # | Page | Lines at base |
| --- | --- | ---: |
| B1-1 | `.claude/skills/file-upload-storage-architect/SKILL.md` | 247 |
| B1-2 | `.claude/skills/flaky-test-detective/SKILL.md` | 195 |
| B1-3 | `.claude/skills/flaky-test-detective/references/flake-taxonomy.md` | 64 |
| B1-4 | `.claude/skills/framework-edition-tracker/SKILL.md` | 173 |
| B1-5 | `.claude/skills/framework-edition-tracker/references/edition-tracking-sheet.md` | 65 |
| B1-6 | `.claude/skills/framework-mapping-refresher/SKILL.md` | 174 |
| B1-7 | `.claude/skills/framework-mapping-refresher/references/mapping-refresh-sheet.md` | 56 |
| B1-8 | `.claude/skills/frontend-perf-engineer/SKILL.md` | 280 |

## 3. Per-page dispositions — 8 of 8 full-page re-reads

Every page below was read whole, line by line, at `e2a3e20b7c20ef8385b219b39c6405237163406f` against
[Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page).
Two complete, complementary passes were made over each page:

1. **Mechanical pass.** Over the file's full line range at the declared revision: every Markdown link
   target resolved offline against the local git object store at that revision; every 40-character
   SHA counted; every backtick-named skill reference checked to exist under `.claude/skills/`; the
   named `evals` files and `references` files existence-checked. Results: **0 broken local links,
   0 bad anchors, 0 unresolvable 40-hex tokens, 0 unresolvable named skills, every named evals/
   references file present.** The two external links (B1-3) were fetched: both HTTP 200.
2. **Prose pass.** Every line read as prose — purpose, terms, workflow, output format, checklist,
   gotchas, stop conditions and supporting-file lists — against the six acceptance bullets.

Mechanical gates: `.venv/Scripts/python.exe -B scripts/validate-skills.py` → exit 0,
`OK: 205 skill(s) valid, 0 warning(s)` (run against the venv at the clone root; the system Python
lacks PyYAML, which the validator requires).

| # | Page | Local links | External links | Broken | 40-hex tokens | Disposition |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| B1-1 | `file-upload-storage-architect/SKILL.md` | 0 | 0 | 0 | 0 | **accepted unchanged** |
| B1-2 | `flaky-test-detective/SKILL.md` | 3 | 0 | 0 | 0 | **accepted unchanged** |
| B1-3 | `flaky-test-detective/references/flake-taxonomy.md` | 1 | 2 | 0 | 0 | **accepted unchanged** |
| B1-4 | `framework-edition-tracker/SKILL.md` | 2 | 0 | 0 | 0 | **accepted unchanged** |
| B1-5 | `framework-edition-tracker/references/edition-tracking-sheet.md` | 1 | 0 | 0 | 0 | **accepted unchanged** |
| B1-6 | `framework-mapping-refresher/SKILL.md` | 2 | 0 | 0 | 0 | **accepted unchanged** |
| B1-7 | `framework-mapping-refresher/references/mapping-refresh-sheet.md` | 1 | 0 | 0 | 0 | **accepted unchanged** |
| B1-8 | `frontend-perf-engineer/SKILL.md` | 2 | 0 | 0 | 0 | **accepted unchanged** |

Local-link counts are occurrence counts; the unique targets are B1-2: 2, every other page: 1.
None of the eight pages carries an in-page anchor link, so the bad-anchor count is zero by
enumeration. Zero pages were corrected; zero lines of any read page were edited by this lane. No
new section was added to any page, so no page owes anything under the targeted-edit rule.

**The six acceptance bullets, addressed for each of the eight pages.** (a) *Purpose and audience up
front* — every page: B1-1 Purpose L17-32, B1-2 Purpose L13-21, B1-3 header + "Detail for … Loaded on
demand" L1-5, B1-4 Purpose L14-27, B1-5 L1-5, B1-6 Purpose L12-25, B1-7 L1-7, B1-8 Purpose L14-27;
each SKILL.md's Use When names when and when not to invoke. (b) *Abbreviations and coded identifiers
defined at first use* — each page carries a Terms paragraph defining its abbreviations before use:
B1-1 L8-15 (SaaS, URL, PII, RLS, CDN, MIME, XSS, DB, HTML, SVG, HTTP, PUT, GET, PDF, SLA), B1-2 L9-11
(CI, TALI, TZ, DST), B1-3 L6-7 (TZ, DST, OOM, CI), B1-4 L8-12 (OWASP, ISO, SOC 2, NIST, AI RMF, LLM),
B1-5 L6-9 (OWASP, ISO, SOC 2, NIST, RMF), B1-6 L8-10 (OWASP, PR, ISO, SOC 2), B1-7 L6-7 (PR, GAP,
edition), B1-8 L8-12 (SSR, SSG, CSR, CI, QA, HTTP, UI, E2E, API). (c) *Descriptive headings, lists or
tables, and at least one concrete example* — every page uses headed sections; concrete worked
examples exist on B1-1 (the `.png`-that-is-an-executable rejection, L121-122; the `key =
req.body.path` traversal, L207), B1-2 ("fails 7/50 shuffled, 0/50 sequential" as a classification
result, L74-76), B1-3 (the same counts sentence as ordering-dependence proof, L48-49), B1-4/5 (the
register and delta-report worked formats), B1-6/7 (the per-site edit patterns table), B1-8 (the
80 ms backend / four-second user opening, L16-20). (d) *Shipped behaviour separated from proposed
or blocked behaviour* — B1-1 separates its design from verification ("bucket-level permissions and
URL-signing … verified only if separately scoped", L116-117; "listed as unverified", L154); B1-2
separates a test bug from a product bug (L80-83); B1-4/6 state detect-vs-propose and propose-vs-apply
boundaries throughout; B1-8 separates design from measurement (L141-142, L197-198). (e) *Navigation
links current and every referenced file or command existing* — the mechanical pass above; 0 broken
local links, every named skill exists, the two external links return HTTP 200. (f) *The non-author
review itself* — this record; the reader wrote none of the eight pages, with the declared deviation
that the same reader writes this lane's ledger section.

**Purpose and normal use restated from each page alone (the acceptance contract's own non-author
test).**

- **B1-1 `file-upload-storage-architect`** — *for:* designing the upload and object-storage
  architecture of a multi-tenant SaaS: upload flow, signed-URL scope, tenancy, content validation,
  malware scanning, derivatives and retention. *Normal use:* feed it the upload inventory,
  authorization and tenant models; it returns the flow design, tenancy + signed-URL contract,
  validation/scan pipeline and retention plan, and routes the personal-data lifecycle of file
  contents to `pii-lifecycle-designer` and database RLS audits to `rls-policy-auditor`.
- **B1-2 `flaky-test-detective`** — *for:* driving one intermittently failing test to a named root
  cause, one fix and bounded repeated-run stability evidence, without retries/sleeps/loosened
  assertions. *Normal use:* invoke it explicitly (it is manual-only), classify from the taxonomy,
  reproduce deterministically, fix one cause, and close with before/after counts; product-side races
  route out as product bugs.
- **B1-3 `flake-taxonomy.md`** — *for:* the classification taxonomy, reproduction escalation ladder
  and forbidden-fix table that B1-2's workflow steps 1-2 and 5 apply. *Normal use:* read on demand
  while running B1-2 to name the category and pick the next reproduction technique.
- **B1-4 `framework-edition-tracker`** — *for:* registering which editions of external standards the
  library's mapping skills cite, detecting when a new edition ships, and producing a delta report.
  *Normal use:* build the register, verify current editions against the standards bodies (never from
  memory), flag drift, and hand the delta to `framework-mapping-refresher` — it reports, it does not
  update.
- **B1-5 `edition-tracking-sheet.md`** — *for:* the register format, verify-don't-assert discipline,
  drift statuses, delta-report structure and priority rule B1-4 applies. *Normal use:* read on demand
  while running B1-4 to fill the register and shape the delta report.
- **B1-6 `framework-mapping-refresher`** — *for:* turning a verified edition delta into concrete
  proposed edits per affected skill/reference/coverage-map site, plus new-coverage-gap findings.
  *Normal use:* consume the tracker's verified delta, sweep every citing site, propose per-site edits
  preserving meaning, surface gaps, and flag the set for human review and `library-diff-reviewer` —
  it proposes, never applies.
- **B1-7 `mapping-refresh-sheet.md`** — *for:* the site-sweep checklist, change-type-to-edit
  patterns, meaning-preservation and gap-surfacing rules B1-6 applies. *Normal use:* read on demand
  while running B1-6 to locate sites and shape proposals.
- **B1-8 `frontend-perf-engineer`** — *for:* designing the frontend's performance work: metric model
  per device/network class, bundle and asset strategy, rendering path, runtime fixes, perceived
  performance and CI budget gates. *Normal use:* pin the symptom to a metric and device class, audit
  weight before tuning, design splitting/assets/rendering/runtime fixes and budgets, and hand
  measurement to `performance-test-harness` and build QA to `vite-build-qa-engineer`.

## 4. Count honesty

- **This lane publishes no readability count of its own** and cites the instrument, as the D84 switch
  requires.
- The instrument classifies the page tree at `--ref` and reads recorded acceptances from the
  committed index JSON. So: **the eight appended rows change nothing until the index rebuild** (the
  two-commit follow-up or the merger-side rebuild the ledger already names); the only movement at
  this lane's head is this lane's own new page, which enters `no_recorded_acceptance`.
- The ledger append adds a dated section of more than 10 lines, so **the ledger stays pending** and
  owes its own independent full-page re-read — the self-cost every prior ledger update states.
- The instrument figures at the base are quoted in section 1 and are not re-derived here.

## 5. The row-quote strings, verbatim

Each line below appears in this file byte-for-byte and is copied verbatim into the ledger row whose
stable ID is prefixed by the same page label. Every line also contains the full 40-character
acceptance revision, which is the second binding rule the validator enforces.

```text
B1-1 accepted: .claude/skills/file-upload-storage-architect/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B1-2 accepted: .claude/skills/flaky-test-detective/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B1-3 accepted: .claude/skills/flaky-test-detective/references/flake-taxonomy.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B1-4 accepted: .claude/skills/framework-edition-tracker/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B1-5 accepted: .claude/skills/framework-edition-tracker/references/edition-tracking-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B1-6 accepted: .claude/skills/framework-mapping-refresher/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B1-7 accepted: .claude/skills/framework-mapping-refresher/references/mapping-refresh-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
B1-8 accepted: .claude/skills/frontend-perf-engineer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
```

## 6. What this lane did not do

It rewrote no dated snapshot; edited, reordered or deleted no existing keeper row; edited none of the
eight read pages; added no new section to any page; bound no acceptance row to the lane's own
unmerged head; ran no `build_index.py --write` and rebuilt no `tools/` artifact; re-read none of
the six lost-commit pages of the `cannot_decide` bucket; and claims no authority beyond recording.
The batching procedure "does not grant provider, private-input, real-host or deployment authority"
(ledger, batching section). The reader is the DeepSeek deepseek-v4-pro model, stated per the
repository's agent-attribution rule.
