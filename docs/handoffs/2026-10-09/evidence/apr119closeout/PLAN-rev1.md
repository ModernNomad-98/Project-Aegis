# APR119-CLOSEOUT — Stage A plan, revision 1

Planner: `/root/readability_index_backlog`, Stage A only.
Start: **2026-10-09 16:49:59 UTC**. Initial estimate: **15–25 active-work minutes**.
The completion message supplies the final file hash, finish time and measured wall time.
This is a local scratch plan, not a repository change or an independent audit.

## 1. Intent and authority

Append one factual `CONSUMED` lifecycle event for **AEGIS-APR-119** to
`docs/approvals/APPROVAL_REGISTER.md`. APR119's single refresh PR, #679,
merged; the event records the already-exhausted use limit and grants nothing.

The owner requested **"add max agents to work on backlogs"** in this current
Project Aegis conversation. The coordinator selected this record gap and
assigned this bounded Stage A task. APR119 itself says its one PR is consumed
by its merge and a later lifecycle event records that fact. The register
preamble requires immutable prior entries and unique appended lifecycle IDs.
This planning assignment permits only this scratch plan and evidence under
`apr119closeout/`. Later stages need their own bounded assignments under the
existing task and delivery authority; neither the spent APR119 grant nor this
plan grants publication or merge authority.

Role A was reverified in `route002/impl`: README begins `# Project Aegis`;
`docs/skills-catalog.md`, `scripts/validate-skills.py` and
`artifacts/audits/skill-contract-audit-baseline.json` exist. Its origin is
`https://github.com/ModernNomad-98/Project-Aegis.git`, HEAD
`8107f50a48cf31b68ab833976d5286b9f8a19c9e`, and read-only status was empty.
That older clone supplied landmarks only. Current authority was read from
GitHub at the separately resolved main below.

## 2. Classification and scope lock

**Class: docs-only, factual governance recording**, applying
`change-classification-gate` and its classification matrix. The target is a
documentary lifecycle record; it changes no permission control, agent
instruction, grant scope, check or runtime behavior.

- Sole future source path: `docs/approvals/APPROVAL_REGISTER.md`.
- One new defining event heading and one EOF append. The entire prior Git blob,
  including its final newline, must remain an exact byte prefix.
- No new D decision entry, baseline regeneration, historical ACTIVE-field edit,
  grant, revocation, supersession, or additional consumption event.
- Do not add the entry to APR099, ROWPOLICY or another held PR under its old
  accepted plan. This task has its own candidate and independent stage chain.
- Preserve all other files, other agents' work, APR120/#682 disposition, and the
  paused readability program.

The PR security answer is **Yes — owner approval register** under
`CONTRIBUTING.md`. Security relevance alone does not invoke MG5: the extra
review is required for an actual outside contribution. The current workflow's
`gate_pattern` at line 528 does not match the register path; C rechecks its
actual base. No guard exception or workflow change belongs to this plan.

## 3. Observed evidence and its limits

Planning main M: **`625fc66711eaf7b3ee788cbc2dff98f05f147c1c`**.
All API calls below were read-only. Fresh main/#679/register/ancestry/open-PR
reads were made during this Stage A; the merge-parent and changed-path reads
were made in the immediately preceding audit and must be rederived by C/D.

| Fact | Source and observed result |
| --- | --- |
| Main identity | `GET /repos/ModernNomad-98/Project-Aegis/branches/main` returned M. |
| Existing limit | [APR119 at M](https://github.com/ModernNomad-98/Project-Aegis/blob/625fc66711eaf7b3ee788cbc2dff98f05f147c1c/docs/approvals/APPROVAL_REGISTER.md#L5064-L5154): one refresh PR, consumed by its merge; no post-merge regeneration covered. |
| Event missing | Read the complete register at M, blob `7ee0e822398382101900c79aea9962b540a86c57`; enumerate definitions and inspect later event kinds/targets plus APR119, PR679 and commit aliases. 121 definitions, 121 unique IDs, maximum 121. APR120 is a grant; APR121 is a policy decision explicitly saying it does not record APR119 consumption. No consumption event targets APR119. |
| Actual delivery | [PR #679](https://github.com/ModernNomad-98/Project-Aegis/pull/679), `GET /pulls/679`: merged=true; merged_at `2026-10-08T15:55:22Z`; head `1d1a50961edd72400371bad5bb4cddb0b12e62aa`; merge `c1acc075910ea1e849401e18cdb60df31c09ef30`. |
| Merge identity | `GET /commits/c1acc075910ea1e849401e18cdb60df31c09ef30`: parents are `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` and the exact PR head above. The diff carries the four generated baseline/report files, AEGIS-060+ register, approval register, and residual library-diff-reviewer eval-note file. |
| Included in main | `GET /compare/c1acc075910ea1e849401e18cdb60df31c09ef30...M`: ahead, behind_by=0, ahead_by=21; merge_base_commit is the named merge. |
| Namespace state | `GET /pulls?state=open&per_page=100` returned an empty array. This says nothing about unpublished reservations. The coordinator directly reports APR122 provisionally reserved to APR099; ROWPOLICY and this item remain unallocated. |
| Separate unspent grant | The immediately preceding audit's `GET /pulls/682` returned closed, merged=false, merged_at=null. This task records no APR120 consumption. |
| Existing plans exclude this event | `apr099closeout/PLAN-rev1.md` SHA-256 `36495a3eb2fb53b839c57c1b36d77f2a9d923e3adb134e314159ec8bfb76f7d2` permits one APR099 event. `rowpolicy/PLAN-rev1.md` SHA-256 `adb968cdbad28215fb261f8a8b90f4e202cc8874f903fc0f6d8965bde65aad63` permits one different POLICY DECISION. Their B verdicts do not cover APR119. |

The missing event does not leave APR119 usable. Actual use limits apply before
transcription. This plan does not recertify #679's historical tests, approval
authenticity, model behavior or all delivery gates. Its narrow assertion is
that the evidenced merge exhausted the recorded one-PR limit.

## 4. Proposed append

The ID and recording fields remain placeholders until implementation. They are
not reserved, timestamps are not backdated, and the old grant stays unchanged.

```markdown
### AEGIS-APR-[allocate]: Consumption of the APR119 skill-contract audit baseline refresh grant

- **Event:** CONSUMED; target grant AEGIS-APR-119.
- **Status at recording:** AEGIS-APR-119 has no remaining use.
- **Effective at:** 2026-10-08 15:55:22 UTC.
- **Recorded at / By:** <actual append timestamp> / <actual recorder>.
- **New authority:** None. Any further baseline regeneration needs a new grant.
- **Reason:** APR119's one permitted refresh pull request merged, exhausting its use limit.
- **Evidence:** [PR #679](https://github.com/ModernNomad-98/Project-Aegis/pull/679)
  merged head `1d1a50961edd72400371bad5bb4cddb0b12e62aa` as
  `c1acc075910ea1e849401e18cdb60df31c09ef30` at the effective time above.
  This records consumption; it does not independently recertify historical
  validation or authorize another refresh.
```

## 5. Entry checks and collision protocol

Before C writes, re-query current main and the complete register, reverify
#679 merge/head/time and ancestry, and confirm no lifecycle entry already
records this use. Inspect every currently open register-touching PR at its
exact head and ask the coordinator for the current unpublished reservations.
The coordinator reconciles the union and supplies an unused ID; main's maximum
alone cannot allocate it. **APR119 has no ID in this plan.**

Use a clean isolated checkout and a single writer. Preserve every existing
append. Do not copy another lane's unmerged bytes. After any competing register
merge, refresh the base, recheck absence/IDs and preserve the new main prefix.
Mechanical base/ID reconciliation within these bounds is logged; changed
scope, policy or acceptance criteria require revised A and independent B.
A changed candidate head requires renewed applicable D/E/F evidence.
Missing API or reservation evidence is unknown, never an empty set.

## 6. Proportionate acceptance criteria and validation

B is the actual implementation base and H the resulting immutable candidate.

| ID | Acceptance criterion | Required evidence |
| --- | --- | --- |
| AC1 | Exactly one source path changes by one EOF lifecycle append; every prior register byte survives; one new unique defining ID is allocated through section 5. | B/H name-status and numstat; raw Git-blob prefix comparison; defining-ID/target parser; current main/open-head/reservation receipt; `git diff --check B H` exits 0. |
| AC2 | The sole new event targets APR119 as CONSUMED, records the verified #679 head/merge/effective timestamp, uses actual recorder/time, says no remaining use and no new authority, and leaves other grants/policies untouched. | Fresh retained API results for #679 and its merge, merge ancestry to current main, complete lifecycle scan, and independent comparison of the final entry with section 4 and APR119's original use limit. |
| AC3 | Mandatory local validation and scoped documentation checks pass at H. | `python -P -B scripts/validate-skills.py`; `python -P -B scripts/tests/test_validator.py`; `python -P -B scripts/ci/check-markdown-links.py --root . docs/approvals/APPROVAL_REGISTER.md`; all exit 0, with outputs retained, plus independent Markdown/rendering and factual review. |

Keep synthetic fixture storage outside the checkout as the current repository
instructions require. No new tests, historical baseline rebuild, or #679 test
rerun is needed for this record-only change. A failure is diagnosed, never
relabeled a pass or bypassed.

All three criteria are intended to be verifiable at H before D; none is
declared unavailable. They are **UNRUN during this planning stage** because no
candidate exists. Future exact-head CI, body-field readback, automated review,
independent F verdict and merge receipt are separate E/F/G duties, not
preclaimed Stage A results.

## 7. Separate stage handoffs and hard stops

- **A:** this exact plan, evidence references, classification, AC1–AC3 and final
  captured SHA-256. The planner holds no later stage of this change.
- **B:** a different agent independently audits the captured text/digest,
  complete lifecycle evidence, one-event scope and collision procedure;
  posts SD-B ACCEPT or REVISE naming that revision.
- **C:** separately assigned implementer follows accepted A/B, refreshes section
  5, appends one event, completes local checks, supplies H/tree/B, byte-preservation
  proof, source/skills reporting and SD-C.
- **D:** different implementation auditor resolves AC1–AC3 individually as
  MET/NOT MET/UNRUN at H. Missing required evidence causes REVISE.
- **E:** separate validator checks H under the current workflow, including
  applicable GitHub checks, records skips/UNRUN honestly and supplies SD-E.
- **F:** separate final reviewer reviews H and current required PR fields,
  stage evidence and source-bound skills reporting; posts the applicable
  head/body-bound SD-F verdict. Apply the row-publication rule actually in
  force then; the unmerged ROWPOLICY proposal is not present policy.
- **G:** separate authorized merger independently checks current authority,
  main/head, all applicable checks, required review/wait and F bindings, then
  records the merge receipt and observes post-merge main checks.

One PR holder at a time; the coordinator routes rather than authors or merges.
Current APR100/048/050 and APR105 govern delivery only alongside the actual
work authority and current owner green-check condition.

Stop the affected work if the event already exists, delivery evidence conflicts,
an ID collision is unresolved, an old byte changes, scope grows, or a required
check/evidence is missing. Reconcile through the coordinator; do not invent a
grant or amend old text. Tool/signing/publication approval rejection is not
permission to bypass through another route. Unknown historical validation is
not a reason to reconstruct or claim it. No provider, credential, settings,
VM, readability repair or baseline-regeneration work belongs to this item.

## 8. Actual skill use and persistence

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| `scoped-approval-register` | APR119-CLOSEOUT Stage A revision 1 / `/root/readability_index_backlog` | Read SKILL and register-format reference; applied immutable lifecycle and effective-status rules to APR119/#679; separated effective time from later recording and preserved prior grants. | Sections 1/3/4/5; factual one-event draft, no new authority, no allocated ID. Source implementation, publication and later validation are UNRUN. |
| `change-classification-gate` | APR119-CLOSEOUT Stage A revision 1 / `/root/readability_index_backlog` | Read SKILL and classification matrix; inspected sole target, CONTRIBUTING and workflow; classified by effect and locked scope/validation. | Sections 2/6; docs-only factual record, security surface Yes, current guard pattern does not match. No permission control or instruction change is included. |

Neither skill is MANUAL-ONLY. This plan is **workspace-persisted scratch** only.
No source register, Git state, PR, setting or provider was changed.
Continuation: send this exact captured plan and its hash to a different Stage B
agent. This planner provides no independent audit verdict.

