---
name: aegis-setup
description: 'MANUAL-ONLY; never auto-invoke. Use when a person explicitly says "Help me set up Aegis" or "Help me change my Aegis setup" to choose Aegis only or explore future local/online helpers. Do not use for a vague product idea, project stage navigation, ordinary skill selection, security review, or an eval run.'
disable-model-invocation: true
---

# Aegis setup

## Purpose

Guide one person through four plain-language setup choices and, on tested
single-user Windows PowerShell, save an Aegis-only preference for this checkout.
The optional helpers are unavailable in this package. The saved preference
never authorizes a tool, provider, model or agent.

## Use When

- Use only after an explicit human setup invocation, including "Help me set up
  Aegis" or "Help me change my Aegis setup" on a host that treats the phrase
  as a deliberate invocation of this manual skill.
- If host routing cannot establish that invocation, show the four choices in
  ordinary conversation and ask for the named `aegis-setup` invocation before
  any state write.
- Do not use for a vague product idea, lifecycle navigation (owned by
  `project-orchestrator`), engineering task, security review, BER run, or a
  request explicitly naming another skill.

## Inputs to Inspect

1. Current checkout root and whether it is a real directory, not a redirect.
2. Operating system and shell: the saved selection path is tested only on
   Windows PowerShell 5.1 in a single user account and one local checkout.
3. For a change request, read current status with `scripts/selection.ps1`.
4. [State contract](references/state-contract.md) before describing persistence.

## Workflow

1. Show all four choices before asking which one the user wants:

   | Choice | Who it suits and practical effect |
   | --- | --- |
   | **Aegis only** | People who want the current skills and assistant with no extra setup or helper fee. The existing assistant still processes task text in its usual location. This is the only completable choice today. |
   | **Aegis plus a local helper** | People interested in a future helper on their computer. It would need separate installation, machine fit and testing; it could add setup effort and local compute cost. The whole coding workflow would still use the existing assistant, so it would not become fully offline. Unavailable today. |
   | **Aegis plus an online helper** | People interested in a future remote decision service. It would need a separately reviewed destination, account/terms, credential and possible extra cost. Selected task text would leave the machine for that service. Unavailable today; do not ask for a credential. |
   | **Help me choose** | People who want one simple preference question at a time. Start by asking whether they want Aegis working now without extra setup. Recommend Aegis only as the currently completable path; explain either helper on request and offer Aegis only again. |

2. Explain that **tokens are units of text processing**. A helper might change
   token use, but no savings have been measured; existing assistant costs
   remain. No model or helper is selected or recommended here. Ask no hardware
   threshold question.
3. If the user explores a helper, mark it **unavailable** and always offer
   "Choose Aegis only". Never save a helper choice as completed or attempt an
   install, connection, provider call or fallback from local to online.
4. If the user chooses Aegis only, on supported Windows PowerShell run:
   `powershell -NoProfile -ExecutionPolicy Bypass -File .claude/skills/aegis-setup/scripts/selection.ps1 -Action select -ProjectRoot "<absolute-checkout-root>"`.
   This setting applies to that PowerShell process. If host policy still blocks
   the script, report the save as unavailable; do not change machine policy.
   A missing path, failed write, unsupported OS or malformed prior record is
   not completion. Report the actual result. On another OS, continue ordinary
   Aegis use and say saved-state support is unverified/unavailable.
5. On "Help me change my Aegis setup", use the same command with `-Action status`
   first. Show the project scope and current state. Missing means unselected, ordinary
   Aegis behavior. If the record is corrupt or an unknown version, explain
   that no helper is active; offer an **explicit** Aegis-only repair. Only after
   the person chooses repair, run `-Action repair` for that same root. An
   ordinary Aegis-only switch uses `-Action select`; it invalidates any former
   helper claim. This package never stores helper verification.

## Output Format

Present the choices and the user's selected path in plain language. For a
successful Windows save, state: "Aegis only is selected for this checkout on
this Windows account. Setup is complete; no helper is configured or verified."
For an unavailable choice or failed save, state that setup did not complete.
Never imply account connection, host routing or measured savings.

## Validation Checklist

- [ ] Four choices were visible at entry and after a change request.
- [ ] One preference question at a time; no hardware or token threshold quiz.
- [ ] Helper processing location, costs and unavailable status were honest.
- [ ] Aegis-only completion followed a successful saved-state response on
      supported Windows; other OS support was not claimed.
- [ ] No provider authority, credentials, install or routing hook was inferred.

## Gotchas

- A copied checkout on another path or host has a new key and starts unselected.
- An unavailable helper is exploration, not a saved completed setup.
- `selected` means preference only. `verified` requires separate host proof and
  is not emitted here.
- A record error is a repair prompt, not permission to overwrite it silently.

## Stop Conditions

- Without deliberate invocation, stop before the state writer.
- A helper request stops at an unavailable explanation and Aegis-only return.
- If the save command fails, stop before claiming completion.
- Never ask for or store a credential, call a provider, install a package, or
  send selected text to a new processing destination.
- Do not repair a corrupt/unknown record until the user explicitly chooses
  Aegis-only repair for this checkout.

## Supporting Files

- [State contract](references/state-contract.md) defines project identity,
  record fields, recovery and limits.
- `scripts/selection.ps1` provides Windows status, select and explicit repair.
- `scripts/test-selection.ps1` uses only synthetic temporary directories.
- `evals/evals.json` and `evals/trigger-evals.json` provide behavioral review
  cases; the validator checks their JSON structure only.
