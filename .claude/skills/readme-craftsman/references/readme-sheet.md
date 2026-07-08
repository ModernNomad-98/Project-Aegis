# README Sheet

Detail for `readme-craftsman`. Read on demand.

## First-screen checklist (highest leverage)

Before any badge, table, or install step, a stranger must learn:
- [ ] **What** it is (one line, plain language).
- [ ] **What** it's for (the problem it solves).
- [ ] **Who** it's for (audience).
- [ ] **Why** choose it (the differentiator, briefly).

If these four aren't clear in the first screen, fix that before anything
else. Badges/license/status go BELOW this.

## Section templates by project type

**Library / package**
1. One-liner + what/why/who
2. Install
3. Minimal usage example (the 80% case)
4. Link to API reference / full docs
5. Compatibility / requirements
6. Contributing, license (below fold)

**CLI tool**
1. One-liner + what/why/who
2. Install
3. Quickstart: the one command that shows value
4. Common commands (a few), link to full command reference
5. Config basics, link out
6. Contributing, license (below fold)

**Service / API**
1. One-liner + what/why/who
2. Quickstart: run locally or hit the hosted endpoint
3. Auth + a first request/response
4. Link to API reference (generated) + guides
5. Deploy/ops pointer
6. Contributing, license (below fold)

**App / product**
1. One-liner + what/why/who + a screenshot/gif
2. Try it / install
3. Key features (brief), link to user docs
4. Contributing, license (below fold)

## Quickstart-verification recipe

1. Start from a clean environment (fresh container / new user).
2. Follow ONLY what the README says — no hidden steps.
3. State every prerequisite the reader needs first.
4. If it doesn't produce the promised result, the README is wrong — fix
   it, don't ship it.
5. If it can't be run now, mark the quickstart provisional/unverified
   rather than implying it works.

## Belongs in README vs link out

| Keep in README | Link out to |
|---|---|
| What/why/who | Full tutorials |
| Quickstart | Complete API reference (generated) |
| Common-case usage | Exhaustive config/options |
| Routes to deeper docs | Changelog |
| Compact badges/license (below fold) | Architecture/design docs, ADRs |

## Maintenance

- Keep it short enough to stay true.
- Single-source or generate drift-prone values (versions, commands).
- The README is a hub: its success metric is getting the reader to the
  right next page, not containing every page.
