# Owner questions and answers

Every question put to the owner, the owner's answer, and the time, in the owner's local time zone (America/Los_Angeles). Answers are recorded word for word where the tool or message record holds them. When an answer was not recorded, this file says so. Decision records and the time log quote from this file.

## Q-1 — 2026-11-14 (asked during the parallel-delivery work; exact minute not recorded, between 19:34 and 19:36 PST)

Question (two parts): (1) The owner's new message said "push and merge when ready", but the owner's explicit P0 directive said "Do not merge, not even under SDP-2. I will merge." Which applies? (2) The new message said "group small fixes into one PR to save on cost", but the P0 objective said three separate PRs. Which applies?

Options offered: (1) Keep no-merge (recommended) / Authorize me to merge. (2) Keep three separate PRs (recommended) / Group PR-C into PR-B / One combined PR.

Answer (verbatim from the structured answer record): selected "Authorize me to merge"; selected "Keep three separate PRs (Recommended)".

## Q-2 — 2026-11-14 (from the saved resume prompt; asked before the session start)

Question: The P0 preflight requires the audit evidence package. The expected roots were absent and a bounded search found nothing. Please supply the unzipped package or its actual nested folder (README.md, REPORT-full.md, plan/HANDOFF.md).

Owner answer (verbatim except the download path, redacted for privacy): "[download path redacted for privacy] unzip and find it"

## Q-3 — 2026-11-14 (asked around 22:56-23:00 PST; exact time not recorded)

Question (two parts): (1) PR-A round 2 has green required checks but a new automated review raised six blocking contradictions; should we run one more PR-A implementation round, pause PR-A and focus on the new P0 workstream, or merge with documented exceptions? (2) The merge gate requires every applicable check green; a known non-required check fails on every PR head and its fix needs a protected path; do you grant a recorded exception, or must the PRs wait?

Owner answer: not recorded — the interactive question hit a tool timeout before an answer was captured, and the question was repeated in prose. As of 2026-11-14 23:25 PST no answer is recorded in this file.

## Q-4 — 2026-11-14 (asked with this tracker setup; exact time not recorded)

Question: Which email address should consumers use to send experience and feedback (or should the repository issue tracker be the only route)? This is needed to complete docs/consumer-feedback.md.

Owner answer (2026-11-15 04:43:37 PST, in Q-6): "Feedback: issues only." Consequently the public issue-tracker route is the only route; no email address is published (P-1 resolved in Q-6).


## Q-5 — 2026-11-15 00:24 PST (from the independent tracker accuracy check)

Question: two privacy/confirmation items before the tracker's first save: (P-1) may the consumer-feedback document keep the public repository issue-tracker address, which contains the project's public account/repository name, or should the send route be email-only / described generically? (P-2) the anonymized log states that no owner experience level was recorded — please confirm, or state the level so the required one-line context can be added.

Owner answer: not recorded yet.


## Q-6 — 2026-11-15 04:43:37 PST (PR-A path / merge conditions; answered after a 4 h 19 min break)

Question (condensed from the escalation): choose PR-A path A (finish PR-A: fix the new review's real high findings, then Stage D/E/F round 2 and merge) or B (pause PR-A, move to WS2 and the tracker); grant or withhold the known non-required aegis-verdict-gate exception; and give the consumer feedback route.

Owner answer (verbatim): "A, with conditions: grant the verdict-gate exception for #1095 only, recorded as a one-PR exception because that gate is red on every PR by design, and only if validate-skills and gate-guard are green. Do not make post-round findings non-gating blind: list every open finding with its severity in the PR body; if all are minor or info, open one follow-up issue for them and proceed; if any is major, stop and ask me. Post a short body (summary, closure before/after table, reviewer verdicts; link the rest). Feedback: issues only. When PR-A is done: WS2 go r3."


Q-4 clarification (2026-11-15): the email address is not needed; the owner chose "issues only", so consumer-feedback.md and its template now name the public issue tracker as the only route.
