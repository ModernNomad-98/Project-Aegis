# Route protection matrix: gates, denials and negative tests

Reference for the route-protection-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Every gated route names its capability and server enforcement source.
- Denied/redirect/onboarding behavior is explicit per route class.
- Deep-link return is defined and cannot bypass the gate.
- Client guards are labeled UX-only; enforcement gaps are named.
- Negative tests cover unauthorized and under-privileged access.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- Routes need auth, role, onboarding or admin gates and behavior is inconsistent.
- A deep link or redirect flow can bypass or break a gate.
- Client route guards are being treated as a security boundary.
- Denied/redirect/onboarding flows need explicit behavior per route.

## 3. Output and evidence rules

1. Route x gate matrix with required capability and enforcement source.
2. Redirect/denied/onboarding behavior per route class.
3. Deep-link return contract.
4. Trust-boundary note (client UX vs server truth).
5. Negative-test plan and enforcement gaps.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Roles/permissions/object-level authorization matrix routes to `authorization-matrix-designer`; this skill does not perform that owner's work.
- Cross-tenant leakage review routes to `tenant-isolation-reviewer`; this skill does not perform that owner's work.
- Security review of an actual diff routes to `security-pr-reviewer`; this skill does not perform that owner's work.
- URL-state schema, history or shareable-link design (Batch-3 sibling seam) routes to `url-state-architect`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `authorization-matrix-designer`, `tenant-isolation-reviewer`, `security-pr-reviewer`, `human-approval-boundary`, `api-event-architect`, `admin-console-architect`, `tenant-modeler`, `rls-policy-auditor`, `secure-migration-reviewer`, `change-classification-gate`, `incident-response-runbook`, `edge-state-ux-designer`, `error-taxonomy-designer`, `ux-design-iteration` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every gated route names its capability and server enforcement source.
- Denied/redirect/onboarding behavior is explicit per route class.
- Deep-link return is defined and cannot bypass the gate.
- Client guards are labeled UX-only; enforcement gaps are named.
- Negative tests cover unauthorized and under-privileged access.
- No route or server code was edited or enforcement claimed.

