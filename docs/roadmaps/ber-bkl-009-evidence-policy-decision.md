# BER-BKL-009 — final evidence handling decision proposal

> **Current status, 2026-09-23:** Behavioral Eval Runner (BER) backlog item 009
> has an owner-selected 30-day complete-bundle policy under
> [AEGIS-APR-009](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection).
> [AEGIS-APR-012](../approvals/APPROVAL_REGISTER.md#aegis-apr-012-offline-behavioral-eval-runner-evidence-policy-proof)
> and [BER-DEC-011](behavioral-eval-runner-backlog.md#ber-dec-011-bounded-offline-evidence-policy-proof)
> separately authorize only a synthetic offline proof. In this checkout,
> [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139) has not
> merged; the [backlog](behavioral-eval-runner-backlog.md#ber-bkl-009--evidence-retention-access-encryption-redaction-and-deletion-policy)
> records it as open at its checkpoint. Recheck the live pull request before
> using that status. Real-host access, encryption, privacy review and cleanup
> still need separate decisions and evidence. The owner options below are the
> historical selection record, not an invitation to choose the policy again.

**Historical policy proposal follows.**

Prepared 2026-09-23. **Proposal only; BER-BKL-009 remains PARTIALLY DELIVERED.**
The owner subsequently selected the recommended 30-day complete-bundle
policy in [approval APR-009](../approvals/APPROVAL_REGISTER.md). That is a
policy choice, not an implementation grant. The separately reviewable
[offline first-increment proposal](ber-bkl-009a-offline-policy-scope-proposal.md)
defines one possible next authorization; no code or cleanup follows from
merging either proposal alone.
The [backlog entry](behavioral-eval-runner-backlog.md#ber-bkl-009--evidence-retention-access-encryption-redaction-and-deletion-policy)
requires owner-set periods, access groups and encryption mechanism, then policy
enforcement and an operator procedure. The existing two-stage evidence writer
is delivered; this proposal does not rebuild it or grant a live run.

## Verified current boundary

- The design §13 requires per-artifact sensitivity, redaction, retention,
  creation/expiration, access reference and preserve-on-failure metadata in the
  Stage A/B manifests. The judge may consume only hash-verified Stage A inputs;
  the final report, final manifest and detached marker form a separate Stage B
  verification chain.
- `evidence.py` supports `days_30`, `days_90` and `days_365` timestamps, but
  `ArtifactMetadata` defaults to `days_30`, `INTERNAL`,
  `sanitized_by_construction`, `BER-DEC-006-build-evidence-handling`, and
  preserve-on-failure. The final report is hardcoded to `days_30` and that
  access reference. The current `expiration_at` is computed from each
  artifact's own creation time, not the first creation time of the bundle;
  a single bundle deadline needs additional enforcement. The detached marker
  is outside the manifest and needs its own cleanup binding. The writer
  records metadata and hashes; it does not
  enforce a reader ACL, verify disk encryption, perform redaction or delete
  expired evidence. Treat the defaults as placeholders, not proof of policy.
- BER-DEC-008 decisions 24–25 already require the WP-2B-3 external root,
  owner+SYSTEM ACL, disabled inheritance, verified encrypted volume, 30-day
  retention from first evidence creation, preserve-on-failure and owner-reviewed
  marker-gated cleanup. BER-DEC-010 changes only replacement input storage and
  bounded offline preparation. Neither record is a general production policy.
- The owner-only private calibration input repository keeps versioned inputs
  until an owner-reviewed deletion; it is separate from runtime evidence. The
  public source repository holds sanitized summaries/decisions in Git history.
  Hosted offline CI artifacts currently retain for 14 days under the workflow;
  they are synthetic check output, not a substitute for a BER runtime bundle.

## Recommended policy for owner selection

Keep a **single 30-calendar-day retention clock for each complete runtime
bundle**, measured from its first evidence creation. This retains the Stage A
and Stage B verification chain together. Do not delete one artifact while a
manifest/report still claims the full bundle verifies. Failed/incomplete runs
remain preserved until the owner reviews the failure and authorizes cleanup;
expiration is an eligibility-for-review date, not an automatic deletion job.
Maintain sanitized, reviewed repository summaries as versioned project records;
keep private calibration inputs under BER-DEC-010's separate version history.

| Artifact class | Examples | Proposed storage / classification | Reader and retention |
| --- | --- | --- | --- |
| Runtime raw input | transcript, activation evidence, sandbox/tool log, fixture/materialization inputs | External run root, `CONFIDENTIAL` or `INTERNAL`, `unredacted_internal_only` until reviewed | Owner and runner components with a verified need; `days_30` with complete bundle |
| Runtime control/accounting | attempt metadata, reservation/cost ledger, deterministic grader inputs, timing | Same external root; `INTERNAL` unless content raises sensitivity | Owner and the responsible verifier/grader only; `days_30` |
| Stage A trust record | input manifest and its hash | Same external root; inherits the strongest linked sensitivity | Judge/verifier reads only verified needed entries; `days_30` |
| Judge exchange | minimal authorized request/envelope, provider output, validation outcome | Same external root; `CONFIDENTIAL` if it carries transcript/output; no credential or expected label in request | Owner and calibration judge/aggregator as narrowly needed; `days_30` |
| Stage B trust/result record | final report, final manifest, detached marker, inventory | Same external root; `INTERNAL` or higher if unsanitized | Owner and final verifier; `days_30` as one bundle |
| Private calibration inputs and approval source | Versioned candidate/approved dataset, guide, split map, hashes, owner review, source cards and any builder that can regenerate hidden holdout content; future `owner-label-approval.json` only after explicit approval | Separate PRIVATE input repository under BER-DEC-010 | Owner-only initially; retain until an owner-reviewed deletion decision; not a runtime evidence class |
| Public-safe derivatives | aggregate counts, opaque hashes, conclusions, approval/governance records | Reviewed public repository PRs only after a sanitization check | Public readers; Git history persists until separately reviewed history policy; never raw transcript/label bytes |
| Offline CI synthetic artifacts | check logs and synthetic fixture results | GitHub Actions artifact store | Workflow's current 14-day retention; no live/raw BER evidence |

The production policy should explicitly assign `sensitivity`,
`redaction_state`, `retention_class` and a versioned `access_policy_ref` at each
artifact creation site. `days_90` and `days_365` stay unused for runtime
bundles until a later owner decision and verifier/deletion design supports
different periods without breaking the bundle. A raw transcript must never be
misclassified as sanitized merely because the current constructor defaults so.
Reserve the `SYNTHETIC` sensitivity value for reviewed, public-safe offline
fixtures whose *content* is deliberately publishable; do not use it for a
private holdout, raw run transcript or provider output merely because the
scenario was invented. Those artifacts remain `INTERNAL` or `CONFIDENTIAL`
under the rows above.

### Proposed read and publication matrix

| Actor | Permitted read | Denied read / publication |
| --- | --- | --- |
| Run controller and evidence verifier | Exact run root; verifier may read untrusted bytes solely to establish hashes and identity before any semantic use; owner-authorized review/cleanup may inspect expired bundles | Other run roots, credentials in evidence, grading/judging/rollup use of unverified or expired bundles |
| Deterministic grader | Only verified Stage A inputs for its control | Candidate labels, unrelated transcripts, judge outputs |
| Semantic judge | Only the minimized, verified Stage A envelope allowed by its gate | Expected answers, candidate/gold labels, risk tags, unverified artifacts, Stage B outputs |
| Trusted calibration scorer | Exact owner-approved labels and split map from an owner-controlled local private checkout, plus bound judge verdicts, only during authorized scoring | Public/CI publication, semantic-judge envelope access, additional private-repo collaborator or Actions permission |
| Aggregator / final verifier | Bound judge outcome and verified Stage A/B records needed for rollup | Unrelated run roots or secret material |
| Owner/operator | Full authorized external root and private inputs for review | Publishing raw bytes into public PRs or CI artifacts |
| Public PR / CI reader | Sanitized derivative and synthetic check output | Raw transcript, full private dataset, unsanitized provider output, credentials |

This matrix is a policy target. Present Python constructors do not enforce
OS-level principal separation for these logical components. Real-host proof
and enforceable reader scopes remain implementation/verification work.

### Proposed encryption, redaction and cleanup

- Require verified full-volume encryption for an external root that may hold
  `INTERNAL` or `CONFIDENTIAL` runtime evidence. On the current Windows host,
  the proposal is owner-managed BitLocker with recovery material held outside
  Git and outside the evidence root. If another host is selected, record its
  exact mechanism and verification command before a live run. An unknown or
  unavailable encryption state is a stop, matching BER-DEC-008. Only the
  owner account and SYSTEM may read/write the WP-2B-3 root; any future service
  principal needs a separate recorded access decision.
- Allow only synthetic calibration content under the current WP-2B-3 scope.
  Credentials, secrets, unrestricted environment dumps, customer/personal or
  production data, unrelated private source and private chain-of-thought are
  forbidden. Redact or construct a minimal judge envelope **before** exposure;
  no expected label/rationale, split/risk tag or private input source enters it.
  Before a public PR or CI artifact, independently screen paths, transcripts,
  provider output, labels and identifiers; publish only sanctioned aggregates
  and opaque hashes. Redaction must record what was removed and must not alter
  the original external bytes or their hashes.
- Cleanup is manual and owner-reviewed after expiration and failure resolution.
  Re-verify root ownership marker, exact path, physical/reparse safety, ACL,
  encryption and final inventory; list intended targets and compare hashes.
  Preserve on any mismatch. Delete only the marked root through a bounded
  operator action, record actual deletion timestamp and a sanitized cleanup
  report. No session-end or unattended timer deletion. Keep the original
  Stage A/B manifest and marker until the entire bundle is removed.

## Owner decisions and implementation gate

1. **Retention:** choose the recommended uniform 30-day runtime bundle,
   separate durable private inputs and reviewed public-safe records; or choose
   a longer complete-bundle period with storage/cost and code implications.
   Per-artifact mixed expiry inside one hash-bound bundle is not recommended.
2. **Readers:** accept the owner+SYSTEM WP-2B-3 root and the read matrix above
   as the general policy target, or identify exact additional principals and
   access needed for a selected later host. No broad user group is proposed.
3. **Encryption/key custody:** accept verified BitLocker for the selected
   Windows WP-2B-3 root, with owner-held recovery material outside Git; name
   another verified mechanism if the selected execution host differs.
4. **Implementation:** after those owner decisions, a separate reviewed and
   merged BER-DEC follow-up must authorize code/runbook work. It must assign
   real metadata at creation, enforce access and sanitization, verify host
   encryption, enforce the first-evidence bundle clock including the detached
   marker, and implement/test marker-gated cleanup without weakening
   BER-DEC-008. No deletion or runtime provider call follows from this proposal.

Until selection and implementation evidence exist, BKL-009 stays PARTIALLY
DELIVERED. The WP-2B-0 temporary spike terms remain historical evidence;
they neither become production defaults nor get retroactively rewritten.
