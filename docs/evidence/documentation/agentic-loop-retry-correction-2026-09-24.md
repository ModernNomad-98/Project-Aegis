# Agentic loop retry correction — 2026-09-24

> **Current reading, checked 2026-09-24:** Pull request (PR) #211 merged the
> [corrected agentic-loop skill](../../../.claude/skills/agentic-loop-designer/SKILL.md).
> Later instructions to record time after merge and the 557/51/506 page
> inventory below describe the pre-merge checkpoint. Use the
> [documentation ledger](../../roadmaps/aegis-documentation-readability-backlog.md)
> for the current inventory.

**Terms:** Coordinated Universal Time (UTC) records review times;
JavaScript Object Notation (JSON) is the format of the evaluation files;
estimated time to complete (ETA) is the planning estimate.

## Why this page needed correction

The `agentic-loop-designer` skill said that a second identical timeout proved
the failure was deterministic. A temporary outage can produce two timeouts,
so that conclusion was unsupported. The full-page documentation review after
pull request #209 left this page open as a named follow-up.

## What changed

The skill now requires failure classification before retry. Policy denials and
evidenced permanent errors stop without retry. A transient operation may be
retried at most once on identical input only when its prior effect is known
absent or safe, idempotent repetition is proven despite an uncertain response.
The retry must also fit the iteration and cost ceilings and any required
delay. A second transient failure means **retry exhausted, cause unresolved**.
A timeout after a possible side effect stops as **unknown outcome** unless
safe repetition is established. An input hash proves the input bytes only; it
does not prove external state or prevent duplicate effects.

The skill's behavior and trigger evaluation cases now check the same rule,
including a timed-out write with uncertain effect. These are offline design
cases. They do not call a provider or authorize a live retry.

## Page review and evidence

| Page | Outcome | Reason |
| --- | --- | --- |
| `.claude/skills/agentic-loop-designer/SKILL.md` | **Corrected and accepted** | Purpose, workflow, output format, checklist, examples and stop conditions agree on retry safety and distinguish all terminal states. First-use terms are explained. Links and design-only authority remain. |

The two accompanying evaluation files are contract checks, not additional
Markdown pages. Independent read-only review ran from **00:57:49 to 00:58:55
UTC** on 2026-09-24 and found no remaining blocker after the response-versus-
effect wording was corrected. The reviewer checked all three changed files,
the safety boundary, and the evaluation cases. Local verification parsed both
JSON files, passed `scripts/validate-skills.py` with **185 valid skills and zero
warnings**, and passed `git diff --check`. No provider call was made.

The original ETA and the current ETA were both **1–2 active hours**. Record the
observed first-work-to-merge wall time in the pull request after merge. This
single accepted existing page increases the full-page acceptance count from
50 to 51. With this evidence note added, the expected inventory is 557
Markdown pages and 506 pages without full-page acceptance. The selected
backlog forecast remains **150–394 active hours** until the next scheduled
five-merge re-estimate.
