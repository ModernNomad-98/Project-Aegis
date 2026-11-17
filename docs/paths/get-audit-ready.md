# Prepare for a compliance audit — ISO 27001, ISO 42001 and SOC 2

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** enterprise customers, procurement or a security questionnaire are
asking for SOC 2 or ISO, or you are asking how far your organisation is from an audit.
You can describe the situation in plain words; this page names the order and what each
specialist checks before it starts.

**How to run it:** open your project in your agent tool (Claude Code, OpenAI's Codex
command-line interface (CLI), or any Agent Skills tool) and describe the situation. The
page names the fixed order for each situation. Paste the order below into the chat so the
agent has the sequence — describing the situation alone does not hand it over, and the
starter package does not ship `docs/paths/`. The experts named are design and
assessment skills — they produce the plan, map, analysis or evidence design and leave
the decision with you and your auditors.

**Before you start — what a starter install has.** The [starter
package](../consumer-starter-package.md) installs none of these nine specialists (42
files / 19 skills; manual-only skills are not installed). None of these nine is
manual-only: all are model-invocable and design or assessment only. Copy each skill you
need with the **selected-skills allow-list** route in [Using the skills in your own
project](../../README.md#using-the-skills-in-your-own-project): copy the allow-listed
files for that skill (its `SKILL.md` and `references/`; do not copy `evals/`, which are
evaluation answer keys), then check it is present at use time in the location your host
discovers: `.claude/skills/<name>/` for Claude Code project skills, or
`.agents/skills/<name>/` / `~/.agents/skills/<name>/` for native Agent Skills mode. If a skill is absent, name
it and copy it — never substitute a different skill. For a starter consumer,
record the extension as a DECISION in `docs/project-state.md` before first use
(the starter §4.2 rule). The starter package does not change
for this page and there is no auto-install claim.

## The four situations

**1. "How far are we from an audit?"** Start with
[`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md). Run
[`compliance-control-foundation`](../../.claude/skills/compliance-control-foundation/SKILL.md)
first only when there is no current-state input at all (no catalog, no artifacts); the
auditor still needs a target framework, which you provide.

**2. "We need to prepare for ISO 27001."** The order is
[`compliance-control-foundation`](../../.claude/skills/compliance-control-foundation/SKILL.md)
→ [`multi-framework-crosswalk`](../../.claude/skills/multi-framework-crosswalk/SKILL.md)
*(only when more than one framework is in scope)* →
[`iso-27001-isms-architect`](../../.claude/skills/iso-27001-isms-architect/SKILL.md) →
[`statement-of-applicability-author`](../../.claude/skills/statement-of-applicability-author/SKILL.md)
→
[`compliance-evidence-collector`](../../.claude/skills/compliance-evidence-collector/SKILL.md)
→ [`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md). The
ISMS step needs organizational context and top-management sponsorship; the Statement of
Applicability step needs the licensed standard's Annex A table and risk-treatment output
— there is no structure-only fallback for that step; the evidence programme needs a
stated audit window.

**3. "Enterprise customers ask for SOC 2."** The order is
[`compliance-control-foundation`](../../.claude/skills/compliance-control-foundation/SKILL.md)
→ crosswalk rows (the foundation catalog rows plus the SOC 2 crosswalk rows the mapper
requires; create them before mapping)
→
[`soc2-trust-criteria-mapper`](../../.claude/skills/soc2-trust-criteria-mapper/SKILL.md)
→
[`compliance-evidence-collector`](../../.claude/skills/compliance-evidence-collector/SKILL.md)
→ [`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md). The
mapper needs a named system and a customer driver; criteria-level mapping needs the TSC
text or the AICPA guide, otherwise only category-level scoping with verification items
is honest; the audit window must not start before the key controls existed.

**4. "We need AI governance (ISO 42001 and/or NIST AI RMF)."** The order is
[`compliance-control-foundation`](../../.claude/skills/compliance-control-foundation/SKILL.md)
→ [`ai-lifecycle-risk-manager`](../../.claude/skills/ai-lifecycle-risk-manager/SKILL.md)
*(RMF programme)* and/or
[`iso-42001-aims-architect`](../../.claude/skills/iso-42001-aims-architect/SKILL.md)
*(AIMS)* →
[`statement-of-applicability-author`](../../.claude/skills/statement-of-applicability-author/SKILL.md)
*(ISO 42001 only)* →
[`compliance-evidence-collector`](../../.claude/skills/compliance-evidence-collector/SKILL.md)
→ [`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md). The
risk programme needs an AI system inventory and a programme owner; the AIMS needs that
inventory and top-management sponsorship; the Statement of Applicability keeps its
licensed Annex A table and risk-treatment preconditions; the evidence programme needs a
stated window. A likely prohibited or severely harmful use is escalated to the
accountable human and legal review — the owning specialist's file carries the exact
stop.

## The nine specialists

| The situation, in plain words | Specialist (linked to its SKILL.md) | Before it can run (quoted from its own Stop Conditions) |
|---|---|---|
| "We're starting a compliance programme and need one common control set for ISO 27001, ISO 42001 and/or SOC 2." | [`compliance-control-foundation`](../../.claude/skills/compliance-control-foundation/SKILL.md) | "No target framework(s) and no catalog owner can be named — stop; an ownerless control set is unauditable by design." |
| "We already have a control set and need to know what it satisfies across frameworks." | [`multi-framework-crosswalk`](../../.claude/skills/multi-framework-crosswalk/SKILL.md) | "No foundation catalog exists — stop; run compliance-control-foundation first (framework-first crosswalks invert the architecture)." |
| "We need an ISO 27001 ISMS / certification-readiness design." | [`iso-27001-isms-architect`](../../.claude/skills/iso-27001-isms-architect/SKILL.md) | "No organizational context is available (business, parties, obligations) — stop; clause 4 cannot be invented." and "Top management sponsorship is absent — an ISMS without clause 5 commitment is theater; surface this to the human before designing further." |
| "We need a certifiable AI management system (ISO 42001)." | [`iso-42001-aims-architect`](../../.claude/skills/iso-42001-aims-architect/SKILL.md) | "No AI system inventory can be established — stop; an AIMS without knowing which AI systems exist and in what role is fiction." and "Top-management sponsorship absent — surface before designing; clause 5 cannot be retrofitted." |
| "Enterprise customers ask for SOC 2; we need to scope the report." | [`soc2-trust-criteria-mapper`](../../.claude/skills/soc2-trust-criteria-mapper/SKILL.md) | "No system can be named and no customer driver exists — stop; scoping without a system or a consumer produces a report nobody accepts." |
| "We need the Statement of Applicability for ISO 27001 or 42001." | [`statement-of-applicability-author`](../../.claude/skills/statement-of-applicability-author/SKILL.md) | "The licensed standard's Annex A table is not available — stop and say so; reconstructing Annex A entries from memory or vendor summaries produces a certifiably wrong document." and "No risk-treatment output exists to trace inclusions to — route to the owning ISO projection to run the 6.1 machinery first." |
| "We need evidence across the audit window." | [`compliance-evidence-collector`](../../.claude/skills/compliance-evidence-collector/SKILL.md) | "No control catalog exists — run compliance-control-foundation first; evidence without controls is a folder of screenshots." and "No audit window or cycle can be stated — stop; cadence and coverage are undefined without a period." |
| "How far are we from an audit?" | [`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md) | "No framework parameter can be established — stop and ask; "audit our compliance" without a target framework is unanswerable." and "No current-state inputs exist at all (no catalog, no artifacts) — run compliance-control-foundation first; a gap audit against nothing is just the framework's table of contents." |
| "We need to run the NIST AI RMF as an AI risk programme." | [`ai-lifecycle-risk-manager`](../../.claude/skills/ai-lifecycle-risk-manager/SKILL.md) | "No AI system inventory can be established and no program owner exists — stop; a risk program needs both a subject and an accountable human." |

## What this is — and isn't

This is a guided map, not a guarantee. These are design and assessment skills: they
produce a plan, map, gap analysis, evidence design or risk method; they do not implement
controls, run an audit, or sign an attestation. The certification body or an independent
CPA makes the certification or attestation decision — the
[`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md) states
it plainly: "Asked to issue, simulate, or pre-write an audit opinion, certification
statement, or attestation language — refuse; readiness assessment only."

No licensed standard text is reproduced here; each owning skill carries its own rules
about licensed material and evidence. The page makes no readiness, coverage or
host-support claim, and adds no new skill, count or registration. Missing specialists
are copied through the selected-skills route or the step stops; a step whose
precondition above is not met stops in the owning skill's own terms.
