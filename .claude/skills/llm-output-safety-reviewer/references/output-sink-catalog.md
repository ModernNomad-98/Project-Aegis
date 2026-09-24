# LLM output sink catalog

Detail for [llm-output-safety-reviewer](../SKILL.md). OWASP LLM05 (Improper Output
Handling), 2025. Model output is untrusted; each sink below re-asks "what if
this is adversarial?".

**Reading key:** LLM means large language model; OWASP is the Open Worldwide
Application Security Project, and LLM05 is its numbered improper-output-
handling category. HTML is HyperText Markup Language; JSX is JavaScript XML;
XSS is cross-site scripting; URL is uniform resource locator; SQL is
Structured Query Language; NoSQL refers to non-relational databases; ORM is
object-relational mapper; OS is operating system; RCE is remote code
execution; SSRF is server-side request forgery; VM is virtual machine; and
CPU is central processing unit. NL means natural language; `venv` means a
Python virtual environment; CRLF means carriage-return/line-feed. ASI05 is
the agentic framework's unexpected-code-execution category, recorded with LLM05
in the [source mapping](../../../../docs/reconciliation/step-0-reconciliation-v4.md).
The [parent review workflow](../SKILL.md) owns the verdict and routing.

## Render sinks (→ XSS / markup injection)

- **HTML/JSX/templates:** must be context-correctly escaped. Auto-escaping on
  by default is good; `dangerouslySetInnerHTML`, `v-html`, `innerHTML`,
  `Element.insertAdjacentHTML`, template `| safe` filters bypass it — each is
  a finding when fed model output unless sanitized.
- **Markdown:** many renderers allow raw HTML by default. Disable raw HTML or
  run an allowlist sanitizer (DOMPurify-style) AFTER rendering. Watch
  `javascript:` / `data:` URLs in links and images, and `onerror`/`onload`
  attributes.
- **Attributes / URLs in markup:** escaping for element text ≠ safe in an
  attribute or `href`. Validate URL schemes (allow http/https/mailto).
- **Defense in depth:** Content-Security-Policy limits blast radius but is not
  a substitute for encoding.

## Execution sinks (→ injection / RCE)

- **SQL/NoSQL:** parameterize; never string-concatenate model output into a
  query. ORM raw-query escapes bypass this.
- **Shell / OS command:** avoid entirely; if unavoidable, use argument arrays
  (no shell), allowlist the command and args. Model output in a shell string
  is command injection.
- **eval / dynamic code:** model output into `eval`, `Function`, `exec`,
  template engines with code, or deserialization is RCE-class.
- **Generated-code execution (agent writes code that runs):** requires a real
  sandbox — isolated process/container/VM, no ambient credentials, network
  denied unless required and then allowlisted, CPU/memory/time limits, no
  access to the host filesystem beyond a scratch dir. "We instruct it to write
  safe code" is not a control. This is the ASI05 seam too (agentic).

### Autonomous generate-and-run loops (ASI05 extension)

When an agent generates AND executes code with no human between the two,
per-generation review does not exist — the sandbox architecture is the whole
control:

- **Ephemeral per-run sandboxes:** state does not survive between runs; a
  poisoned run must not be able to plant packages, files, or config the next
  run trusts (a shared venv/container reused across runs is persistent
  contamination surface).
- **Escape-path review:** kernel/container escape surface, mounted volumes,
  shared sockets (the Docker socket inside a sandbox is game over), and
  host-visible side channels.
- **Package installs are supply-chain events:** `pip install` inside the
  sandbox executes third-party code chosen partly by the model — restrict to
  an allowlisted mirror or deny; route registry-trust questions to
  `supply-chain-security-reviewer`.
- **NL-to-execution path map:** enumerate every input channel (user chat,
  retrieved docs, peer-agent messages) that can lead to code being written
  and run — each is an NL-to-RCE path whose payload the injection layer may
  miss; the sandbox is what bounds it.
- **Execution budget:** per-run and per-period caps on runs, CPU, and cost
  (compose `ai-cost-guardrail-designer`) — an execution loop is also a
  consumption amplifier.
- **The tool-side row** (approval posture, identity, side-effect class of the
  execution TOOL) lives with `agent-tool-safety-guard`; this file owns what
  happens inside the sandbox.

## URL / path / request sinks

- **SSRF:** server-side fetch of a model-produced URL must use an allowlist and
  block private/link-local ranges and cloud metadata endpoints
  (169.254.169.254 and equivalents). Validate all resolved A/AAAA addresses
  and revalidate every redirect hop or disable redirects; account for DNS
  rebinding. "Follow the link the model found" is the classic hole.
- **Path traversal:** model-chosen filenames/paths resolved without
  canonicalization + base-dir check allow `../` escapes. Resolve and verify
  containment.
- **Request construction:** headers/bodies built from output can smuggle
  (CRLF, extra params).

## Tool-argument sinks

- Validate shape/type/values before the side effect (compose
  `structured-output-validator`); enforce the permission/identity boundary
  (compose `agent-tool-safety-guard`). Shape-valid output can still be a
  malicious value (another tenant's id).

## Store-and-reuse (second-order)

- Output persisted then later rendered/executed is untrusted again on READ.
  Encoding at write time helps only the writer's context; a different reader
  (admin console, export, another service) may render it raw.
- Classic path: model output stored as "internal data", later displayed in a
  trusted-internal UI that skips escaping.
- Rule: sanitize/encode at the sink that USES the data, in that sink's
  context — not (only) once at write time.

## Severity gating

Rank potential consequence separately from confidence in the exploit path.
A concrete flow from adversarial model output to XSS/RCE/SSRF/injection or
data exposure supports high confidence. An unconfirmed reachable sink is a
hypothesis requiring investigation; uncertainty alone does not cap impact.
