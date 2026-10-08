# Owner answers to the coordinator's multiple-choice questions (verbatim)

Extracted programmatically from the session transcript (tool results of the AskUserQuestion tool). Each block gives the exact question text and the label the owner chose. Option texts for some questions are in artifacts/cifix/owner-q2-q4-verbatim.json and the briefs under artifacts/.

## 2026-10-07T17:33:29.728Z

````text
Your questions have been answered: "Got it on the team setup: planning, plan audit and reviews on Opus 5.5 at xhigh effort, coding on Opus 5.5, and a different agent for each stage. Which backlog item should that team work on? I still need you to name one, because the repo records the next pick as your decision."="Readability count fix (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-07T20:51:17.665Z

````text
Your questions have been answered: "159 pages have never had a review recorded. Under the official count, how should they be treated? Counting them as pending is cautious and honest, and a page stops being pending as soon as someone reviews it. Treating them as accepted unless listed matches some older ledger readings, but would call unreviewed pages accepted."="Count as pending (Recommended)", "When should the index be regenerated? Each regeneration is a full 7-stage PR, about 40 minutes and about 4 minutes of CI."="On demand + keeper (Recommended)", "This needs several new PRs: one recording your decision in the approval register and decision log, then the tool repair, then the switch. Your earlier merge approval covered only PR #677. May the team merge these PRs on the same terms: every stage passed and all checks green, admin merge allowed, fix and retry on failure?"="Yes, same terms (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-07T21:13:09.213Z

````text
Your questions have been answered: "How should the index learn which pages were accepted?"="B: structured table (Recommended)", "After the switch, routine index rebuilds will each be a small PR (on demand, and after each keeper acceptance). May the team merge those on the same terms (all stages passed, all checks green, admin merge allowed, fix and retry), without asking you each time?"="Yes, standing approval (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-07T21:46:57.258Z

````text
Your questions have been answered: "Some pages have an acceptance recorded in the ledger, but the exact commit it points to no longer exists anywhere (at least 6 such commits are permanently lost), so the tool can't verify it. How should those pages count?"="Pending until re-reviewed (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-07T22:29:14.885Z

````text
Your questions have been answered: "Which speed-ups do you want? Pick any."="Ask open decisions now,Parallel repair PRs,High effort for low-risk,Raise rebuild fast path later". You can now continue with these answers in mind.
````

## 2026-10-07T22:30:01.031Z

````text
Your questions have been answered: "Should the ledger keeper be allowed to record a "targeted review" in the table, meaning an independent reviewer checked a small edit of 10 lines or fewer, so the page stays accepted?"="Yes, explicit grant (Recommended)", "Should the readability index tool (tools/readability_acceptance/) be classed as security-relevant "approval/evidence tooling"?"="Yes, security-relevant (Recommended)", "If the tool can't measure a page's change for a reason other than a lost commit, how should the page count?"="Pending until re-reviewed (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-07T23:15:46.772Z

````text
Your questions have been answered: "Which version of the repair should the team build? In every version the official pending count starts at about 510–610 of 609 pages and falls as pages are reviewed."="Pause the program", "May each of the smaller repair PRs merge on the same terms you already gave the repair (every stage passed, all checks green, admin merge allowed, fix and retry), without asking you each time?"="Yes (Recommended)", "After the switch, if a recorded acceptance row turns out to be wrong, may the ledger keeper add a "withdraw" row to cancel it? The ledger is never rewritten; the cancellation is appended."="Yes, keeper may (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-08T14:08:58.865Z

````text
Your questions have been answered: "Which backlog item should the team take next? My pick is the first: it's verified, small, ungated, and overlaps the PR template the team is already editing."="Stale CI docs (Recommended)", "May the team merge this follow-up PR (dated corrections, PR template markers, plus whatever you pick above) on the same terms as before: every stage passed, all checks green, admin merge allowed, fix and retry on failure?"="Yes, same terms (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-08T14:14:48.569Z

````text
Your questions have been answered: "How should the two new items (audit baseline refresh, library-diff-reviewer wording) ship? They're separate from FU-1, and my session is set up to push to one branch."="Second branch, in parallel", "May FU-2 merge on the same terms (every stage passed, all checks green, admin merge allowed, fix and retry)? Your request to do the baseline refresh will also be recorded as a new approval register grant, quoted word for word, because the register says any further regeneration needs a new grant."="Yes, same terms (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-08T15:26:38.922Z

````text
Your questions have been answered: "main's CI failure was a rare race in one CI test: Git 2.55 starts a background clean-up job in a throwaway test folder, and the test deletes the folder while that job is still writing. The one re-run passed, so main is green again, and the same race has happened once before (2026-09-30). The proposed fix adds two lines to scripts/tests/test_offline_ci.py telling Git not to run that background job in the test's folder. scripts/ is protected, so a fix PR's protected-file guard (gate-guard) will be red until you grant a one-time exception for that exact PR commit. Do you want the fix?"="Yes, one-time exception (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-08T16:01:08.352Z

````text
Your questions have been answered: "The exception has to name the fix PR's exact commit, which only exists once the fix is written. The last one-time exception (AEGIS-APR-106) handled this with a separate small PR that changes only the approval register, merged just before the protected PR. That's a fourth PR your instruction didn't name. May the team open and merge it on the same terms (all seven stages, all checks green, admin merge allowed)?"="Yes, same terms (Recommended)", "After the fix merges, the register should record that the one-time exception has been used up. Should that be its own small PR right after the merge (the AEGIS-APR-107 precedent), or wait for the next register PR?"="Batch it later (Recommended)", "Suppose the fix PR's commit changes after the exception is recorded, for example because a reviewer asks for a change. The recorded exception would then name the wrong commit. What should happen?"="Ask me again (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-08T16:23:16.528Z

````text
Your questions have been answered: "The PR that stores the skill-batch plan in the repo is a proposal page only: it selects and builds nothing. May the team merge it on the same terms as FU-1 and FU-2 (all seven stages passed, all checks green, admin merge allowed, fix and retry on failure)?"="Yes, same terms (Recommended)". You can now continue with these answers in mind.
````

## 2026-10-08T17:51:48.809Z

````text
Your questions have been answered: "For the CI test fix, your answer says the exception must be "recorded in the register". I read that as: the register entry has to be merged on main (not just written in an open PR) before the fix can merge. Is that right?"="Yes, merged on main (Recommended)". You can now continue with these answers in mind.
````

