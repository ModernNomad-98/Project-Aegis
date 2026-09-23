# Conversational setup and optional routing — issue #101

Prepared 2026-09-23. Canonical planning home for [issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101).
Package 1 is design and candidate screening only. Package 2 delivers a
manual-only four-choice setup conversation and tested Windows PowerShell
Aegis-only saved selection. Optional helpers remain unavailable. There is no
host hook, model, installation, credential, paid evaluation, or savings claim.
Later packages need their own bounded scope and authority. The [BER](behavioral-eval-runner-backlog.md) and
[delivery control](resumable-control-plane-backlog.md) registers remain separate.
The [package-2 authorization proposal](aegis-setup-package-2-authorization-proposal.md)
defines the implementation scope approved in AEGIS-APR-007; the proposal alone
does not grant runtime authority.

Package 3's approved offline advisory contract is implemented in
[`tools/aegis_setup`](../../tools/aegis_setup/README.md). It validates bounded
synthetic offers and responses but has no host hook, provider call, dispatch
authority or real compatibility proof. Package 4 still owns host integration
and fallback verification.

## Dated product decisions

| Date | Decision | Status |
| --- | --- | --- |
| 2026-09-23, original proposal | Make setup conversational in the user's existing coding assistant; explore GLiClass as local and Jev as online assistance | Historical proposal, not a selected implementation |
| 2026-09-23, owner forward correction in issue #101 | Offer Aegis only, Aegis plus a local helper, Aegis plus an online helper, and Help me choose; GLiClass/Jev are candidates | Governing product choice |
| 2026-09-23, owner routing clarification in issue #101 | Use Jev-style structured decisions to assign bounded work to eligible agents with suitable skills and measure complete-task token use | Governing evaluation objective; no vendor chosen |
| 2026-09-23, this package 1 design | Keep the baseline usable without an add-on; use a single advisory contract and separate setup/host/adapter responsibilities | Proposed implementation architecture, subject to review and package 2/3 authority |

## Current source boundary and forces

Inspected at public `main` after PR #108 (`2b13be9fac1169bf8f6cd0cfcbe4da0c5b8bf926`).
`AGENTS.md` and `CLAUDE.md` route the host to installed skill files; the
library's seven `.claude/agents/` definitions are read-only specialists. The
current host/implementing assistant owns execution. `docs/skills-catalog.md`
lists shipped skill identities, while each `SKILL.md` declares its trigger and
invocation posture. Consumer repositories copy the startup files and skills;
the source library does not own their application data. The existing setup is
README-guided copying. There is no issue #101 setup state, host invocation,
decision adapter, or measured routing baseline in this repository. A skill
description or an available MCP endpoint alone cannot prove host use.

Ranked design forces: (1) preserve eligibility, manual-only invocation and
required reviews; (2) work in the existing assistant, including a direct
Aegis-only finish; (3) measure complete-task quality and tokens before a
helper recommendation; (4) minimize installation and data exposure; (5)
support change, disablement and recovery without stale verified claims.

## Proposed component and data ownership

| Component | Responsibility and allowed dependency | Owned state |
| --- | --- | --- |
| Proposed `aegis-setup` skill | Own plain-language choice flow, Help me choose and status explanation; call a package-2 state API only after the user selects; never install/connect on selection alone | No credential or provider state |
| Setup state service (package 2) | Validate schema, scope and state transition; atomically write a per-user, per-project record. Aegis-only can finish with no provider probe | User choice, project identity, selection timestamp, `selected/configured/verified/unavailable`, evidence version and last verification time; no secret |
| Host bridge (package 3/4 proof) | On one pinned host/version, gather approved task context and installed catalog metadata, derive eligible agent/skill IDs, invoke the optional router and consume only validated output | Ephemeral request/result and measured telemetry; no authority grants |
| Eligibility and policy gate | Apply host permissions, explicit user skill choices, manual-only flags, required specialists/reviews and stage rules before dispatch, and recheck after a suggestion | Current host and catalog policy, not model output |
| Provider-neutral decision adapter (package 3) | Accept a bounded, minimized request; return known IDs or abstain with typed errors and timeout; do not dispatch work | Adapter-specific configuration, separated from model identity and local/hosted location |
| Optional local/online provider (packages 4–6) | Compute a recommendation only after explicit setup and evaluation authority | Model weights local or provider-side; online credential in host secret storage, never chat or tracked state |
| Evidence and evaluator (packages 4/7) | Freeze reviewed cases and report paired host workflows, costs, failures and claims | Versioned sanitized protocol/results; any sensitive test input in separately approved private storage |

The setup state service owns writes. The host bridge may read its selected
configuration but must reverify a changed catalog, provider, machine or host
version before claiming `verified`. A missing record means Aegis only with
`unselected` status, not an invented prior choice. The proposed state is local
to one user and one project on one host. Package 2 must choose and test exact
Windows and other supported paths, project identity, permissions, migration,
atomic writes and recovery; syncing or committing preferences requires a
separate decision. A fresh machine shows the choice as unavailable until
reconfigured. Credential references may be stored, never credential values.

The request contract contains a bounded task synopsis, stage/context IDs,
current eligible agent IDs and role summaries, eligible skill IDs and short
descriptions, and policy/catalog versions. It excludes arbitrary repository
files, secrets, raw conversations and unrelated project data. Outbound online
fields and destination must be shown to the user before connection. The result
is a subset of offered IDs, optional calibrated score with model-specific
meaning, and `abstain/escalate`. Unknown IDs, omitted required specialists,
malformed output, timeout, stale version or ineligible suggestion are rejected
and fall back within existing authority. The model cannot authorize a write,
choose a new coding model, waive a review, or convert a read-only agent to a
writer. Local failure never changes the processing destination to online.

### Setup and invocation boundary

The setup skill is side-effecting and must be manual-only. The explicit
phrases "Help me set up Aegis" and "Help me change my Aegis setup" name the
setup task; a supported host may treat them as human invocations, but must
not infer setup from a vague request. If a host cannot establish an explicit
invocation, it may show the choices in ordinary conversation and request the
named skill before writing state. It explains all four choices first. Aegis only saves
the selection and finishes immediately. Exploring a helper retains a visible
route back to Aegis only. Read-only compatibility checks may follow explicit
local interest; installation or online connection needs the user's exact
choice, host support and its own authority. `selected` describes intent,
`configured` proves dependencies/credentials are present, `verified` requires
actual host invocation and result consumption, and `unavailable` records a
failed or unsupported condition. Changing or disabling a helper returns to
ordinary Aegis behavior and invalidates stale verification.

The proposed host integration is an explicit pre-dispatch hook in a selected,
versioned coding-assistant surface. Package 4 must prove that the host invokes
it, applies eligibility, consumes or rejects a result, records fallback, and
exposes enough telemetry to measure main/subagent tokens. If no supported host
hook is proven, only the conversational Aegis-only path may be called working.
An SDK feature does not imply equivalent CLI/editor behavior.

## Candidate discovery and screen

Read the live issue's [source-based audit](https://github.com/ModernNomad-98/Project-Aegis/issues/101) and linked primary project sources on 2026-09-23. This is a discovery screen, not a model benchmark or shortlist freeze. API shape, README claims, hardware estimates and author benchmarks do not establish Aegis task accuracy. Before package 4, pin an exact repository/checkpoint/license/dependency version and verify each claimed runtime on the chosen host. Re-screen source currency before installing.

| Candidate class | Discovery disposition | Required resolution before a bounded test |
| --- | --- | --- |
| Aegis only; deterministic eligible-ID rules | Mandatory two baselines | Capture actual assistant-native skill loads and agent calls; use the same host bridge for rules versus learned helpers |
| [Laya](https://github.com/NandhaKishorM/laya) | Direct typed-decision candidate; project documents choice/score/yes-no checkpoints and Windows setup | Pin checkpoint, license and 512/1024 context handling; test full Aegis task descriptions, CPU load and calibration |
| [Mapika/decider](https://github.com/Mapika/decider), [Kev](https://github.com/jaredpalmer/kev) | Direct trained-decision candidates, separate checkpoint profiles | Verify available weights, license, memory/backend, exact interface and safe handling of long state |
| [OpenDecision](https://github.com/deepanwadhwa/OpenDecision), [SemIf](https://github.com/TheoLeeCJ/SemIf) | Packaged NLI or scoring method candidates | Pin underlying model; do not count a wrapper and its same weights as independent model evidence |
| [OpenJev](https://github.com/SiliconLabAI/OpenJev) | Integration/UX wrapper reference | Its LLM and Decider modes need separate cost/error accounting; not a new independent checkpoint |
| [Verdict](https://github.com/Heman10x-NGU/openJev-verdict-2.0), [NanoJev](https://github.com/TianyuCodings/NanoJev) | Research candidates | Resolve downloadable weight/license and domain transfer; keep out of a supported default until proven |
| [GLiClass](https://github.com/Knowledgator/GLiClass), DeBERTa/ModernBERT NLI | Generic classification controls | Pin exact checkpoint, label count, truncation, runtime and terms; classification is not automatically Jev-equivalent |
| [BGE-small](https://huggingface.co/BAAI/bge-small-en-v1.5), [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) | Retrieval and small-instruction controls | Include candidate retrieval/recall or constrained-output errors and local memory/latency |
| [TypeSafe Jev](https://docs.typesafe.ai/primitives), other hosted providers | Online decision-service candidates | Verify exact model/service, destination, pricing, credential and retention terms, budget control and host telemetry before calls |

An interface-compatible server can make adapter experiments cheaper, but its
intelligence and error profile remain candidate-specific. Do not rank models
from project-provided benchmark claims. A deployment location is a separate
choice from the model; an open checkpoint can be local or hosted only if that
actual offering and terms are verified.

## Predeclared evaluation protocol for package 4

1. **Freeze before test.** Choose one host/version and two target machine
   profiles, then pin source/catalog/agent definitions and supported candidate
   configurations. Record license, maintenance, availability, exact model,
   runtime, quantization and data destination. Exclude candidates that cannot
   be run under the approved budget or cannot meet the required data boundary;
   publish the reasons. The short list is a later reviewed artifact, not this
   document's candidate list.
2. **Reviewed cases.** Build development and sealed holdout partitions from
   real Aegis task/skill/agent-capability scenarios. Include simple, ambiguous,
   multi-skill, security-sensitive, explicit/manual-only, no-match, injection,
   stale-catalog and failed-provider cases. Keep related paraphrases in one
   partition. A reviewer labels eligible destinations, required specialists,
   skills and acceptable abstentions; do not infer gold labels from a model.
   Public trigger evals can seed development only unless independently screened.
3. **Equal tuning and comparison.** Declare a bounded development-data tuning
   budget per candidate before opening holdout. Compare assistant-native Aegis,
   deterministic rules and each short-listed helper on identical offered IDs,
   context, permissions, executor models, required review and completion
   criteria. Record prompt/preprocessing/truncation, fallback and all revisions.
4. **Routing measures.** Report eligible agent and skill precision/recall,
   missed required specialist/skill, prohibited manual-only invocation,
   abstention and high-confidence errors, unnecessary calls, wrong-agent
   reroutes and duplicated context. Treat any uncorrected prohibited or missed
   mandatory selection as a selection-gate failure; report sample counts and
   uncertainty rather than calling a small zero-error set proof of safety.
5. **Whole-task measures.** Run paired completed tasks with the same executor
   model, permissions, reviews and quality criteria. Count router and executor
   input/output, cached/uncached tokens per model, dispatch, retries, correction,
   fallback and independent review. Report router compute, cold/warm latency,
   local peak memory, hosted charges and local setup/operating burden separately.
   Token counts from different tokenizers are not directly comparable costs.
6. **Selection gate.** A helper needs a proven host hook, no unresolved
   authority/safety defect, acceptable complete-task quality and statistically
   described gains in end-to-end coding-assistant token use or another stated
   user benefit after added work. Publish results per deployment profile and
   support level; Aegis only may win. A savings percentage, subscription-bill
   reduction or model recommendation requires measured evidence. Any live
   provider evaluation needs exact inputs, destination, call/token/dollar caps
   and a separate owner grant before execution.

The package 4 authorization must fix case counts, repeats, quality tolerance,
sampling/uncertainty method, hardware, time and spend caps before results are
seen. Changing them after holdout requires a new version and review. A severe
safety failure stops selection even if average token count improves.

## Options, ADR draft and migration

| Option | Delivery/cost | Operability and failure | Reversibility |
| --- | --- | --- | --- |
| Aegis only with conversational setup | Smallest new surface; no helper service cost | Existing assistant routing remains measurable baseline | Immediate disable/return path |
| Provider-neutral optional advisory hook (proposed) | More contract and host-proof work; compare local/online without separate setup designs | Validation, data minimization and fallback need explicit ownership | Disable helper without changing Aegis skills |
| Provider-specific setup first | Quicker single demo, but couples onboarding and claims to an untested candidate | Stale provider/host assumptions can report false verified state | Migration and user trust cost higher |

**ADR draft:** Choose Aegis-only setup as the first shippable increment and
design one optional advisory contract for later evaluated helpers. Preserve
host-owned eligibility/dispatch and separate model from deployment location.
Consequence: local/online setup remains unavailable until host proof and
candidate selection, but users can complete setup without dependencies.
Revisit if the chosen host cannot expose a safe pre-dispatch hook or meaningful
complete-task telemetry. This is a design proposal, not provider selection.

Incremental sequence: (1) package 1 planning and review; (2) package 2
setup conversation, saved state and Aegis-only completion with unavailable
helper status; (3) package 3 offline contract and mocked error paths; (4)
package 4 host proof and predeclared comparison under separate authority;
(5) conditional local/online integration only for selected profiles; (6)
package 7 full evaluation and release review. Stop at each package boundary
when its authority, evidence or acceptance is missing.
