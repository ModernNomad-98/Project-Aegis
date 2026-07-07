# Skill Quality Review — per-check criteria

The mechanical validator (`scripts/validate-skills.py`) is the entry gate.
Everything it enforces — frontmatter parse, `name` == directory, description
present and < 1024 chars, no broad `allowed-tools`, SKILL.md < 500 lines, all
nine sections present, `evals/*.json` parse, catalog + README registration,
duplicate and reserved-name collisions — is settled by its exit code and is
never re-checked, re-implemented, or re-scored by this review. A validator
PASS admits the skill to review; it contributes nothing to any verdict below.

## Verdict semantics

- **PASS** — criterion met; no action needed.
- **CONCERN** — quality risk with evidence; ship is defensible only with a
  written rationale, revise is the default.
- **FAIL** — the skill should not ship as-is on this axis; evidence quoted.

Roll-up to the overall recommendation:

| Situation | Recommendation |
|---|---|
| All PASS, or isolated CONCERNs with rationale | **ship** |
| Any FAIL on checks 1, 2, 4, 5, or 7; or CONCERNs on 3+ checks | **revise** (list the required changes per check) |
| Check 3 FAIL where the new content fits an additive diff to a shipped skill | **make-it-an-extension** (name the base skill) |
| Check 6 FAIL (multiple jobs) plus check 2/3 FAILs; or the skill's job is already fully owned elsewhere | **reject** (or split; say which) |

## Check 1 — trigger quality

A description is trigger-oriented when a model holding a user request can
answer from the description alone: does this skill WIN this request, and on
which nearby requests must it YIELD?

Test each element:

- **Situation present** — at least one "Use when …" phrased as a user
  situation, not a capability ("use when a spreadsheet needs cleaning", not
  "handles spreadsheets").
- **Yield clause present** — at least one "Do NOT use …" naming the neighbor
  that wins instead. In a library at this density, a description with no
  yield clause is a CONCERN by default.
- **Vague verbs** — "helps with", "handles", "supports", "assists" carry no
  trigger information; their presence as the primary verb is a FAIL signal.
- **Standard reference examples** (`docs/skill-generation-standard.md` §2):
  good — "Convert a messy .xlsx export into a normalized sheet… Use when the
  user hands you a spreadsheet to clean"; bad — "Helps with spreadsheets."

Descriptive-not-trigger-oriented is a FAIL even when specific and well
under the length limit: "This skill audits RLS policies for recursion and
broad grants" describes the mechanism but never says when to fire.

## Check 2 — trigger overlap/collision (highest value)

Procedure:

1. Extract every shipped description:
   `grep -h "^description:" .claude/skills/*/SKILL.md` (or read
   `docs/skills-catalog.md` trigger summaries, then confirm against
   frontmatter — the frontmatter is authoritative).
2. For the skill under review, write 3–5 plausible user requests that should
   invoke it (take them from its own Use When).
3. For each request, ask: does any OTHER shipped description also plausibly
   win it? Symmetrically: do the target's triggers capture requests a
   shipped skill owns?
4. For every hit, record: the colliding skill's name, the confusing request,
   and which skill SHOULD win it.

Scoring:

- Overlap resolved by explicit yield clauses on BOTH sides **and** a
  trigger-evals case naming that exact neighbor → PASS (documented seam).
- Overlap with discrimination on one side only, or none → CONCERN.
- The target would fire on a shipped skill's core case (or vice versa) with
  no yield clause → FAIL; the collision must be named in the report.

Sweep the WHOLE corpus, not the skill's own cluster: the confusable neighbor
is often cross-phase (agent authority vs end-user RBAC;
`model-poisoning-reviewer` LLM04 vs `memory-context-poisoning-reviewer`
ASI06; evidence policy vs closeout reporting).

Also judge near-miss NAMES here: the validator blocks exact duplicates and
exact `RESERVED_BUNDLED_NAMES` matches only. A name one word away from a
bundled skill (`code-review-helper` vs bundled `code-review`) or from a
shipped skill confuses invocation and is a CONCERN/FAIL by closeness.

## Check 3 — duplication / extension

- Compare the skill's Purpose + Workflow against the nearest shipped skills
  (read them in full, not just descriptions).
- Substantial duplication = a stranger reading both would say they do the
  same job for the same trigger, differing in wording or one input.
- The library's precedent for the fix: **extension over clone** — LLM03
  (AI/ML supply chain) and ASI04 (agentic supply chain: MCP servers,
  tool/skill registries, plugins) both landed as scoped additive diffs to
  `supply-chain-security-reviewer`, not as new skills.
- Recommend make-it-an-extension when: the genuinely new content is a
  bounded slice (a new surface, a new framework edition, a new attack class)
  that fits the base skill's Purpose without changing its verdict shape.
- Recommend a separate skill when: trigger situations are disjoint, the
  output artifact differs in kind, or the base skill would need a new
  Output Format to absorb it.

## Check 4 — eval integrity

`evals/evals.json` must test the boundary, not decorate it. Required case
types (repo convention, standard §6): happy path, genuine edge,
should-not-trigger, should-not-do/refusal.

Hollow patterns (each named finding cites the case id):

- **Workflow echo** — assertions restate Workflow steps ("runs the checks,
  produces the report") instead of an observable outcome for THIS prompt.
- **Strawman negative** — the should-not-trigger prompt is something no
  skill would route here ("write a poem"); a real negative is a request the
  nearest neighbor actually owns.
- **Adjective edge** — the "edge" is the happy path with an intensifier
  ("a really large skill"), not a boundary the Workflow or Gotchas handle
  differently.
- **Toothless refusal** — the should-not-do case asserts behavior the
  SKILL.md never promises (no matching Stop Condition), so nothing anchors
  the refusal.
- **Assertion-free case** — `assertions` that cannot be judged true/false
  against an actual transcript.

`evals/trigger-evals.json` (required when the trigger overlaps — at this
library density, expect it): the `overlaps_with` list and cases must name
the neighbors check 2 actually found. Discriminating only against easy,
distant skills while omitting the real collider is a FAIL on this check.

## Check 5 — section substance

Present-but-empty detection, per section:

- **Purpose** — states what is produced and for whom; not a restated
  description.
- **Use When** — situations plus counter-examples; "use when needed" = empty.
- **Inputs to Inspect** — concrete files/paths/commands; an input list the
  Workflow never uses is filler.
- **Workflow** — ordered, executable by a stranger; each step has an output
  or a decision.
- **Output Format** — the deliverable's exact shape; "a report" = empty.
- **Validation Checklist** — checkable statements about THIS skill's
  output, not generic virtues.
- **Gotchas** — earned failure modes (each implies a story); platitudes
  ("be careful with edge cases") = empty.
- **Stop Conditions** — the load-bearing one: each entry names a condition
  and the refusal/halt it triggers, including who gets asked. "Ask the user
  when unsure" alone = empty. Side-effecting skills must name the
  irreversible step here (standard §5).
- **Supporting Files** — every listed file exists; every shipped
  `references/*` file is listed.

## Check 6 — scope discipline

- Count the distinct jobs: verbs-with-objects in Purpose + Output Format. A
  skill producing three unrelated artifacts for three unrelated triggers is
  a catch-all → split.
- Smells: "and also", multiple Output Format blocks for different modes,
  Use When entries that never co-occur in one user's head, a description
  that needs semicolons to hold its job list together (a shaped verdict
  list is fine; a job list is not).
- Narrow-but-deep is the target; narrow-but-trivial (a skill wrapping one
  grep) is a CONCERN the other direction — fold it into its natural parent.

## Check 7 — invocation posture

| Behavior found in SKILL.md | Required posture |
|---|---|
| Edits files/config outside its own report, runs state-changing commands, arms CI/deploys, calls external networks, spends money/tokens on execution | `disable-model-invocation: true` (manual-only) + irreversible step named in Stop Conditions |
| Pure read/review/design/report — produces findings or a proposal artifact, changes nothing | auto-invocable: omit the field (or explicit `false`) |

- Judge from the WORKFLOW TEXT, not the frontmatter claim: a "review" skill
  whose step 6 is "apply the fix" is side-effecting.
- Posture is re-judged on every revision — side effects added later must
  flip the flag.
- Reference points from the shipped library: `code-reviewer` auto /
  `code-simplifier` manual; `rls-policy-auditor` auto (delivers migrations,
  never runs DDL) / `appsec-implementer` manual (edits code).

## Evidence discipline

Every non-PASS verdict quotes its evidence: the description phrase, the
named colliding skill plus the confusing request, the eval case id, the
empty section text. A CONCERN that cannot cite text is an opinion — drop it
or label it explicitly as reviewer opinion outside the verdict table.
