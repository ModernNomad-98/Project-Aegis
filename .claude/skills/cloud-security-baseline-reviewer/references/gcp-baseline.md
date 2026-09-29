# GCP Baseline Reference

Detail file for [cloud-security-baseline-reviewer](../SKILL.md). Loaded on
demand. GCP is Google Cloud Platform; IAM is identity and access
management; MFA is multi-factor authentication (Google calls it 2-Step
Verification); KMS is Cloud Key Management Service; Cloud SQL is Google's
managed relational database; TLS is Transport Layer Security (encryption in
transit); CIS is the Center for Internet Security; CLI is the command-line
interface (`gcloud`).

**Verification rule.** Every service name, setting name, command and
default below is a verification item: confirm it against current Google
Cloud documentation before citing it. The user runs every command; this
skill runs none. All commands are read-only (`list`, `describe`,
`get-iam-policy`).

## Published baselines to name

- CIS Google Cloud Platform Foundation Benchmark (state the version).
- A team's own baseline, named and versioned in the repository.
- Otherwise: the Aegis minimum baseline below, labelled as such.

## Aegis minimum baseline, by control family

| Family | Control | Read-only evidence the user supplies | GAP signal |
| --- | --- | --- | --- |
| Identity | Basic roles (Owner, Editor) limited to a few people; none to service accounts (identities that software runs as) | `gcloud projects get-iam-policy <project>` | `roles/owner` or `roles/editor` on many members or on a service account |
| Identity | 2-Step Verification enforced for the organization | Google Workspace or Cloud Identity admin screen | not enforced |
| Identity | No user-managed service account keys, or keys rotated | `gcloud iam service-accounts keys list --iam-account <sa> --managed-by=user` | old or unused user-managed keys |
| Network | No administration port open to the internet | `gcloud compute firewall-rules list` | source `0.0.0.0/0` on 22, 3389 or a database port |
| Network | Cloud SQL not open to all addresses and requiring TLS | `gcloud sql instances describe <instance>` (`ipConfiguration`) | authorized network `0.0.0.0/0`; TLS not required |
| Secrets | Secrets in Secret Manager, not in environment variables or code | `gcloud secrets list` (names only, never `versions access`) | secrets in plain environment variables or IaC |
| Encryption | No public buckets unless intended; public access prevention on | `gcloud storage buckets describe gs://<bucket>` (IAM and `public_access_prevention`) | `allUsers` or `allAuthenticatedUsers` without a reason |
| Encryption | Customer keys rotated | `gcloud kms keys list --keyring <ring> --location <loc>` (`rotationPeriod`) | no rotation period |
| Audit logging | Data Access audit logs on for sensitive services | `auditConfigs` in the IAM policy export | absent for services holding customer data |
| Guardrails | Organization policies enforce the baseline | `gcloud org-policies list --project <project>` | none on key-creation, public access or external sharing |
| Posture | Security Command Center on at the tier the baseline expects | Security Command Center settings screen or findings export | off, or a tier missing required detectors |
| Incident readiness | Essential contacts set for security; runbook exists | `gcloud essential-contacts list`; the runbook path | no security contact; no runbook (hand to `incident-response-runbook`) |

## Gotchas

- Admin Activity audit logs are always on; Data Access logs are not. A
  "logging on" claim needs to say which.
- IAM is inherited from folders and the organization; a clean project
  policy can still hide an organization-level Owner.
- `gcloud secrets versions access` returns secret values. Never ask for it.
