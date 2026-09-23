# Offline setup routing guide readability batch — 2026-09-23

## Scope and reason

This bounded batch makes the implemented [offline setup routing contract](../../../tools/aegis_setup/README.md)
usable from its own first screen. Its previous opening named issue #101 package 3
and then listed fields and statuses. A maintainer had to consult the setup plan
and tests to learn who uses the package, what a normal offline check does, and
why a validated recommendation is only advice.

The guide now explains its maintainer audience, links to the
[issue #101 plan](../../roadmaps/aegis-setup-routing-plan.md), shows a
synthetic request followed by recommendation and abstention, and maps its four
entry points. The detailed field, size, failure and compatibility contracts
remain on the page. The [documentation index](../../README.md) now links
directly to the implemented package guide. One row in the
[readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md)
records this batch. These four paths are the entire edit scope.

The example uses only local validation functions. It does not prove installed
agent or skill compatibility, connect a provider, invoke an assistant, dispatch
work or authorize a later package. The package-4 host and evaluation work in
the plan remains separate. The full repository documentation sweep is open.

## Verification and limits

- The README example was executed from the repository root with `python -B`;
  it printed `recommend ('reviewer',) ('api',)` and `abstain () ()`, matching the
  guide. Its request and response shapes were checked against
  [the offline contract tests](../../../tools/aegis_setup/tests/test_routing_contract.py).
- `python -B -m unittest tools.aegis_setup.tests.test_routing_contract -v`
  passed all 9 synthetic contract tests.
- `python -B scripts/validate-skills.py` passed: 185 skills valid, zero
  warnings.
- All 53 local links in the four changed pages resolved, including the new
  `#offline-checks` anchor. `git diff --check` passed.
- Independent read-only review first found undefined `API` and `JSON` and a
  stale latest-file count in the backlog footer. Those were corrected; the
  reviewer then found no blocker. The reviewer reproduced the example output,
  ran all nine contract tests, checked the anchor and links, and confirmed the
  guide grants no host, provider or dispatch authority. The review took 1 minute
  7 seconds before the corrections; the follow-up was a separate short pass.

Work began at **2026-09-23 17:58:19 UTC**. The previous and current full
documentation estimate is **80–200 active hours**. This batch is estimated at
**1–3 active hours**; active-only time is not instrumented. The selected
remaining backlog at the start was **175–394 active hours**. This readability
batch does not lower that forecast without a separate review.
