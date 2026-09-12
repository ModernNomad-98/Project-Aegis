# Independent preservation review — 2026-09-11

Reviewer: `independent_phase01_review`, read-only.
Verdict: PASS; no blocking findings.

The reviewer independently verified the initial archive's 85 files and the
complete archive's 103 files against sizes, hashes and manifest digests; the Git
bundle's 86 refs and absence of prerequisite-object declarations; the restored
clone's exact reviewed HEAD and tree; and all 18 wheel metadata identities.

Complete archive SHA-256:
`bdb55a3d7877320c60d3972b37133371bc981692fc93f0188a55e0df8c57e103`.

The reviewer inspected the completed verification report and script, which record
successful offline hash-locked installation, dependency checking, exact installed
versions, 15 passing synthetic tests and 21/21 self-checks. Installation was not
independently repeated.

The inventory correctly separates required approved inputs, supporting provenance,
historically uncreated execution records and unknown activity outside documented
intervals. It does not reconstruct approvals or imply an accounting reset.

Claims are limited to local preservation and Windows x64/CPython 3.14 runtime
restoration with a separately supplied interpreter. No calibration inputs were
recovered, and no off-device copy or provider readiness was verified. Retain the
detached checksum and verification report alongside the ZIP when transferring it.
A source-only GitHub push preserves the selected source commits, not the complete
recovery package.
