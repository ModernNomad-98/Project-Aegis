# Eight readability sweep pages after pull request #705

This batch starts from the exact pull request (PR) #705 merge
`58058ca95a281491f429b6129001f300bc85fabd`. It is the FOURTH batch under
the same accepted plan (PLAN-first-batch.md `4eeaf8aa…` + AUDIT-B
`ca7e3b9f…` + STAGE0 `8cbd113f…`): the remaining limb-C pages, then the
new-page set, per the selection rule recorded in the batch-3 close.
Previous/current repository-wide estimate: unchanged — the forecast still
holds its selected-backlog total; this batch adds measurement samples only.

**Re-measure skip rule applied (two pages skipped and replaced):** the two
issue-101 setup pages (`docs/evidence/setup/issue-101-package-4a-host-feasibility.md`
and `…-offline-review.md`) each have a recorded later full-page acceptance at
`e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e` (the keeper's first recording,
2026-10-02). Re-measured at the base:
`git diff --numstat e6fc8d24… 58058ca9… -- <both paths>` produced **no
output** — zero drift and no new section — so both are skipped per the
plan's binding re-measure rule and replaced by the next pages in order, the
first two new-page skills below. No page entered the batch without the
ledger naming it pending.

Three read-only reviewers took disjoint page sets under the ledger's
up-to-three structure (tracker L2941–2947), each independent of the pages'
authors (tracker L2801): pr-publisher reviewed
`tools/aegis_delivery_control/README.md` and
`docs/roadmaps/resumable-control-plane-backlog.md`; stage-b-auditor reviewed
`docs/skills-catalog.md`, `exploratory-charter-designer`,
`mobile-journey-test-designer`; auditor-2 reviewed the readability ledger
itself (owed its own re-read per the self-cost rule),
`membership-invitation-designer`, and `observability-by-design`. All eight
pages were reviewed in full at the base head against the
[Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page)
checklist. The catalog and the ledger were structured full-page reviews
(complete section/heading maps, full openings/reading keys and normative
sections, machine link checks — 25 and 172 relative links, 0 broken — and
section sampling); reviewer-stated methods. Observed wall time:
auditor-2 ≈ 3m36s for 3 pages; stage-b-auditor ≈ 2 min for 3 pages;
pr-publisher's own set unmeasured. Active time not measured by any reviewer;
wall time is an imperfect comparison with the estimate rule's active-time
requirement.

| Page | Recorded acceptance | Re-measured drift | Full-page disposition |
| --- | --- | ---: | --- |
| `tools/aegis_delivery_control/README.md` | `8ed59cd761d156b85bf80b16246131d84159cbda` (index) | 50 | Accepted unchanged |
| `docs/roadmaps/resumable-control-plane-backlog.md` | none (carried set — cited) | not derivable | Accepted unchanged |
| `docs/skills-catalog.md` | `8ed59cd761d156b85bf80b16246131d84159cbda` (index) | 451 | Corrected: pronoun disambiguation in the D80 note — "the latter" → "(the dropped candidate itself …)"; the D80 decision mark and all decision text preserved verbatim, re-verified line-level before batch close |
| `.claude/skills/exploratory-charter-designer/SKILL.md` | none (new-page rule, D77 batch) | not derivable | Accepted unchanged |
| `.claude/skills/mobile-journey-test-designer/SKILL.md` | none (new-page rule, D77 batch) | not derivable | Accepted unchanged |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | none (self-cost rule — cited) | not derivable | Accepted unchanged (two candidates examined and declined: C1's target sentence is a dated snapshot the page itself states is left as written — the no-rewrite discipline forbids the edit; C2, BER's first use inside a dated record row, is likewise not edited — the expansion exists at L820) |
| `.claude/skills/membership-invitation-designer/SKILL.md` | none (new-page rule, D81 batch) | not derivable | Accepted unchanged |
| `.claude/skills/observability-by-design/SKILL.md` | none (new-page rule, D77 batch) | not derivable | Accepted unchanged |

Batch labels for the two new skills were corrected during review (the
assignment note had swapped them): observability-by-design was built by D77
(reconciliation L3965–3987); membership-invitation-designer by D81
(reconciliation L4093–4117) — reviewer-verified against the decision log.
The one applied correction is backlog-note prose in the catalog; no decision
mark, posture, Stop Condition, Security Rule, or governance text changed.

Candidate checks: `python -B scripts/validate-skills.py` exit 0
("OK: 204 skill(s) valid, 0 warning(s)"), `scripts/tests/test_validator.py`
exit 0, the changed-path link check exit 0 (broken 0, dead 0), and a clean
`git diff --check`. Exact-head GitHub Actions and merge remain delivery
gates. No `tools/` file edit, generated report, fixture, or `.github/`
change is part of this batch. No provider call, private input, production
operation, or host change. This new note enters the pending dated-note bucket
and is not counted among the eight accepted existing pages.
