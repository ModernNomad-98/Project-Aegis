# Coordinator idle/running check log

This page explains [`coordinator-idle-checks.jsonl`](coordinator-idle-checks.jsonl),
the append-only record of what the recurring coordinator cadence found and did.

**Reading boundary.** The log records what a coordinator observed and assigned
at a moment in time. It is not a work queue, not an approval grant, and not a
statement that the assigned work was completed or is still open. For current
authority and status, read the
[owner approval register](../approvals/APPROVAL_REGISTER.md) and the owning
backlog. Counts are point-in-time observations of subagent state and carry no
independent meaning once the session that produced them has ended.

## Why this is a tracked file at all

The coordinator cadence wakes periodically, counts how many subagents are idle
versus running, and assigns the idle capacity to unblocked work. Recording that
only in session state fails exactly when it matters: session-local state does
not survive a new chat, so a fresh coordinator cannot tell whether the previous
check ran, when, or what it handed out. A tracked file survives that boundary,
and a file that is edited in place by hand grows conflicts instead of history —
hence append-only [JSON Lines](https://jsonlines.org/), one object per line.

## Format

One JSON object per line, no trailing commas, no wrapping array:

```json
{"checked_at":"2026-10-01T19:00:00-07:00","idle":69,"running":3,"action":"assigned PR #601 security LOW fix to author-skill-fixes-1; no other unblocked work"}
```

| Field | Meaning |
| --- | --- |
| `checked_at` | When the check ran: ISO 8601 with a UTC offset (`Z` or `±HH:MM`). The offset is mandatory so entries from different timezones stay comparable. |
| `idle` | Subagents idle at that moment, as a non-negative integer. |
| `running` | Subagents running at that moment, as a non-negative integer. |
| `action` | What the check did with the unblocked work, on one line. Write `no other unblocked work` when that is the honest answer. |

The object has no schema version, status or `id` field on purpose: the format
is small enough that a reader can parse it unaided, and an entry cannot be
retracted once the work it describes has moved on.

## Appending an entry

Do not hand-write the JSON — a mis-escaped quote silently breaks every reader
of the file. Use the helper, which validates the timestamp and the counts and
refuses malformed input instead of writing it:

```bash
python -P scripts/append-idle-check.py \
    --checked-at 2026-10-01T19:00:00-07:00 \
    --idle 69 --running 3 \
    --action "assigned PR #601 security LOW fix to author-skill-fixes-1; no other unblocked work"
```

It prints the line it appended and exits `0`; rejected input exits `2` with the
reason on stderr and writes nothing; an unwritable log path exits `1`.

## Why the explanation lives in this sibling file

JSON Lines has no comment syntax — a header line would have to be a JSON object,
which every reader would then have to special-case, and the first thing a
consumer would have to do is skip it. Keeping the prose in this sibling Markdown
file leaves the `.jsonl` parseable by any line-oriented reader with no
exceptions. The log's location, beside the other dated operational records under
`docs/roadmaps/`, keeps the data with the roadmap material it reports on while
leaving `docs/evidence/`, a curated index of selected evidence pages, untouched.
