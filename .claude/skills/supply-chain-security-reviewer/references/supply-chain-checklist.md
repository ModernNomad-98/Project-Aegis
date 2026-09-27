# Supply-Chain Checklist — CI/CD paths, triage, pinning, provenance

Use this reference with the [Supply Chain Security Reviewer](../SKILL.md).

Progressive-disclosure detail for `supply-chain-security-reviewer`.
Supply-chain assurance asks where artifacts came from and whether they were
tampered with, alongside vulnerability counts.

## Terms used here

- **SLSA / CVE:** Supply-chain Levels for Software Artifacts (a supply-chain
  assurance framework) and Common Vulnerabilities and Exposures (published
  vulnerability identifiers).
- **CI/CD / PR / SHA:** continuous integration and continuous delivery, pull
  request, and Secure Hash Algorithm (the commit digest used for pinning).
- **TP / SAST / RCE:** true positive, static application security testing,
  and remote code execution.
- **AI / ML / RAG:** artificial intelligence, machine learning, and
  retrieval-augmented generation (answering with retrieved source material).
- **OWASP / ASI04 / ASI07:** Open Worldwide Application Security Project and
  its agentic threat identifiers used below; `ASI04` concerns agentic supply
  chains and `ASI07` concerns inter-agent communication.
- **MCP / A2A:** Model Context Protocol (a tool-integration protocol) and
  agent-to-agent communication.
- **OS / authn:** operating system and authentication (checking a caller's
  identity).
- **LLM04:2026:** the supply-chain category of the OWASP Top 10 for large
  language model (LLM) Applications, 2026 edition (LLM03 in 2025).
- **SBOM / AI-BOM:** software bill of materials, and its AI counterpart — an
  inventory of model artifacts with digests, sources, licenses, and
  base-model lineage.
- **LoRA:** low-rank adaptation, a small fine-tuning adapter loaded on top
  of a base model.

## Reachability triage rubric (for scanner output)

For each flagged CVE / advisory:

1. Is the vulnerable package a **direct** or **transitive** dependency?
   Compare the lockfile with the resolved installed graph in the reviewed
   environment; a lockfile entry alone does not prove what was installed.
2. Is the vulnerable **code path called** by this project, or only present?
3. Is it a **runtime**, **build/dev-only**, or **test-only** dependency?
4. Is there a **fixed version**, and does upgrading break anything?

Sort into:
- **TP-reachable** — called on a real path → severity per impact.
- **TP-latent** — present but unreachable → low/informational, note for hygiene.
- **False-positive** — not applicable (wrong OS, unused feature) → dismiss with reason.
- **Duplicate** — same root advisory via multiple paths → collapse.

Presence ≠ exploitability. A "critical" in an unreachable dev dep can rank
below a "moderate" in a reachable parser.

## CI/CD compromise-path catalog

| Path | Signal | Remediation |
|---|---|---|
| Untrusted trigger + secrets | `pull_request_target` (or self-hosted runner) that checks out PR code AND has secrets available | Split: untrusted build without secrets; privileged step on trusted code only |
| Over-broad token | `permissions: write-all` or default broad `GITHUB_TOKEN` | Least-privilege `permissions:` per job |
| Unpinned third-party action | `uses: someorg/action@v3` (mutable tag) | Pin to full commit SHA; review the SHA'd code |
| Secret in logs/artifacts | secrets echoed, or uploaded in build artifacts | Mask; never upload secrets; scope artifact reads |
| Cache poisoning | shared cache key writable by untrusted jobs | Scope cache keys; don't restore untrusted caches into trusted jobs |
| Script injection | `${{ github.event.* }}` interpolated into `run:` shell | Pass via env, quote; never inline untrusted event data |

## Install/build execution review

- Enumerate `postinstall`/`preinstall`/`prepare` (npm), `build.rs` (cargo),
  `setup.py`/build hooks (python), Dockerfile `RUN`, Makefile targets.
- Flag: remote downloads (`curl | sh`, fetching a blob), obfuscated/encoded
  commands, credential/env access, network calls during install.
- These run with developer or CI privileges BEFORE tests — treat as code exec.

## Dependency-specific risk

- **Typosquatting:** name close to a popular package (`reqests`, `lodahs`).
- **Dependency confusion:** an internal package name also resolvable on a
  public registry → attacker publishes higher version. Check registry/scope
  config, not just the lockfile.
- **Maintainer/abandonment:** sudden new maintainer, long-dead package
  suddenly updated, or unmaintained package on a critical path.
- **Surface bloat:** heavy/native deps for trivial needs widen the attack
  surface.

## Pinning & provenance checks

- Lockfile committed and used in CI (`npm ci`, `--frozen-lockfile`)?
- Integrity hashes present (subresource/`integrity`, `go.sum`, hash-pinned
  requirements)?
- Third-party actions pinned to commit SHA?
- Vendored binaries: documented source + checksum, or unexplained?
- Releases signed/attested (Sigstore/provenance) where the ecosystem supports
  it? Frame maturity with SLSA levels (source→build→provenance→hardened).

## AI/ML supply chain (OWASP LLM04)

Acquired AI artifacts are dependencies too — third-party base models,
downloaded datasets, and fine-tuning adapters. Review them like any untrusted
package. Scope: ACQUISITION. Integrity of data you curate or pipelines you run
(training sets, feedback loops, RAG ingestion) is `model-poisoning-reviewer`.

- **Serialization / format (code execution on unsafe load):** `pickle.load`,
  `torch.load(..., weights_only=False)`, and Python-code custom layers can
  execute arbitrary code from an untrusted artifact. Recent PyTorch releases
  default to restricted `weights_only=True` (verification item: confirm the
  default against the installed version); verify the loading mode and
  allowlisted globals. File suffixes such as `.bin`/`.pt`/`.ckpt`
  do not prove the mode. Prefer **safetensors** where suitable; do not treat
  scanning alone as proof that untrusted pickle can be loaded safely.
- **Pinning:** pin models/datasets to an immutable revision (commit hash /
  content digest), never a mutable hub tag or `latest` — the remote can change
  under you. An unpinned model reference is unpinned dependency risk.
- **Provenance & source:** which registry/hub, which publisher, is it the
  official upstream or a look-alike (model-name typosquatting on public hubs)?
  Is there a model card, license, and documented training provenance?
- **Integrity:** checksum/signature on the downloaded artifact; does the hub
  support attestation? Vendored model weights checked in without a documented
  source are unexplained artifacts.
- **Transitive AI deps:** the ML framework, tokenizer, and model-loading libs
  are ordinary package dependencies — review them in the dependency set above.

Boundary: a backdoored/poisoned artifact you DOWNLOADED is this skill; poisoning
of data you COLLECT or a model you TRAIN is `model-poisoning-reviewer`.
Promotion of either kind of artifact is the next section.

## Promoted model artifacts (OWASP LLM04:2026)

The 2026 edition names promoted-artifact trust: the model artifact serving
production is not the one that was reviewed or claimed. Scope: every model
artifact that moves through a registry — acquired or built in-house — from
the moment it is registered to the moment production loads it. The
question is integrity and provenance of the ARTIFACT; whether the pipeline
you run taught it malicious behavior is `model-poisoning-reviewer`.

Trace one artifact end to end and check each link:

| Link | What to verify | Finding when |
|---|---|---|
| Identity | Production loads an immutable content digest; the digest equals the one the promotion approved | Serving references a mutable alias, version name, or `latest`; digests differ with no promotion record |
| Provenance | A signature or attestation ties the digest to the build job, source revision, base model, and data snapshot; verified at promotion AND at load | Unsigned artifacts; signature checked only at upload; attestation names a different digest |
| Format | Non-executable format (for example safetensors) or a verified restricted loader | Pickle-based checkpoint promoted to production; loader mode unverified |
| Adapters | A LoRA adapter records and is pinned to its base-model digest; a merged model has its own digest and signature | Adapter on a base resolved by tag; merged model inherits "trust" from its inputs' signatures |
| Registry access | Write, overwrite, and promote rights are least-privilege and separate from training rights; registered versions are immutable; promotions are logged | A training job or broad CI token can overwrite a version or move the production alias |
| Promotion gate | Staging to production requires evaluation and human-approval evidence bound to the digest | Approval recorded against a version name; gate skippable by a direct registry call |
| Inventory | Model card, license, and an SBOM/AI-BOM entry exist for what ships and match the signed source | License or lineage unknown for a production model |

Notes:

- Verify at load, not only at promotion: a swap between gate and load
  defeats a gate that only checks at promotion.
- Signing proves origin, not safety — a signed pickle still executes code,
  and a signed model can still carry a learned backdoor.
- Converting an untrusted pickle to safetensors requires loading it; do the
  conversion in an isolated environment or re-export from a trusted build.
- Registry infrastructure declared in infrastructure-as-code (bucket
  policies, identity roles) is reviewed as a diff by `iac-reviewer`; this
  section states the access the promotion path needs.
- Whether the gate's evaluation would catch a poisoned behavior is
  `model-poisoning-reviewer`; running the evaluation is
  `ai-evaluation-harness` (manual-only).

## Agentic supply chain (OWASP Agentic ASI04)

Agentic components are dependencies whose compromise grants AGENCY, not just
code execution — an installed MCP server answers your agent's tool calls.
Scope: ACQUISITION and update. Live message security between installed
components is `inter-agent-comms-reviewer` (ASI07).

- **MCP servers & manifests:** which registry/source, which maintainer, is
  it the official upstream or a look-alike (server-name squatting on
  registries)? Diff the manifest's declared tools/permissions against what
  the use case needs — permission width is the blast radius your agent
  inherits; a note-taking server declaring shell/filesystem/network tools is
  a finding at install time. Local-stdio servers execute on your host with
  your privileges: treat like any install-script risk above.
- **Pinning & update path:** pin servers/plugins to immutable versions
  (digest/SHA); a registry entry that can silently update is an unpinned
  dependency WITH AGENCY. Manifest changes on update are reviewed like
  dependency-code changes — a benign v1 that adds `exec` in v1.1 is the
  agentic version of a maintainer-change attack.
- **Tool/skill registries:** registry entries (skills, tool definitions,
  agent templates) are behavior-steering artifacts — review who can publish,
  whether entries are signed/attested, and pin what you consume. A poisoned
  skill/tool DESCRIPTION steers the model's tool choice even when the code
  is clean (the description is part of the attack surface).
- **A2A dependencies:** external agents your agents delegate to are
  supply-chain endpoints — source/operator trust, contract pinning, and the
  attenuated-authority rules of `agent-identity-privilege-reviewer` apply at
  acquisition; runtime authn/integrity is ASI07.
- **Transitive agentic deps:** an MCP server's own dependency tree (and the
  packages a plugin pulls) go through the ordinary dependency review above.

## HIGH-severity gate

A HIGH/CRITICAL finding must state a compromise path: weakness → attacker
action → material impact, which may include code execution, secret theft,
data exposure or corruption, unauthorized action, or availability loss.
Reachable runtime exploit,
install-time script execution, an untrusted-CI-to-secret path, or loading a
pickle-serialized model from an untrusted source qualifies, as does a
production model alias that a non-release identity can re-point. A latent
unreachable CVE does not — rank it low and say why.

## Handoffs

- First-party SAST/CodeQL findings → `static-analysis-reviewer`.
- Integrity of curated training data / feedback loops / RAG ingestion →
  `model-poisoning-reviewer` (acquire-vs-ingest split); learned-behavior
  poisoning in a promoted model → `model-poisoning-reviewer`
  (artifact-integrity-vs-learned-behavior split).
- Registry infrastructure changes in an infrastructure-as-code (IaC) diff →
  `iac-reviewer`.
- Live agent/MCP message security (authn, integrity, replay) →
  `inter-agent-comms-reviewer` (install-vs-runtime split, ASI04 vs ASI07).
- Applying an upgrade/CI change → separate classified, approved change.
