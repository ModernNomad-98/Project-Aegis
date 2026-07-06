# QA, Test Architecture & Validation

QA skills for risk-based validation, test harnesses, E2E, CI evidence, and release confidence.

These are product-agnostic, repeatable Claude skills. They are meant to become executable `SKILL.md` workflows, not one-off prompts.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 181 | Test Strategy Authoring | P0 | Define test layers, risk coverage, ownership, fixtures, environments, and required evidence. |
| 182 | Risk-Based Validation Matrix | P0 | Select docs-only, fast, full, backup-gated, deployment-gated, or production-safe validation based on change risk. |
| 183 | Unit Test Design | P1 | Test pure functions, validators, reducers, mappers, state machines, and small components in isolation. |
| 184 | Integration Test Design | P0 | Test modules through realistic service, command, database, auth, and permission boundaries. |
| 185 | Contract Test Design | P1 | Validate API, command, provider, webhook, and edge-function contracts without relying on UI tests. |
| 186 | RLS Test Harness Design | P0 | Prove tenant isolation, role authorization, denied writes, and sensitive-column protection. |
| 187 | E2E Journey Design | P1 | Test critical workflows through browser automation with deterministic data and stable selectors. |
| 188 | Production-Safe Smoke Testing | P0 | Run safe checks against production without creating unsafe records or using fixture-only routes. |
| 189 | Fixture Mode E2E Design | P1 | Use local or test-only routes and deterministic fixtures for broad UI regression coverage. |
| 190 | Regression-First Bug Fixing | P0 | Write a failing test that reproduces the bug before implementing the fix. |
| 191 | Golden Path Test Mapping | P1 | Map the most important happy paths for each user role and business-critical workflow. |
| 192 | Negative Path Test Mapping | P0 | Test unauthorized, invalid, expired, missing, duplicated, conflicting, and out-of-order scenarios. |
| 193 | Boundary Value Test Design | P1 | Test limits, empty inputs, maximum sizes, date boundaries, timezones, and precision boundaries. |
| 194 | Property-Based Test Design | P2 | Generate broad input combinations for validation, parsing, math, state, and transformation logic. |
| 195 | Mutation Testing Review | P2 | Use mutation thinking to identify tests that pass without proving important behavior. |
| 196 | Test Data Isolation | P0 | Keep test data scoped, disposable, traceable, and isolated from demo or production tenants. |
| 197 | Seed Fixture Governance | P1 | Create deterministic seed data with clear roles, tenants, resources, and cleanup expectations. |
| 198 | Test Tenant Provisioning | P0 | Create test tenants and users for repeatable auth, RLS, integration, and E2E validation. |
| 199 | Test Cleanup Strategy | P1 | Use finalizers, scoped namespaces, TTLs, and cleanup jobs without deleting real data. |
| 200 | Mock Strategy Design | P1 | Choose mocks, fakes, stubs, adapters, recordings, or live tests based on risk and confidence. |
| 201 | Test Double Contract Review | P1 | Ensure mocks and fakes stay aligned with real provider and database behavior. |
| 202 | Snapshot Test Governance | P2 | Use snapshots only for stable, meaningful outputs with explicit update review. |
| 203 | Visual Regression Test Design | P2 | Capture critical UI states with stable data, deterministic viewport, and reviewable diffs. |
| 204 | Accessibility Test Harness | P1 | Automate and manually verify keyboard, labels, focus, contrast, and screen reader expectations. |
| 205 | Performance Test Harness | P1 | Measure load, render, query, API, edge function, and background job performance. |
| 206 | Load Test Planning | P2 | Plan realistic traffic, tenants, data volume, ramp-up, success metrics, and safe environments. |
| 207 | Soak Test Planning | P2 | Run long-duration tests to detect memory leaks, queue buildup, token expiry, and degradation. |
| 208 | Chaos Test Planning | P2 | Inject service failures, timeouts, retries, and partial outage scenarios safely. |
| 209 | Flake Detection | P1 | Identify nondeterministic tests, timing dependencies, shared state, ordering assumptions, and environment leaks. |
| 210 | Flake Quarantine Governance | P1 | Quarantine only with ownership, issue, expiry, and repair plan. |
| 211 | CI Shard Design | P1 | Split large suites into stable shards with run IDs, isolated resources, and useful artifacts. |
| 212 | Parallel Test Isolation | P1 | Prevent parallel tests from sharing users, tenants, records, ports, browser state, or queues unsafely. |
| 213 | Test Timeout Policy | P1 | Set timeouts that distinguish slow failure, infra instability, hidden hangs, and real product problems. |
| 214 | Hidden Runtime Marker Detection | P0 | Scan logs for console errors, unhandled rejections, skipped tests, auth failures, and hidden runtime failures. |
| 215 | CI Failure Classification | P0 | Classify failure as product bug, test bug, missing secret, timeout-only, infra failure, or skipped runtime. |
| 216 | GitHub Actions Evidence Review | P0 | Verify required checks, job status, artifacts, logs, and final gates before accepting a change. |
| 217 | Local Validation Protocol | P0 | Run relevant local tests, typecheck, build, lint, and project-specific validation before pushing. |
| 218 | Docs-Only Validation | P0 | Confirm documentation-only changes run lightweight checks and avoid unnecessary full validation. |
| 219 | Backup-Gated Validation | P0 | Require backup evidence, migration verification, and smoke tests for schema, RLS, or storage changes. |
| 220 | Deployment-Gated Validation | P1 | Separate tests that can run before deploy from smoke tests that require deployed state. |
| 221 | Manual QA Script Authoring | P1 | Write step-by-step manual checks with expected results, screenshots, roles, and cleanup notes. |
| 222 | Clickthrough Testing Protocol | P1 | Define systematic UI walkthroughs for navigation, forms, dialogs, permissions, and error states. |
| 223 | Screenshot Evidence Capture | P2 | Capture screenshots for important UI changes, regressions, and manual verification evidence. |
| 224 | Bug Report Authoring | P1 | Document reproduction steps, expected result, actual result, environment, logs, and suspected area. |
| 225 | QA Triage Facilitation | P1 | Prioritize bugs by severity, frequency, customer impact, security risk, and release impact. |
| 226 | Acceptance Criteria Review | P0 | Verify requirements are testable, complete, unambiguous, and tied to validation evidence. |
| 227 | Definition of Done Review | P0 | Check code, tests, docs, security, migration, CI, screenshots, and closeout before marking done. |
| 228 | Exploratory Testing Charter | P1 | Define mission, risks, personas, data, paths, and timebox for exploratory testing. |
| 229 | Role-Based QA Matrix | P1 | Test behavior across anonymous, member, manager, admin, owner, support, and platform roles. |
| 230 | Mobile Viewport QA | P1 | Verify critical journeys on mobile breakpoints, touch interactions, dialogs, and navigation. |
| 231 | Timezone QA Strategy | P1 | Test scheduling, reports, reminders, filters, and date boundaries across timezones. |
| 232 | Notification QA Strategy | P1 | Test in-app, email, push, SMS, digest, preference, unsubscribe, and retry behavior. |
| 233 | Import QA Strategy | P1 | Test file upload, parsing, mapping, preview, edit, exclude, confirm, and failure recovery. |
| 234 | Export QA Strategy | P2 | Test authorization, redaction, file generation, expiration, and audit evidence. |
| 235 | QA Closeout Report | P0 | Summarize tests run, evidence, skips, failures, risks, and recommended release decision. |

## Skill implementation standard

When this category is converted into executable skills, each `SKILL.md` should include:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns / stop conditions
