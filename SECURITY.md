# Security Policy

This page is for anyone who finds a security problem in the Project Aegis
source library. It explains which branch receives fixes and how to send a
private report to the maintainer. For example, if a skill could make an
assistant reveal credentials, use the private reporting path below so the
details are not published before they can be reviewed.

## Supported versions

This project ships from a single rolling `main` branch. Only `main` is supported;
fixes land there and are not backported to tags or older commits.

## Reporting a vulnerability

Please report security issues **privately** through GitHub Private Vulnerability
Reporting: open the repository's **Security** tab and choose **"Report a
vulnerability."** Do not open a public issue, pull request, or discussion for a
security problem.

A useful report names the affected file and revision, describes the behavior
and its impact, and gives the smallest safe reproduction steps available. Do
not paste a live credential or private customer data into a report.

This is a solo-maintainer project, so handling is best-effort: expect an
acknowledgment within **7 days**. There is no dedicated security inbox — please
use the private reporting flow above rather than sending email.

## Scope

This source library contains agent skills, documentation, validation tooling
and the Behavioral Eval Runner (BER), which grades recorded skill behavior.
Its security-relevant surfaces include instructions that can cause an agent or
continuous-integration (CI) automation to act, and the runner's execution and
evidence controls.
In scope, for example:

- malicious or unsafe **skill content** (instructions that could drive harmful,
  destructive, or data-exfiltrating agent behavior);
- **validator or CI bypasses** that let unsafe content pass the gate;
- **workflow injection** against the repository's automation;
- bypasses of **BER approval, execution, budget or evidence-integrity controls**;
- tampering with **owner approval provenance**, lifecycle records or pinned CI dependencies;
- changes that **weaken a manual-only invocation posture** (a skill that
  requires a deliberate human request), a skill's Security
  Rules or Stop Conditions, or the repository's safety rules.

See [CONTRIBUTING](CONTRIBUTING.md#external-contributions) for review requirements
and [offline CI](docs/offline-ci.md#protected-files) for the enforced protected-file
guard. The guard's path list is narrower than the full security-review scope.
