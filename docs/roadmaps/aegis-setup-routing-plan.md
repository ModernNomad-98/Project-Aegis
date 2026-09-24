# Conversational setup and optional routing — issue #101

Prepared 2026-09-23. Canonical planning home for [issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101).
For maintainers planning the next package, start with the [current delivery
boundary](#component-map-shipped-seams-and-future-work), the [agreed local
comparison](#agreed-first-local-comparison-for-package-4), and the
[evaluation protocol](#predeclared-evaluation-protocol-for-package-4). Product
users invoke the manual [`aegis-setup`](../../.claude/skills/aegis-setup/SKILL.md)
skill for the four-choice conversation; this plan grants no execution authority.

Package 1 delivered design and candidate screening. Package 2 delivers a
manual-only four-choice setup conversation and tested Windows PowerShell
Aegis-only saved selection. Optional helpers remain unavailable. No optional
helper model or host hook is installed, connected or evaluated, and there is
no paid evaluation or measured savings claim.
Later packages need their own bounded scope and authority. The
[Behavioral Eval Runner (BER)](behavioral-eval-runner-backlog.md) and
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
| 2026-09-23, owner local-evaluation shortlist in issue #101 | Evaluate Laya and Mapika/Decider 0.8B first on ordinary central processing units (CPUs); compare OpenJev as an optional wrapper around the same Decider checkpoint | Governing package-4 research order, not an installed helper, production selection or execution grant |
| 2026-09-23, this package 1 design | Keep the baseline usable without an add-on; use a single advisory contract and separate setup/host/adapter responsibilities | Proposed implementation architecture, subject to review and package 2/3 authority |

## Historical source snapshot and design forces

This is the package-1 snapshot, inspected at public `main` after
pull request (PR) #108
(`2b13be9fac1169bf8f6cd0cfcbe4da0c5b8bf926`), before packages 2 and 3.
`AGENTS.md` and `CLAUDE.md` route the host to installed skill files; the
library's seven `.claude/agents/` definitions are read-only specialists. The
current host/implementing assistant owns execution. `docs/skills-catalog.md`
lists shipped skill identities, while each `SKILL.md` declares its trigger and
invocation posture. Consumer repositories copy the startup files and skills;
the source library does not own their application data. Setup was then
README-guided copying. At that snapshot there was no issue #101 setup state,
host invocation, decision adapter, or measured routing baseline. A skill
description or a Model Context Protocol (MCP) endpoint alone cannot prove
host use. The [current package boundaries](#component-map-shipped-seams-and-future-work)
below supersede this snapshot for delivery status.

Ranked design forces: (1) preserve eligibility, manual-only invocation and
required reviews; (2) work in the existing assistant, including a direct
Aegis-only finish; (3) measure complete-task quality and tokens before a
helper recommendation; (4) minimize installation and data exposure; (5)
support change, disablement and recovery without stale verified claims.

## Component map: shipped seams and future work

The first two rows and the offline contract are shipped. Other rows describe
future host integration or conditional helpers; none grants new authority.

| Component | Responsibility and allowed dependency | Owned state |
| --- | --- | --- |
| Shipped `aegis-setup` skill (package 2) | Show four choices; save only an explicit Aegis-only choice on tested Windows PowerShell; never install or connect a helper | No credential or provider state |
| Shipped state writer (package 2) | Validate and atomically save one user's Aegis-only selection for one checkout | `selected` record and `unselected` missing status; no helper verification or secret |
| Future host bridge (package 4) | On a pinned host/version, derive eligible agent/skill identifiers (IDs), invoke optional advice and recheck it before dispatch | Ephemeral request/result and measured telemetry; no authority grants |
| Future eligibility and policy gate | Apply host permissions, explicit choices, manual-only flags, required specialists/reviews and stage rules before dispatch and after advice | Current host and catalog policy, not model output |
| Shipped offline advisory contract (package 3) | Validate bounded synthetic offers and recommendations or abstentions with typed failures; fake adapter has no host hook or dispatch | In-memory request/result only; no provider configuration or credential |
| Conditional local/online providers (packages 5/6, after package 4) | Compute advice only after selection, host proof and separate integration authority | Future local weights or hosted service; credentials must remain outside chat and tracked state |
| Future evidence and evaluator (packages 4/7) | Freeze reviewed cases and report paired host workflows, costs, failures and claims | Versioned sanitized protocol/results; any sensitive test input in separately approved private storage |

The package-2 writer owns the only setup write: an Aegis-only selection for one
user and checkout on tested Windows PowerShell 5.1. A missing record means
`unselected` and ordinary Aegis behavior, including on a fresh machine; a
moved checkout gets a different key. Other operating systems have no verified
saved-state support. The writer stores no credential reference, helper choice,
or `configured`, `verified` or `unavailable` helper state. A future host must
reverify any changed catalog, provider, machine or host version before it can
claim helper verification. Syncing preferences needs a separate decision.

The package-3 [offline contract](../../tools/aegis_setup/README.md) accepts a
versioned, bounded one-line task synopsis, stage, offered agent/skill IDs and
descriptions, mandatory and explicit selections, and policy/catalog versions.
It has no context-ID or raw-file field. Its structural checks cannot prove
that free-text synopsis content contains no secret or copied conversation;
a future host must curate that text. A recommendation is a subset of offered
IDs that preserves mandatory and explicit selections. The optional score is
**uncalibrated**. The typed outcomes are `recommend`, `abstain`, `timeout`,
`invalid` and `unavailable`; invalid or failed advice contains no selections.
Its compatibility checker uses synthetic supplied facts and proves no real
host support. A future host must still enforce eligibility, approvals and
dispatch, show online fields and destination before any connection, and prove
fallback under separate package-4 authority. Local failure must never switch
processing to an online service silently.

### Setup and invocation boundary

The setup skill is side-effecting and must be manual-only. The explicit
phrases "Help me set up Aegis" and "Help me change my Aegis setup" name the
setup task; a supported host may treat them as human invocations, but must
not infer setup from a vague request. If a host cannot establish an explicit
invocation, it may show the choices in ordinary conversation and request the
named skill before writing state. It explains all four choices first. Aegis only saves
the selection and finishes immediately. Exploring a helper retains a visible
route back to Aegis only. Package 3 checks synthetic catalog facts only;
real read-only compatibility checks would follow explicit local interest and
separate host proof. Installation or online connection needs the user's exact
choice, host support and its own authority. `selected` describes intent and
is the only state package 2 saves. Proposed future `configured` would
prove dependencies/credentials are present; `verified` would require actual
host invocation and result consumption; `unavailable` would record a failed
or unsupported helper. Changing or disabling a future helper must return to
ordinary Aegis behavior and invalidate stale verification.

The proposed host integration is an explicit pre-dispatch hook in a selected,
versioned coding-assistant surface. Package 4 must prove that the host invokes
it, applies eligibility, consumes or rejects a result, records fallback, and
exposes enough telemetry to measure main/subagent tokens. If no supported host
hook is proven, only the conversational Aegis-only path may be called working.
Software development kit (SDK) support does not imply equivalent command-line
interface (CLI) or editor behavior.

## Candidate discovery and screen

This table preserves the broader package-1 discovery screen. The
[agreed first local comparison](#agreed-first-local-comparison-for-package-4)
below is narrower; the other rows remain alternatives or controls, not a
commitment to test every candidate. Read the live issue's
[source-based audit](https://github.com/ModernNomad-98/Project-Aegis/issues/101)
and linked primary project sources before changing the shortlist. An
application programming interface (API) shape, README claim, hardware estimate
or author benchmark does not establish Aegis task accuracy. Before package 4,
pin exact source, checkpoint, license and dependencies; verify each claimed
runtime on the chosen host and re-screen source currency before installing.
In the table, natural-language inference (NLI) is a text-classification method,
large language model (LLM) names a model class, and user experience (UX)
describes interaction design.

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

### Agreed first local comparison for package 4

[Issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101)
records a narrower first evaluation order than the historical discovery table
above. Compare **Laya** and **Mapika/Decider 0.8B** with Aegis-only behavior
and simple eligible-agent rules on a CPU. For Laya, start with its English
checkpoint for short agent classification and compare its typed-decisions
checkpoint on development cases before choosing one. For Decider, start with
the 0.8B checkpoint; larger variants are outside this first comparison.
OpenJev is optional integration around that same Decider checkpoint: measure
direct `Aegis → Decider` against `Aegis → OpenJev → Decider`, including the
wrapper's setup, response validation, credential and destination checks,
maintenance and latency costs. Do not count the
wrapper as an independent model or make it a fifth user-facing setup choice.

The local baseline must work without a dedicated graphics processing unit
(GPU) or NVIDIA's Compute Unified Device Architecture (CUDA) accelerator.
Measure cold and warm response time and peak memory
while normal development tools are running. Machines with **8 and 16 gigabytes
(GB)** of memory are proposed evaluation profiles, not verified minimum
requirements. A failed installation or unusable response time leaves Aegis
only available; it never silently switches a user's work to an online service.
No local helper is currently installed, selected for production or authorized
for a live evaluation by this planning record. Pin versions, license,
dependencies, host, cases, budgets and evidence in a separate reviewed
package-4 authorization before executing the comparison. Preserve the wider
discovery table as alternatives and screening history, without committing to
prototype every listed candidate.

## Predeclared evaluation protocol for package 4

1. **Freeze before test.** Choose one host/version and two target machine
   profiles, then pin source/catalog/agent definitions and supported candidate
   configurations. Record license, maintenance, availability, exact model,
   runtime, quantization and data destination. Exclude candidates that cannot
   be run under the approved budget or cannot meet the required data boundary;
   publish the reasons. The agreed first research shortlist is above; the
   exact runnable configuration and any changed shortlist require a later
   reviewed, version-pinned package-4 authorization.
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

## Historical options and architecture decision record (ADR) draft

| Option | Delivery/cost | Operability and failure | Reversibility |
| --- | --- | --- | --- |
| Aegis only with conversational setup | Smallest new surface; no helper service cost | Existing assistant routing remains measurable baseline | Immediate disable/return path |
| Provider-neutral optional advisory hook (proposed) | More contract and host-proof work; compare local/online without separate setup designs | Validation, data minimization and fallback need explicit ownership | Disable helper without changing Aegis skills |
| Provider-specific setup first | Quicker single demo, but couples onboarding and claims to an untested candidate | Stale provider/host assumptions can report false verified state | Migration and user trust cost higher |

**Historical ADR draft:** Aegis-only setup was selected as the first shippable
increment, followed by one optional advisory contract. Packages 2 and 3 now
deliver those two seams. Host-owned eligibility and dispatch, and the
separation of model from deployment location, remain required. Local and
online helpers remain unavailable until host proof, evaluation and a later
selection. Revisit the design if a selected host cannot expose a safe
pre-dispatch hook or meaningful complete-task telemetry. This draft does not
select a provider.

Delivery sequence: (1) package 1 planning — **delivered**; (2) package 2
conversation and Windows Aegis-only saved selection — **delivered**; (3)
package 3 offline contract and fake adapter — **delivered**; (4) package 4
host proof and predeclared comparison — **pending separate authority**;
(5) packages 5 and 6 local/online integrations — **conditional on package 4**;
(6) package 7 full evaluation and release review — **pending**. Stop at each
remaining boundary when its authority, evidence or acceptance is missing.
