# Conflict Resolution — Worked Examples

Supporting detail for `source-of-truth-reconciler`. Read on demand.

## Example 1 — Doc vs code (IS-question → repo state wins)

Claim A: `docs/architecture.md:41` — "the public API is rate-limited to
100 req/min per key."
Claim B: `middleware/ratelimit.ts:17` — `limit: 60`.

- Type: IS (what does the system do today?).
- Verdict: code wins (rule 2). Current behavior is 60 req/min.
- Assumption surfaced: no other middleware overrides this value (checked the
  middleware chain; none found).
- Follow-up proposed: correct `docs/architecture.md:41`, OR — if 100 was the
  intended contract — open a SHOULD-conflict for the owner to decide. Note the
  drift either way; do not silently edit the doc while answering.

## Example 2 — Instruction references deleted state (stale instruction)

Instruction: "Continue from the plan on branch `feature/billing-v2`."
Repo state: branch absent; PR #87 shows it merged and deleted three weeks ago.

- Verdict: instruction is stale, not wrong — its intent (continue the billing
  work) survives; its referent (the branch) does not.
- Correct behavior: cite the merge commit, state what the merged PR contains,
  and confirm the intended next step with the human.
- Wrong behaviors: recreating the branch from an old ref and continuing as if
  nothing happened (silent obedience), or ignoring the reference entirely
  (silent override).

## Example 3 — Dueling canonical docs (no precedence winner → escalate)

`docs/standards/testing.md` ("canonical, 2026-03") requires coverage ≥ 80%.
`docs/quality-policy.md` ("single source of truth, 2026-05") requires ≥ 70%
"per the Q2 revision".

- Both are current, both claim authority, and no reconciliation record ranks
  them. Newer date is NOT sufficient — the newer file may be the rogue one.
- Verdict: blocked. Present both claims with anchors, ask the owner which
  governs, and propose recording the answer in a reconciliation note so the
  next agent doesn't re-litigate it.

## Anti-pattern gallery

| Anti-pattern | Why it fails |
| --- | --- |
| "The newest file wins" | Timestamps track edits, not authority. |
| Averaging the claims (e.g. "80 req/min") | Invents a third truth nobody wrote. |
| Editing the losing doc mid-task | Side-effect edit nobody reviewed. |
| Trusting memory over the repo | Memory reflects when it was written, not now. |
| Deciding security conflicts by precedence | Those need a human (approval boundary). |
