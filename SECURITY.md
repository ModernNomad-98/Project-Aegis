# Security Policy

## Supported versions

This project ships from a single rolling `main` branch. Only `main` is supported;
fixes land there and are not backported to tags or older commits.

## Reporting a vulnerability

Please report security issues **privately** through GitHub Private Vulnerability
Reporting: open the repository's **Security** tab and choose **"Report a
vulnerability."** Do not open a public issue, pull request, or discussion for a
security problem.

This is a solo-maintainer project, so handling is best-effort: expect an
acknowledgment within **7 days**. There is no dedicated security inbox — please
use the private reporting flow above rather than sending email.

## Scope

This is a library of agent skills and documentation, not a running service. The
security-relevant surface is what the content can cause an agent — or a
maintainer's CI — to do. In scope, for example:

- malicious or unsafe **skill content** (instructions that could drive harmful,
  destructive, or data-exfiltrating agent behavior);
- **validator or CI bypasses** that let unsafe content pass the gate;
- **workflow injection** against the repository's automation;
- changes that **weaken a manual-only invocation posture**, a skill's Security
  Rules or Stop Conditions, or the repository's safety rules.
