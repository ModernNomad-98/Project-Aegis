# Usage signal catalog

Companion to [../SKILL.md](../SKILL.md). Field-level schema, minimization
rules, tiers, and the threshold catalog for a skill-library usage design.

## Signal schema

### Invocation event

| Field | Type | Notes |
| --- | --- | --- |
| `skill` | name (enum: shipped list) | The activated skill |
| `mode` | `auto` \| `explicit` | Trigger-matched vs named by the user |
| `at` | date (day precision suffices) | Finer precision adds risk, not value |
| `task_class` | small fixed enum (e.g. `build`, `review`, `audit`, `design`, `debug`, `other`) | Never free text |
| `session_ref` | opaque id | Correlation only; carries no content |

### Correction (wrong-fire) event

| Field | Type | Notes |
| --- | --- | --- |
| `fired` | skill name | What activated |
| `redirected_to` | skill name \| `none` | What the user invoked instead |
| `mode` | `overridden` \| `abandoned` | Redirected vs simply stopped |

### Completion hint

`skill`, `outcome ∈ {delivered, abandoned, unknown}` — coarse by design; this
is not a quality score and must not grow into one.

### Non-event (computed, not captured)

`never_fired = shipped_list − distinct(invocation.skill)` over the stated
window. Always derived from the CURRENT shipped list at computation time.

## Minimization table

| Captured | Never captured (any tier, any reason) |
| --- | --- |
| Skill names (shipped enum) | Prompt text or fragments |
| Fixed enums (`mode`, `task_class`, `outcome`) | Response/output content |
| Day-precision dates | User identifiers (names, emails, accounts) |
| Opaque session ids | Live product, company, repo, or path names |
| Counts and derived rates | Anything requiring redaction before commit |

The line: **every record must be committable to the library repo openly.**
If publishing it would leak anything, the schema captures too much.

## Evidence tiers

| Tier | Source | Sufficient for |
| --- | --- | --- |
| 1 | Host-recorded invocation events | Any threshold action, including a deprecation evidence package |
| 2 | Self-reported (closeouts/session notes naming skills used) | Investigation, trigger re-review; NOT deprecation on its own |
| 3 | Anecdote | Nothing — prompts a look at tier 1/2, never an action |

State plainly which tiers exist today. A design that assumes tier-1 hooks
the host doesn't expose is fiction with a schema.

## Threshold → action → consumer catalog

| Signal pattern (over stated window) | Action | Consumer |
| --- | --- | --- |
| Fires only `explicit`, never `auto` | Trigger-description re-review | `skill-quality-reviewer` (checks 1–2) |
| Repeated corrections toward the same neighbor | Discriminating trigger-evals + description fix on BOTH sides | Skill authors; re-review |
| Zero fires across N consecutive windows AND not exempt | Deprecation evidence package | `skill-deprecation-planner` |
| High fires + high `abandoned` | Substance review (fires but doesn't help) | `skill-quality-reviewer` (check 5) |
| One sibling wins all contested requests in a cluster | Consider absorbing the loser | `skill-quality-reviewer` → possibly `skill-deprecation-planner` |

Every row names a consumer. Counts with no consequence are decoration;
consequences with no counts are the assumption this design exists to
replace.

## Denominators

- Prefer honest raw counts over rates with invented denominators.
- Usable denominators: sessions in window, invocations in window, tasks per
  `task_class`.
- "Eligible requests" (how often SHOULD it have fired) is an estimate by
  construction — label it `estimated`, state the method, and never rank
  skills by an estimated-denominator rate alone.

## Rare-but-critical exemption list format

```
EXEMPT: <skill-name>
Reason: fires only on <rare event class — incident, recovery, refusal, rollback>;
        low usage is its success mode.
Review: substance re-review on <cadence> instead of usage threshold.
```

Written BEFORE the first count is read; additions later are allowed,
removals require the same scrutiny as a deprecation.

## Evidence-package format (handoff to skill-deprecation-planner)

```
USAGE EVIDENCE — <skill-name>
Window:        <start–end; workload representativeness note>
Tier:          <1 | 2 — and what each tier contributed>
Invocations:   <count; auto/explicit split; last-fired date>
Corrections:   <count; toward which neighbors>
Denominator:   <sessions/tasks in window; estimates labeled>
Exempt status: <not exempt | exempt (reason) — exempt skills stop here>
Blind spots:   <hosts/sessions not covered; tier-2 bias notes>
```

The package is evidence, not a verdict — the retirement decision belongs to
the planner's process and its human approver.
