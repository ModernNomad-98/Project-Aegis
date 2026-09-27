---
name: llm-output-safety-reviewer
description: 'Review how an application consumes LLM output for improper output handling (OWASP LLM10) — treat model output as untrusted and trace it to each sink: HTML/markdown rendering (XSS), SQL/shell/eval execution (injection, RCE), file paths and URLs (traversal, SSRF), tool arguments, stored-then-reused output (second-order), and AI-generated code before it is saved, committed or run (no auto-run, sandbox, checks, human review gate, provenance). Verify context-correct encoding, sandboxing incl. autonomous generate-and-run loops and sandbox escape/persistence (agentic ASI05), and validate-before-act discipline. Use when model output is rendered, executed, stored, committed, or used to build a command, query, path, or request. Do NOT use for output shape (structured-output-validator), upstream injection (prompt-injection-defender), factual correctness (ai-misinformation-guard), tool-permission scope (agent-tool-safety-guard), one diff''s bugs (code-reviewer), or leaked sensitive data (sensitive-disclosure-guard).'
---

# LLM Output Safety Reviewer

## Purpose

Review whether an application handles model output safely (OWASP large
language model output-handling category LLM10 in the 2026 edition, LLM05
in 2025): the model output is untrusted data, and every place it flows — a rendered page, a
database query, a shell command, a file path, a URL, a tool argument, or a
store it will later be read from — is a potential injection or execution sink.
The 2026 edition also names insecure generated code: code a model writes is
model output too, and saving, committing or running it is a sink that needs
the same untrusted-until-verified handling.
The review traces output to each sink and verifies context-correct
encoding/escaping, sandboxing for executed generated code, and
validate-before-act discipline, producing severity-ranked findings each with
the flow from model output to impact.

**Reading key:** OWASP is the Open Worldwide Application Security Project;
LLM means large language model, and LLM10:2026 means category LLM10 in the
2026 edition of its LLM Top 10. AI means artificial intelligence. HTML is
HyperText Markup Language; JSX is JavaScript XML; JS is JavaScript; SQL is
Structured Query Language; URL is uniform resource locator; HTTP is
Hypertext Transfer Protocol; I/O means input/output; PII is personally
identifiable information; CSP is Content Security Policy; SAST is static
application security testing; CI is continuous integration; NL means natural
language; and `venv` is a Python virtual environment. XSS is cross-site
scripting, RCE is remote code execution, SSRF is server-side request
forgery, and ASI05 is the agentic framework's unexpected-code-execution
category. The [sink catalog](references/output-sink-catalog.md) carries the
per-sink detail.

## Use When

- Use when: model output is rendered as HTML/markdown, executed as SQL/shell/
  code, written to files, used to build URLs or requests, passed as tool
  arguments, or stored and later re-consumed.
- Use when: reviewing an AI feature's output path for cross-site scripting
  (XSS), injection, remote code execution (RCE), server-side request
  forgery (SSRF), path traversal, or second-order (stored-output) issues.
- Use when: an agent generates code that the system then runs.
- Use when: AI-generated code (from a coding assistant, an agent, or an
  app feature that writes code) is about to be saved, committed, merged or
  run, and the question is whether that path treats it as untrusted: no
  automatic execution, a sandbox before any run, static checks and a human
  review gate before commit, and provenance labels (LLM10:2026, insecure
  generated code).
- Use when: an AUTONOMOUS agent loop generates and executes code with no
  human between generate and run (OWASP agentic code-execution category
  ASI05) — sandbox boundaries and escape
  paths, in-sandbox persistence between runs, package installs inside the
  sandbox, and which natural-language inputs can reach an execution path.
- Do NOT use when: the concern is the SHAPE/type of structured output —
  `structured-output-validator` (this skill is the injection/exec sink review;
  they compose).
- Do NOT use when: the concern is the injection that manipulated the model
  (`prompt-injection-defender`), factual accuracy
  (`ai-misinformation-guard`), or how broad the tools are
  (`agent-tool-safety-guard`).
- Do NOT use when: the concern is sensitive data (secrets, PII, other-tenant
  data) leaking into or out of the model — that is
  `sensitive-disclosure-guard`; this skill reviews output execution sinks.
- Do NOT use when: reviewing the CONTENT of one generated diff for bugs or
  vulnerabilities — that is `code-reviewer` or `security-pr-reviewer`; this
  skill reviews the gate generated code must pass and requires that review,
  never replaces it. Triaging scanner findings is `static-analysis-reviewer`.
- Do NOT use when: the question is whether a dependency the generated code
  adds is trustworthy (`supply-chain-security-reviewer`) or whether a
  suggested package exists at all (`ai-misinformation-guard`); this skill
  only requires that dependency additions are routed there.
- Do NOT use when: designing who may merge or deploy AI-assisted changes
  (`agent-authorization-matrix`, manual-only) or the AI-assisted lifecycle
  and its gates (`ai-sdlc-operating-model`), or how SAST is run
  (`sast-orchestration-designer`); this skill checks the generated-code
  path against those gates.

## Inputs to Inspect

1. The output sinks: every place the model's output is used — templates/JSX,
   query builders, command execution, file I/O, HTTP clients, tool-call
   dispatch, storage writes.
2. The rendering path: is output treated as text or as markup; is auto-escaping
   on; is `dangerouslySetInnerHTML`/`v-html`/`innerHTML` or a markdown renderer
   with raw-HTML enabled in play.
3. Execution paths: any `eval`, dynamic SQL, shell-out, code interpreter, or
   generated-code runner; the sandbox (or absence) around it. For agent
   loops (ASI05): what natural-language input can trigger execution, what
   persists in the sandbox between runs, and whether executed code can
   install packages or reach the network.
4. URL/path construction from output: SSRF (model-chosen URL fetched
   server-side), path traversal (model-chosen filename).
5. Storage-and-reuse: output persisted then later rendered/executed as if
   trusted (second-order injection).
6. Existing encoding/validation: escaping helpers, allowlists, content
   security policy, and where they are and aren't applied.
7. The generated-code path (if code is generated): where it lands (editor,
   working tree, branch, pull request, runtime), what runs automatically on
   save or commit (hooks, file watchers, CI workflows, install scripts), the
   checks and human review required before commit or merge, how provenance
   is recorded, and any dependency-manifest changes it carries.

## Workflow

1. **Enumerate output sinks.** List every consumer of model output and
   classify each: render, execute, store, or drive-an-action. No output-
   handling code to inspect → Stop Conditions.
2. **Treat output as untrusted.** For each sink, ask the same question you'd
   ask of raw user input: what happens if the output is adversarial? Model
   output is attacker-influenced whenever untrusted content was in context.
3. **Review rendering sinks** using
   [references/output-sink-catalog.md](references/output-sink-catalog.md):
   HTML/markdown must be context-correctly encoded or sanitized; raw-HTML
   rendering of model output is a finding unless sanitized with an allowlist;
   check CSP as defense in depth.
4. **Review execution sinks.** Model output that becomes SQL, shell, eval, or
   generated code that runs: require parameterization/allowlisting, and for
   generated-code execution require a real sandbox (isolated, no secrets, no
   network unless required, resource-limited). Unsandboxed execution of
   generated code is RCE-class. For AUTONOMOUS generate-and-run loops
   (ASI05): require per-run ephemeral sandboxes (no cross-run persistence a
   poisoned run can plant into), package installs treated as untrusted
   supply-chain events, an execution budget, and a map of every
   natural-language path that reaches execution — "user asks a question" →
   "agent writes and runs code" is an NL-to-RCE path to enumerate, not a
   feature to assume safe.
5. **Review the generated-code commit path (LLM10:2026).** When model-
   written code is saved, committed or merged, apply the generated-code
   rubric in the sink catalog: nothing auto-executes it (no `eval` of a
   suggestion, no run-on-save of files that execute — hooks, CI workflows,
   install scripts); any pre-review run happens in the step-4 sandbox;
   static checks (tests, linters, SAST, secret scan) run before a HUMAN
   review gate the author or agent cannot bypass; provenance marks the
   change as AI-generated so the gate applies; and every new dependency is
   routed to `supply-chain-security-reviewer`. The line-by-line review
   itself is `code-reviewer`/`security-pr-reviewer`.
6. **Review URL/path/request sinks.** Server-side fetch of a model-chosen URL
   is SSRF — require an allowlist and block internal ranges/metadata
   endpoints. Model-chosen file paths need traversal-safe resolution.
7. **Review tool-argument sinks.** Output used as tool arguments must be
   validated before the side effect (compose `structured-output-validator`
   for shape, `agent-tool-safety-guard` for the permission boundary).
8. **Review store-and-reuse.** Output persisted and later rendered/executed is
   re-untrusted on read: encoding at write time is not enough if a different
   reader trusts it. Flag second-order paths.
9. **Rank findings by flow.** Each finding names the flow (model output →
   sink → impact) and severity gated on a concrete exploit; give the
   context-correct fix (escape here, parameterize there, sandbox, allowlist).

## Output Format

```
LLM OUTPUT-HANDLING REVIEW — <feature>
Output sinks: <render | execute | store | action — each location>
Findings (severity-ranked):
  [SEV] <sink type> at <file:line>
    Flow: <model output → sink → impact (XSS/RCE/SSRF/injection/2nd-order)>
    Fix: <context-correct encoding | parameterize | sandbox | allowlist>
Sandbox posture (if code exec): <isolation, secrets, network, limits>
Generated-code path (if code is generated): <lands where | auto-run on
  save/commit? | sandbox before run | static checks | human review gate |
  provenance | dependency additions routed>
Second-order paths: <stored output re-consumed as trusted>
Defense-in-depth: <CSP, output length caps, content types>
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] Every model-output sink enumerated and classified (render/execute/
      store/action).
- [ ] Rendering sinks use context-correct encoding; raw-HTML rendering is
      sanitized with an allowlist or flagged.
- [ ] Execution sinks are parameterized/allowlisted; generated-code execution
      runs in a real sandbox or is flagged as RCE-class.
- [ ] Autonomous generate-and-run loops (if any) use per-run ephemeral
      sandboxes with no default secrets/network, and every natural-language
      path that reaches execution is mapped (ASI05).
- [ ] Generated code (if any) is never auto-executed, runs only in a
      sandbox before review, and reaches commit/merge only through static
      checks plus a human review gate, with provenance recorded and new
      dependencies routed to supply-chain-security-reviewer (LLM10:2026).
- [ ] URL sinks checked for SSRF (allowlist, internal-range block); path sinks
      checked for traversal.
- [ ] Tool-argument sinks validate before the side effect (composed with
      structured-output-validator / agent-tool-safety-guard).
- [ ] Stored-then-reused output is treated as untrusted on read (second-order).
- [ ] Findings name the output→sink→impact flow; severity is exploit-gated.

## Security Rules

- Model output is untrusted data, handled with the same discipline as raw user
  input — no sink gets to assume it's clean.
- Encoding is context-specific: HTML-escaping does not make output safe for a
  SQL string, a shell command, a URL, or a filename. Match the sink.
- Generated code that executes requires a sandbox; "we prompt it to write safe
  code" is not a control.
- Escaping at write time does not sanitize a later trusting read — second-order
  sinks re-validate.
- Generated code is untrusted until a human-reviewed gate passes; a green
  scan or passing tests written by the same model are evidence for that
  reviewer, not approval.

## Gotchas

- Markdown renderers often pass through raw HTML by default — a model emitting
  `<img onerror=…>` inside markdown becomes XSS unless raw HTML is disabled or
  sanitized.
- Streaming output tempts teams to render incrementally before any
  sanitization runs — the sanitize step must not be skipped for the stream.
- "It's just displayed, not executed" ignores that display IS execution for a
  browser — HTML/JS renders.
- SSRF via model output is easy to miss: the model helpfully returns a URL and
  the server fetches it to "follow the link" — straight into the metadata
  endpoint.
- The exploit often lands one hop away: output stored today, rendered in an
  admin console tomorrow by code that assumes internal data is safe.
- Don't conflate with shape validation: JSON that parses cleanly can still
  carry an XSS payload in a string field — shape-valid ≠ safe-to-render.
- Agent loops normalize execution (ASI05): when generate→run fires dozens of
  times an hour autonomously, one hijacked generation is RCE with nobody
  watching — and a sandbox that persists state between runs lets a poisoned
  run plant what the next run trusts (pip install into a shared venv is the
  classic). Ephemeral per-run sandboxes and NL-path mapping are the
  controls, not human review of each generation.
- Saving can be executing: a generated git hook, CI workflow, `postinstall`
  script, or file-watcher task runs on the next commit, push, install or
  save — before any reviewer sees it. Treat those paths as execution sinks.
- Provenance gets lost: squash merges, copy-paste from a chat window, and
  rewritten commit messages drop the "AI-generated" marker, and the review
  gate keyed to it silently stops applying.
- Volume erodes the gate: when assistants produce most of a diff, reviewers
  skim; size limits per change and required tests are what keep review real.

## Stop Conditions

- No output-handling code (templates, query builders, exec paths) is
  available — stop; this skill reviews concrete sinks, not a description.
- The review finds generated code executing unsandboxed with access to
  secrets or the network — flag as blocking and route remediation through
  `human-approval-boundary`.
- Generated code can reach a deploying branch with no human review gate
  (an agent commits and merges its own output) — flag as blocking and
  route remediation through `human-approval-boundary`.
- The real issue is the model being manipulated (injection), output shape, or
  factual correctness — hand to the owning skill.
- A live exploit is evident (active XSS/RCE via output) — route to
  `incident-response-runbook`.

## Supporting Files

- [references/output-sink-catalog.md](references/output-sink-catalog.md) —
  per-sink review checklist (render/execute/URL/path/tool-arg/store),
  context-correct encoding rules, the generated-code sandbox rubric
  (including the ASI05 autonomous-loop and sandbox-escape extension), the
  generated-code commit-path rubric (LLM10:2026) with its neighbour seam,
  and second-order injection patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the output & agency
  cluster and against `security-pr-reviewer`, `structured-output-validator`,
  `agent-tool-safety-guard`, `supply-chain-security-reviewer`,
  `code-reviewer` and `ai-sdlc-operating-model`.
