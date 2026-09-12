# GitHub review corrections

The automatic review of PR #90 revision
`e9b8ec03c6a462fb9a33cb0a2c90a275de25ba9c` completed on 2026-09-12 with two P2
findings. Both were reproduced and corrected; the earlier local reviews missed
them. The initial verification record remains evidence of that earlier candidate,
not a claim that passing tests had established defect-free behavior.

## Expiry before grant time

[The expiry finding](https://github.com/ModernNomad-98/Project-Aegis/pull/90#discussion_r3995022579)
showed that a grant expiring before it began returned PASS with no action, or FAIL
with an action. That interval is malformed evidence and must return ERROR.

The grader now rejects `expires_at < at` before evaluating any action. A new
regression reproduced all four incorrect outcomes before the fix: standing and
single-use grants, each with and without an action. Another case preserves the
boundary where `expires_at == at`: the grant is valid evidence but is immediately
inactive. All 33 focused approval/lifecycle tests pass after the fix. An independent
read-only code reviewer approved the bounded code, tests and documentation diff.

## Count the shipped corpus

[The count finding](https://github.com/ModernNomad-98/Project-Aegis/pull/90#discussion_r3995022583)
showed that the earlier 19-to-28 manual total included a commented example in
`_template`. The validator excludes that directory. Recounting discovered shipped
skills using parsed YAML yields **184 shipped**, with manual skills changing
**18 to 27** and automatic skills **166 to 157**. Exactly the intended nine skills
changed posture. The README/catalog tables already have the correct 27 unique
manual rows.

The closeout count is corrected. The consumer warning now refers to all manual-only
skills without a separate hardcoded count, preventing that sentence from becoming
stale after future reclassifications. The [count proof](manual-posture-counts.json)
records both revisions and their exact manual-skill sets. Historical raw audits,
logs and older checkpoint counts are preserved; the separate 19 confirmed repairs
and 19 reviewed jobs remain correct.

The correction does not change any skill metadata or invocation route. Full BER
verification of the new implementation and hosted checks of the submitted revision
are recorded in the PR and the follow-up verification evidence when complete.
