# Lane Authoring Guide — Template & Authoring Notes

Companion to `lane-authoring-guide`. One guide per lane, authored BEFORE the
lane's first unit of work.

## Citation convention

Every load-bearing claim carries one of:

- `(src/api/orders.ts:88)` — file:line for code facts;
- `(src/router/index.ts — registerRoute)` — file + symbol when lines churn;
- `(PR #61)` — for behavior established by a reviewed change;
- `(contract doc §3)` — for frozen inter-lane interfaces;
- `[unverified]` — the claim could not be checked at authoring time. An
  `[unverified]` load-bearing claim is a to-verify item for the lane's first
  task, not a fact.

A guide claim with none of these is a defect — the implementing agent cannot
tell distilled knowledge from planner assumption.

## Guide template

```markdown
# Lane Guide — <lane name>            (authored <YYYY-MM-DD>, baseline <SHA>)

Approved by: <plan-of-record doc/phase>   Coordinator: <named human/role>

## 1. Lane identity
- Surface: <paths/modules this lane owns>
- Unit of work: <the repeating unit, e.g. "one read handler + its tests">
- Sibling lanes: <names + their surfaces — one line each>

## 2. Request lifecycle (this lane's slice)
<entry point> (cite) → <hop> (cite) → … → <exit/response> (cite)
Notes: <error path, auth/tenant context propagation — cited>

## 3. Contracts
MAY RELY ON (frozen for this effort — cite the contract doc, don't restate):
- <interface/schema/invariant> (contract §, or file:line)
MUST HONOR (other lanes rely on this from us):
- <shape/behavior> (cite)
Contract changes are OUT OF LANE → raise to <coordinator>, never edit in-lane.

## 4. Recipe — one unit of work
1. Read: <the specific files/utilities to read first> (cite)
2. <step> …
3. Validate: <the tier/checks this unit must pass>
4. Done when: <unit definition-of-done>

## 5. Per-unit checklist
- [ ] contract shapes honored (§3)
- [ ] conventions reused, not reinvented: <named utilities>
- [ ] tests: <what per unit>
- [ ] no files outside §1 surface touched
- [ ] evidence captured for the closeout

## 6. MUST NOT (the boundary)
- Do not touch: <files/dirs — explicit globs>
- Do not decide: <schema changes, shared contract changes, sibling-lane
  behavior, dependency additions — as applicable>
- If a unit seems to REQUIRE crossing any line above: STOP, escalate to
  <coordinator>. Crossing with good intentions is still a collision.

## 7. Authority
This lane operates under <register entry APR-<NNN> / phase approval>. The
recipe never exceeds it.
```

## Authoring notes per section

- **§2 Lifecycle:** walk the code, don't recall it. If the planner "knows"
  the flow but the file contradicts them, the file wins and the guide
  records the file. This is the section where uncited guides do their damage.
- **§3 Contracts:** the point of a parallel effort's shared contract doc is
  that N guides cite it once. If no contract doc exists yet, writing it is a
  prerequisite (coordinate with the human) — a lane guide cannot freeze
  interfaces unilaterally.
- **§4 Recipe:** written for the lane's SECOND-best day, not its best:
  assume the implementing agent knows nothing it can't read from here. Name
  real helpers ("use `makeHandler` — src/api/util.ts:12") over abstractions
  ("follow existing patterns").
- **§6 MUST NOT:** derive it from the sibling lanes' §1 surfaces plus the
  effort's frozen decisions. Then cross-check: no path may appear in two
  lanes' §1, and every shared path (types file, router registry, fixtures)
  appears in exactly one lane's §1 and the others' §6 — or carries a named
  coordination rule ("append-only; one lane per phase touches it").

## Worked boundary example (three lanes)

| Surface | Lane A (backend read handlers) | Lane B (frontend) | Lane C (AI routing) |
| --- | --- | --- | --- |
| `src/api/read/**` | §1 owns | §6 must-not | §6 must-not |
| `src/app/routes/**` | §6 must-not | §1 owns | §6 must-not |
| `src/ai/router/**` | §6 must-not | §6 must-not | §1 owns |
| `src/shared/types.ts` | §6: append-only via coordinator | §6: read-only | §6: read-only |
| DB schema / migrations | §6 all lanes: out of scope for this effort — coordinator only | | |

The table is the exclusivity check made visible; author it once across all
lanes before finalizing any single guide.

## Staleness rule

The guide's header carries its baseline (date + SHA). When a new stage
starts, either re-verify the citations against current mainline or bump the
baseline explicitly — an implementing agent may trust the guide only as of
its stated baseline.
