# Encryption Decision Matrix

Companion to [SKILL.md](../SKILL.md). Use this matrix to make each design decision explicit and to record why the rejected option lost. Every provider-specific statement here - defaults, tier availability, key limits, rotation support, deletion windows - is a **verification item**: confirm it against current provider documentation and record the version and date consulted. Nothing in this matrix is a provider fact to repeat from memory.

## Store-type matrix

| Store type | Typical data class | Default-at-rest question | Envelope encryption? | Key scoping question | Deletion / crypto-shred question | Evidence to request |
| --- | --- | --- | --- | --- | --- | --- |
| Relational database | Identity, tenant business data, PII | Provider-managed disk encryption or customer-managed key? Verify platform support and whether it covers snapshots and replicas. | Usually not for the disk; field-level envelope encryption only for the highest class. | One key per environment, per tenant, or per data class? | Row deletion versus destroyed field key; what remains in backups and PITR logs? | Store configuration record, key identifier, snapshot inheritance statement |
| Object storage | Documents, exports, media, dumps | Bucket-default encryption versus per-object key; verify default algorithm and key-support per tier. | Yes when per-object or per-tenant keys are required. | Per tenant or per object class; who can decrypt? | Object delete, version delete, key destroy; what about replicas and lifecycle copies? | Bucket policy record, default-encryption record, key mapping |
| Cache | Sessions, hot tenant data, derived PII | Is the cache encrypted at rest, or is it treated as ephemeral? Verify persistence and snapshot behavior. | Rarely; prefer excluding the highest class from cache. | Shared cache key or per-tenant namespace encryption? | Eviction is not deletion; snapshots and replicas may retain values. | Cache configuration, retention/TTL, exclusion decision record |
| Search index | Indexed documents, facets, PII | Index-at-rest encryption support and whether replicas and snapshots inherit it. | Yes for per-tenant or per-field isolation. | Per index, per tenant, or per field? | Reindex or delete-by-query versus key destruction; snapshot retention. | Index settings, snapshot policy, field mapping of sensitive fields |
| Queue / event bus | Events carrying PII, integration payloads | Broker encryption at rest; message retention and dead-letter copies. | Sometimes, per message or per tenant. | Shared broker key versus per-producer key. | Retention expiry is not cryptographic erasure; dead-letter stores are copies. | Broker configuration, retention policy, dead-letter handling |
| Logs / observability | Request logs, audit trails, error payloads | Log-store encryption at rest, plus redaction before write. | Rarely; redaction is the primary control. | Shared platform key; who can query? | Log retention and deletion; third-party processor copies. | Pipeline redaction rules, retention policy, processor terms |
| Backups / snapshots | Full copies of everything above | Backup encryption and key custody, independent of the source store. | Inherited from source or backup-specific key. | Separate backup key so source-key loss does not destroy recovery. | Key destruction must not silently destroy the only recovery copy; test policy. | Backup configuration, key custody, restore-path key availability |
| Analytics / warehouse | Aggregated and raw event data | Warehouse encryption at rest; external tables and export buckets. | Often per-dataset or per-tenant. | Warehouse key versus per-dataset key. | Partition drop versus key destruction; derived tables and exports. | Dataset configuration, export destinations, retention |

Verify each cell that names a provider capability against current provider documentation before repeating it in a design.

## Transit options

| Option | What it protects | Termination and ownership question | Failure mode to design against |
| --- | --- | --- | --- |
| TLS at the public edge | Client to edge | Who owns the certificate, the private key and renewal? CDN/proxy or application? | Expiry, mis-issued certificate, weak policy, plaintext origin hop |
| TLS on internal hops | Service to service | Is termination at a load balancer, sidecar or application? Who owns each certificate? | Assumed encryption on a hop that is actually plaintext inside the network |
| mTLS | Both ends authenticated, service identity | Certificate authority ownership, workload identity issuance, rotation without downtime | Stale or shared client certificates, trust-anchor sprawl |
| Pinned or scoped trust | Specific upstream identity | Who maintains the pin or trust bundle, and how is it rotated? | Rotation breaks or silently widens trust |
| Encryption at the application layer | Payload end to end, across intermediaries | Application key ownership and versioning | Key shipped to clients, unversioned ciphertext, no decrypt path |
| Plaintext with compensating control | Nothing on the wire; a segmented network only | Who accepts the residual risk? | The exception becomes permanent and unowned |

Certificate lifecycle is part of the design: issuance, storage of private keys, renewal ownership, revocation path, trust-anchor distribution, and what breaks if renewal fails.

## Key custody options

| Custody model | Who can use | Who can administer | Who can delete | Design caution |
| --- | --- | --- | --- | --- |
| Provider-managed key, no customer control | Provider, scoped by service policy | Provider | Provider, on service deletion | Simplest; verify what the provider can access and what its deletion window is |
| Customer-managed key in provider KMS | Named principals via key policy | Key administrator role | Key administrator, with a deletion window | Separate use, administer and delete duties; verify window and irreversibility |
| Customer-managed key in external KMS | Application principals via grants | External key team | External key team | Latency, availability and break-glass path must be designed |
| Hardware security module (HSM) custody | Application via crypto operations | HSM administrators | HSM administrators | Operational cost and quorum design; verify integration support |
| Bring-your-own-key import | As above, with imported material | Importer plus administrator | Administrator | Imported material may be non-recoverable; verify expiry and re-import path |
| Application-held data key, wrapped by KMS | Application | Key administrator | Key administrator | Envelope encryption: cache lifetime, re-wrap on rotation, plaintext key never logged |

Record custody as a decision with rejected alternatives. The same role must not be able to use, rotate and delete a key without a second party where the data class requires it.

## Rotation triggers

| Trigger | What rotates | Design question |
| --- | --- | --- |
| Calendar policy | Data keys, wrapping keys, certificates | Period, owner, and the compatibility window for old ciphertext |
| Suspected compromise | The exposed key and everything wrapped by it | Blast radius, re-encryption plan, revocation before rotation |
| Personnel change | Access grants, possibly keys | Who loses use rights, and how is that proven? |
| Provider deprecation | Algorithm, key type, service tier | Migration path and verification of the new support status |
| Tenant offboarding | Per-tenant keys | Crypto-shred as deletion evidence, with backup coverage stated |
| Algorithm weakness | Cipher suite, TLS policy | Inventory of affected hops and stores before the change |
| Certificate expiry window | TLS/mTLS certificates | Automated renewal and a monitored expiry budget |

Rotation is not complete until old ciphertext is re-wrapped or re-encrypted, or the compatibility window and its deadline are recorded.

## Crypto-shred semantics

- **Crypto-shredding** means destroying the key that makes ciphertext readable; it is not the same as deleting rows, objects or index entries.
- State exactly which copies the destroyed key covered: primary store, replicas, snapshots, backups, caches, search indexes, logs, exports and third-party processors.
- State what remains readable after key destruction: metadata, key identifiers, access logs, already-exported plaintext, and any copy encrypted under a different key.
- Key destruction is usually irreversible and may destroy the only recoverable backup; record the accepted risk and the approval owner.
- Deletion evidence differs per path: a deletion record, a key-destruction record, a retention-policy expiry, or a processor attestation. Mark which evidence exists and which is UNVERIFIED.

## Evidence list

- Data classification record with source, date and owner.
- Store and flow inventory with the boundary each crosses.
- Transit design record: TLS/mTLS per hop, termination point, certificate owner and renewal mechanism.
- At-rest decision record per store: provider default or customer-managed key, envelope choice, rejected alternative.
- Key hierarchy record: root, wrapping and data keys, custody, separation of duties, rotation and revocation.
- Rotation schedule and the last completed rotation evidence, or UNVERIFIED.
- Deletion and crypto-shredding record, including backup and replica coverage.
- Backup, replica and DR inheritance statement, or a named exception with compensating control.
- Provider verification notes: document version, date consulted, and the exact capability confirmed.
- Residual-risk acceptance with the owner who accepted it.

**Provider facts:** every entry above that names a provider behavior is a verification item. Confirm against current provider documentation and cite what was read; do not fill the gap from memory.
