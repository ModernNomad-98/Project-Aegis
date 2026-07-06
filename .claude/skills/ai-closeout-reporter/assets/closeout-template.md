# Closeout Report Template

Copy this structure verbatim. Every section appears in every report — write
"None." rather than deleting a section. Section 2 is never optional.

---

## 1. Summary

What changed and why, in a few sentences. Written against the original request.

## 2. Intentionally not done / omitted

> REQUIRED ALWAYS. Every requested or implied deliverable that was consciously
> skipped, delivered partially, or downgraded — each with its reason. If truly
> nothing was omitted, write exactly: **None.**

- <item> — <reason it was skipped / reduced> — <where it's tracked, if anywhere>

## 3. Files touched

Exact paths from `git diff --stat` / `git status`, not from memory. Curate to
what matters; link the PR/diff for the exhaustive list when it is long.

## 4. Tests & validation run

| Command | Result |
| --- | --- |
| `<command>` | `<actual output summary — failures verbatim>` |

## 5. Evidence

Outputs, links, screenshots, PR URL, CI runs — whatever lets a human verify
without rerunning everything.

## 6. Risks & known gaps

What could bite later; what is fragile; what depends on unverified assumptions.

## 7. Skipped validation

What the change class expected but was not run, and why. "Nothing skipped." is
an acceptable entry; absence of the section is not.

## 8. Next actions / handoff

The recommended next step, and anything the next person needs to know to pick
this up cold.
