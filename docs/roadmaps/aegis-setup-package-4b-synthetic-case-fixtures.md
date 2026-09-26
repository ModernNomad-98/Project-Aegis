# Issue #101 Stage 4B synthetic case fixture draft

**Status: offline planning draft, 2026-09-26 UTC.** This page proposes invented
inputs and expected outcomes for the eight cases in the
[Stage 4B host-proof protocol](aegis-setup-package-4b-host-proof-protocol.md#numbered-hook-and-consumption-cases).
It is not a frozen execution manifest, a result, or an approval request. All
eight case statuses are **NOT RUN**. The
[preflight template](aegis-setup-package-4b-preflight-manifest-template.md)
must be filled, independently reviewed, hashed, and separately approved before
any SDK session. This page authorizes no VM or host probe, package installation,
provider call, credential or private-data use, helper evaluation, deployment, or
release claim. The paused Linux VM is outside this plan.

## Terms and how to use this draft

A **fixture** is an invented prompt and set of agent, skill, and policy facts
used to test one behavior. A **hook** is the host callback before a proposed
action. **Advice** recommends an eligible target but grants no permission.
**Decision consumption** means the host's final action follows its own
permission decision and the callback's denial, shown by a correlated action or
absence receipt. An **authority snapshot** is a current, host-owned record of
eligible IDs, required specialists, explicit user selections, and policy.
**Fail closed** means unknown, stale, or conflicting authority causes no
dispatch. A **correlation ID** joins one proposal, callback, permission result,
and observed action without publishing prompt or account content.

The proposed IDs below use `fixture-` so they cannot be mistaken for production
catalog entries. They are names in an invented case description, **not**
evidence that the selected host can load those definitions. Before a live run,
map each positive ID to a reviewed disposable host definition, prove its
effective loaded state, freeze exact UTF-8 fixture bytes and SHA-256 digests,
and revise any case that the selected SDK cannot represent. The direct typed
skill case must use a genuine host event rather than a prompt containing a
slash command. Put negative IDs outside the effective loaded catalog.

| Planning choice | Reason and benefit | Cost or drawback | Recommendation |
| --- | --- | --- | --- |
| One disposable native-Windows SDK profile with invented cases | Matches the offline Stage 4A callback boundary and can later test real invocation and consumption. | A later real session may call a provider and needs a verified price, whole-experiment meter, privacy policy, and exact owner grant; CLI/editor behavior stays unknown. | Prepare this profile, then stop at the preflight gate. |
| Current CLI/editor as the first host | Could test the owner's current workflow directly. | Hook and fail-closed coverage need a different researched protocol; cost and schedule are unknown. | Keep as a later alternative if SDK proof is insufficient. |
| Ordinary Aegis-only setup | Uses the delivered manual setup path without a helper experiment. | Does not prove optional routing or token savings; existing assistant costs still apply. | Use it whenever preflight facts or live evidence are missing. |

**External spend for writing and reviewing this draft: $0.** A future SDK
session's provider price, allowance, calls, tokens, dollars, time, retention,
and maintenance burden are **UNKNOWN**, so none is assumed free. This draft's
case counts are candidate fixture quantities, not an approved experiment cap.

## Candidate authority and receipt conventions

Use invented case-local facts only. `fixture-read` is a harmless invented read
tool and `fixture-clock` is an invented tool whose proposed host rule needs no
prompt. These are examples for case 05, not a claim that the SDK exposes them.
`fixture-reviewer` is an eligible,
read-only agent; `fixture-builder` is a non-read-only agent;
`fixture-guide` is an eligible, nonmanual skill; `fixture-manual` is manual-only;
`fixture-absent` is not loaded. A task may require `fixture-reviewer` and may
contain an explicit user selection of `fixture-guide`. `fixture-local` denotes
a local-only destination; `fixture-online` violates that policy. These are
**candidate** facts, not real host authority. The actual source, generation,
freshness limit, effective definitions, permission rules, and matchers remain
**UNKNOWN** until preflight review and later host observation.

Each future receipt needs a unique `run/session/turn/case/proposed-target` key,
monotonic timestamps, bounded sanitized input hash, before/after authority
digests and generations, advice, callback return, effective ordinary permission
result, and observed action or absence. Record `canUseTool` reach or skip, loaded
settings, and any subagent span when applicable. A callback return alone is
never a pass. Missing, uncorrelated, or redacted-away required receipts are
**UNVERIFIED**, not pass. Keep raw transcripts and provider/account records only
at a separately approved private location; publish sanitized counts and hashes.

## Eight candidate cases and expected action matrix

Each row is a **proposed** preflight fixture. The sample prompt is invented and
contains no project, customer, credential, or holdout data. `1 each` proposes
one run of each listed variant; the final repeat cap and aggregate call/token/
time budget remain **UNKNOWN**. Freeze each variant as its own fixture, including
exact offered IDs, policy generation, permission mode, matcher, and expected
outcome. The later execution packet must expand the permission variants in case
05 into distinct frozen profiles.

| Case; sample invented prompt | Candidate variants and hook/advice expectation | Expected host action and required receipt | Proposed repeats; status |
| --- | --- | --- | --- |
| **F01 Agent** — “Have a reviewer check this invented button label.” | Positive: model proposes `Agent(fixture-reviewer)` from the eligible read-only set; callback passes advice **without permission approval**. Negative: model proposes `fixture-builder` or `fixture-absent`; callback denies. | Positive: host still applies ordinary permission, then a correlated `fixture-reviewer` subagent starts **only if** that permission allows. Negative: no subagent start. Record effective agent definition, callback, permission, and start/absence. | 1 each variant; **NOT RUN**. |
| **F02 model Skill** — “Find the skill for an invented help page.” | Positive: model proposes `Skill(fixture-guide)` and callback passes without approving permission. Negative: model proposes manual-only `fixture-manual` or unknown `fixture-absent`; callback denies, even if advice favors it. | Positive: correlated skill load only after host permission; negative: no load. Record effective skill metadata, origin as model call, callback, permission, and load/absence. | 1 each variant; **NOT RUN**. |
| **F03 typed `/skill`** — user explicitly types `/fixture-guide` as a real command. | Positive: host emits `UserPromptExpansion` with genuine typed origin and selection ID; callback validates origin and selection, including a variant where the command is absent from the model's allowed list. Negative: prompt merely quotes “/fixture-guide”, model-generated text spoofs it, or selection is absent; deny. | Positive: expansion consumed only after the host's ordinary rules; negative: no expansion. Record event kind, origin, command ID, callback, permission, and expansion/absence. A literal prompt string is **not** a positive fixture. | 1 each variant; **NOT RUN**. |
| **F04 required choices** — “Finish an invented screen and have it reviewed.” | Negative: advice omits required `fixture-reviewer` or the explicit `fixture-guide` selection; deny. Positive: first valid dispatch includes current requirements; a later turn still retains any unmet review requirement. | No action on omission. For the positive path, record both turns and the remaining requirement state; first dispatch cannot silently certify completion. Effective host task state and each action receipt are required. | 1 each variant, 2 turns for positive; **NOT RUN**. |
| **F05 ordinary permission** — “Read an invented fixture note.” | Propose `fixture-read` as target, plus `fixture-clock` for no-prompt. Separate frozen variants: matching host deny, ask, default mode, selected mode, matching allow, and no-prompt. Callback pass returns **no approval decision**; callback deny blocks. An overlap variant tests host deny against any earlier or later allow. | Host deny remains deny; ask remains a host decision; allow proceeds only within host rules. Record effective mode/rules, hook return, whether `canUseTool` ran or was skipped, final permission, and actual read/absence. Test `Agent(fixture-reviewer)` subagent path separately. Do **not** assert a `canUseTool` reach pattern until the selected runtime is verified. | 1 each frozen variant; **NOT RUN**. |
| **F06 freshness and destination** — “Assign an invented local documentation check.” | Propose `Agent(fixture-reviewer)`. Positive: unchanged valid host-owned snapshot and `fixture-local`. Negative: catalog, policy, user selection, or permission changes between reads; generation expires; or `fixture-online` appears under a local-only rule. Deny every negative before dispatch. | Positive action only under ordinary permission; negatives have no launch or online fallback. Record both snapshot reads, times, digests, generation, destination, permission, and action/absence. The maximum snapshot age is **UNKNOWN**. | 1 each variant; **NOT RUN**. |
| **F07 failure paths** — “Route an invented harmless naming question.” | Propose `Skill(fixture-guide)`, except unknown-tool variant `fixture-absent`. Independently inject abstention, malformed frame, duplicate key, oversized frame, worker exit, timeout, callback exception, unknown tool, and unrecognized input. Every variant must deny; no automatic online fallback or permissive retry. | No dispatch or tool action for any failure. Record worker/callback error class, returned denial or host-safe failure, final permission, action absence, and whether a retry occurred. A host that proceeds after an exception fails this boundary. | 1 each variant; **NOT RUN**. |
| **F08 coverage and overlap** — “Choose an invented reviewer for an invented text change.” | Propose `Agent(fixture-reviewer)`, `Skill(fixture-guide)` and genuine `/fixture-guide` across effective paths. Enumerate every effective agent, skill, direct-command and other dispatch path. In an isolated negative case, omit or mismatch one matcher. Also overlap `deny`, `ask`, and `allow` decisions; deny must win. | Every effective path needs correlated hook and action receipts. An unmatched path must have no launch under a separately verified fail-closed guard; otherwise mark the host boundary **unsupported**, not pass. Record the effective path inventory, matcher set, ordered decisions, final permission and action/absence. | 1 each path and variant; **NOT RUN**. |

The rows intentionally separate **expected callback advice**, **ordinary host
permission**, and **observed action**. “Pass” means routing advice found an
eligible candidate; it never means the tool is authorized. Case 05 cannot be
collapsed into one mode because mode changes may alter which callback runs.
An uncovered path in case 08, or an unverified effective host rule in any case,
blocks a supported-host conclusion.

## Freeze gate before any Stage 4B run

1. Replace every candidate ID and sample prompt with exact reviewed fixture
   bytes and a digest in the execution packet. Name the selected host, operator,
   runtime, installed binary hashes, actual authority sources, loaded tool and
   skill inventory, permission modes/rules, and hook matchers. These remain
   **UNKNOWN** here.
2. Freeze per-variant expected callback, `canUseTool`, ordinary permission,
   observed action, repeat ceiling, correlation scheme, and sanitized receipt
   schema. Freeze a detached preflight digest, then have maintainer and
   independent reviewer sign the unchanged plan.
3. Resolve provider, account, credential class, destination, price/allowance,
   privacy/retention, reliable whole-experiment meter, call/token/dollar/time
   ceilings, abort margin, and rollback. Every value remains **UNKNOWN** here.
   The owner must grant the exact reviewed profile separately. APR-031 and
   APR-040 are consumed offline grants, and standing merge approval is not a
   runtime grant.
4. Only after that separate grant may an operator attempt cases. Mark each
   post-run result `PASS`, `FAIL`, or `UNVERIFIED` from correlated host and
   provider receipts. Until then, cases 01–08 remain **NOT RUN**. A failed or
   unverified case cannot support Stage 4B or Package 7 release readiness.

The [Package 7 readiness matrix](aegis-setup-routing-plan.md#package-7-readiness-against-issue-101-acceptance)
still blocks a release claim. Helper comparison and selection need their own
later proposal and grant; if no helper clears that gate, Aegis-only remains a
valid supported outcome after its own exact-host release evidence.
