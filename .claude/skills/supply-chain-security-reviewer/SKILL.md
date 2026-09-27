---
name: supply-chain-security-reviewer
description: 'Review software supply-chain risk with SLSA-style provenance thinking — dependencies (CVEs triaged by reachability, not presence), lockfile integrity/pinning, transitive/typosquat/confusion risk, install and build scripts, CI/CD workflows (untrusted PR triggers, secret exposure, token scopes, unpinned Actions), artifact provenance, and postinstall/hook execution. Extends to the AI/ML (LLM04: models, datasets, adapters, registry promotion) and agentic (ASI04: MCP servers/manifests, tool/skill registries, plugins, A2A dependencies) supply chains. Findings carry a compromise path, exploitability verdict, and remediation (pin, upgrade, remove, isolate). Use when reviewing dependencies, lockfiles, CI workflows, a build pipeline, a dependency bump, an acquired model/dataset/adapter/MCP server, or a model-registry promotion. Do NOT use to triage SAST/CodeQL findings in first-party code (static-analysis-reviewer), review app logic in a diff (security-pr-reviewer), or model feature threats (threat-modeler).'
---

# Supply-Chain Security Reviewer

**Reading key:** SLSA is Supply-chain Levels for Software Artifacts, a
provenance framework. CVE is Common Vulnerabilities and Exposures, the
public vulnerability ID system; CVSS is the Common Vulnerability Scoring
System behind scanner severities; OSV is Open Source Vulnerabilities, a
vulnerability database. CI/CD is continuous integration and continuous
delivery; a PR is a pull request; SHA (Secure Hash Algorithm) names a
commit's immutable hash; SAST is static application security testing
(CodeQL is one such tool). AI/ML is artificial intelligence and machine
learning; MCP is Model Context Protocol; A2A is the Agent2Agent protocol.
OWASP is the Open Worldwide Application Security Project: LLM04 (2026
edition; LLM03 in 2025) is the supply-chain category of its Top 10 for
large language model (LLM) Applications, and ASI04 and ASI07 are
identifiers in its Agentic Top 10 (2026). An SBOM is a software bill of
materials; an AI-BOM is its AI counterpart, an inventory of model
artifacts with their digests, sources, licenses, and base-model lineage.
LoRA is low-rank adaptation, a common small fine-tuning adapter that is
loaded on top of a base model. A model registry holds versioned model
artifacts; promotion moves one version between stages, typically staging
to production.

## Purpose

Assess whether an attacker can compromise the software through what it
depends on and how it is built — not just whether a scanner printed CVEs. The
review applies SLSA-style provenance thinking to dependencies, lockfiles,
install/build scripts, CI/CD workflows, and artifacts, and reports
severity-ranked findings where each carries a compromise path (how an attacker
gets from the weakness to material impact), an exploitability
verdict (reachable/exploitable vs latent), and a concrete remediation. A CVE
in a package that is never called on a reachable path is triaged as such, not
treated as an automatic critical; a `postinstall` script pulling a remote blob
is a finding whether or not a scanner flagged it.

## Use When

- Use when: reviewing dependencies / lockfiles / a dependency bump for
  supply-chain risk.
- Use when: reviewing CI/CD workflows, GitHub Actions, or a build pipeline for
  compromise paths (untrusted triggers, secret exposure, token scope, unpinned
  actions).
- Use when: install/build scripts, postinstall hooks, or vendored artifacts
  need a trust review.
- Use when: a scanner (Dependabot, `npm audit`, Snyk, Trivy) produced output
  that needs triage into what actually matters.
- Use when: acquiring an AI/ML artifact — a third-party base model, a
  downloaded dataset, or a fine-tuning adapter — and its provenance, format
  safety, and pinning need a supply-chain review (OWASP LLM04).
- Use when: a model artifact — acquired or built in-house: weights, a LoRA
  adapter, a merged fine-tune — is promoted through a model registry, and
  the question is whether the artifact that serves production is the one
  that was reviewed: digest pinning, signature and provenance verification,
  safe format, model card and license, registry write/promote access, the
  promotion gate, and an SBOM/AI-BOM inventory (the promoted-artifact trust
  named in LLM04:2026).
- Use when: adopting or updating agentic components (OWASP Agentic ASI04) —
  MCP servers and their manifests, tool/skill registry entries, plugin
  packages, or agent-to-agent dependencies — and their source, requested
  permissions, and pinning need review. Runtime message security between
  installed components is `inter-agent-comms-reviewer` (install-vs-runtime
  is the split).
- Do NOT use when: reviewing the integrity of training data YOU collect or
  pipelines YOU run (feedback loops, RAG ingestion) — that is
  `model-poisoning-reviewer` (acquire-vs-ingest is the split). For a
  promoted model, this skill proves the promoted bytes are the reviewed,
  signed bytes; whether the training or fine-tuning pipeline you run
  taught those bytes malicious behavior (a backdoor, a trigger phrase) is
  `model-poisoning-reviewer` (artifact-integrity-vs-learned-behavior is
  the split).
- Do NOT use when: triaging SAST/CodeQL findings in FIRST-PARTY code — that is
  `static-analysis-reviewer` (dependency-vs-own-code is the split).
- Do NOT use when: reviewing application logic in a diff —
  `security-pr-reviewer`.
- Do NOT use when: modeling feature-level threats — `threat-modeler`.

## Inputs to Inspect

1. Manifests and lockfiles: `package.json`/`package-lock.json`/`pnpm-lock`/
   `yarn.lock`, `requirements.txt`/`poetry.lock`, `go.mod`/`go.sum`, etc. —
   the lockfile records the intended resolved set; verify the installed graph
   and build platform for what actually ships.
2. Scanner output if provided (Dependabot/`npm audit`/Snyk/Trivy/OSV) — input
   to triage, never the final verdict.
3. CI/CD workflows: `.github/workflows/*`, pipeline configs — triggers,
   permissions/token scopes, third-party actions and their pinning, where
   secrets are exposed, and whether untrusted PRs reach privileged jobs.
4. Install/build scripts: `postinstall`/`preinstall`/`prepare` hooks, build
   scripts, Makefiles, Dockerfiles — anything that executes during install or
   build, especially remote fetches.
5. Dependency metadata for risk signals: maintenance status, sudden
   maintainer changes, typosquat/confusion candidates, direct vs transitive.
6. Artifact/provenance signals: are builds reproducible, signed, attested;
   are vendored binaries checked in without provenance.
7. AI/ML artifacts if any (LLM04): third-party base models, downloaded
   datasets, and fine-tuning adapters — their source/registry, revision
   pinning (a mutable tag/`latest` is not pinned), serialization format
   (unsafe pickle or unrestricted `torch.load` can execute code on load;
   prefer safetensors or a verified restricted loading mode), and
   license/provenance. Promotion of any model artifact is item 9; integrity
   of data you curate or pipelines you run is `model-poisoning-reviewer`.
8. Agentic components if any (ASI04): MCP server packages and their
   manifests (which tools/permissions they declare), tool/skill registry
   entries, plugin packages, and A2A dependency declarations — source and
   maintainer, version pinning, and what the manifest asks to access.
9. Model registry and promotion path if any (LLM04:2026 promoted-artifact
   trust): the registry and its stages, who can write, overwrite, or
   promote, promotion records, artifact digests and signatures or
   attestations, the evaluation or approval evidence each promotion cites,
   model cards and licenses, the SBOM/AI-BOM if one exists, and the exact
   reference the serving layer loads (digest, version, or mutable alias).

## Workflow

1. **Establish what actually ships/builds.** Read the lockfile (not just the
   manifest) for the real dependency set; identify direct vs transitive. No
   manifest/lockfile or pipeline to review → Stop Conditions.
2. **Triage scanner output** (if any) by reachability: for each flagged CVE,
   is the vulnerable code path called by this project? Sort into
   true-positive-reachable, true-positive-latent, false-positive, duplicate.
   Presence ≠ exploitability.
3. **Review install/build execution:** enumerate scripts that run on install
   or build; flag remote downloads, curl-to-shell, obfuscated steps,
   credential access. These execute with developer/CI privileges.
4. **Review CI/CD for compromise paths** using
   [references/supply-chain-checklist.md](references/supply-chain-checklist.md):
   untrusted trigger reaching secrets (e.g. `pull_request_target` +
   checkout of PR code + secret use), over-broad `GITHUB_TOKEN`/permissions,
   unpinned third-party actions (tag vs commit SHA), cache poisoning, and
   artifact upload/download trust.
5. **Assess dependency-specific risk:** typosquatting, dependency confusion
   (internal name resolvable from a public registry), abandoned/maintainer-
   changed packages, and unnecessary heavy/native deps that widen the surface.
6. **Check integrity and provenance:** lockfile committed and pinned; hashes/
   integrity present; vendored artifacts have a documented source; releases
   signed/attested where the ecosystem supports it (SLSA levels as a frame).
   For **AI/ML artifacts (LLM04)** — third-party models, datasets, adapters —
   see [references/supply-chain-checklist.md](references/supply-chain-checklist.md):
   pin to an immutable revision/digest (not a mutable tag or `latest`), prefer
   safetensors over unrestricted pickle loading; check the actual `torch.load`
   version and `weights_only` mode before judging its deserialization risk,
   confirm the source registry and license, and treat a downloaded artifact as
   untrusted until its provenance checks out. Integrity of data you curate or
   pipelines you run stays with `model-poisoning-reviewer`. For **agentic
   components (ASI04)** — MCP servers, tool/skill registries, plugins, A2A
   dependencies — verify registry/source trust and maintainer continuity, pin
   to immutable versions, and diff the manifest's requested tools/permissions
   against need (a note-taking server requesting shell access is a finding);
   treat manifest changes on update like dependency-code changes. An MCP
   server is code that answers your agent's tool calls — live message
   security is `inter-agent-comms-reviewer` (ASI07).
7. **Review promoted-model-artifact trust (LLM04:2026)** when a registry or
   promotion path exists, using the promoted-artifacts section of
   [references/supply-chain-checklist.md](references/supply-chain-checklist.md).
   Trace one artifact from build or download to what production loads:
   (a) identity — production loads an immutable content digest, not a
   mutable alias or `latest`, and that digest equals the one the
   promotion approved; (b) provenance — a signature or attestation ties
   the digest to the build job, source revision, base model, and data
   snapshot, verified at promotion AND at load; (c) format — the promoted
   file uses a non-executable format such as safetensors, or the loader's
   restricted mode is verified (step 6); (d) LoRA adapters and merged
   models — the adapter is pinned to its base-model digest, and a merged
   model is a new artifact with its own digest and signature; (e) registry
   access — who can write, overwrite, or promote is least-privilege and
   separate from who trains, versions are immutable once registered, and
   promotions are logged; (f) promotion gate — staging to production
   requires evaluation and human-approval evidence bound to the digest,
   not to a version name; (g) inventory — model card, license, and an
   SBOM/AI-BOM entry exist for what ships. Judge that the gate exists and
   is bound to the artifact; whether its evaluation would catch a poisoned
   behavior is `model-poisoning-reviewer`'s.
8. **Rank findings** with a compromise path and exploitability verdict.
   High severity REQUIRES a path from the weakness to material impact such
   as code execution, secret theft, data exposure or corruption,
   unauthorized action, or availability loss. A reachable exploit or a
   plausible install-time execution can qualify; a latent unreachable CVE
   does not.
9. **Remediate concretely:** pin (to SHA/version+hash), upgrade (state the
   safe version), remove, or isolate (least-privilege token, split trusted/
   untrusted jobs). For model artifacts: serve by approved digest, verify
   the signature at load, re-export to a safe format from a trusted build
   (converting an untrusted pickle means loading it), and restrict promote
   rights. Note accepted risk only with written rationale.

## Output Format

```
SUPPLY-CHAIN REVIEW — <repo/scope>
Dependency set: <direct N / transitive M — from lockfile>
Scanner triage: reachable-TP <n> | latent-TP <n> | false-positive <n> | dup <n>
Findings (severity-ranked):
  [CRITICAL|HIGH|MEDIUM|LOW] <area: dep / script / CI / artifact>
    Compromise path: <weakness → attacker action → material impact>
    Exploitability: <reachable/exploitable | install-time | latent>
    Remediation: <pin SHA / upgrade to <v> / remove / isolate / split job>
Install/build execution: <scripts that run + risk>
CI/CD posture: <triggers, token scope, action pinning, secret exposure>
Provenance: <lockfile pinned? integrity hashes? signing/attestation? SLSA frame>
Model promotion: <served digest = approved digest? signature verified at promote/load? format; registry write/promote access; gate bound to digest? model card/license; AI-BOM>
Accepted risk: <finding — written rationale>
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] Lockfile (not just manifest) used to determine the real dependency set.
- [ ] Scanner findings triaged by reachability into TP-reachable / TP-latent /
      FP / duplicate — none accepted at face value.
- [ ] Install/build scripts and postinstall hooks reviewed for remote fetch
      and privileged execution.
- [ ] CI/CD reviewed for untrusted-trigger-to-secret paths, token scope, and
      third-party action pinning (SHA vs tag).
- [ ] Typosquat/confusion/abandonment risk considered for notable deps.
- [ ] Every HIGH+ finding has a compromise path AND an exploitability verdict.
- [ ] Remediations are concrete (pin/upgrade/remove/isolate), not "update deps".
- [ ] AI/ML artifacts (if any) reviewed for revision pinning, safe
      serialization (safetensors vs pickle/`torch.load`), source, and license;
      curated-data/pipeline integrity routed to `model-poisoning-reviewer`.
- [ ] Promoted model artifacts (if a registry exists) traced from build or
      download to the served reference: digest identity, signature or
      attestation verified at promotion and load, safe format, adapter-to-
      base pinning, registry write/promote access, a promotion gate bound
      to the digest, and model card/license/AI-BOM; learned-behavior
      poisoning routed to `model-poisoning-reviewer`.
- [ ] Agentic components (if any — MCP servers/manifests, tool/skill
      registries, plugins, A2A deps) reviewed for source trust, immutable
      pinning, and manifest permission width (ASI04); runtime message
      security routed to `inter-agent-comms-reviewer`.
- [ ] Accepted risk carries written rationale; not-reviewed list present.

## Security Rules

- Scanner output is input, not truth
  ([historical master prompt, section 6](../../../docs/prompts/claude-skills-master-generation-prompts-v4.md)):
  a CVE is triaged by reachability and exploitability before it gets a
  severity.
- High-severity claims require a compromise path to material impact;
  "a CVE exists" without a reachable/exploitable path is not high.
- Unpinned third-party CI actions (mutable tags) are a finding — pin to a
  full commit SHA.
- `pull_request_target`/privileged workflows that check out and run untrusted
  PR code while secrets are available are treated as critical unless proven
  isolated.
- A model reaches production only by immutable digest, with verified
  signature or provenance and approval evidence bound to that digest; a
  production alias that anyone with registry write access can move is a
  finding, not a promotion process.
- Findings are not suppressed without written rationale via
  `human-approval-boundary`; upgrades that only relocate risk are labeled, not
  claimed as fixes.

## Gotchas

- `npm audit`/Dependabot severity is CVSS-based and context-blind — a
  "critical" in a dev-only or unreachable transitive dep may be noise, while a
  "moderate" on a reachable parser may be the real risk. Triage by reachability.
- The dangerous code often runs at INSTALL time (postinstall) or BUILD time,
  before any test — a scanner scoped to runtime deps misses it.
- Pinning to a version tag is not pinning: tags are mutable; only a commit SHA
  (for actions) or version+integrity-hash (for packages) is fixed.
- Dependency confusion: an internal package name that also resolves on a
  public registry lets an attacker publish a higher version and win — check
  scoping/registry config, not just the lockfile.
- A green Dependabot dashboard says nothing about install scripts, CI token
  scope, or unpinned actions — those are not "vulnerabilities" it scans for.
- Bumping a dependency to clear a CVE can pull a new maintainer's compromised
  release — review the upgrade target, don't just accept "latest".
- Unsafe model deserialization can execute code: `pickle.load` and
  `torch.load(..., weights_only=False)` can run arbitrary code from an
  untrusted checkpoint. Recent PyTorch releases default to a restricted
  `weights_only=True` loader (a verification item): confirm the installed
  version, mode, and any allowlisted globals. Prefer safetensors where
  suitable and never treat an untrusted artifact as safe solely from its
  `.bin`/`.pt`/`.ckpt` suffix.
  See [PyTorch's loading guidance](https://docs.pytorch.org/docs/stable/generated/torch.load.html).
- A model/dataset pinned to a mutable hub tag or `latest` is not pinned — the
  remote can change under you; pin to an immutable revision/commit/digest.
- MCP servers are dependencies with hands: a malicious or hijacked server
  doesn't just ship bad code — it ANSWERS your agent's tool calls, so a
  compromised registry entry becomes an active manipulator after install.
  Vet the manifest's declared tools/permissions at acquisition, and pin: a
  server that can silently update is an unpinned dependency with agency
  (ASI04). The spoofed-result handling at runtime is
  `inter-agent-comms-reviewer`'s.
- An evaluation that passed "model v7" proves nothing about production if
  "v7" is a name that can be re-pointed: bind the eval result and the
  approval to the content digest, then check the serving layer loads that
  digest. The swap usually happens between gate and load, not in the model.
- A signature proves who produced the bytes, not that the bytes are safe:
  a signed pickle checkpoint still executes code on load, and a signed
  model can still carry a learned backdoor (that half is
  `model-poisoning-reviewer`'s). Safetensors removes load-time code
  execution; it does not remove a backdoor.
- A LoRA adapter is only as trusted as the base it is applied to: an
  adapter pinned by digest on top of a base referenced by a mutable tag is
  unpinned. A merged model is a new artifact — the inputs' signatures do
  not carry over to it.
- A model card and license are claims by the publisher, not provenance;
  verify them against the signed source and record them in the AI-BOM.

## Stop Conditions

- No manifest, lockfile, or pipeline is available to review → stop; this
  skill does not assess supply chain from a description.
- A finding indicates an ACTIVE compromise (malicious package already
  installed, secret already exfiltrated via CI) → report immediately with the
  path; containment/rotation is the human's call (`human-approval-boundary`).
  This includes a production model whose loaded digest differs from the
  approved digest with no promotion record: report it as a possible
  artifact swap; rollback is the human's call.
- A promotion review is asked for but the registry records, digests, or
  serving configuration are not available → stop and name what is
  missing; this skill does not certify a promotion path from a diagram.
- The question is whether the model LEARNED malicious behavior from data
  or feedback you run → hand to `model-poisoning-reviewer`.
- Remediation requires applying a dependency upgrade or editing CI on a live
  repo with breaking potential → propose the change; applying it is a
  separate, classified, approved step (not done from this review skill).
- The finding is in first-party code flagged by SAST, not a dependency/CI
  issue → hand to `static-analysis-reviewer`.

## Supporting Files

- [references/supply-chain-checklist.md](references/supply-chain-checklist.md)
  — the CI/CD compromise-path catalog, reachability-triage rubric, pinning
  and provenance checks, dependency-confusion/typosquat detection notes,
  the AI/ML supply-chain section (LLM04), the promoted-model-artifacts
  section (LLM04:2026: registry, signing, promotion gate, AI-BOM), and the
  agentic supply-chain section (ASI04: MCP servers/manifests, registries,
  plugins, A2A deps).
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `static-analysis-reviewer`,
  `security-pr-reviewer`, and `secure-migration-reviewer` (security-review
  cluster), and the promoted-artifact seam with `model-poisoning-reviewer`.
