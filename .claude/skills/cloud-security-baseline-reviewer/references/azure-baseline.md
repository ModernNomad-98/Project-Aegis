# Azure Baseline Reference

Detail file for [cloud-security-baseline-reviewer](../SKILL.md). Loaded on
demand. Entra ID is Microsoft's identity service; MFA is multi-factor
authentication; RBAC is role-based access control; NSG is a network
security group; TLS is Transport Layer Security (encryption in transit);
SQL is the database query language (Azure SQL is Microsoft's managed
database); CIS is the Center for Internet Security; CLI is the command-line
interface (`az`).

**Verification rule.** Every service name, setting name, command and
default below is a verification item: confirm it against current Microsoft
documentation before citing it. The user runs every command; this skill
runs none. All commands are read-only (`list`, `show`).

## Published baselines to name

- CIS Microsoft Azure Foundations Benchmark (state the version).
- Microsoft cloud security benchmark (state the version).
- A team's own baseline, named and versioned in the repository.
- Otherwise: the Aegis minimum baseline below, labelled as such.

## Aegis minimum baseline, by control family

| Family | Control | Read-only evidence the user supplies | GAP signal |
| --- | --- | --- | --- |
| Identity | Few standing Owner assignments; none to guests | `az role assignment list --role Owner --all` | many Owners; guest or service principal (application identity) Owner without a reason |
| Identity | MFA required for all people with access | Entra Conditional Access policy export or security defaults screen | no policy or security defaults; exclusions without a reason |
| Network | No administration port open to the internet | `az network nsg list` (security rules) | source `*` or `Internet` on 22, 3389 or a database port |
| Secrets | Key Vault with soft delete and purge protection; no secrets in app settings | `az keyvault list` then `az keyvault show` (properties only, never `secret show`) | purge protection off; secrets as plain app settings |
| Encryption | Storage accounts block public blob access and require modern TLS | `az storage account list` (`allowBlobPublicAccess`, `minimumTlsVersion`, `publicNetworkAccess`) | public access allowed without a reason; old TLS allowed |
| Network | Databases not open to all addresses | `az sql server firewall-rule list` per server | a rule covering `0.0.0.0`–`255.255.255.255` |
| Audit logging | Subscription activity log exported and retained | `az monitor diagnostic-settings subscription list` | no export; retention shorter than the baseline |
| Guardrails | Policy assignments enforce the baseline | `az policy assignment list` | no assignments, or audit-only where the baseline expects deny |
| Posture | Defender for Cloud plans on for resource types in use | `az security pricing list` | free tier on a type in use, without a recorded reason |
| Incident readiness | Security contact and alert notifications set; runbook exists | `az security contact list`; the runbook path | no contact; no runbook (hand to `incident-response-runbook`) |

## Gotchas

- Owner at a management group (a folder of subscriptions) is inherited by every subscription below it;
  ask for the management-group assignments too.
- Conditional Access exclusions ("break-glass" accounts) are expected; an
  exclusion list that includes ordinary users is a GAP.
- A private endpoint (a private network address for the service) does not by itself turn public network access off;
  check both.
- `az keyvault secret show` returns secret values. Never ask for it.
