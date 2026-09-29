# AWS Baseline Reference

Detail file for [cloud-security-baseline-reviewer](../SKILL.md). Loaded on
demand. AWS is Amazon Web Services; IAM is identity and access management;
MFA is multi-factor authentication; KMS is Key Management Service; S3 is
the object storage service; SCP is a service control policy (an
organization-wide guardrail); SSO is single sign-on; CSV is a
comma-separated values file; CIS is the Center for Internet Security; CLI
is the command-line interface.

**Verification rule.** Every service name, setting name, command and
default below is a verification item: confirm it against current AWS
documentation before citing it in a report. The user runs every command;
this skill runs none. All commands listed are read-only (`get`, `list`,
`describe`); drop any that the user's permissions do not allow rather than
widening permissions.

## Published baselines to name

- CIS Amazon Web Services Foundations Benchmark (state the version).
- AWS Foundational Security Best Practices (a Security Hub standard).
- A team's own baseline, named and versioned in the repository.
- Otherwise: the Aegis minimum baseline below, labelled as such.

## Aegis minimum baseline, by control family

| Family | Control | Read-only evidence the user supplies | GAP signal |
| --- | --- | --- | --- |
| Identity | Root user has MFA and no access keys | `aws iam get-account-summary` (`AccountMFAEnabled`, `AccountAccessKeysPresent`) | MFA 0, or keys present |
| Identity | People sign in through SSO or MFA-protected users; no unused or old user keys | IAM credential report (CSV) the user downloads | user with console access and no MFA; key unused for months or never rotated |
| Identity | No wildcard administrator policy on workloads | `aws iam list-policies --scope Local` plus the policy documents in question | `"Action": "*"` with `"Resource": "*"` outside a break-glass role |
| Network | No administration port open to the internet | `aws ec2 describe-security-groups` | `0.0.0.0/0` or `::/0` on port 22, 3389 or a database port |
| Secrets | Secrets live in a secret store with rotation where supported | `aws secretsmanager list-secrets` (names and rotation flags only; never `get-secret-value`) | secret in plain environment variables, IaC or an S3 object; rotation off |
| Encryption | Account-level S3 Block Public Access on | `aws s3control get-public-access-block --account-id <id>` | any flag false without a recorded reason |
| Encryption | No public bucket unless intended | `aws s3api get-bucket-policy-status --bucket <name>` per bucket | `IsPublic: true` without an accepted-risk record |
| Encryption | Default volume encryption in every used region | `aws ec2 get-ebs-encryption-by-default` per region | false in any region in scope |
| Encryption | Customer keys rotated | `aws kms get-key-rotation-status --key-id <id>` | rotation off for symmetric customer keys |
| Audit logging | A multi-region trail is logging | `aws cloudtrail describe-trails` and `get-trail-status` | no multi-region trail; `IsLogging` false; one region only |
| Guardrails | Organization guardrails exist | `aws organizations list-policies --filter SERVICE_CONTROL_POLICY` | none, or none preventing log or guardrail disablement |
| Posture | Posture and threat services on in every used region | `aws securityhub get-enabled-standards`; `aws guardduty list-detectors` per region; `aws configservice describe-configuration-recorder-status` | off in any region in scope |
| Incident readiness | Security contact set and a runbook exists | `aws account get-alternate-contact --alternate-contact-type SECURITY`; the runbook path | no contact; no runbook (hand to `incident-response-runbook`) |

## Gotchas

- Many controls are per region. A single-region export proves one region.
- The credential report is generated on request; its timestamp is the
  evidence date.
- Security Hub findings are only as complete as the enabled standards and
  regions; a clean dashboard with one standard enabled is not a clean
  account.
- `get-secret-value`, `get-parameter --with-decryption` and similar calls
  return secret values. Never ask for them.
