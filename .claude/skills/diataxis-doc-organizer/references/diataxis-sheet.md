# Diátaxis Sheet

Detail for `diataxis-doc-organizer`. Read on demand.

## The two axes

```
                 PRACTICAL (steps)      THEORETICAL (knowledge)
ACQUISITION      Tutorial               Explanation
(learning)       (learn by doing)       (understand the why)

APPLICATION      How-to guide           Reference
(working)        (achieve a goal)       (look up a fact)
```

## The four modes

| Mode | Serves | Voice | Belongs | Anti-pattern |
|---|---|---|---|---|
| **Tutorial** | A beginner learning | Teacher, hand-held, "we" | A lesson with guaranteed success; minimal choices | Reference dumps; assuming knowledge |
| **How-to guide** | A competent user doing a task | Recipe, imperative | Steps to one real goal; assumes competence | Teaching; tangents; the "why" |
| **Reference** | Someone looking up a fact | Dry, structured, complete | Accurate description of the machinery | Chatty prose; teaching; incompleteness |
| **Explanation** | Someone wanting to understand | Discursive, reflective | Background, why, tradeoffs, context | Step-by-step instructions |

## Classification decision tree

1. Is the reader LEARNING or WORKING?
   - Learning → Tutorial or Explanation
   - Working → How-to or Reference
2. Does the page give STEPS or KNOWLEDGE?
   - Steps + learning → **Tutorial**
   - Steps + working → **How-to**
   - Knowledge + working → **Reference**
   - Knowledge + learning → **Explanation**
3. If it does two of these → it's a two-job doc → SPLIT.

## Split patterns (two-job docs)

| Symptom | Split into |
|---|---|
| Tutorial + big config tables | Tutorial (lesson) + Reference (tables, linked) |
| How-to + architecture essay | How-to (steps) + Explanation (the why, linked) |
| Reference written like a lesson | Reference (dry) + Tutorial/Explanation as needed |
| Explanation with embedded steps | Explanation + How-to (the steps, linked) |

## Cross-link, don't embed

- How-to → links to the reference it needs.
- Tutorial → links to explanation for the curious.
- Reference → single source (ideally generated →
  `api-doc-generator-designer`), linked from everywhere, duplicated
  nowhere.

## Maintenance

- Classify every new doc on creation (which of the four?).
- If a page starts serving two needs, split it before it rots the set.
- The tree's top level IS the four modes (or a clear mapping), so readers
  self-route by need.
