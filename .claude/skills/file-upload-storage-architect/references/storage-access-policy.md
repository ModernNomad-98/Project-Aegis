# Storage access policy: roadmap #115 and the signed-URL residual

Reference for the `file-upload-storage-architect` skill (extension-only bundle; the coverage row #115 remains PARTIAL in this batch - a bounded reference does not make this owner the material covering skill).

## Bucket policy baseline

- Private by default: no public-read bucket or object ACL; access only through the application's authorization path or a short-lived signed URL issued after an authorization check.
- One bucket policy per environment and purpose; state the principal, action, resource and condition for each statement that widens access.
- Separate upload-intent issuance from object read; never let a client choose the storage prefix or tenant path.
- Log object reads/writes and signed-URL issuance; keep the audit trail out of the same writable bucket.

## Signed-URL residual (explicit)

- A signed URL is a bearer capability for its lifetime: bound its TTL, scope it to one object and one method, and treat a leaked URL as an access event.
- Residual, named rather than hidden: a signed URL cannot be un-issued, so revocation is TTL-bound; path/tenant scoping must be enforced at issuance.
- PII/tenant content stored in objects follows the `pii-lifecycle-designer` masking and retention rules.

## Boundaries

- This reference does not design the upload pipeline, validate file content, or audit RLS policies; route those to their owners.
- No coverage-map status change is claimed by this bundle.
