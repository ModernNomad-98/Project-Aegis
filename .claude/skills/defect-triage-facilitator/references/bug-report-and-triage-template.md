# Bug report and triage template: defect-triage-facilitator artifact

## 1. Bug report fields

| Field | Required content | Missing-field behaviour |
| --- | --- | --- |
| Summary | one-line observed vs expected | rewrite, mark assumptions |
| Reproduction | ordered steps, data/role/environment | UNKNOWN if not supplied |
| Expected vs actual | observable outcomes | UNKNOWN |
| Environment | build/version, tenant, browser/device | UNKNOWN |
| Evidence | logs, screenshots, trace ids | required for S1/S2 |
| Suspected area | component/service if known | optional |
| Impact | frequency, affected users/tenants | UNKNOWN if not supplied |

### Completed example (fictional)

| Field | Entry |
| --- | --- |
| Summary | Saved search returns results for the wrong tenant after the account switch |
| Reproduction | 1) login as tenant A; 2) create a saved search; 3) switch to tenant B; 4) open the saved search |
| Expected vs actual | Expected: tenant-B scoped results; actual: tenant-A result ids appear in the list |
| Environment | build 2026.10.3, tenant A/B test accounts, Chrome 130 |
| Evidence | trace id, screenshot, server log line (redacted) |
| Suspected area | saved-search query builder tenant filter |
| Impact | 1 of 3 tenants reported, intermittent |
| Triage | S2 / intermittent / some tenants / potential security flag -> route to tenant-isolation-reviewer; owner = search team; next action = reproduce in staging |

## 2. Triage axes

| Axis | Levels | Rationale requirement |
| --- | --- | --- |
| Severity | S1 blocking/data-loss/security, S2 major, S3 minor, S4 cosmetic | cite consequence and evidence |
| Frequency | always, common, intermittent, rare | cite observations |
| Customer impact | all tenants, some tenants, single account, internal | cite affected scope |
| Security | security-flagged, potential, not-security | route if flagged |
| Release risk | must-fix, fix-in-next, defer with owner | cite release context |

## 3. Decision record

| Defect | Axes result | Owner | Next action | Assumptions/unknowns |
| --- | --- | --- | --- | --- |
| <id> | <S2 / common / some tenants / not-security / fix-in-next> | <name> | <reproduce, then fix in owner cycle> | <missing env> |

Rules: no invented facts, no fix promise, no release date the triage cannot authorize.

## 4. Completion checklist

- [ ] Report complete or UNKNOWN-labelled.
- [ ] Every decision cites axes + rationale.
- [ ] One owner + one next action per defect.
- [ ] Security/release-risk routed; duplicates recorded.
