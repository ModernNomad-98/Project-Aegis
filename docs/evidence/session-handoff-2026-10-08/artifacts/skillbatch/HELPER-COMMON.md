# Common rules for every skill-batch planning research helper (Stage A support only)
Repo /home/user/Project-Aegis (Role A source library). Base: origin/main 52289779 (re-verify with git ls-remote).
Read first: AGENTS.md, CLAUDE.md, docs/delivery-workflow.md, $S/rcf/BRIEF-COMMON.md (rules 1–7), $S/skillbatch/BRIEF.md
(owner requests, the six groups, the owner's "store these plans in the repo's backlog" and the scrutiny instruction).
Precedent proposals: docs/roadmaps/qa-tier1-skill-batch-proposal.md, phase6-reliability-skill-batch-proposal.md,
phase7-ai-engineering-skill-batch-proposal.md, ai-sdlc-skill-batch-proposal.md.
Previous helpers were interrupted; partial working files exist under $S/skillbatch/ (desc*.txt etc.). You may reuse
them only after re-verifying them; do not trust them.

OWNER RULE (verbatim, binding): "always audit and scrutinize your recommendations. Do not make any assumptions on your
recommendation, if you are unsure, look for evidence or research it first."
=> Every verdict, estimate, MANUAL-ONLY call and recommendation cites file:line, command output or PR/commit. If you are
unsure, research until you are sure; what remains unproven is labelled "unverified" and is NOT used to support the
recommendation. Overlap verdicts must quote the shipped skill's description AND check its body where the description is
ambiguous. End your recommendation with a self-scrutiny section: the strongest counter-argument, which claims are least
certain, and what evidence would change your recommendation.

Per candidate: (1) source rows file:line + stated priority; (2) overlap verdict NEW / PARTIAL (shipped skill + exact
remaining gap) / COVERED vs all shipped skills in .claude/skills/ (196 entries; grep widely); (3) model-invocable vs
MANUAL-ONLY under the library's own rules (find and cite them); (4) estimate in agent-hours with its basis (measured
actuals in docs/roadmaps/aegis-execution-metrics.md / earlier batches where available; else say low confidence);
(5) value to a SaaS builder now, dependencies; (6) trigger boundary "use when / not when" + 2–3 shipped skills its
trigger-evals must pin against. Then recommend the best coherent sub-batch of 3–6 from your groups, or "none".

Write no repo files, make no commits, no GitHub writes (GitHub reads allowed). Never write the word codex prefixed with @.
No reserved scope (paused evaluation, rehearsal, VM, ISO, Stage 4B, BER calibration, provider spend). Dogfood: identify and
read any matching Aegis skill for your work (never MANUAL-ONLY) and name it. Report date -u start/finish.
