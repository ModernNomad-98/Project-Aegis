# Consumer manual-only policy - copied reference (verbatim-derived, NORMATIVE - REV-6, 2026-10-26)

Status: NORMATIVE for consumers that adopt the Aegis manual-only policy (OD-Q903-5=A). OD-Q903-1 is a docs-only determination: this item adds documentation only and no machine enforcement; source-repo scripts cannot enforce consumer-local records; no runtime enforcement is claimed. Owner choices recorded 2026-10-26T07:29 America/Los_Angeles: OD-Q903-2=A (any MANUAL-ONLY skill by exact name and reason, no fixed allowlist); OD-Q903-3=B (trigger-scoped standing override); OD-Q903-4=A (consumer-local append-only register); OD-Q903-5=A (normative contract).

## Definition

1. Manual-only skills are human-invoked. A skill is MANUAL-ONLY when its description carries the MANUAL-ONLY prefix AND its declaration is consistent with disable-model-invocation: true (both, per the D50 declaration check). It is used only when a human names that exact skill by exact name for the task; a model must never auto-apply it.

## Manual-only obligations

2. The consumer must not auto-apply, preload, chain, or simulate a manual-only skill, and must not rewrite its declaration/description to make it model-invocable.

## Override meaning and limits

3. An override is an authorization record, not a waiver. Any MANUAL-ONLY skill may be overridden by exact name and reason: the record identifies that exact skill and states the reason, and there is no fixed allowlist. It records that a named human authorized a named MANUAL-ONLY skill for a named trigger and a task/scope; it is not a blanket permission, not a model-initiated escape, and never relaxes the manual-only rule for any other skill.

## Authorization requirements

4. Authorization requirements (mandatory): actor identity, exact skill name, reason, the named trigger in the consumer's recorded policy, task/scope, date, and the exact head/commit where the authorization or pin references a code tree (mandatory where applicable; not required per invocation). The record is written before use in a consumer-local append-only register that cites this policy; the register is the consumer's record of authority and is normative for that consumer. No anonymous or implicit overrides.

## Trigger-scoped standing override

5. Overrides are standing but trigger-scoped (OD-Q903-3=B): a standing override is bound to a named trigger in the consumer's recorded policy; it is revocable at any time and must be re-pinned on every sync to the current contract version and, where applicable, the exact head/commit. If the entry is revoked or not re-pinned on sync, the override is not valid and fail-closed defaults apply. Per-invocation overrides are not permitted: the owner rejected per-invocation because it reproduces manual-only.

## Fail-closed defaults

6. Fail-closed defaults: if the host cannot prove the human invocation, the named trigger, the current pin, or the override record, the manual-only skill is NOT applied; if in doubt, do not run it. A missing, unverifiable, stale, or revoked override is not consent.

## Audit evidence

7. Audit evidence: keep the minimal record (exact skill name and reason, actor, named trigger, scope, date, exact head/commit where applicable, the pin/version at each sync, and revocation events) in the consumer-local append-only register; do not record secrets or PII. Evidence is available to the consumer's reviewers on request.

## Consumer obligations

8. Escalation and non-substitution: if a task seems to require a manual-only skill and no human or valid trigger-scoped override is available, stop and surface the request; do not substitute an auto-applied skill or a paraphrased procedure. An override never substitutes for any other required approval or authority.
