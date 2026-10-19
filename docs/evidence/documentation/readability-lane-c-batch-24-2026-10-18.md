# Readability Phase 4 re-read lane C - Stage C batch record, batch 24, 2026-10-18

**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** True identity **sd-a-789-repl-r2**; stage role **sd-c-read-lc-448-c1**. Stage C implementation record for lane C block 448-455 under accepted lean plan r1 comment **6265651287** + Stage B ACCEPT **6265698815**; owner decision 6242532417 (ODR-1). No merge; owner #848 untouched.

## 1. Scope, basis and one-path accounting
Basis/live main **907a602625255bcb4647beae60b0348e89fa6196** (60th record merge #863, tree 9886b734, parents 907a6026+b0472e91); capture basis 907a6026. Exactly one added path **docs/evidence/documentation/readability-lane-c-batch-24-2026-10-18.md**; no other added/modified/deleted path; no page/keeper/index/ledger/register/manifest/tool/test/workflow change; no merge. Fresh derivation: reader **741**, accepted **107**, provably **6**, no-record **618**, cannot-decide **6**, partial **4**, official **634**; R2 union **624**; ceil(624/4)=**156** capacity-624 quarters A0-155/B156-311 complete/C312-467/D468-623; arithmetic 741-107=634; sorted union positions **440-447 = lane C batch 24**, next 456-463; lane C batches 1-23 merged through 440-447. Duplicate-read contract: 66 merged lane A-D records; exact-path audit **0 page-read rows** for the eight targets; no older pre-lane read found; no unread-by-every-record claim.

## 2. Eight pages - mixed pin 1 pinned-equal + 7 re-pinned at 907a6026
| Page | Union index | Path | Blob at 907a6026 | 2db1ffb7 | Bytes / LF |
| --- | ---: | --- | --- | --- | ---: |
| P448 | 448 | docs/evidence/documentation/readability-lane-b-batch-9-2026-10-18.md | c3263f2e453c9cc43a0f6376f8cfbbe1291dd514 | re-pin | 33,416 / 175 |
| P449 | 449 | docs/evidence/documentation/readability-lane-c-batch-1-2026-10-15.md | 44616c0a1031b11b7c16c15bfd6e58d1faecb940 | pinned-equal | 74,117 / 852 |
| P450 | 450 | docs/evidence/documentation/readability-lane-c-batch-10-2026-10-18.md | 623b38f6a18e4688c8378224714ea4e5d5f6cfd4 | re-pin | 285,177 / 2,521 |
| P451 | 451 | docs/evidence/documentation/readability-lane-c-batch-11-2026-10-18.md | 3f18b6ae75076f06a2ab98c936d6eb90678b610e | re-pin | 191,951 / 1,574 |
| P452 | 452 | docs/evidence/documentation/readability-lane-c-batch-12-2026-10-18.md | e884578fea4ad1b859e0a66bf701b1e5f9252b3f | re-pin | 109,701 / 854 |
| P453 | 453 | docs/evidence/documentation/readability-lane-c-batch-13-2026-10-18.md | 857ecb411fad0de5b8f9fa43c184c3766ebdfd37 | re-pin | 204,341 / 1,650 |
| P454 | 454 | docs/evidence/documentation/readability-lane-c-batch-14-2026-10-18.md | 281e51fedd49cd5e4f0b0b3d428a0e285ca7f78d | re-pin | 99,933 / 809 |
| P455 | 455 | docs/evidence/documentation/readability-lane-c-batch-15-2026-10-18.md | d5717a7b46f16f3bd56c50be3fd2c6dca47efe38 | re-pin | 33,018 / 262 |
| **Totals** | | **eight pages** | | **1 pinned-equal / 7 re-pinned** | **404,305 / 3,428** |

## 3. Candidate-token inventory (never exact-once; unique keys; at-most-one defined/named per page/raw token)

**Descriptor:** candidate-token inventory for the eight pages at basis 907a6026. Keys are unique (page,line,raw token); no duplicate mentions; at most one defined/named disposition per (page,raw token). Counts come from the FINAL table below. Class rules: i uppercase/coded identifiers/acronyms/roles; ii lowercase technical/audience prose; iii non-backticked path/identifier; iv whole backticked code/command/identifier/SHA; v statuses, dates, line-ranges, ranges, placeholders, operators. Disposition codes: defined at first use, named gap - first use before any expansion on this page, or documented exclusion - CODE: reason with legend DATE, LINE-RANGE, STATUS, RANGE, PLACEHOLDER, OPERATOR, PROSE, EMPHASIS, PATH, COMMAND, SHA, LITERAL. Status tokens ACCEPT/ACCEPTED and variants are class v; operator glyphs incl U+21D4/U+2194 are class v OPERATOR; SHA/commit hashes are class iv SHA; H/M/L/P placeholders class v PLACEHOLDER; all-caps common words class i EMPHASIS; coded IDs class i named/defined; lowercase json/api prose class ii PROSE; DATE/LINE-RANGE class v.

| P448 | 3@230 | ii | evidence | documented exclusion - PROSE: lowercase technical/audience prose |
| P448 | 3@335 | ii | workflow | documented exclusion - PROSE: lowercase technical/audience prose |
| P448 | 9@65 | i | PR | named gap - first use before any expansion on this page |
| P448 | 9@89 | v | 6246622264 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 9@121 | v | 2026-10-18T06:35:38Z | documented exclusion - DATE: date/time literal |
| P448 | 9@121 | v | 2026-10 | documented exclusion - DATE: date/time literal |
| P448 | 9@199 | v | 6246654264 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 9@219 | v | ACCEPT | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 9@250 | v | 176-183 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 11@36 | iv | c8942134a9bb6d2eb6aec739a4dbe9e245194026 | documented exclusion - SHA: commit/blob hash |
| P448 | 12@29 | iv | 2db1ffb7985ddc1c087c455740fd59e962967461 | documented exclusion - SHA: commit/blob hash |
| P448 | 13@77 | iv | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json` | documented exclusion - COMMAND: backticked command/CLI token |
| P448 | 14@90 | v | 144-287 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 18@79 | v | 0-143 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 19@43 | v | 148-155 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 19@151 | iv | c8942134 | documented exclusion - SHA: commit/blob hash |
| P448 | 19@177 | v | 168-175 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 19@307 | v | 144-159 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 20@72 | v | 160-167 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 20@125 | v | 184-191 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 20@146 | v | MERGED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 21@53 | v | 144-175 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 26@32 | iv | `docs/evidence/documentation/readability-lane-b-batch-9-2026-10-18.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 26@85 | i | JSON | named gap - first use before any expansion on this page |
| P448 | 27@30 | i | LF | named gap - first use before any expansion on this page |
| P448 | 29@54 | iv | 2db1ffb7 | documented exclusion - SHA: commit/blob hash |
| P448 | 33@13 | iv | `.claude/skills/n-plus-one-detector/references/chatty-access-patterns.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 33@36 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 33@89 | iv | `33df95efa6069131e4fb3c3ebe7ab2e8f535d627` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 34@13 | iv | `.claude/skills/notification-webhook-ux-designer/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 34@74 | iv | `f7056b0699a16e2d26f3a868c5c4885bb6ae5f78` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 35@13 | iv | `.claude/skills/notification-webhook-ux-designer/references/notification-webhook-sheet.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 35@106 | iv | `56468b6843fbb34371faeb6cfe5696df27864a6b` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 36@13 | iv | `.claude/skills/observability-operator/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 36@64 | iv | `26d3a992bafd5cd1f752d40a32185aee016644c6` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 37@13 | iv | `.claude/skills/observability-operator/references/instrumentation-checklist.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 37@95 | iv | `f0f013791a8fbfed6d2c02103fcf2e2be43aaa27` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 38@13 | iv | `.claude/skills/offline-first-sync-architect/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 38@70 | iv | `31a2e43a69df82dfd8ac209cc9293b6302391ff2` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 39@13 | iv | `.claude/skills/onboarding-doc-designer/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 39@65 | iv | `1a679284e273b0a792f3587c59f92440b9cec157` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 40@13 | iv | `.claude/skills/onboarding-doc-designer/references/onboarding-sheet.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 40@87 | iv | `fca56c2ee98db63c303e255194f955d832c9d89e` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 42@48 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 42@69 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 44@27 | ii | token | documented exclusion - PROSE: lowercase technical/audience prose |
| P448 | 46@36 | v | 6246786004 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 46@163 | iv | `[A-Z][A-Z0-9]{1,7}` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P448 | 46@173 | v | 2-8 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 46@392 | v | `<...>` | documented exclusion - PLACEHOLDER: placeholder token |
| P448 | 46@401 | iv | `{...}` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@410 | iv | `N` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@415 | iv | `top-N` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@424 | iv | `after-N` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@486 | iv | `ms` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@492 | iv | `px` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@498 | iv | `dp` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@504 | iv | `×` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@509 | iv | `%` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 46@776 | i | SQL | named gap - first use before any expansion on this page |
| P448 | 46@825 | i | SELECT | named gap - first use before any expansion on this page |
| P448 | 46@833 | i | COUNT | named gap - first use before any expansion on this page |
| P448 | 46@840 | i | SUM | named gap - first use before any expansion on this page |
| P448 | 46@845 | i | GROUP | named gap - first use before any expansion on this page |
| P448 | 46@851 | i | BY | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P448 | 46@913 | i | SKILL | named gap - first use before any expansion on this page |
| P448 | 46@935 | ii | json | documented exclusion - PROSE: lowercase technical/audience prose |
| P448 | 46@987 | i | MANUAL | named gap - first use before any expansion on this page |
| P448 | 46@995 | i | BEFORE | named gap - first use before any expansion on this page |
| P448 | 46@1003 | i | DRAWS | named gap - first use before any expansion on this page |
| P448 | 46@1009 | i | ON | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P448 | 50@40 | v | L1-94 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 50@50 | v | L3 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 50@69 | v | L4 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 50@85 | v | L18 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 50@89 | v | L19 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 50@93 | v | × | documented exclusion - OPERATOR: operator glyph |
| P448 | 51@40 | v | L1-245 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 51@54 | i | UX | defined at first use |
| P448 | 51@89 | v | L8 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 51@94 | v | L33 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 51@105 | v | L80 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 51@150 | v | L124 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 51@158 | v | L154 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 51@172 | v | L160 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 51@182 | v | L161 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 52@40 | v | L1-80 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 52@50 | v | L1 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 52@74 | v | L3-4 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 52@81 | v | L37 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 52@92 | v | L44 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 52@99 | v | L56 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 52@103 | i | UI | named gap - first use before any expansion on this page |
| P448 | 53@40 | v | L1-195 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 53@95 | v | L68 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 53@99 | i | PII | named gap - first use before any expansion on this page |
| P448 | 53@104 | v | L76 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 53@108 | v | L148 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 54@40 | v | L1-74 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 54@77 | v | L52 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 54@81 | v | L57 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 54@92 | v | L58 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 54@96 | i | SLO | named gap - first use before any expansion on this page |
| P448 | 55@40 | v | L1-236 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 55@71 | v | L93 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 55@81 | v | L120 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 56@40 | v | L1-175 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 56@54 | i | README | named gap - first use before any expansion on this page |
| P448 | 56@70 | v | L53 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 57@40 | v | L1-75 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 57@50 | v | L7 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 57@53 | i | API | defined at first use |
| P448 | 57@79 | v | L47 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 59@36 | v | 6246952427 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 59@90 | iv | `≥2×` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 59@106 | iv | `N × round-trip` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 59@221 | iv | `per-category × per-channel` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 59@353 | iv | `dedups` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 61@27 | v | 6247059800 | documented exclusion - RANGE: numeric range/unit token |
| P448 | 61@100 | iv | `auth` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 61@123 | iv | `dup` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 70@135 | i | IN | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P448 | 71@37 | v | L3-10 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@127 | v | L12-84 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@362 | v | L7-9 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@489 | v | L14-21 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@511 | v | L23-46 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@536 | v | L48-54 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@560 | v | L56-63 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@587 | v | L65-82 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@617 | v | L84-94 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@772 | iv | `../SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P448 | 71@781 | v | L67-76 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 71@1033 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 72@19 | v | L3-9 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 72@175 | i | ORM | named gap - first use before any expansion on this page |
| P448 | 72@256 | i | APM | named gap - first use before any expansion on this page |
| P448 | 72@310 | i | TTL | named gap - first use before any expansion on this page |
| P448 | 76@350 | iv | `api-event-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 77@50 | v | L6 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@62 | v | L11-26 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@82 | v | L28-50 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@366 | i | SMS | named gap - first use before any expansion on this page |
| P448 | 77@525 | v | L52-68 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@542 | v | L70-140 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@558 | v | L146-167 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@579 | v | L169-190 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@597 | v | L192-217 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@623 | v | L219-234 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@653 | v | L236-245 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@799 | v | L144 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 77@804 | v | L238 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 78@19 | v | L8-9 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 83@297 | i | DM | named gap - first use before any expansion on this page |
| P448 | 83@314 | v | L5 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 83@318 | i | HTTP | named gap - first use before any expansion on this page |
| P448 | 83@363 | v | L6-7 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 83@495 | v | L11-22 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 83@525 | v | L24-35 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 83@548 | v | L37-44 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 83@576 | v | L46-61 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 83@596 | v | L63-72 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 83@618 | v | L74-80 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 84@19 | v | L3-7 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 88@288 | iv | `slo-reliability-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 88@358 | iv | `audit-log-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 89@50 | v | L9-19 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@69 | v | L21-40 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@257 | i | ID | defined at first use |
| P448 | 89@265 | v | L50 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@456 | v | L65 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@570 | iv | `disable-model-invocation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 89@663 | v | L42-59 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@680 | v | L61-102 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@696 | v | L104-122 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@717 | v | L124-139 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@744 | v | L141-149 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@762 | v | L151-167 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@788 | v | L169-185 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@818 | v | L187-195 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 89@959 | v | L189-195 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 90@19 | v | L65-69 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 95@103 | v | L11-65 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 95@171 | v | L6-9 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 95@456 | v | L11-20 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 95@476 | v | L22-32 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 95@503 | v | L34-40 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 95@526 | v | L42-50 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 95@546 | v | L52-63 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 95@579 | v | L65-74 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 96@82 | i | RED | named gap - first use before any expansion on this page |
| P448 | 96@132 | i | USE | named gap - first use before any expansion on this page |
| P448 | 96@183 | i | CPU | named gap - first use before any expansion on this page |
| P448 | 96@222 | i | GC | named gap - first use before any expansion on this page |
| P448 | 101@50 | v | L13-27 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@70 | v | L29-52 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@171 | v | L8-11 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@314 | v | L41 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@318 | v | L43 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@322 | v | L100 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@327 | v | L116 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@397 | iv | `dedup` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 101@575 | iv | `id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 101@653 | v | L54-72 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@670 | v | L74-133 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@686 | v | L135-160 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@707 | v | L162-182 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@725 | v | L184-206 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@751 | v | L208-224 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@781 | v | L226-236 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 101@917 | v | L228-236 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 102@47 | i | CRDT | named gap - first use before any expansion on this page |
| P448 | 102@145 | i | LWW | named gap - first use before any expansion on this page |
| P448 | 102@172 | i | SSE | named gap - first use before any expansion on this page |
| P448 | 107@50 | v | L8-21 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@69 | v | L23-40 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@218 | v | L35 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@222 | v | L157 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@284 | v | L150 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@340 | v | L72 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@520 | v | L42-56 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@537 | v | L58-92 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@552 | v | L94-108 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@572 | v | L110-127 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@590 | v | L129-151 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@616 | v | L153-164 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@646 | v | L166-175 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@766 | v | L92 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 107@770 | v | L168 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 108@19 | v | L19-21 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 108@55 | i | JOINING | named gap - first use before any expansion on this page |
| P448 | 113@61 | v | L5-9 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 113@353 | v | L11-19 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 113@382 | v | L21-32 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 113@409 | v | L34-41 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 113@429 | v | L43-49 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 113@457 | v | L51-62 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 113@476 | v | L64-68 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 113@496 | v | L70-75 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 113@644 | v | L57-61 | documented exclusion - LINE-RANGE: page-line reference |
| P448 | 114@146 | iv | `diataxis-doc-organizer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P448 | 121@295 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| P448 | 131@41 | v | REVISE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 133@52 | iv | d131f4ae | documented exclusion - SHA: commit/blob hash |
| P448 | 133@79 | i | NOT | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P448 | 133@83 | v | MET | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 137@545 | i | SHA | named gap - first use before any expansion on this page |
| P448 | 141@6 | i | AC | named gap - first use before any expansion on this page |
| P448 | 149@45 | v | OWED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P448 | 149@109 | i | CR | named gap - first use before any expansion on this page |
| P448 | 149@151 | i | EOF | defined at first use |
| P448 | 150@121 | i | AEGIS-APR-050 | defined at first use |
| P448 | 152@130 | iv | f5cde4b7 | documented exclusion - SHA: commit/blob hash |
| P448 | 152@320 | i | DCO | named gap - first use before any expansion on this page |
| P448 | 160@10 | i | MG | named gap - first use before any expansion on this page |
| P448 | 161@10 | i | SD | named gap - first use before any expansion on this page |
| P448 | 165@6 | i | AGENTS | named gap - first use before any expansion on this page |
| P449 | 1@70 | v | 2026-10-15 | documented exclusion - DATE: date/time literal |
| P449 | 1@70 | v | 2026-10 | documented exclusion - DATE: date/time literal |
| P449 | 3@12 | i | PHASE | named gap - first use before any expansion on this page |
| P449 | 3@39 | i | LANE | named gap - first use before any expansion on this page |
| P449 | 4@35 | ii | readability | documented exclusion - PROSE: lowercase technical/audience prose |
| P449 | 5@2 | iv | `e2a3e20b7c20ef8385b219b39c6405237163406f` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 5@40 | i | PR | named gap - first use before any expansion on this page |
| P449 | 5@46 | iv | `origin/main` | documented exclusion - PATH: backticked path identifier |
| P449 | 6@54 | iv | e6ed06a3 | documented exclusion - SHA: commit/blob hash |
| P449 | 7@35 | v | 2026-10-13 | documented exclusion - DATE: date/time literal |
| P449 | 7@79 | i | AI | named gap - first use before any expansion on this page |
| P449 | 10@2 | iv | `readability-lane-c-implementer-c` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 12@2 | iv | `code-review` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 15@70 | ii | evidence | documented exclusion - PROSE: lowercase technical/audience prose |
| P449 | 16@46 | iv | `Quote` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 20@25 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| P449 | 20@62 | i | AEGIS-APR-117 | named gap - first use before any expansion on this page |
| P449 | 21@22 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P449 | 25@55 | iv | `refs/remotes/origin/main` | documented exclusion - PATH: backticked path identifier |
| P449 | 26@3 | iv | `git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 27@55 | iv | `wt-laneC-b1` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 30@48 | iv | `docs/roadmaps/aegis-documentation-readability-backlog.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 36@8 | v | P | documented exclusion - PLACEHOLDER: placeholder letter token |
| P449 | 36@13 | iii | tools/readability_acceptance/check_index.py | documented exclusion - PATH: non-backticked path identifier |
| P449 | 36@71 | iv | e2a3e20b7c20ef8385b219b39c6405237163406f | documented exclusion - SHA: commit/blob hash |
| P449 | 58@2 | iv | `no_recorded_acceptance` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 58@38 | iv | `provably_pending` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 60@19 | iv | `git ls-tree -r --name-only e2a3e20b7c20ef8385b219b39c6405237163406f` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 61@29 | iv | `scripts/` | documented exclusion - PATH: backticked path identifier |
| P449 | 63@2 | iv | `tools/readability_acceptance/acceptance-index.json` | documented exclusion - PATH: backticked path identifier |
| P449 | 63@57 | iv | `reader_pages` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 66@20 | v | 296–443 | documented exclusion - RANGE: numeric range/unit token |
| P449 | 67@2 | iv | `.claude/skills/skill-deprecation-planner/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 68@2 | iv | `docs/evidence/documentation/full-page-readability-batch-after-231-2026-09-24.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 69@26 | iv | `skill-…` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 69@44 | iv | `docs/evidence/…` | documented exclusion - PATH: backticked path identifier |
| P449 | 73@2 | iv | `.claude/skills/share-link-access-architect/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 74@10 | iv | `cannot_decide` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 81@9 | iv | `.claude/skills/skill-deprecation-planner/references/deprecation-stage-playbook.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 82@9 | iv | `.claude/skills/skill-quality-reviewer/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 83@9 | iv | `.claude/skills/skill-quality-reviewer/references/quality-review-checklist.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 84@9 | iv | `.claude/skills/skill-usage-instrumenter/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 85@9 | iv | `.claude/skills/skill-usage-instrumenter/references/usage-signal-catalog.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 86@9 | iv | `.claude/skills/skill-usage-ledger/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 87@9 | iv | `.claude/skills/slo-reliability-architect/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 89@75 | v | <page> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P449 | 93@100 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P449 | 99@0 | iv | `acceptance-index.json` | documented exclusion - PATH: backticked path identifier |
| P449 | 102@2 | v | PENDING | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P449 | 106@74 | ii | candidate | documented exclusion - PROSE: lowercase technical/audience prose |
| P449 | 121@0 | iv | `full-page-acceptance` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 121@34 | iv | `targeted-review` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 122@87 | iv | `withdrawal` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 123@0 | iv | `lost-commit` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 123@51 | iv | `tools/readability_acceptance/check_index.py` | documented exclusion - PATH: backticked path identifier |
| P449 | 124@1 | v | L139-146 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 124@14 | v | L181-184 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 126@43 | iv | `build_index.py` | documented exclusion - PATH: backticked path identifier |
| P449 | 126@64 | iv | `check_index.py` | documented exclusion - PATH: backticked path identifier |
| P449 | 129@29 | v | ACCEPTED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P449 | 147@15 | i | WITHHELD | named gap - first use before any expansion on this page |
| P449 | 147@51 | v | L3149-3159 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 148@67 | v | L3155-3157 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 155@3 | v | L3090-3128 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 158@84 | iv | `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 158@113 | i | NOT | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P449 | 158@142 | iv | `main` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 158@156 | iv | `50241ba5` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 158@197 | iv | `e2a3e20b` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 159@52 | v | L5038-5042 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 172@21 | iv | `bfcf402a` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 172@31 | v | 2026-10-15T22:50:57Z | documented exclusion - DATE: date/time literal |
| P449 | 184@60 | iv | `LLM05` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 184@63 | v | L168 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 184@78 | iv | `ASI06` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 185@56 | v | L83-84 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 186@60 | iv | `LLM04` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 186@68 | iv | `ASI04` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 187@14 | v | L88 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 187@60 | v | L5-7 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 187@70 | iv | `RBAC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 187@87 | iv | `DDL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 188@25 | iv | `D<digits>` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 188@36 | i | ID | named gap - first use before any expansion on this page |
| P449 | 190@89 | iv | `CRLF` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 194@53 | v | 2026-10-12 | documented exclusion - DATE: date/time literal |
| P449 | 199@22 | iv | `read` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 205@28 | v | L1-236 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 211@27 | iv | `references/deprecation-stage-playbook.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 219@43 | v | L13-23 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 219@171 | v | → | documented exclusion - OPERATOR: operator glyph |
| P449 | 219@401 | i | SKILL | named gap - first use before any expansion on this page |
| P449 | 220@87 | v | L8-11 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 220@145 | i | CI | named gap - first use before any expansion on this page |
| P449 | 220@150 | i | PM | defined at first use |
| P449 | 220@178 | v | `<squash-sha>` | documented exclusion - PLACEHOLDER: placeholder token |
| P449 | 221@291 | iv | `git revert <squash-sha>` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 221@296 | v | L119 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 221@335 | v | L44-45 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 222@106 | v | L23 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 222@200 | v | L147 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 223@253 | iv | `docs-retention-index` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 223@277 | iv | `sunset-deprecation-communicator` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 223@312 | iv | `skill-usage-instrumenter` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 223@340 | iv | `library-diff-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 223@368 | iv | `skill-quality-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 238@28 | v | L1-106 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 243@65 | iv | `../SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 250@43 | v | L3-7 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 251@130 | v | `<successor>` | documented exclusion - PLACEHOLDER: placeholder token |
| P449 | 251@298 | v | L3 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 252@149 | v | L31-34 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 253@96 | i | PLAN | named gap - first use before any expansion on this page |
| P449 | 253@177 | v | L4-6 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 253@259 | v | L97-106 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 268@28 | v | L1-216 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 274@4 | iv | `../../../docs/skill-generation-standard.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 274@50 | iv | `../../../docs/skills-catalog.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 275@3 | iv | `references/quality-review-checklist.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 276@3 | iv | `RESERVED_BUNDLED_NAMES` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 276@38 | iv | `scripts/validate-skills.py` | documented exclusion - PATH: backticked path identifier |
| P449 | 282@43 | v | L8-19 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 283@218 | v | L12 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 283@300 | i | TALI | named gap - first use before any expansion on this page |
| P449 | 283@310 | v | L111 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 283@654 | i | LLM | named gap - first use before any expansion on this page |
| P449 | 283@689 | i | ASI | named gap - first use before any expansion on this page |
| P449 | 283@808 | v | L38 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 283@813 | v | L216 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 283@815 | iv | `D13` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 283@821 | iv | `D22` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 284@267 | iv | `code-review-helper` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 285@89 | v | PASS | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P449 | 285@154 | v | L71-72 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 285@238 | v | L155-156 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 285@283 | ii | workflow | documented exclusion - PROSE: lowercase technical/audience prose |
| P449 | 301@28 | v | L1-191 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 304@43 | v | 1-7 | documented exclusion - RANGE: numeric range/unit token |
| P449 | 313@43 | v | L1-3 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 314@158 | i | RLS | named gap - first use before any expansion on this page |
| P449 | 314@173 | i | MCP | named gap - first use before any expansion on this page |
| P449 | 314@265 | v | L97-98 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 314@512 | v | L82 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 314@537 | v | L184 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 315@113 | v | L26-31 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 315@144 | v | L172-176 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 316@182 | iv | `code-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 316@201 | v | L182-184 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 316@205 | iv | `code-simplifier` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 317@201 | iv | `rls-policy-auditor` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 317@223 | iv | `appsec-implementer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 317@245 | iv | `supply-chain-security-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 317@279 | iv | `model-poisoning-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 317@310 | iv | `memory-context-poisoning-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 317@551 | iv | `git cat-file -e e2a3e20b:.claude/skills/code-review/SKILL.md` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 317@627 | iv | `.claude/skills/code-reviewer/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 323@87 | i | CONCERN | named gap - first use before any expansion on this page |
| P449 | 324@2 | v | FAIL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P449 | 330@28 | v | L1-228 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 336@4 | iv | `references/usage-signal-catalog.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 342@193 | v | L19 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 344@342 | v | L179-180 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 345@205 | v | L128-129 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 346@235 | iv | `observability-operator` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 346@287 | iv | `eval-runner-designer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 346@314 | iv | `skill-deprecation-planner` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 361@28 | v | L1-113 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 373@43 | v | L3-4 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 376@306 | v | L59-60 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 376@366 | v | L112-113 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 391@28 | v | L1-111 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 397@13 | iv | `tools/skills-manifest.json` | documented exclusion - PATH: backticked path identifier |
| P449 | 398@21 | iv | `--refresh-skills-manifest` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 404@43 | v | L15-24 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 405@87 | v | L8-13 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 405@190 | i | CRLF | defined at first use |
| P449 | 407@100 | v | L22-24 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 407@140 | v | L90 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 408@283 | iv | `ai-closeout-reporter` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 422@28 | v | L1-214 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 428@18 | iv | `references/slo-derivation.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 434@43 | v | L8-17 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 434@88 | v | L19-28 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 435@127 | i | SLI | named gap - first use before any expansion on this page |
| P449 | 435@158 | i | SLO | named gap - first use before any expansion on this page |
| P449 | 435@189 | i | SLA | named gap - first use before any expansion on this page |
| P449 | 435@209 | i | CPU | named gap - first use before any expansion on this page |
| P449 | 435@214 | i | DNS | named gap - first use before any expansion on this page |
| P449 | 435@219 | i | CDN | named gap - first use before any expansion on this page |
| P449 | 435@224 | i | GC | named gap - first use before any expansion on this page |
| P449 | 435@236 | i | API | named gap - first use before any expansion on this page |
| P449 | 437@148 | v | L79 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 437@225 | iv | `incident-response-runbook` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 437@230 | v | L167-168 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 438@260 | iv | `systematic-debugger` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 438@283 | iv | `qa-strategy-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 438@308 | iv | `test-plan-designer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 438@330 | iv | `architecture-designer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 438@355 | iv | `human-approval-boundary` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 438@385 | iv | `saas-cost-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 445@10 | ii | inventory | documented exclusion - PROSE: lowercase technical/audience prose |
| P449 | 457@6 | iv | `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 457@8 | v | × | documented exclusion - OPERATOR: operator glyph |
| P449 | 457@91 | iv | `22cf10be2f3b4dff3b727288700dea2b1a6861e8` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 457@140 | iv | `e3fa656bdbffb99d661e3c9e0b5fff27fedefa34` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 457@189 | iv | `48230d027c5e8580419efc596fae3cad96896f65` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 457@238 | iv | `9e5a912a2be5fc3ab1036dc40591c275ad247dff` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 457@287 | iv | `fcc886160b3ca4d15d3fd6e757b113dcfcf00f5b` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 457@336 | iv | `54b4bec5f9a1b125f1c097d759ba12dc7e803d60` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 457@385 | iv | `594220d9701f964700030e1408a61b022f86b869` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 457@434 | iv | `74ced9ed454753657e2f8f0de3648a08f22b9fa9` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 458@6 | iv | `git cat-file -e e2a3e20b7c20ef8385b219b39c6405237163406f:<target>` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 458@68 | i | EXISTS | defined at first use |
| P449 | 459@6 | iv | `git cat-file -e e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/<name>/SKILL.md` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 460@6 | iv | `git show e2a3e20b7c20ef8385b219b39c6405237163406f:scripts/validate-skills.py` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 461@6 | iv | `".venv\\Scripts\\python.exe" -B scripts/validate-skills.py` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 461@75 | iv | `OK: 205 skill(s) valid, 0 warning(s)` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 462@6 | iv | `python -B scripts/ci/check-markdown-links.py <8 pages>` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 462@73 | iv | `files: 8   links checked: 11   anchors checked: 0   broken: 0   dead: 0   external-skipped: 0   other-skipped: 0` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 464@47 | iv | `http(s)://` | documented exclusion - PATH: backticked path identifier |
| P449 | 465@7 | iv | `python -P -B tools/readability_acceptance/check_index.py --quiet --ref e2a3e20b7c20ef8385b219b39c6405237163406f` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 478@2 | iv | `docs/evidence/documentation/readability-lane-c-batch-1-2026-10-15.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 481@69 | iv | `tools/` | documented exclusion - PATH: backticked path identifier |
| P449 | 481@84 | i | JSON | named gap - first use before any expansion on this page |
| P449 | 483@30 | iv | `No` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 488@78 | iv | `Blob ID` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 504@26 | iv | `\| K-082 \|` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 504@46 | iv | `\| K-089 \|` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 505@48 | iv | `K-081` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 515@42 | i | DISPOSED | named gap - first use before any expansion on this page |
| P449 | 538@45 | iv | `--ref` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 541@34 | iv | `built_at_ref` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 543@7 | iv | `--write` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 551@15 | i | UNREAD | named gap - first use before any expansion on this page |
| P449 | 553@31 | v | 296-303 | documented exclusion - RANGE: numeric range/unit token |
| P449 | 553@63 | v | 304-335 | documented exclusion - RANGE: numeric range/unit token |
| P449 | 554@77 | v | 336-343 | documented exclusion - RANGE: numeric range/unit token |
| P449 | 556@2 | iv | `.claude/skills/tenant-isolation-reviewer/references/isolation-surface-checklist.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 557@2 | iv | `.claude/skills/tenant-modeler/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 558@2 | iv | `.claude/skills/tenant-modeler/references/tenant-lifecycle-catalog.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 559@2 | iv | `.claude/skills/test-coverage-mapper/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 560@2 | iv | `.claude/skills/test-coverage-mapper/references/coverage-mapping-method.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 561@2 | iv | `.claude/skills/test-data-architect/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 562@2 | iv | `.claude/skills/test-data-architect/references/test-data-patterns.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 563@2 | iv | `.claude/skills/test-plan-designer/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 588@61 | iv | `build_index.py --write` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 595@27 | iv | `.claude/skills/` | documented exclusion - PATH: backticked path identifier |
| P449 | 596@51 | iv | `scripts/ci/check-markdown-links.py` | documented exclusion - PATH: backticked path identifier |
| P449 | 598@46 | v | REVISE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P449 | 613@0 | iv | aa88923f2517ebf2b0b3b56c3891fabe53d20b4c | documented exclusion - SHA: commit/blob hash |
| P449 | 613@40 | iv | `** (the head this repair supersedes),` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 614@0 | iv | `isOutdated: false` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 618@1181 | iv | `deepseek-v4-pro-apr117-keeper` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 620@171 | iv | `git log -1 --format="%an <%ae>" <head> -- <page>` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 620@278 | iv | `petern@carrotanddaikon.com` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 620@350 | iv | `263130032+ModernNomad-98@users.noreply.github.com` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 631@0 | iv | `bd533020a6b4a1ae68d0d3f96cfe8903aa09e026` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 632@11 | iv | `(partial; gaps...)` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 633@0 | iv | `build_index.py --report --ref <probe>` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 634@1 | iv | `table_rows 102, full_page_acceptances 82, reader_pages_with_rows 69` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 635@27 | iv | `check_index.py --ref <probe> --path .claude/skills/tenant-modeler/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P449 | 636@9 | iv | `accepted_on_recorded_review: 1` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 636@46 | iv | `official_pending_count: 0` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 650@16 | iv | `git ls-tree -r --name-only` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 651@45 | iv | `50241ba5036e36ec9bcd1ce7a4b93ffa23a0392b` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 652@10 | iv | `git show` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 660@2 | iv | `LLM03` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 661@91 | v | L83 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 664@2 | iv | `MCP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 664@12 | iv | `TALI` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 664@23 | iv | `RLS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 664@33 | iv | `LLM` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 664@43 | iv | `ASI` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 683@12 | iv | `3913683c686e6e71` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 684@12 | iv | `82ed906d2f228f0e` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 685@12 | iv | `88300e711714200a` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 686@12 | iv | `5fabf87b2df899e9` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 688@74 | iv | `30b62d11a991abcf` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 689@8 | iv | `c34e4d0057b09a3f` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 693@67 | iv | `30b62d11 a991abcf` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 694@0 | iv | `c34e4d00 57b09a3f` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 697@52 | iv | `userContentEdits.totalCount` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 698@71 | v | ⇒ | documented exclusion - OPERATOR: operator glyph |
| P449 | 703@36 | v | 2026-10-16 | documented exclusion - DATE: date/time literal |
| P449 | 705@2 | iv | `283d9ad6647090cb` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 705@72 | iv | `283d9ad6 647090cb` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 708@5 | iv | `0c68bdd68a75dcab` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 709@77 | iv | `58f9c49557487336` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 710@77 | iv | `Row source` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 711@38 | iv | `scripts/ci/check_pr_body_skills.py` | documented exclusion - PATH: backticked path identifier |
| P449 | 721@0 | iv | `60e418c2031077cd2b8e2db5d4282b19850976661b1c9baf4a888dc67fe2fc4e` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 723@0 | iv | `---` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 725@0 | iv | `## Footer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 737@104 | v | L180-182 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 740@57 | v | L345 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 740@91 | v | L348 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 740@143 | v | L22 | documented exclusion - LINE-RANGE: page-line reference |
| P449 | 751@71 | v | 296-443 | documented exclusion - RANGE: numeric range/unit token |
| P449 | 759@7 | v | 9-16 | documented exclusion - RANGE: numeric range/unit token |
| P449 | 767@70 | iv | `aa88923f..9c9b13de` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 768@11 | iv | `410 added / 154 deleted` | documented exclusion - PATH: backticked path identifier |
| P449 | 772@7 | iv | `git diff --numstat` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 776@67 | iv | `[KL]-digits` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 777@30 | iv | `T-001` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 777@38 | iv | `T-010` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P449 | 779@2 | iv | `build_index.py --report --ref <this head>` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 782@2 | iv | `check_index.py --quiet --ref <this head>` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 782@55 | iv | `reader_pages_in_tree 654` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 783@15 | iv | `accepted_on_recorded_review 57` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 783@49 | iv | `provably_pending 4` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 784@2 | iv | `no_recorded_acceptance 587` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 784@32 | iv | `recorded_acceptance_within_10_lines 0` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 785@2 | iv | `within_10_not_covered_by_targeted_review 0` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 785@48 | iv | `cannot_decide 6` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 786@2 | iv | `official_pending_count 597` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 792@15 | iv | `git rev-list --count e2a3e20b..HEAD` | documented exclusion - COMMAND: backticked command/CLI token |
| P449 | 792@59 | iv | `aa88923f2517ebf2b0b3b56c3891fabe53d20b4c` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 793@23 | iv | `9c9b13ded93db0667f42e5088cf1046db339c851` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 794@34 | iv | `6b80493da508037aa3f12b9bea73bbbdd4f6ca1c` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 804@62 | iv | `Peter Nguyen` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 805@16 | iv | `ModernNomad-98` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 806@0 | iv | `reviewer@example.invalid` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 811@50 | iv | `aa88923f` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 811@65 | iv | `validate-skills` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 812@27 | iv | `run_attempt 1` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 812@56 | iv | `changes` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 812@67 | iv | `gate-guard` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 813@51 | iv | `windows-offline-checks` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 814@0 | iv | `tools-tests-linux` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 814@15 | i | SKIPPED | named gap - first use before any expansion on this page |
| P449 | 814@24 | iv | `tools-tests-windows` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P449 | 815@47 | v | `pending` | documented exclusion - STATUS: backticked status keyword |
| P449 | 850@93 | i | LF | named gap - first use before any expansion on this page |
| P450 | 1@71 | v | 2026-10-18 | documented exclusion - DATE: date/time literal |
| P450 | 1@71 | v | 2026-10 | documented exclusion - DATE: date/time literal |
| P450 | 7@33 | v | 336-343 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 7@64 | v | 6252567082 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 7@91 | i | LF | named gap - first use before any expansion on this page |
| P450 | 7@99 | iv | c44405dd | documented exclusion - SHA: commit/blob hash |
| P450 | 7@134 | v | 6252525863 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 7@166 | v | ACCEPT | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 7@173 | v | 6252601127 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 7@214 | iv | 9085bf6ab5910989fc24166a28f862b5b06b5408 | documented exclusion - SHA: commit/blob hash |
| P450 | 7@297 | v | 2026-10-18T16:45:50Z | documented exclusion - DATE: date/time literal |
| P450 | 7@324 | iv | 55c939ec | documented exclusion - SHA: commit/blob hash |
| P450 | 7@349 | iii | docs/evidence/documentation/readability-lane-c-batch-10-2026-10-18.md** | documented exclusion - PATH: non-backticked path identifier |
| P450 | 7@354 | ii | evidence | documented exclusion - PROSE: lowercase technical/audience prose |
| P450 | 7@377 | ii | readability | documented exclusion - PROSE: lowercase technical/audience prose |
| P450 | 7@402 | v | 10-2026 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 7@410 | v | 10-18 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 9@27 | iv | 9085bf6a | documented exclusion - SHA: commit/blob hash |
| P450 | 9@251 | v | 0-152 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 9@265 | v | 153-305 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 9@335 | v | 144-279 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 9@352 | v | 306-458 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 9@368 | v | 459-609 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 9@392 | v | 1-9 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 9@502 | v | 344-351 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 11@92 | i | BATCH | named gap - first use before any expansion on this page |
| P450 | 11@241 | ii | inventory | documented exclusion - PROSE: lowercase technical/audience prose |
| P450 | 11@251 | ii | token | documented exclusion - PROSE: lowercase technical/audience prose |
| P450 | 11@359 | v | 6250828860 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 11@373 | iii | docs/delivery-workflow.md | documented exclusion - PATH: non-backticked path identifier |
| P450 | 11@387 | ii | workflow | documented exclusion - PROSE: lowercase technical/audience prose |
| P450 | 11@415 | v | 2026-10-12 | documented exclusion - DATE: date/time literal |
| P450 | 11@468 | iii | docs/design/behavioral-eval-runner-v1-fast-track-successor.md, | documented exclusion - PATH: non-backticked path identifier |
| P450 | 11@531 | iii | docs/design/behavioral-eval-runner-v1.md | documented exclusion - PATH: non-backticked path identifier |
| P450 | 11@576 | iii | docs/design/resumable-control-plane-v1.md | documented exclusion - PATH: non-backticked path identifier |
| P450 | 11@663 | v | 237-2026 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 11@667 | v | 2026-09-24 | documented exclusion - DATE: date/time literal |
| P450 | 11@672 | v | 09-24 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 11@681 | v | L68-L70 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 13@43 | iv | 9a5cb28d | documented exclusion - SHA: commit/blob hash |
| P450 | 13@63 | iv | e3f535e4 | documented exclusion - SHA: commit/blob hash |
| P450 | 13@83 | iv | 3ef6c735 | documented exclusion - SHA: commit/blob hash |
| P450 | 13@103 | iv | 6afc845a | documented exclusion - SHA: commit/blob hash |
| P450 | 13@123 | iv | 4b99f69f | documented exclusion - SHA: commit/blob hash |
| P450 | 13@143 | iv | 2c3c6ffe | documented exclusion - SHA: commit/blob hash |
| P450 | 13@163 | v | 38212595 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 13@183 | iv | f325daac | documented exclusion - SHA: commit/blob hash |
| P450 | 13@203 | iv | 7cea211e | documented exclusion - SHA: commit/blob hash |
| P450 | 13@223 | iv | 6f584c9d | documented exclusion - SHA: commit/blob hash |
| P450 | 13@425 | v | 304-335 | documented exclusion - RANGE: numeric range/unit token |
| P450 | 19@13 | iv | `docs/behavioral-eval-runner-schema-compatibility.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 19@41 | iv | 2db1ffb7 | documented exclusion - SHA: commit/blob hash |
| P450 | 19@69 | iv | `5390e533afb6355ae75a31ddf45640830a95fa63` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 20@13 | iv | `docs/delivery-workflow.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 20@43 | iv | `9a2ea2bd3557740373cce1285b9f31736b7fe1ec` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 21@13 | iv | `docs/design/behavioral-eval-runner-v1-fast-track-successor.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 21@79 | iv | `6e3811289bd108b078d07798856db645ea7e82e4` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 22@13 | iv | `docs/design/behavioral-eval-runner-v1.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 22@58 | iv | `24909a8d6f7ac4eb28970a19d0fe5c0b51aedec5` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 23@13 | iv | `docs/design/fast-save-handoff-protocol-v1.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 23@62 | iv | `aa3965fe0212a7c786103547aca67310a73a4b82` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 24@13 | iv | `docs/design/resumable-control-plane-v1.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 24@59 | iv | `fd6ee015b5a0004eda15e5879ddc83e02eb6784e` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 25@13 | iv | `docs/evidence/README.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 25@41 | iv | `7097e1341a6f28b4aa3fd266f13ff63e7adc1987` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 26@13 | iv | `docs/evidence/backlog-status-reconciliation-2026-09-12.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 26@75 | iv | `40d6ab55e1935f57898822cf89337f494de7c40b` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 31@45 | v | L2841-2862 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 31@250 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 31@273 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 33@36 | v | L1-106 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@74 | iv | `compatibility` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@76 | v | L1 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@94 | iv | `policy` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@94 | v | L4 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@100 | v | L5 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@106 | v | L6 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@107 | iv | `schema` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@118 | v | L9 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@120 | iv | `records` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@124 | v | L10 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@131 | v | L11 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@134 | iv | `contract` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@138 | v | L14 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@145 | v | L15 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@149 | iv | `report` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@162 | iv | `valid` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@166 | v | L18 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@173 | v | L24 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@174 | iv | `versioned` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@180 | v | L27 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@190 | iv | `evidence` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@194 | v | L28 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@201 | v | L29 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@206 | iv | `checkpoint` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@215 | v | L30 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@222 | v | L32 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@224 | iv | `event` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@229 | v | L33 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@237 | iv | `bounded` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@243 | v | L47 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@250 | v | L49 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@252 | iv | `field` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@257 | v | L50 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@264 | v | L54 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@265 | iv | `rule` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@271 | v | L56 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@277 | iv | `calibration` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@278 | v | L57 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@285 | v | L65 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@296 | iv | `external` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@306 | v | L67 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@312 | iv | `checks` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@313 | v | L68 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@320 | v | L78 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@326 | iv | `hashes` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@327 | v | L81 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@334 | v | L86 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@340 | v | `accepted` | documented exclusion - STATUS: backticked status keyword |
| P450 | 37@341 | v | L87 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@348 | v | L90 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@355 | v | L92 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@356 | iv | `path` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@368 | iv | `tests` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@369 | v | L94 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@376 | v | L96 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@381 | iv | `artifact` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@383 | v | L98 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@390 | v | L99 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@397 | iv | `permission` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@404 | v | L100 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@412 | v | L101 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@415 | iv | `approval` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@420 | v | L104 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 37@431 | iv | `release` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@446 | iv | `input` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@459 | iv | `marker` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@473 | iv | `aggregate` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@490 | iv | `decision` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@506 | iv | `integrity` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@523 | iv | `validation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@541 | iv | `diff` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@553 | iv | `dispatch` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@569 | iv | `key` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@580 | iv | `PR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 37@590 | iv | `binding` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@605 | iv | `retained` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@621 | iv | `review` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@635 | iv | `source` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@649 | iv | `digest` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@663 | iv | `quarantine` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@681 | v | `approved` | documented exclusion - STATUS: backticked status keyword |
| P450 | 37@697 | iv | `hash` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@709 | iv | `operation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@726 | iv | `revision` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@742 | iv | `immutable` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@759 | iv | `disposition` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@778 | iv | `request` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@793 | iv | `baseline` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@810 | iv | `rules` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 37@824 | iv | `item` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 46@11 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 48@36 | v | L1-1165 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@86 | iv | `stage` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@89 | v | L3 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@108 | iv | `repository` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@125 | v | L7 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@137 | v | L8 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@139 | iv | `integration` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@143 | v | L12 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@150 | v | L13 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@170 | iv | `head` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@181 | iv | `consumer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@192 | v | L25 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@209 | iv | `workspace` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@225 | iv | `canonical` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@242 | iv | `model` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@255 | iv | `provider` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@286 | iv | `harness` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@317 | iv | `reference` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@332 | v | L31 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@353 | iv | `PLAN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@365 | iv | `acceptance` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@383 | iv | `AUDIT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@396 | iv | `INDEPENDENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@409 | v | L42 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@415 | iv | `bound` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@416 | v | L45 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@428 | iv | `content` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@444 | v | L59 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@451 | v | L71 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@465 | v | L72 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@472 | v | L77 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@486 | v | L84 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@488 | iv | `routing` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@493 | v | L85 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@500 | v | L103 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@516 | iv | `verdict` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@531 | iv | `IMPLEMENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@540 | v | L120 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@548 | iv | `block` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@548 | v | L127 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@556 | v | L131 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@561 | iv | `entry` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@564 | v | L138 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@572 | v | L143 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@574 | iv | `governance` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@580 | v | L144 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@588 | v | L152 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@592 | iv | `local` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@596 | v | L153 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@604 | v | L158 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@605 | iv | `IMPLEMENTATION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@620 | v | L163 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@627 | iv | `audit` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@628 | v | L177 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@636 | v | L179 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 52@640 | v | `UNRUN` | documented exclusion - STATUS: backticked status keyword |
| P450 | 52@653 | iv | `VALIDATE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@669 | iv | `CODE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@681 | iv | `FINAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@694 | iv | `REVIEW` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@708 | iv | `author` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@722 | iv | `table` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@735 | iv | `MERGE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@748 | iv | `authority` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@765 | iv | `conditions` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@783 | iv | `gate` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@795 | iv | `AFFIRMATIVE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@814 | iv | `classification` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@836 | v | `MET` | documented exclusion - STATUS: backticked status keyword |
| P450 | 52@847 | iv | `build` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@860 | iv | `LISTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@874 | iv | `status` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@904 | iv | `name` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@931 | iv | `SKILL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@944 | iv | `scope` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@957 | v | `ACCEPT` | documented exclusion - STATUS: backticked status keyword |
| P450 | 52@989 | iv | `action` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1004 | iv | `boundary` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1021 | iv | `branch` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1053 | iv | `grant` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1067 | iv | `answer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1082 | iv | `mechanism` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1100 | iv | `surface` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1132 | iv | `lane` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1160 | iv | `runner` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1175 | iv | `provenance` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1194 | iv | `protocol` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1211 | iv | `row` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1223 | iv | `SCIF` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 52@1236 | iv | `reason` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 52@1251 | iv | `base` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 63@36 | v | L1-325 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@75 | iv | `AUTHORIZED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 67@147 | iv | `BER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 67@166 | v | L22 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@169 | iv | `phase` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@173 | v | L23 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@236 | v | L34 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@243 | v | L35 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@250 | v | L41 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@257 | iv | `offline` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@272 | iv | `tools` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@278 | v | L46 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@292 | v | L48 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@301 | iv | `behavior` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@327 | v | L52 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@329 | iv | `DESIGN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 67@334 | v | L53 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@343 | iv | `SPECIFICATION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 67@355 | v | L60 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@362 | v | L66 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@377 | iv | `HEAD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 67@389 | iv | `main` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@390 | v | L74 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@397 | v | L79 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@401 | iv | `github` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@425 | v | L93 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@433 | iv | `docs` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@457 | iv | `tree` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@461 | v | L108 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@469 | v | L112 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@485 | iv | `state` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@485 | v | L140 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@498 | iv | `actual` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@501 | v | L142 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@512 | iv | `judge` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@517 | v | L147 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@533 | v | L150 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@541 | iv | `body` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@557 | v | L154 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@565 | v | L160 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@581 | v | L166 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@583 | iv | `live` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@595 | iv | `durable` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@597 | v | L167 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@605 | v | L171 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@610 | iv | `register` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@621 | v | L181 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@629 | v | L183 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@637 | v | L189 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 67@688 | iv | `parent` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@702 | iv | `containment` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@734 | iv | `suite` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@747 | iv | `STOP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 67@759 | iv | `condition` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@792 | v | `DONE` | documented exclusion - STATUS: backticked status keyword |
| P450 | 67@804 | iv | `semantic` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@836 | iv | `BACKLOG` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 67@851 | iv | `cost` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@863 | iv | `workflow` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@880 | iv | `test` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@972 | iv | `subagent` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@1036 | iv | `activation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@1148 | iv | `assertions` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@1167 | iv | `drift` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@1181 | iv | `session` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@1212 | iv | `budget` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 67@1227 | iv | `COHERENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 67@1244 | iv | `DISCOVERY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 78@36 | v | L1-3092 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@175 | v | L16 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@189 | v | L19 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@196 | v | L20 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@203 | v | L21 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@259 | v | L37 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@261 | iv | `history` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@303 | iv | `version` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@315 | v | L55 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@371 | v | L61 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@385 | v | L62 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@386 | iv | `units` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@399 | v | L63 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@406 | v | L64 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@420 | v | L69 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@427 | v | L70 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@462 | v | L82 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@469 | v | L88 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@476 | v | L91 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@528 | v | L105 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@536 | v | L109 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@560 | v | L113 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@576 | v | L114 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@592 | v | L115 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@608 | v | L116 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@616 | v | L117 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@632 | v | L119 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 82@673 | iv | `isolation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@702 | iv | `blocker` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@768 | iv | `assertion` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@798 | iv | `stale` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@854 | iv | `stability` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@940 | iv | `evals` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@971 | iv | `reconciliation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1007 | iv | `validator` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1025 | iv | `workflows` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1043 | iv | `index` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1071 | iv | `EVAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 82@1084 | iv | `RUNNER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 82@1099 | iv | `cases` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1113 | iv | `json` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1126 | iv | `AUTHORED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 82@1143 | iv | `prompt` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1158 | iv | `POTENTIAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 82@1176 | iv | `scenario` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1193 | iv | `RUNNABLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 82@1210 | iv | `NEVER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 82@1224 | iv | `capability` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 82@1243 | iv | `DIVERGENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 82@1261 | iv | `LEGACY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 93@36 | v | L1-337 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@75 | iv | `FAST` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@86 | iv | `SAVE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@112 | iv | `HAND` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@123 | iv | `OFF` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@147 | v | L17 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@154 | v | L26 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@171 | iv | `DOCUMENTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@189 | iv | `POLICY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@210 | v | L38 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@219 | iv | `QA` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@231 | v | L39 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@242 | v | `FAILED` | documented exclusion - STATUS: backticked status keyword |
| P450 | 97@303 | iv | `ID` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@313 | iv | `command` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 97@315 | v | L95 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@337 | v | L107 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@353 | v | L130 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@385 | v | L135 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@401 | v | L141 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@403 | iv | `STOPPED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@417 | v | L155 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@418 | v | `UNKNOWN` | documented exclusion - STATUS: backticked status keyword |
| P450 | 97@425 | v | L161 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@433 | iv | `resume` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 97@433 | v | L165 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@447 | iv | `CI` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@457 | v | L168 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@465 | v | L169 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@481 | v | L206 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@483 | iv | `cleanup` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 97@489 | v | L213 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@497 | v | L228 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@505 | v | L233 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@521 | v | L238 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@537 | v | L239 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@545 | v | L240 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@553 | v | L248 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@561 | iv | `id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 97@569 | v | L249 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@585 | v | L251 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@601 | v | L253 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@605 | iv | `tokens` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 97@609 | v | L254 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@617 | v | L258 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@625 | v | L271 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@633 | v | L282 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@636 | iv | `SAVED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@650 | v | `ACTIVE` | documented exclusion - STATUS: backticked status keyword |
| P450 | 97@657 | v | L283 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 97@665 | iv | `INCOMPLETE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@684 | iv | `PAUSE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@713 | iv | `MEASUREMENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@733 | iv | `TARGET` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@907 | iv | `ids` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 97@1066 | iv | `FAILURE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@1098 | iv | `REAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@1167 | iv | `runtime` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 97@1236 | iv | `SHA` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 97@1248 | iv | `git` | documented exclusion - COMMAND: backticked command/CLI token |
| P450 | 108@36 | v | L1-971 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 112@104 | iv | `recovery` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@243 | v | L51 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 112@263 | iv | `process` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@327 | v | L76 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 112@374 | iv | `receipt` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@376 | v | L83 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 112@435 | iv | `gates` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@448 | iv | `adapter` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@479 | iv | `lifecycle` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@572 | v | L89 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 112@649 | iv | `JSON` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@661 | iv | `REUSE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@736 | iv | `OS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@791 | iv | `semantics` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@808 | iv | `ADS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@819 | iv | `BEHIND` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@833 | iv | `INTERFACE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@850 | iv | `WRAP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@919 | iv | `fixture` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@934 | iv | `preflight` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@951 | iv | `proof` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@994 | iv | `BEFORE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@1008 | iv | `CORRECTION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@1026 | iv | `REQUIRES` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@1042 | iv | `accounting` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@1121 | iv | `intent` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@1135 | iv | `lock` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@1147 | iv | `SDK` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 112@1226 | iv | `terminal` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 112@1242 | iv | `finalization` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 123@36 | v | L1-89 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 125@17 | i | README | named gap - first use before any expansion on this page |
| P450 | 127@260 | iv | `tool` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 127@308 | v | L43 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 127@378 | v | L58 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 127@530 | iv | `summary` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 127@675 | iv | `sha256` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 127@689 | v | `REVISE` | documented exclusion - STATUS: backticked status keyword |
| P450 | 127@800 | v | `OWED` | documented exclusion - STATUS: backticked status keyword |
| P450 | 138@36 | v | L1-84 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 140@38 | v | 2026-09-12 | documented exclusion - DATE: date/time literal |
| P450 | 140@38 | v | 2026-09 | documented exclusion - DATE: date/time literal |
| P450 | 142@370 | v | L36 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 142@531 | v | L75 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 142@552 | v | L80 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 142@581 | iv | `census` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 142@620 | iv | `PM` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 142@693 | iv | `CANDIDATE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 142@787 | iv | `metadata` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 142@898 | iv | `selection` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 142@915 | iv | `threshold` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 142@993 | iv | `claims` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 153@57 | i | ONE | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P450 | 155@24 | i | REAL | named gap - first use before any expansion on this page |
| P450 | 155@285 | i | DOTALL | named gap - first use before any expansion on this page |
| P450 | 162@15 | i | BER | named gap - first use before any expansion on this page |
| P450 | 167@16 | iv | `schema_version` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 169@16 | i | JSON | named gap - first use before any expansion on this page |
| P450 | 173@16 | i | YAML | named gap - first use before any expansion on this page |
| P450 | 175@16 | i | WP | named gap - first use before any expansion on this page |
| P450 | 187@18 | iv | `1.0.0-wp2b1` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 191@17 | iv | `runner_version` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 206@17 | iv | `baseline_identity` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 207@17 | iv | `execution_profile` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 209@17 | iv | `materialization` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 212@16 | i | CLI | named gap - first use before any expansion on this page |
| P450 | 217@16 | i | PR | named gap - first use before any expansion on this page |
| P450 | 242@15 | i | CI | named gap - first use before any expansion on this page |
| P450 | 246@15 | i | ID | named gap - first use before any expansion on this page |
| P450 | 247@15 | i | SHA | named gap - first use before any expansion on this page |
| P450 | 255@16 | i | AGENTS | named gap - first use before any expansion on this page |
| P450 | 259@18 | iv | `AGENTS.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 264@16 | i | PLAN | named gap - first use before any expansion on this page |
| P450 | 267@16 | i | AUDIT | named gap - first use before any expansion on this page |
| P450 | 288@16 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 289@16 | i | VALIDATE | named gap - first use before any expansion on this page |
| P450 | 290@16 | i | CODE | named gap - first use before any expansion on this page |
| P450 | 291@16 | i | FINAL | named gap - first use before any expansion on this page |
| P450 | 292@16 | i | REVIEW | named gap - first use before any expansion on this page |
| P450 | 296@16 | i | MERGE | named gap - first use before any expansion on this page |
| P450 | 303@17 | iv | `MG1` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 304@17 | iv | `MG5` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 305@17 | iv | `MG` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 307@17 | iv | `Affirmative?` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 310@16 | v | MET | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 311@17 | v | `FAIL` | documented exclusion - STATUS: backticked status keyword |
| P450 | 313@17 | iv | `NOT MET` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 314@16 | v | → | documented exclusion - OPERATOR: operator glyph |
| P450 | 317@16 | i | LISTED | named gap - first use before any expansion on this page |
| P450 | 318@17 | iv | `SD-C: INCOMPLETE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 319@17 | iv | `SD-E: INCOMPLETE — UNRUN LISTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 323@17 | iv | `ai-sdlc-operating-model` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 325@16 | i | SKILL | named gap - first use before any expansion on this page |
| P450 | 327@18 | iv | `SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 331@17 | iv | `ai-task-decomposer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 332@17 | iv | `NEEDS-REWRITE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 333@17 | iv | `TESTABLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 334@17 | iv | `UNTESTABLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 335@17 | iv | `acceptance-criteria-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 337@17 | iv | `reviewable-diff-discipline` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 338@18 | iv | `code-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 339@18 | iv | `library-diff-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 340@18 | iv | `risk-tiered-validation-selector` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 347@18 | iv | `agent-authorization-matrix` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 348@18 | iv | `human-approval-boundary` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 349@18 | iv | `change-classification-gate` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 350@18 | iv | `ai-closeout-reporter` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 362@17 | i | SCIF | named gap - first use before any expansion on this page |
| P450 | 364@17 | v | COMPLETE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 369@19 | iv | `git rev-parse <head>^{tree}` | documented exclusion - COMMAND: backticked command/CLI token |
| P450 | 370@17 | v | <head> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 371@17 | i | IMPL | named gap - first use before any expansion on this page |
| P450 | 372@17 | v | PASS | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 373@18 | iv | `## Reconciliation witness` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 374@18 | iv | `No` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 375@18 | iv | `Yes` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 376@17 | v | MERGED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 379@18 | iv | `grep -i '^PASS'` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 382@18 | iv | `INCOMPLETE — UNRUN LISTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 383@18 | iv | `From` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 384@18 | iv | `To` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 389@18 | iv | `absent` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 390@18 | iv | `not applicable` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 391@18 | iv | `present` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 392@18 | iv | `MG2` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 393@18 | iv | `MG3` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 394@18 | iv | `MG4` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 395@18 | iv | `answered` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 396@18 | iv | `MG5: not applicable` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 397@18 | iv | `grep` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 401@17 | v | <marker> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 404@18 | iv | `AEGIS-APR-047` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 405@17 | i | AEGIS-APR-013 | named gap - first use before any expansion on this page |
| P450 | 407@18 | iv | `gate-guard` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 410@18 | iv | `P0` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 411@18 | iv | `AEGIS-APR-050` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 412@19 | iv | `AGENTS.md:97-100` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 413@17 | iv | `:97-98` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 417@19 | iv | `CONTRIBUTING.md:233-236` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 419@18 | iv | `security-pr-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 421@19 | iv | `AGENTS.md:73-74` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 422@19 | iv | `CONTRIBUTING.md:253-258` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 426@18 | iv | `docs-only` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 433@18 | iv | `AEGIS-APR-100` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 435@17 | i | DCO | named gap - first use before any expansion on this page |
| P450 | 436@40 | v | 2026-09-23 | documented exclusion - DATE: date/time literal |
| P450 | 437@18 | iv | `D103` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 440@17 | i | AEGIS-APR-137 | named gap - first use before any expansion on this page |
| P450 | 442@17 | i | AEGIS-APR-115 | named gap - first use before any expansion on this page |
| P450 | 445@18 | ii | json | documented exclusion - PROSE: lowercase technical/audience prose |
| P450 | 447@19 | iv | `tools/readability_acceptance/acceptance-index.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 449@19 | iv | `tools/readability_acceptance/acceptance-verdicts-stage-1.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 451@19 | iv | `build_index.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 456@19 | iv | `.github/dependabot.yml` | documented exclusion - PATH: backticked path identifier |
| P450 | 458@18 | iv | `github-actions` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 459@18 | iv | `npm` | documented exclusion - COMMAND: backticked command/CLI token |
| P450 | 460@18 | iv | `pip` | documented exclusion - COMMAND: backticked command/CLI token |
| P450 | 464@18 | iv | `dismiss_stale_reviews: false` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 465@18 | iv | `require_last_push_approval: false` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 470@19 | iv | `.claude/skills/<skill-name>/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 471@17 | v | <skill-name> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 478@17 | i | URL | named gap - first use before any expansion on this page |
| P450 | 481@17 | v | <author> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 482@17 | v | <round> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 483@17 | v | <source locator/ordinal> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 484@17 | v | <stage> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 485@17 | v | <plan digest or candidate head> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 485@33 | ii | candidate | documented exclusion - PROSE: lowercase technical/audience prose |
| P450 | 486@17 | v | <retrievable locator> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 487@17 | v | <immutable source revision OR digest of retained exact author record> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 487@44 | i | OR | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P450 | 490@17 | i | API | named gap - first use before any expansion on this page |
| P450 | 493@18 | iv | `not derivable` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 494@18 | v | `unknown` | documented exclusion - STATUS: backticked status keyword |
| P450 | 495@18 | iv | `unsure` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 496@18 | iv | `validate-skills` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 497@17 | i | SDK | named gap - first use before any expansion on this page |
| P450 | 498@19 | iv | `test_offline_ci.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 499@17 | i | CLAUDE | named gap - first use before any expansion on this page |
| P450 | 501@19 | iv | `CLAUDE.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 502@19 | iv | `README.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 503@19 | iv | `test_validator.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 504@19 | iv | `validate-skills.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 508@18 | iv | `windows-offline-checks` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 509@19 | iv | `scripts/tests/fixtures/markdown-links/bad/README.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 510@19 | iv | `.claude/agents/example-agent.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 511@19 | iv | `tools/behavioral_eval_runner/README.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 513@19 | iv | `docs/` | documented exclusion - PATH: backticked path identifier |
| P450 | 514@18 | iv | `.gitattributes` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 515@19 | iv | `(.*/)?\\.gitattributes$` | documented exclusion - PATH: backticked path identifier |
| P450 | 516@19 | iv | `anything.exe` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 517@19 | iv | `foo.dll` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 518@19 | iv | `setup.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 519@19 | iv | `docs/x.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 521@17 | iv | `^` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 522@18 | iv | `.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 523@18 | iv | `tools-tests-linux` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 524@18 | iv | `tools-tests-windows` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 525@18 | iv | `enforce_admins` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 526@18 | iv | `false` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 528@19 | iv | `scripts/` | documented exclusion - PATH: backticked path identifier |
| P450 | 530@18 | iv | `### Before merging: Stage G entry conditions` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 531@18 | iv | `### Stage dispositions` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 532@18 | iv | `SD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 533@18 | iv | `### Stage dependencies` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 534@18 | v | `changed` | documented exclusion - STATUS: backticked status keyword |
| P450 | 535@18 | iv | `unchanged-and-verified` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 537@17 | v | <!-- bound-field: end --> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 538@17 | v | <!-- bound-field: witness --> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 539@17 | v | <!-- bound-field: skills --> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 540@17 | v | <!-- bound-field: security --> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 541@18 | iv | `skills` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 542@18 | iv | `end` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 544@17 | i | ERROR | named gap - first use before any expansion on this page |
| P450 | 546@18 | iv | `agent-governance-audit` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 549@19 | iv | `docs-as-code-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 551@20 | iv | `ModernNomad-98/Project-Aegis` | documented exclusion - PATH: backticked path identifier |
| P450 | 552@19 | iv | `source-of-truth-reconciler` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 554@19 | iv | `agent-failure-recovery` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 560@19 | iv | `D72` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 561@19 | iv | `D` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 563@19 | iv | `phased-work-handoff-designer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 564@19 | iv | `scoped-approval-register` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 574@15 | v | BLOCKED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 600@16 | i | DESIGN | named gap - first use before any expansion on this page |
| P450 | 603@18 | iv | `behavioral-eval-runner-v1.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 606@17 | iv | `eval-runner-designer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 607@16 | i | HEAD | named gap - first use before any expansion on this page |
| P450 | 610@17 | iv | `72e74af6f0183fef25e353ec2bf3a851d83b5df6` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 618@18 | iv | `docs/roadmaps/behavioral-eval-runner-backlog.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 621@17 | iv | `5d16bace5fec9f7c394ad7f3b4147ac9d4ad74f2` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 623@17 | iv | `b84e43ad9f42a793c6f68c2f5aebf0abfad2b8ed` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 624@17 | iv | `81404d350a26e8349d3c869209ae04f8628e0a95` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 631@17 | iv | `LIVE_DISPATCH_DISABLED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 654@16 | i | STOP | named gap - first use before any expansion on this page |
| P450 | 657@16 | v | DONE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 660@16 | i | BACKLOG | named gap - first use before any expansion on this page |
| P450 | 679@18 | iv | `ERROR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 681@18 | iv | `AMBIGUOUS_ACTIVATION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 684@18 | iv | `JUDGE_ERROR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 691@17 | i | AI | named gap - first use before any expansion on this page |
| P450 | 695@17 | i | COHERENT | named gap - first use before any expansion on this page |
| P450 | 697@17 | i | PER | named gap - first use before any expansion on this page |
| P450 | 698@17 | i | TOPIC | named gap - first use before any expansion on this page |
| P450 | 699@17 | i | TURN | named gap - first use before any expansion on this page |
| P450 | 713@17 | v | FAIL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 714@17 | v | CRITICAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 715@18 | iv | `project-orchestrator` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 739@16 | iv | `MCP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 745@16 | iv | `API` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 746@16 | iv | `RC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 748@17 | iv | `URL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 749@17 | iv | `ACL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 750@17 | iv | `DCO` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 778@17 | iv | `e2f1da0` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 796@18 | iv | `references/runner-design-blueprint.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 800@17 | iv | `e2f1da0beb6e4aed07044ca3a90e841962bfd590` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 802@18 | iv | `design/behavioral-eval-runner-v1` | documented exclusion - PATH: backticked path identifier |
| P450 | 822@17 | iv | `INCONCLUSIVE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 840@17 | iv | `run_evidence_binding` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 852@18 | iv | `docs/skill-generation-standard.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 856@18 | iv | `docs/design/` | documented exclusion - PATH: backticked path identifier |
| P450 | 859@18 | iv | `acceptance/` | documented exclusion - PATH: backticked path identifier |
| P450 | 860@18 | iv | `audits/` | documented exclusion - PATH: backticked path identifier |
| P450 | 861@18 | iv | `prompts/` | documented exclusion - PATH: backticked path identifier |
| P450 | 862@18 | iv | `reconciliation/` | documented exclusion - PATH: backticked path identifier |
| P450 | 863@18 | iv | `research/` | documented exclusion - PATH: backticked path identifier |
| P450 | 864@18 | iv | `roadmaps/` | documented exclusion - PATH: backticked path identifier |
| P450 | 865@18 | iv | `paths/` | documented exclusion - PATH: backticked path identifier |
| P450 | 866@18 | iv | `skills/` | documented exclusion - PATH: backticked path identifier |
| P450 | 869@19 | iv | `scripts/validate-skills.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 873@19 | iv | `.claude/agents/` | documented exclusion - PATH: backticked path identifier |
| P450 | 875@19 | iv | `docs/paths/` | documented exclusion - PATH: backticked path identifier |
| P450 | 876@19 | iv | `.claude/skills/` | documented exclusion - PATH: backticked path identifier |
| P450 | 877@19 | iv | `docs/skills-catalog.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 878@19 | iv | `scripts/audit-skill-contracts.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 883@17 | i | EVAL | named gap - first use before any expansion on this page |
| P450 | 884@17 | i | RUNNER | named gap - first use before any expansion on this page |
| P450 | 889@17 | i | AUTHORED | named gap - first use before any expansion on this page |
| P450 | 893@17 | i | RUNNABLE | named gap - first use before any expansion on this page |
| P450 | 894@17 | i | NEVER | named gap - first use before any expansion on this page |
| P450 | 898@17 | i | LEGACY | named gap - first use before any expansion on this page |
| P450 | 901@17 | i | IDENTITY | named gap - first use before any expansion on this page |
| P450 | 906@17 | i | SURFACES | named gap - first use before any expansion on this page |
| P450 | 907@17 | i | TRUSTED | named gap - first use before any expansion on this page |
| P450 | 915@17 | i | CORPUS | named gap - first use before any expansion on this page |
| P450 | 917@17 | i | SHIPPED | named gap - first use before any expansion on this page |
| P450 | 919@17 | i | ALWAYS | named gap - first use before any expansion on this page |
| P450 | 923@17 | i | EXCLUDED | named gap - first use before any expansion on this page |
| P450 | 926@17 | i | FRESH | named gap - first use before any expansion on this page |
| P450 | 931@17 | i | PINNED | named gap - first use before any expansion on this page |
| P450 | 932@17 | i | PROFILE | named gap - first use before any expansion on this page |
| P450 | 938@17 | i | EXPECTED | named gap - first use before any expansion on this page |
| P450 | 940@17 | i | MODE | named gap - first use before any expansion on this page |
| P450 | 944@17 | i | DATA | named gap - first use before any expansion on this page |
| P450 | 945@17 | i | MEASURED | named gap - first use before any expansion on this page |
| P450 | 952@17 | i | ATTEMPT | named gap - first use before any expansion on this page |
| P450 | 959@17 | v | ACTIVE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 960@17 | i | INACTIVE | named gap - first use before any expansion on this page |
| P450 | 976@17 | i | DETACHED | named gap - first use before any expansion on this page |
| P450 | 985@17 | v | HIGH | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 986@17 | i | STANDARD | named gap - first use before any expansion on this page |
| P450 | 988@17 | i | BLOCKS | named gap - first use before any expansion on this page |
| P450 | 996@17 | i | DECIDED | named gap - first use before any expansion on this page |
| P450 | 998@17 | i | DISABLED | named gap - first use before any expansion on this page |
| P450 | 1000@17 | i | SELECTED | named gap - first use before any expansion on this page |
| P450 | 1001@17 | v | UNKNOWN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 1004@17 | i | ADVISORY | named gap - first use before any expansion on this page |
| P450 | 1006@17 | i | MATCHING | named gap - first use before any expansion on this page |
| P450 | 1014@17 | i | BEFORE | named gap - first use before any expansion on this page |
| P450 | 1015@17 | i | DECISION | named gap - first use before any expansion on this page |
| P450 | 1016@17 | i | OWNER | named gap - first use before any expansion on this page |
| P450 | 1018@17 | i | REQUIRED | named gap - first use before any expansion on this page |
| P450 | 1021@17 | i | REVIEWED | named gap - first use before any expansion on this page |
| P450 | 1030@17 | i | EXCEPT | named gap - first use before any expansion on this page |
| P450 | 1032@17 | i | DURING | named gap - first use before any expansion on this page |
| P450 | 1033@17 | i | EVIDENCE | named gap - first use before any expansion on this page |
| P450 | 1040@17 | i | GENERAL | named gap - first use before any expansion on this page |
| P450 | 1044@18 | iv | `partial_install` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1046@18 | iv | `attempt_state` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1047@18 | iv | `aggregate_blocker` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1048@18 | iv | `assertion_uid` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1049@18 | iv | `case_uid` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1053@19 | iv | `docs/acceptance/scenario-a-runbook.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 1056@19 | iv | `scripts/acceptance/Invoke-ScenarioAEvidence.ps1` | documented exclusion - PATH: backticked path identifier |
| P450 | 1057@19 | iv | `Test-ScenarioAEvidence.ps1` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1058@18 | iv | `and` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1059@17 | iv | `?` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1061@19 | iv | `Invoke-/Test-ScenarioAEvidence.ps1` | documented exclusion - PATH: backticked path identifier |
| P450 | 1062@19 | iv | `project-state.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 1065@18 | iv | `51a89bae06a635f1881172ebc4b774bd0239baa0` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1066@19 | iv | `.claude/skills/*/evals/*.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 1068@18 | iv | `C:\\temp` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1069@18 | iv | `_template` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1070@18 | iv | `should_not_do` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1071@18 | iv | `should_not_trigger` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1072@18 | iv | `should_trigger` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1073@18 | iv | `type` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1074@19 | iv | `expect.triggers` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1076@18 | iv | `expected_skill` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1077@18 | iv | `overlaps_with` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1078@18 | iv | `4074d49` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1079@18 | iv | `phrase-without-invocation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1083@18 | iv | `adr-writer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1087@18 | ii | api | documented exclusion - PROSE: lowercase technical/audience prose |
| P450 | 1089@18 | iv | `api-event-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1090@18 | iv | `authorization-matrix-designer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1091@18 | iv | `observability-operator` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1095@18 | iv | `multi-tenant-data-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1096@18 | iv | `slo-reliability-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1097@18 | iv | `streaming-event-architect` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1098@19 | iv | `superadmin-observability-console-designer/evals/evals.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 1099@18 | iv | `refusal-admin-write-access-to-metrics` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1100@18 | iv | `refusal-content-reveal-without-incident` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1101@18 | iv | `triggers: true` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1104@17 | i | CASE | named gap - first use before any expansion on this page |
| P450 | 1105@17 | i | REFUSAL | named gap - first use before any expansion on this page |
| P450 | 1106@17 | i | TYPE | named gap - first use before any expansion on this page |
| P450 | 1107@18 | iv | `skill-quality-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1108@19 | iv | `release-readiness-reviewer/delegated-review-composes-subagent` | documented exclusion - PATH: backticked path identifier |
| P450 | 1111@19 | iv | `skill-quality-reviewer/whole-skill-adding-pr-is-the-library-diff-reviewer-seam` | documented exclusion - PATH: backticked path identifier |
| P450 | 1112@19 | iv | `source-of-truth-reconciler/security-conflict-still-triggers-then-routes` | documented exclusion - PATH: backticked path identifier |
| P450 | 1113@18 | iv | `(subagent)` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1114@18 | iv | `agent-goal-hijack-defender` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1115@18 | iv | `ai-security-red-team-reviewer (subagent)` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1116@18 | iv | `ai-threat-modeler` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1117@18 | iv | `prompt-injection-defender` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1118@18 | iv | `release-readiness-reviewer (subagent)` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1119@18 | iv | `release-readiness-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1120@18 | iv | `ai-security-red-team-reviewer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1122@18 | iv | `target_annotation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1123@18 | iv | `target_kind = subagent` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1124@18 | iv | `target_name` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1126@18 | iv | `ambiguous_needs_owner_review` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1127@18 | iv | `control_plane_only` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1128@18 | iv | `runtime_required` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1137@18 | iv | `aggregate_verdict ∈ {PASS, FAIL, INCONCLUSIVE}` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1148@18 | iv | `run_provenance` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1163@18 | iv | `code-simplifier` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1165@18 | iv | `triggers: false` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1166@18 | iv | `attempt_state = UNRUN` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1167@18 | iv | `aggregate_blocker: PRECHECK_EXCLUDED` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1168@18 | iv | `reason_code: UNJUDGEABLE_ASSERTION` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1169@19 | iv | `/skill-name` | documented exclusion - PATH: backticked path identifier |
| P450 | 1170@18 | iv | `attempt_state = ERROR` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1171@18 | iv | `aggregate_blocker: BUDGET_EXHAUSTED` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1175@18 | iv | `git archive` | documented exclusion - COMMAND: backticked command/CLI token |
| P450 | 1177@19 | iv | `git rev-parse <sha>^{tree}` | documented exclusion - COMMAND: backticked command/CLI token |
| P450 | 1178@17 | v | <sha> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1180@19 | iv | `evals/evals.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 1181@19 | iv | `evals/trigger-evals.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 1182@19 | iv | `references/*` | documented exclusion - PATH: backticked path identifier |
| P450 | 1183@19 | iv | `evals/**` | documented exclusion - PATH: backticked path identifier |
| P450 | 1186@18 | iv | `consumer_skills_only` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1187@18 | iv | `consumer_with_startup_routing` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1188@18 | iv | `consumer_with_subagents` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1189@18 | iv | `source_library` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1192@18 | iv | `consumer_partial_install` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1193@19 | iv | `profile_version/hash` | documented exclusion - PATH: backticked path identifier |
| P450 | 1194@18 | iv | `materialization_profile_id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1195@18 | iv | `workspace_role` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1196@18 | iv | `claim_scope` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1197@18 | iv | `# Project Aegis` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1198@19 | iv | `artifacts/audits/skill-contract-audit-baseline.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 1200@19 | iv | `workspace_role: consumer \\\| source_library` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1202@18 | iv | `regression-actual-project-aegis-source-landmarks-remain-library` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1203@18 | iv | `authored_eval_corpus_manifest_hash` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1204@18 | iv | `sanitized_runtime_surface_manifest_hash` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1205@18 | iv | `product_fixture_manifest_hash` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1210@18 | iv | `clickthrough-test-engineer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1211@18 | iv | `vite-build-qa-engineer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1215@18 | iv | `reason_code: MISSING_PREREQUISITE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1216@18 | iv | `reason_code: FIXTURE_SETUP_FAILED` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1217@18 | iv | `reason_code: INCOMPATIBLE_INVOCATION_MODE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1218@18 | iv | `MANUAL-ONLY; never auto-invoke.` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1219@18 | iv | `disable-model-invocation: true` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1220@18 | iv | `model_selected` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1221@18 | iv | `explicit_skill_invocation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1222@18 | iv | `delegated_subagent` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1223@18 | iv | `activation_mode_expected` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1224@18 | iv | `activation_mode_observed` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1225@18 | iv | `disable-model-invocation` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1226@18 | iv | `description` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1227@19 | iv | `.claude/agents/<name>.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 1228@19 | iv | `.claude/skills/<name>/` | documented exclusion - PATH: backticked path identifier |
| P450 | 1229@17 | v | <name> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1230@17 | i | CHANGES | named gap - first use before any expansion on this page |
| P450 | 1232@18 | iv | `target_kind` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1235@17 | i | OUTSIDE | named gap - first use before any expansion on this page |
| P450 | 1236@18 | iv | `isolated_consumer_skills_only` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1237@18 | iv | `isolated_consumer_with_startup_routing` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1238@18 | iv | `isolated_consumer_with_subagents` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1239@18 | iv | `isolated_source_library` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1240@17 | i | HOST | named gap - first use before any expansion on this page |
| P450 | 1241@17 | i | DISK | named gap - first use before any expansion on this page |
| P450 | 1243@19 | iv | `→ invokes requirements-gathering-facilitator` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1246@18 | iv | `Skill` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1247@19 | iv | `.claude/skills/<name>/SKILL.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 1249@17 | i | EXIT | named gap - first use before any expansion on this page |
| P450 | 1250@17 | i | GATE | named gap - first use before any expansion on this page |
| P450 | 1251@17 | i | OWNERS | named gap - first use before any expansion on this page |
| P450 | 1254@17 | i | STATUS | named gap - first use before any expansion on this page |
| P450 | 1255@18 | iv | `EXIT GATE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1256@18 | iv | `RECORDING STATUS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1257@18 | iv | `STAGE-2 OWNERS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1259@19 | iv | `→ invokes X` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1260@18 | iv | `reason_code: AMBIGUOUS_ACTIVATION` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1261@18 | i | TYPED | named gap - first use before any expansion on this page |
| P450 | 1263@19 | iv | `requirements-gathering-facilitator` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1264@19 | iv | `expected typed target ∈ activations` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1265@19 | iv | `should_not_trigger ∩ activations = ∅` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1266@19 | iv | `Test-ZeroCommitCount` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1267@19 | iv | `Test-AppendOnly` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1269@19 | iv | `SS-002` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1270@19 | iv | `SS-003` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1271@18 | i | FIXED | named gap - first use before any expansion on this page |
| P450 | 1272@19 | iv | `Test-ManifestStep` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1273@19 | iv | `Test-SpecArtifact` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1280@20 | iv | `calibration_dataset_version/hash` | documented exclusion - PATH: backticked path identifier |
| P450 | 1289@19 | iv | `regression-one-process-walkthrough-is-one-valid-target` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1291@20 | iv | `scripts/acceptance/Invoke-/Test-ScenarioAEvidence.ps1` | documented exclusion - PATH: backticked path identifier |
| P450 | 1292@19 | iv | `observed_turn_class` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1293@19 | iv | `prior_state` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1294@19 | iv | `next_state` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1295@19 | iv | `selected_answer_id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1296@20 | iv | `project-orchestrator/evals/evals.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 1297@19 | iv | `edge-consumer-repo-not-skills-library` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1298@19 | iv | `regression-fresh-consumer-with-copied-aegis-files-stays-product` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1299@19 | iv | `positive-cold-vague-idea` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1300@19 | iv | `regression-fresh-consumer-…` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1302@19 | iv | `edge-exact-preview-is-byte-for-byte-no-ellipsis` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1303@20 | iv | `→ invokes …` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1304@19 | iv | `regression-clinic-stage1-handoff-one-question` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1305@19 | iv | `regression-clinic-observed-compound-question-is-rejected` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1306@19 | iv | `regression-clinic-stage1-many-areas-one-question` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1307@19 | iv | `regression-orchestrator-atomic-gate-rewrites-delegated-candidate` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1308@19 | iv | `should-not-treat-scope-acceptance-as-build-authority` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1309@19 | iv | `should-not-auto-merge-or-apply-migration` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1311@19 | iv | `should-not-batch-high-risk-actions` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1313@19 | iv | `edge-immutable-history-is-append-only-placeholder-preserved` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1314@19 | iv | `edge-no-recording-operation-this-turn` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1315@19 | iv | `should-not-treat-business-answer-as-write-approval` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1317@20 | iv | `selected_runnable_units × N` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1318@18 | v | × | documented exclusion - OPERATOR: operator glyph |
| P450 | 1319@19 | iv | `N=3` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1320@19 | iv | `2-of-3` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1321@19 | iv | `N=5` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1322@19 | iv | `N` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1323@19 | iv | `N_attempts` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1324@20 | iv | `k > N/2` | documented exclusion - PATH: backticked path identifier |
| P450 | 1325@20 | iv | `wins/N` | documented exclusion - PATH: backticked path identifier |
| P450 | 1326@19 | iv | `quarantine_status: ACTIVE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1327@19 | iv | `risk_class` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1328@19 | iv | `quarantine_history` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1329@19 | iv | `quarantine_status: INACTIVE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1333@19 | iv | `NONE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1334@19 | iv | `quarantine_status ∈ {ACTIVE, INACTIVE}` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1337@20 | iv | `PASS count ≥ 2` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1338@19 | iv | `aggregate_blocker = NONE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1339@19 | iv | `aggregate_verdict = PASS` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1340@20 | iv | `FAIL count ≥ 2` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1341@19 | iv | `aggregate_verdict = FAIL` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1342@19 | iv | `aggregate_verdict = INCONCLUSIVE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1343@18 | i | FIRST | named gap - first use before any expansion on this page |
| P450 | 1344@19 | iv | `aggregate_blocker = ERROR` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1345@19 | iv | `aggregate_blocker = JUDGE_ERROR` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1346@19 | iv | `aggregate_blocker = INSUFFICIENT_ATTEMPTS` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1347@19 | iv | `aggregate_blocker = PRECHECK_EXCLUDED` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1348@19 | iv | `reason_code` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1349@19 | iv | `aggregate_blocker = BUDGET_EXHAUSTED` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1350@19 | iv | `reason_code: BUDGET_CAP` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1351@19 | iv | `execution_degraded: true` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1352@19 | iv | `aggregate_verdict` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1353@19 | iv | `execution_degraded` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1354@19 | iv | `reason_code: MISSING_FIXTURE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1355@19 | iv | `k = floor(N/2)+1` | documented exclusion - PATH: backticked path identifier |
| P450 | 1356@19 | iv | `QUARANTINED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1357@19 | iv | `quarantine_status` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1358@19 | iv | `latest_aggregate_blocker` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1359@19 | iv | `latest_aggregate_verdict` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1360@19 | iv | `quarantine_reason` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1361@19 | iv | `quarantine_since` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1362@19 | iv | `stability_window` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1363@19 | iv | `aggregate_verdict: FAIL, quarantine_status: ACTIVE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1365@19 | iv | `risk_class ∈ {CRITICAL, HIGH, STANDARD}` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1366@19 | iv | `waiver_id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1367@19 | iv | `expires_at` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1368@19 | iv | `issued_at` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1369@18 | i | EXISTING | named gap - first use before any expansion on this page |
| P450 | 1370@18 | i | BOUND | named gap - first use before any expansion on this page |
| P450 | 1371@18 | i | UPPER | named gap - first use before any expansion on this page |
| P450 | 1373@19 | iv | `runnable_units` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1375@19 | iv | `judge_cost` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1376@19 | iv | `session_cost` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1378@20 | iv | `remaining_enforceable_budget − reserved_maximum ≥ 0` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1379@19 | iv | `concurrency = 1` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1380@18 | i | CEILINGS | named gap - first use before any expansion on this page |
| P450 | 1381@18 | i | HARD | named gap - first use before any expansion on this page |
| P450 | 1382@18 | i | DEFAULT | named gap - first use before any expansion on this page |
| P450 | 1383@19 | iv | `ai-cost-guardrail-designer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1384@18 | i | WHICH | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P450 | 1386@20 | iv | `scheduling_policy_version/hash` | documented exclusion - PATH: backticked path identifier |
| P450 | 1387@20 | iv | `.claude/skills/<X>/` | documented exclusion - PATH: backticked path identifier |
| P450 | 1388@18 | v | <X> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1389@19 | iv | `frontend-perf-engineer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1391@19 | iv | `claim_scope: partial_install` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1396@18 | v | <case-definition-hash> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1397@18 | v | <case-id> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1398@18 | v | <eval-file-kind> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1399@18 | v | <target-owner> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1400@18 | v | <assertion-content-hash> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1401@18 | v | <assertion-index> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1402@18 | v | <case_uid> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1403@19 | iv | `case-definition-hash` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1406@18 | i | EXACTLY | named gap - first use before any expansion on this page |
| P450 | 1409@19 | iv | `input_evidence_manifest_sha256` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1410@19 | iv | `final_evidence_manifest_sha256` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1411@19 | iv | `final_report_sha256` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1412@19 | iv | `finalization_marker_sha256` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1413@19 | iv | `what_fired_instead` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1416@19 | iv | `attempt_state: UNRUN` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1417@19 | iv | `aggregate_verdict: INCONCLUSIVE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1419@18 | i | READ | named gap - first use before any expansion on this page |
| P450 | 1420@18 | i | OUTPUT | named gap - first use before any expansion on this page |
| P450 | 1421@20 | iv | `input_evidence_manifest.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 1422@19 | iv | `run_id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1423@18 | i | AFTER | named gap - first use before any expansion on this page |
| P450 | 1424@20 | iv | `final_evidence_manifest.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 1426@19 | iv | `reason_code: EVIDENCE_INTEGRITY_FAILURE` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1427@18 | i | FINALIZE | named gap - first use before any expansion on this page |
| P450 | 1430@18 | i | SNAPSHOT | named gap - first use before any expansion on this page |
| P450 | 1431@18 | i | BUNDLE | named gap - first use before any expansion on this page |
| P450 | 1432@18 | i | MARKER | named gap - first use before any expansion on this page |
| P450 | 1435@18 | i | PROVEN | named gap - first use before any expansion on this page |
| P450 | 1436@20 | iv | `spawn_fresh_session(prompt\\\|script) → session handle` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1437@20 | iv | `stream_events(session) → event stream` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1438@19 | iv | `capability_report()` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1443@18 | i | OTHER | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P450 | 1445@18 | i | AGENT | named gap - first use before any expansion on this page |
| P450 | 1446@18 | i | CONTROL | named gap - first use before any expansion on this page |
| P450 | 1447@18 | i | PLANE | named gap - first use before any expansion on this page |
| P450 | 1448@18 | i | SANDBOX | named gap - first use before any expansion on this page |
| P450 | 1449@18 | i | TOOL | named gap - first use before any expansion on this page |
| P450 | 1450@19 | iv | `.scenario-a-run-id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1451@19 | iv | `run-id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1452@19 | iv | `Remove-Item -ErrorAction Stop` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1453@19 | iv | `Remove-OwnedRunRoot` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1454@19 | iv | `Test-Path` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1455@19 | iv | `Resolve-PhysicalDir` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1456@19 | iv | `should_not_*` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1457@18 | iv | `0` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1458@20 | iv | `.github/workflows/` | documented exclusion - PATH: backticked path identifier |
| P450 | 1462@19 | iv | `assertion_coverage` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1463@19 | iv | `claim_scope: full_library` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1466@19 | iv | `risk_class: CRITICAL` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1467@18 | i | ACTUALLY | named gap - first use before any expansion on this page |
| P450 | 1468@20 | iv | `→ invokes skill-name` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1469@19 | iv | `workspace_role: source_library` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1470@18 | i | BUILD | named gap - first use before any expansion on this page |
| P450 | 1475@18 | i | LATER | named gap - first use before any expansion on this page |
| P450 | 1487@19 | iv | `execution_state` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1488@19 | iv | `evidence_manifest_sha256` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1489@18 | i | DEFERRED | named gap - first use before any expansion on this page |
| P450 | 1493@18 | i | RESERVE | named gap - first use before any expansion on this page |
| P450 | 1494@18 | iv | `$` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1497@18 | i | WOULD | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P450 | 1498@15 | i | FAST | named gap - first use before any expansion on this page |
| P450 | 1499@15 | i | SAVE | named gap - first use before any expansion on this page |
| P450 | 1501@15 | i | HAND | named gap - first use before any expansion on this page |
| P450 | 1502@15 | i | OFF | named gap - first use before any expansion on this page |
| P450 | 1505@41 | v | 2026-10-11 | documented exclusion - DATE: date/time literal |
| P450 | 1513@16 | v | L266-271 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 1515@16 | i | POLICY | named gap - first use before any expansion on this page |
| P450 | 1518@16 | i | QA | named gap - first use before any expansion on this page |
| P450 | 1522@16 | v | FAILED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 1548@16 | i | STOPPED | named gap - first use before any expansion on this page |
| P450 | 1573@17 | i | SAVED | named gap - first use before any expansion on this page |
| P450 | 1576@17 | i | PAUSE | named gap - first use before any expansion on this page |
| P450 | 1580@17 | i | TARGET | named gap - first use before any expansion on this page |
| P450 | 1589@17 | v | L11-79 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 1590@17 | v | L96-111 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 1592@17 | i | FS | named gap - first use before any expansion on this page |
| P450 | 1610@17 | i | HANDOFF | named gap - first use before any expansion on this page |
| P450 | 1611@17 | v | <workstream/item> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1613@17 | v | <path> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1614@17 | v | <what/why> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1615@17 | v | <reason> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1616@17 | v | <command> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1618@17 | v | <tell-tale output: counts / ids / output line> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1619@17 | v | <decision> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1620@17 | v | <rationale> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1621@17 | v | <item> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1622@17 | v | <the single line that resumes the work cold> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 1626@18 | iv | `AT-10` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1648@17 | i | FAILURE | named gap - first use before any expansion on this page |
| P450 | 1660@17 | v | L126-131 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 1666@17 | v | L128 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 1683@18 | iv | `6c83b723` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1684@18 | iv | `7fbc2335` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1686@19 | iv | `tools/aegis_delivery_control` | documented exclusion - PATH: backticked path identifier |
| P450 | 1687@19 | iv | `fast_save.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1702@18 | iv | `ad1e40fc` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1703@19 | iv | `tools/aegis_delivery_control/fast_save.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1704@18 | iv | `REQUIRED_CHECKPOINT_KEYS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1705@18 | iv | `STATE_KEYS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 1706@18 | iv | `pause_incomplete_reason` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1723@16 | iv | `57e6928d2849aa5377daf52c723b85736292585d` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1731@16 | i | CP | named gap - first use before any expansion on this page |
| P450 | 1777@16 | i | AEGIS-APR-001 | named gap - first use before any expansion on this page |
| P450 | 1778@16 | i | AEGIS-APR-002 | named gap - first use before any expansion on this page |
| P450 | 1793@18 | iv | `tools/behavioral_eval_runner/` | documented exclusion - PATH: backticked path identifier |
| P450 | 1795@18 | iv | `tests/` | documented exclusion - PATH: backticked path identifier |
| P450 | 1798@16 | i | REUSE | named gap - first use before any expansion on this page |
| P450 | 1804@18 | iv | `test_canonical.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1807@16 | i | OS | named gap - first use before any expansion on this page |
| P450 | 1812@18 | iv | `test_identity.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1814@16 | i | ADS | named gap - first use before any expansion on this page |
| P450 | 1815@16 | i | BEHIND | named gap - first use before any expansion on this page |
| P450 | 1817@16 | i | WRAP | named gap - first use before any expansion on this page |
| P450 | 1821@18 | iv | `test_pathsafe.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1823@17 | iv | `safe_join` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 1829@18 | iv | `test_preflight.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1832@18 | iv | `test_process_control.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1834@18 | iv | `test_scheduler.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1838@16 | i | REQUIRES | named gap - first use before any expansion on this page |
| P450 | 1846@18 | iv | `test_budget.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1852@18 | iv | `test_calibration_first_live_corrections.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1853@18 | iv | `test_calibration_ledger.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1858@18 | iv | `test_calibration_development_driver.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1860@18 | iv | `test_calibration_phase01.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1866@18 | iv | `test_evidence.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1867@18 | iv | `test_group_bcde.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1868@18 | iv | `test_hardening.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1871@18 | iv | `test_approval_lifecycle.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1878@18 | iv | `test_grading_schemas.py` | documented exclusion - PATH: backticked path identifier |
| P450 | 1886@19 | iv | `tools/aegis_control_plane` | documented exclusion - PATH: backticked path identifier |
| P450 | 1888@19 | iv | `tools/aegis_controller` | documented exclusion - PATH: backticked path identifier |
| P450 | 1889@19 | iv | `tools/aegis_runner` | documented exclusion - PATH: backticked path identifier |
| P450 | 1892@19 | iv | `python -m tools.aegis_delivery_control` | documented exclusion - COMMAND: backticked command/CLI token |
| P450 | 1905@17 | v | COMPLETED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 1948@17 | i | UID | named gap - first use before any expansion on this page |
| P450 | 1960@17 | i | SAME | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P450 | 1966@17 | i | EXPIRED | named gap - first use before any expansion on this page |
| P450 | 1973@17 | i | CAS | named gap - first use before any expansion on this page |
| P450 | 1976@17 | i | CONSUMED | named gap - first use before any expansion on this page |
| P450 | 1977@17 | i | RELEASED | named gap - first use before any expansion on this page |
| P450 | 1978@17 | i | RESERVED | named gap - first use before any expansion on this page |
| P450 | 1984@17 | i | BOTH | named gap - first use before any expansion on this page |
| P450 | 1994@17 | i | ADJUSTED | named gap - first use before any expansion on this page |
| P450 | 2008@17 | i | PLANNED | named gap - first use before any expansion on this page |
| P450 | 2009@17 | v | RUNNING | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 2010@17 | i | PAUSING | named gap - first use before any expansion on this page |
| P450 | 2011@17 | v | PAUSED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 2016@17 | i | READY | named gap - first use before any expansion on this page |
| P450 | 2020@17 | i | UI | named gap - first use before any expansion on this page |
| P450 | 2064@17 | i | PID | named gap - first use before any expansion on this page |
| P450 | 2070@17 | i | RESULT | named gap - first use before any expansion on this page |
| P450 | 2084@17 | i | FREE | named gap - first use before any expansion on this page |
| P450 | 2088@17 | i | APPLY | named gap - first use before any expansion on this page |
| P450 | 2089@17 | i | CURRENT | named gap - first use before any expansion on this page |
| P450 | 2092@17 | v | PASSED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 2102@18 | iv | `acquire_writer` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2103@18 | iv | `load_verified` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2104@18 | iv | `commit(expected_head, transaction)` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2105@18 | iv | `export_checkpoint` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2106@18 | iv | `read_verified` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2115@19 | iv | `control-plane/project.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 2116@19 | iv | `control-plane/work-items/*.json` | documented exclusion - PATH: backticked path identifier |
| P450 | 2118@19 | iv | `control-plane/policy/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2119@19 | iv | `tools/aegis_delivery_control/schemas/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2120@17 | i | HOME | named gap - first use before any expansion on this page |
| P450 | 2123@19 | iv | `${XDG_STATE_HOME:-$HOME/.local/state}/project-aegis/control-plane/<repo-id>/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2124@19 | iv | `%LOCALAPPDATA%/ProjectAegis/control-plane/<repo-id>/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2126@17 | v | <repo-id> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 2128@19 | iv | `raw-evidence/<run-id>/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2129@17 | v | <run-id> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 2131@19 | iv | `exports/<run-id>/<export-id>/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2132@17 | v | <export-id> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 2134@19 | iv | `docs/evidence/control-plane/checkpoints/<run-id>/<checkpoint-id>/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2135@17 | v | <checkpoint-id> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P450 | 2138@18 | iv | `.gitignore` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2139@19 | iv | `artifacts/recovery/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2140@19 | iv | `artifacts/reviews/` | documented exclusion - PATH: backticked path identifier |
| P450 | 2152@17 | i | ACL | named gap - first use before any expansion on this page |
| P450 | 2169@17 | i | UNC | named gap - first use before any expansion on this page |
| P450 | 2194@17 | iv | `e2145b1` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2198@17 | iv | `503c3b30` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2202@17 | iv | `dbe2ee28` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2204@17 | iv | `e2a3e20b` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2207@16 | v | L51-L52 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2211@18 | iv | `docs/roadmaps/aegis-ci-baseline-2026-10-11.md` | documented exclusion - PATH: backticked path identifier |
| P450 | 2219@16 | i | BKL | named gap - first use before any expansion on this page |
| P450 | 2226@17 | iv | `AEGIS-APR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 2227@17 | iv | `BER-DEC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 2232@17 | iv | `OD-1` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 2242@17 | v | `PENDING` | documented exclusion - STATUS: backticked status keyword |
| P450 | 2245@17 | v | `BLOCKED` | documented exclusion - STATUS: backticked status keyword |
| P450 | 2292@16 | v | REVISE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 2300@17 | iv | `56a8e603` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2304@16 | v | OWED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 2326@17 | iv | `BER-BKL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P450 | 2333@16 | i | OD | named gap - first use before any expansion on this page |
| P450 | 2341@16 | i | RLS | named gap - first use before any expansion on this page |
| P450 | 2346@18 | iv | `review/ber-phase01-corrections` | documented exclusion - PATH: backticked path identifier |
| P450 | 2347@17 | iv | `6bd5abadd16a3ab6cfd89cc15dfaa5572ac9dedd` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2348@17 | iv | `000352f55b71f0c3e897a482d279d34bfaa3d66b` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2362@17 | iv | `CoverageMetrics` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2391@16 | i | PM | named gap - first use before any expansion on this page |
| P450 | 2399@17 | iv | `docs-retention-index` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2402@17 | iv | `rls-policy-auditor` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2412@16 | v | REJECTED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P450 | 2419@17 | iv | `1c3e4931329179d9a3f9cc9ec1bb93020378c043` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P450 | 2441@16 | i | AEGIS | named gap - first use before any expansion on this page |
| P450 | 2472@1067 | v | L180 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1093 | v | L190 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1116 | v | L209 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1131 | v | L229 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1160 | v | L242 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1174 | v | L247 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1187 | v | L325 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1198 | v | L329 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1210 | v | L330 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1220 | v | L351 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1231 | v | L352 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1247 | v | L372 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1259 | v | L379 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1270 | v | L391 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1282 | v | L394 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1302 | v | L401 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1319 | v | L418 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1334 | v | L444 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1352 | v | L455 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1364 | v | L466 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1374 | v | L468 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1385 | v | L487 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1396 | v | L488 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1417 | v | L501 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1432 | v | L512 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1447 | v | L540 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1459 | v | L566 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1471 | v | L587 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1485 | v | L590 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1497 | v | L592 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1514 | v | L609 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1526 | v | L652 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1541 | v | L656 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1554 | v | L670 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1567 | v | L672 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1578 | v | L678 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1593 | v | L682 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1603 | v | L684 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1617 | v | L702 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1631 | v | L722 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1647 | v | L735 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1657 | v | L737 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1670 | v | L740 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1682 | v | L787 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1698 | v | L817 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1709 | v | L829 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1721 | v | L925 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1735 | v | L1094 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1751 | v | L1121 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1765 | v | L1131 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1775 | v | L1142 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2472@1792 | v | L1145 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1083 | v | L202 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1118 | v | L204 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1148 | v | L207 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1177 | v | L210 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1205 | v | L224 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1221 | v | L230 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1252 | v | L237 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1286 | v | L260 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1299 | v | L261 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1313 | v | L264 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1324 | v | L274 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1337 | v | L287 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1365 | v | L288 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2473@1378 | v | L310 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1063 | v | L125 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1093 | v | L126 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1125 | v | L129 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1166 | v | L132 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1233 | v | L136 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1305 | v | L149 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1428 | v | L156 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1473 | v | L159 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1499 | v | L164 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1559 | v | L172 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1576 | v | L176 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1617 | v | L182 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1640 | v | L184 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1656 | v | L185 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1697 | v | L192 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1712 | v | L193 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1727 | v | L194 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1755 | v | L199 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1809 | v | L201 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1827 | v | L203 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1843 | v | L205 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1909 | v | L212 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1936 | v | L214 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1951 | v | L215 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1980 | v | L217 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@1995 | v | L218 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2011 | v | L221 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2045 | v | L222 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2148 | v | L231 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2204 | v | L236 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2220 | v | L241 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2233 | v | L243 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2249 | v | L244 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2262 | v | L245 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2326 | v | L256 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2381 | v | L263 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2393 | v | L272 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2408 | v | L276 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2420 | v | L304 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2432 | v | L305 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2470 | v | L362 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2481 | v | L402 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2505 | v | L446 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2541 | v | L465 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2556 | v | L510 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2580 | v | L537 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2597 | v | L562 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2607 | v | L616 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2617 | v | L620 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2633 | v | L630 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2647 | v | L685 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2659 | v | L770 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2673 | v | L866 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2684 | v | L874 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2696 | v | L885 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2710 | v | L886 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2721 | v | L919 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2732 | v | L920 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2749 | v | L965 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2763 | v | L966 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2783 | v | L974 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2794 | v | L976 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2858 | v | L979 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2870 | v | L1021 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2884 | v | L1022 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2898 | v | L1062 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2911 | v | L1063 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2926 | v | L1066 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2940 | v | L1069 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2958 | v | L1133 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@2974 | v | L1169 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3032 | v | L1177 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3048 | v | L1292 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3061 | v | L1379 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3077 | v | L1483 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3090 | v | L1484 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3117 | v | L1501 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3129 | v | L1527 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3144 | v | L1534 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3157 | v | L1560 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3168 | v | L1649 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3183 | v | L1658 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3195 | v | L1710 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3212 | v | L1716 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3228 | v | L1807 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3240 | v | L1833 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3254 | v | L1834 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3267 | v | L1850 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3283 | v | L1895 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3296 | v | L1896 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3326 | v | L1897 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3340 | v | L1926 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3357 | v | L1971 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3370 | v | L2003 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3385 | v | L2006 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3398 | v | L2043 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3443 | v | L2109 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3459 | v | L2198 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3472 | v | L2535 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3485 | v | L2542 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3501 | v | L2775 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3516 | v | L2795 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2474@3529 | v | L3041 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2475@1063 | v | L284 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2475@1075 | v | L291 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2475@1084 | v | L296 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2475@1096 | v | L297 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2475@1111 | v | L299 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2475@1124 | v | L309 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2475@1149 | v | L314 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2475@1159 | v | L322 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1161 | v | L97 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1198 | v | L102 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1268 | v | L121 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1283 | v | L122 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1322 | v | L124 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1540 | v | L151 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1689 | v | L157 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1765 | v | L178 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1795 | v | L186 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1806 | v | L191 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1860 | v | L223 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1886 | v | L225 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1925 | v | L232 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@1948 | v | L246 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2001 | v | L268 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2043 | v | L286 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2054 | v | L290 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2072 | v | L294 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2117 | v | L318 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2132 | v | L337 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2144 | v | L341 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2157 | v | L355 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2171 | v | L360 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2186 | v | L364 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2200 | v | L392 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2214 | v | L393 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2241 | v | L395 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2271 | v | L396 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2280 | v | L405 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2308 | v | L430 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2325 | v | L440 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2338 | v | L441 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2352 | v | L442 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2362 | v | L450 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2376 | v | L452 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2387 | v | L457 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2399 | v | L542 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2413 | v | L560 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2426 | v | L569 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2450 | v | L625 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2466 | v | L635 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2482 | v | L651 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2493 | v | L756 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2512 | v | L758 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2536 | v | L760 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2547 | v | L761 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2557 | v | L762 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2583 | v | L824 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2593 | v | L855 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2603 | v | L872 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2614 | v | L876 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2627 | v | L883 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2643 | v | L884 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2663 | v | L890 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2680 | v | L901 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2690 | v | L923 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2476@2705 | v | L968 | documented exclusion - LINE-RANGE: page-line reference |
| P450 | 2488@2 | i | AC | named gap - first use before any expansion on this page |
| P450 | 2494@18 | i | PROC | named gap - first use before any expansion on this page |
| P450 | 2503@98 | iv | c6e5d5649bf8 | documented exclusion - SHA: commit/blob hash |
| P450 | 2504@94 | iv | b5fd9feda972 | documented exclusion - SHA: commit/blob hash |
| P450 | 2505@94 | iv | 08d91a834460 | documented exclusion - SHA: commit/blob hash |
| P450 | 2505@297 | iii | docs/evidence/documentation/readability-lane-c-batch-10-2026-10-18.md; | documented exclusion - PATH: non-backticked path identifier |
| P450 | 2506@78 | iv | 6a27b5c8e690 | documented exclusion - SHA: commit/blob hash |
| P450 | 2508@218 | iii | _A/evidence/read-lc-336-c5/Crows.txt | documented exclusion - PATH: non-backticked path identifier |
| P451 | 1@71 | v | 2026-10-18 | documented exclusion - DATE: date/time literal |
| P451 | 1@71 | v | 2026-10 | documented exclusion - DATE: date/time literal |
| P451 | 7@59 | v | 6253595591 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 7@95 | i | DELTA | named gap - first use before any expansion on this page |
| P451 | 7@101 | v | ACCEPT | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 7@108 | v | 6253608810 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 7@129 | iv | 55151039d1ea2bd146d4fb4287c8787820d7e951 | documented exclusion - SHA: commit/blob hash |
| P451 | 7@212 | v | 2026-10-18T18:18:57Z | documented exclusion - DATE: date/time literal |
| P451 | 7@308 | i | PR | named gap - first use before any expansion on this page |
| P451 | 7@368 | iii | docs/evidence/documentation/readability-lane-c-batch-11-2026-10-18.md**. | documented exclusion - PATH: non-backticked path identifier |
| P451 | 7@373 | ii | evidence | documented exclusion - PROSE: lowercase technical/audience prose |
| P451 | 7@396 | ii | readability | documented exclusion - PROSE: lowercase technical/audience prose |
| P451 | 7@421 | v | 11-2026 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 7@429 | v | 10-18 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 9@57 | v | 144-279 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 9@83 | v | 1-10 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 9@104 | v | 304-343 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 9@145 | v | 344-351 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 9@194 | v | 352-359 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 9@241 | v | 55151039 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 9@261 | iv | 9085bf6a | documented exclusion - SHA: commit/blob hash |
| P451 | 9@281 | iv | 9a5cb28d | documented exclusion - SHA: commit/blob hash |
| P451 | 9@301 | iv | e3f535e4 | documented exclusion - SHA: commit/blob hash |
| P451 | 9@321 | iv | 3ef6c735 | documented exclusion - SHA: commit/blob hash |
| P451 | 9@341 | iv | 6afc845a | documented exclusion - SHA: commit/blob hash |
| P451 | 9@361 | iv | 4b99f69f | documented exclusion - SHA: commit/blob hash |
| P451 | 9@381 | iv | 2c3c6ffe | documented exclusion - SHA: commit/blob hash |
| P451 | 9@401 | v | 38212595 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 9@421 | iv | f325daac | documented exclusion - SHA: commit/blob hash |
| P451 | 9@441 | iv | 7cea211e | documented exclusion - SHA: commit/blob hash |
| P451 | 9@461 | iv | 6f584c9d | documented exclusion - SHA: commit/blob hash |
| P451 | 11@251 | v | 0-152 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 11@265 | v | 153-305 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 11@292 | v | 306-458 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 11@308 | v | 459-610 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 11@418 | iv | 2db1ffb7 | documented exclusion - SHA: commit/blob hash |
| P451 | 13@188 | ii | inventory | documented exclusion - PROSE: lowercase technical/audience prose |
| P451 | 13@253 | v | L154 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 13@258 | v | L155 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 13@263 | v | L156 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 13@386 | v | 6250828860 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 13@442 | v | L212 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 13@467 | v | L35 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 13@503 | v | L36-L38 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 17@45 | i | LF | named gap - first use before any expansion on this page |
| P451 | 19@13 | iii | docs/evidence/behavioral-eval-runner-phase01-independent-corrections.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 19@87 | iv | daa32aeca8cfd93e02fe965ef05bd3c9e380fe9f | documented exclusion - SHA: commit/blob hash |
| P451 | 20@13 | iii | docs/evidence/behavioral-eval-runner-phase01-review.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 20@70 | iv | fbaf95168510754c101e53e3ffe3ae427cf93db4 | documented exclusion - SHA: commit/blob hash |
| P451 | 21@13 | iii | docs/evidence/behavioral-eval-runner-wp-2b-0-summary.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 21@71 | iv | a9eee439bd59dd0bec5bf1e32df81f9ddb19b7f1 | documented exclusion - SHA: commit/blob hash |
| P451 | 22@13 | iii | docs/evidence/behavioral-eval-runner-wp-2b-1-summary.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 22@71 | iv | 0f8e9e0ae3aa80f3a0277d46ee65e826961530ff | documented exclusion - SHA: commit/blob hash |
| P451 | 23@13 | iii | docs/evidence/behavioral-eval-runner-wp-2b-2-summary.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 23@71 | iv | 5b10ad947e5a9cb0bac4bd6e0a1c8de27fe1726a | documented exclusion - SHA: commit/blob hash |
| P451 | 24@13 | iii | docs/evidence/behavioral-eval-runner-wp-2b-3-summary.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 24@71 | iv | 9846025dfbce1f1e72854490d8eca1be727d23cb | documented exclusion - SHA: commit/blob hash |
| P451 | 25@13 | iii | docs/evidence/ber-bkl-007-schema-integrity.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 25@61 | iv | e72003f7fba0997be19e66b77518ecb6aa5dc5ae | documented exclusion - SHA: commit/blob hash |
| P451 | 26@13 | iii | docs/evidence/ber-bkl-009-policy-integration-review.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 26@70 | iv | 25f5f75537849ff1e4c71080ec46ff760cb32a53 | documented exclusion - SHA: commit/blob hash |
| P451 | 31@38 | v | L2841-2862 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 31@227 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 31@250 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 34@16 | v | L1-113 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 34@200 | i | BER | named gap - first use before any expansion on this page |
| P451 | 34@211 | ii | candidate | documented exclusion - PROSE: lowercase technical/audience prose |
| P451 | 35@66 | iv | `BER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@68 | v | L4 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@74 | v | L5 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@76 | iv | `PR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@80 | v | L6 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@85 | iv | `README` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@92 | v | L12 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@98 | iv | `md` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P451 | 35@99 | v | L15 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@107 | iv | `SDK` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@113 | v | L22 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@118 | iv | `OD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@127 | v | L58 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@128 | iv | `WP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@134 | v | L61 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@138 | iv | `PR87` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@141 | v | L71 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@148 | v | L78 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@150 | iv | `PR88` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@155 | v | L86 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@162 | iv | `RED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@162 | v | L113 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 35@173 | iv | `GREEN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@186 | iv | `HTTP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@198 | iv | `POSIX` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 35@211 | iv | `stderr` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P451 | 35@225 | v | `DONE` | documented exclusion - STATUS: backticked status keyword |
| P451 | 35@238 | v | `OPEN` | documented exclusion - STATUS: backticked status keyword |
| P451 | 40@11 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 44@16 | v | L1-186 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@68 | v | L1 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@86 | v | L10 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@100 | v | L37 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@107 | v | L38 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@114 | v | L49 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@129 | iv | `CI` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@135 | v | L53 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@139 | iv | `OS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@142 | v | L55 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@156 | v | L66 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@162 | iv | `https` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P451 | 45@170 | v | L67 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@175 | iv | `METADATA_OK` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@184 | v | L68 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@191 | v | L69 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@194 | iv | `CAP_WOULD_BE_EXCEEDED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@198 | v | L98 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@205 | v | L99 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@212 | v | L103 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@220 | v | L107 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@223 | iv | `RUN_STOPPED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@228 | v | L110 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@242 | iv | `AUTHORIZED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@244 | v | L112 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@260 | v | L135 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@268 | v | L162 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@272 | iv | `F27` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@276 | v | L164 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@283 | iv | `SHOULD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@292 | v | L165 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 45@297 | iv | `F19` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@308 | iv | `F23` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@319 | iv | `OWNER_WAIT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@337 | iv | `USD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@348 | iv | `ACL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@371 | iv | `TLS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@383 | iv | `api` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P451 | 45@395 | iv | `MAM` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@407 | iv | `ZDR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@419 | iv | `SYSTEM` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@434 | iv | `python` | documented exclusion - COMMAND: backticked command/CLI token |
| P451 | 45@449 | iv | `TEMP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@462 | iv | `TMP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@474 | iv | `GID` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 45@486 | iv | `UID` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 54@16 | v | L1-215 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 54@174 | i | WP | named gap - first use before any expansion on this page |
| P451 | 55@74 | v | L3 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@85 | iv | `R1` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@94 | iv | `R5` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@110 | v | L7 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@112 | iv | `R2` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@116 | v | L9 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@121 | iv | `R3` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@130 | iv | `R4` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@135 | v | L11 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@139 | iv | `DEC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@142 | v | L13 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@149 | v | L23 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@156 | v | L26 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@168 | iv | `SHA` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@191 | v | L27 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@211 | iv | `LIMITED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@226 | iv | `OUTCOME` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@226 | v | L28 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@241 | iv | `OWNER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@254 | iv | `SCOPE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@267 | iv | `UTC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@268 | v | L29 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@278 | iv | `EVIDENCE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@294 | iv | `ID` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@296 | v | L33 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@303 | v | L84 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@304 | iv | `INCOMPLETE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@318 | v | L111 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@322 | iv | `STATE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@326 | v | L121 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@334 | v | L127 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@335 | v | `UNAVAILABLE` | documented exclusion - STATUS: backticked status keyword |
| P451 | 55@342 | v | L144 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@350 | v | L145 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@354 | iv | `BEHAVIORAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@358 | v | L146 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@366 | v | L148 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@372 | iv | `BY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@382 | iv | `EXECUTION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@382 | v | L182 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@390 | v | L201 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 55@399 | iv | `LIVE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@421 | iv | `STILL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@434 | iv | `GOVERNANCE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@452 | iv | `NEXT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@476 | iv | `STEP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@488 | iv | `config` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P451 | 55@502 | iv | `SAME` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@514 | v | `PASSED` | documented exclusion - STATUS: backticked status keyword |
| P451 | 55@529 | iv | `shell` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P451 | 55@543 | iv | `RESERVED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@572 | iv | `D3` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@583 | iv | `MCP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@595 | iv | `CLAUDE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@610 | iv | `PROCEDURAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@629 | iv | `SEQUENCING` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@648 | iv | `AGENTS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 55@663 | iv | `MATCHED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 64@16 | v | L1-526 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@92 | v | L8 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@104 | v | L32 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@113 | iv | `id` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P451 | 65@122 | v | `MERGED` | documented exclusion - STATUS: backticked status keyword |
| P451 | 65@125 | v | L48 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@139 | v | L54 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@146 | v | L70 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@160 | v | L77 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@171 | iv | `JSON` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@175 | v | L106 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@183 | iv | `S25` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@206 | iv | `NON` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@231 | iv | `AI` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@231 | v | L161 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@263 | v | L172 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@287 | v | L198 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@311 | v | L208 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@319 | iv | `DCO` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@319 | v | L217 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@331 | iv | `WSL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@335 | v | L224 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@343 | iv | `BUT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@343 | v | L225 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@351 | v | L226 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@355 | iv | `IMPLEMENTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@359 | v | L227 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@367 | v | L229 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@375 | iv | `IMPLEMENTED_BUT_UNRUN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@375 | v | L231 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@383 | v | L271 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@391 | v | L299 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@399 | v | L305 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@405 | iv | `AST` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@407 | v | L309 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@415 | v | L312 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@417 | iv | `PRE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@423 | v | L324 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@431 | v | L328 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@439 | v | L333 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@454 | iv | `MANUAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@455 | v | L338 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@463 | v | L353 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@469 | iv | `PROPOSED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@471 | v | L354 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@479 | v | L357 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@486 | iv | `STANDARD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@487 | v | L362 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@495 | v | L366 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@503 | v | L369 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@511 | v | L376 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@514 | iv | `API` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@519 | v | L377 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@527 | v | L378 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@535 | v | L380 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@543 | v | L389 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@551 | v | L399 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@559 | v | L403 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@567 | v | L404 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@575 | v | L405 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@583 | v | L410 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@591 | v | L421 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@599 | v | L424 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@606 | iv | `RECOMPUTES` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@615 | v | L425 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@623 | v | L437 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@625 | iv | `PATH` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@631 | v | L450 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@638 | iv | `HKLM` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@639 | v | L475 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@647 | v | L480 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@651 | iv | `P1` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@655 | v | L481 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@662 | iv | `CONFIRMED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@663 | v | L499 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 65@680 | v | `UNVERIFIED` | documented exclusion - STATUS: backticked status keyword |
| P451 | 65@699 | iv | `ABSOLUTE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@716 | iv | `PARTIALLY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@734 | iv | `TOCTOU` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@749 | iv | `PARENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@764 | iv | `TIGHTENED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@782 | iv | `FULL_LIBRARY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@803 | iv | `EXACTLY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@819 | iv | `TOTAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@833 | iv | `BINDABLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@850 | iv | `CORRECTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@868 | iv | `DETECTS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@884 | iv | `PREVENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@900 | iv | `BASELINE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@917 | iv | `CREATION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@934 | iv | `TYPES` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@948 | iv | `NON_BASELINE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@969 | iv | `ONCE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@982 | iv | `AREA` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@995 | iv | `PREVENTS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@1012 | iv | `OUR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@1024 | iv | `REQUIRES` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@1041 | iv | `LEADER_COMPLETED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@1066 | iv | `TIMEOUT_KILLED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@1089 | iv | `NOT_ATTEMPTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@1111 | iv | `BKL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@1123 | iv | `FFI` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 65@1135 | iv | `stdout` | documented exclusion - LITERAL: backticked literal/prose identifier |
| P451 | 66@79 | iii | tests/outcomes | documented exclusion - PATH: non-backticked path identifier |
| P451 | 74@16 | v | L1-456 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@94 | iv | `D9` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@138 | v | L19 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@154 | iv | `ZERO` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@173 | v | L43 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@187 | v | L50 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@201 | v | L51 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@222 | v | L52 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@257 | v | L56 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@270 | iv | `SS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@278 | v | L57 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@280 | iv | `EVIDENCE_MALFORMED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@313 | v | L64 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@316 | iv | `LF` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@326 | iv | `STEP_00` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@341 | iv | `STEP_08` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@356 | iv | `CONTROL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@371 | iv | `SCOPED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@385 | iv | `PS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@406 | iv | `CR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@416 | iv | `CRLF` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@420 | v | L116 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@428 | iv | `AMBIGUOUS_ACTIVATION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@444 | v | L117 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@452 | v | L118 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@456 | iv | `COMPOSITE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@468 | v | L132 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@473 | v | `PENDING` | documented exclusion - STATUS: backticked status keyword |
| P451 | 75@476 | v | L136 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@484 | v | L137 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@488 | iv | `SEMANTIC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@492 | v | L150 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@504 | iv | `SEMANTIC_PENDING` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@508 | v | L178 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@524 | v | L235 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@528 | iv | `DATA` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@540 | v | L239 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@548 | v | L251 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@552 | v | `CLOSED` | documented exclusion - STATUS: backticked status keyword |
| P451 | 75@556 | v | L255 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@564 | v | L264 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@566 | iv | `COHERENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@572 | v | L266 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@580 | v | L283 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@582 | iv | `DISCOVERY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@588 | v | L300 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@596 | v | L307 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@612 | v | L311 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@614 | iv | `ONE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@625 | iv | `PER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@628 | v | L321 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@636 | iv | `TOPIC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@636 | v | L344 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@644 | v | L364 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 75@649 | iv | `TURN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@661 | iv | `RATIFIED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@677 | iv | `ROLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@689 | iv | `SYNTHETIC_MOCK` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@711 | iv | `DETERMINISTIC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@733 | iv | `SCAFFOLDED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@752 | iv | `EVIDENCE_UNAVAILABLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@801 | iv | `UNJUDGEABLE_AS_WRITTEN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@832 | iv | `OUT_OF_SCOPE_FOR_WP2B2` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@922 | iv | `CLI` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@958 | iv | `UTF` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@970 | iv | `HOLDOUT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@986 | iv | `TRAIN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@1000 | iv | `PR85` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@1013 | iv | `SEPARATELY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@1032 | iv | `BOTH` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@1045 | iv | `TRUSTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@1061 | iv | `PENDING_OWNER_DECISION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@1092 | iv | `ABSTAIN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@1108 | iv | `WITHHELD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 75@1219 | v | `APPROVED` | documented exclusion - STATUS: backticked status keyword |
| P451 | 84@16 | v | L1-674 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 84@199 | i | SDK | named gap - first use before any expansion on this page |
| P451 | 85@67 | iv | `A1` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@76 | iv | `A2` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@131 | v | L18 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@145 | v | L21 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@166 | iv | `OFFLINE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@187 | v | L24 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@191 | iv | `CANDIDATE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@194 | v | L25 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@215 | v | L39 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@218 | iv | `PREFLIGHT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@222 | v | L40 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@229 | v | L44 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@235 | iv | `SYNTHETIC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@252 | iv | `DEVELOPMENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@310 | iv | `OWNER_LABEL_APPROVAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@374 | iv | `DRAFT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@398 | iv | `URL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@409 | iv | `STOP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@418 | v | L59 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@425 | v | L60 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@442 | iv | `BPE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@446 | v | L62 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@467 | v | `COMPLETE` | documented exclusion - STATUS: backticked status keyword |
| P451 | 85@481 | v | L100 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@483 | iv | `FORBIDDEN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@522 | iv | `PROVEN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@545 | v | L123 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@547 | iv | `ACTIVE_SEGMENT_BEGIN` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@561 | v | L151 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@575 | iv | `ATTEMPT_TERMINAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@577 | v | L163 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@585 | v | L168 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@599 | iv | `END` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@601 | v | L175 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@609 | v | L196 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@610 | iv | `EVENT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@617 | v | L219 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@623 | iv | `FILE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@625 | v | L221 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@633 | v | L234 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@635 | iv | `GENESIS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@641 | v | L237 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@650 | iv | `OPENED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@657 | v | L259 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@664 | iv | `REOPENS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@665 | v | L278 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@673 | v | L284 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@679 | iv | `SEMANTIC_OUTCOME` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@703 | iv | `SINGLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@705 | v | L323 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@717 | iv | `SOURCED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@732 | iv | `STARTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@745 | v | L330 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@747 | iv | `STOPS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@753 | v | L331 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@761 | v | L367 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@775 | iv | `EXACT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@801 | v | L379 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@815 | iv | `DURABLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@817 | v | L422 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@825 | v | L427 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@841 | v | L474 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@849 | v | L478 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@856 | iv | `OUTPUT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@857 | v | L489 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@865 | v | L504 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@870 | iv | `VALIDATED_PASS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@873 | v | L525 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@881 | v | L578 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@892 | iv | `EXTERNAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@897 | v | L594 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@905 | v | L603 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@909 | iv | `CHANGES` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@913 | v | L621 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@921 | v | L633 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@937 | iv | `REQUIRED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@945 | v | L666 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 85@954 | iv | `V1` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@965 | iv | `PROMPT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@980 | iv | `PROMPT_INJECTION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1005 | iv | `ROLE_CONFUSION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1028 | iv | `MD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1039 | iv | `V2` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1050 | iv | `ACTUAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1065 | iv | `ZIP` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1077 | iv | `ORIGINAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1145 | iv | `TWO` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1174 | iv | `RECORDED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1191 | iv | `REPORTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1208 | iv | `REPLACED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1225 | iv | `REQUEST` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1241 | iv | `ANY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1253 | iv | `REJECTS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1269 | iv | `BLOCKER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1285 | iv | `BLOCKERS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1302 | iv | `SOUND` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1316 | iv | `F4` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1327 | iv | `NAMED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1341 | iv | `PRECONDITION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1362 | iv | `STAGE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1376 | iv | `F1` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1387 | iv | `F2` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1398 | iv | `F3` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1409 | iv | `BRAND` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1423 | iv | `CALIBRATION` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1460 | iv | `INTERNAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1477 | iv | `TECHNICAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1522 | iv | `IMMUTABLE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1540 | iv | `BLOCKED_PENDING_OWNER_WAIT_FREEZE` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1582 | iv | `NOT_STARTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1602 | iv | `DUMMY` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1616 | iv | `THIRD` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1643 | iv | `PRECONDITIONS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1665 | iv | `OWNER_APPROVAL_PENDING` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1714 | iv | `PROVIDER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1731 | iv | `SPECIFIC` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1748 | iv | `REAL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1761 | iv | `COUNT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1775 | iv | `INPUT` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1789 | iv | `REASONING` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1821 | iv | `MISMATCH` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 85@1838 | iv | `MODEL` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 86@83 | iii | tests/accounting/boundaries. | documented exclusion - PATH: non-backticked path identifier |
| P451 | 94@16 | v | L1-86 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 95@122 | v | L14 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 95@129 | v | L16 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 95@135 | iv | `YAML` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 95@157 | v | L83 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 95@191 | iv | `OWNER_ACCEPTED` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 95@226 | iv | `AEGIS` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 95@239 | iv | `APR` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 104@16 | v | L1-73 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 105@118 | iv | `APPROVAL_REGISTER` | documented exclusion - EMPHASIS: backticked uppercase emphasis |
| P451 | 105@127 | v | L20 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 105@141 | v | L45 | documented exclusion - LINE-RANGE: page-line reference |
| P451 | 112@39 | ii | token | documented exclusion - PROSE: lowercase technical/audience prose |
| P451 | 112@57 | i | ONE | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 114@20 | i | REAL | named gap - first use before any expansion on this page |
| P451 | 114@219 | i | DOTALL | named gap - first use before any expansion on this page |
| P451 | 120@15 | i | README | named gap - first use before any expansion on this page |
| P451 | 121@35 | v | 2026-09-12 | documented exclusion - DATE: date/time literal |
| P451 | 121@35 | v | 2026-09 | documented exclusion - DATE: date/time literal |
| P451 | 131@16 | i | OD | named gap - first use before any expansion on this page |
| P451 | 134@17 | iv | 40bfabc91b60d46f201a575911d0f2a9edac2a2e | documented exclusion - SHA: commit/blob hash |
| P451 | 135@17 | iv | a9e12ad61aafb0434bf36e256553fdf634c58053 | documented exclusion - SHA: commit/blob hash |
| P451 | 144@16 | v | <sdk-python> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P451 | 146@16 | i | RED | named gap - first use before any expansion on this page |
| P451 | 149@16 | i | GREEN | named gap - first use before any expansion on this page |
| P451 | 157@16 | i | HTTP | named gap - first use before any expansion on this page |
| P451 | 158@16 | i | POSIX | named gap - first use before any expansion on this page |
| P451 | 161@17 | iv | c6822e1c3fd0dd2b8195c3909c1cf57faeab6607 | documented exclusion - SHA: commit/blob hash |
| P451 | 167@17 | v | BLOCKED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 168@17 | v | DONE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 169@17 | v | OPEN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 179@17 | iv | ac9e1cdb020f4efb7a52e5ea606c3b329fb486e2 | documented exclusion - SHA: commit/blob hash |
| P451 | 180@17 | iv | 1c3e4931329179d9a3f9cc9ec1bb93020378c043 | documented exclusion - SHA: commit/blob hash |
| P451 | 186@16 | i | CI | named gap - first use before any expansion on this page |
| P451 | 190@18 | iii | tools/behavioral_eval_runner/tests | documented exclusion - PATH: non-backticked path identifier |
| P451 | 191@18 | iii | tools/behavioral_eval_runner/tests/ | documented exclusion - PATH: non-backticked path identifier |
| P451 | 192@18 | iii | tools/behavioral_eval_runner/tests/test_calibration_phase01.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 195@16 | i | OS | named gap - first use before any expansion on this page |
| P451 | 212@16 | i | SHOULD | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 219@16 | v | → | documented exclusion - OPERATOR: operator glyph |
| P451 | 221@18 | iii | tools/behavioral_eval_runner/judge/ | documented exclusion - PATH: non-backticked path identifier |
| P451 | 237@16 | v | CRITICAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 238@16 | v | FAIL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 244@143 | v | PASS | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 253@16 | i | USD | named gap - first use before any expansion on this page |
| P451 | 258@17 | i | ACL | named gap - first use before any expansion on this page |
| P451 | 263@17 | i | TLS | named gap - first use before any expansion on this page |
| P451 | 264@18 | ii | api | documented exclusion - PROSE: lowercase technical/audience prose |
| P451 | 267@17 | i | MAM | named gap - first use before any expansion on this page |
| P451 | 268@17 | i | ZDR | named gap - first use before any expansion on this page |
| P451 | 277@17 | i | SYSTEM | named gap - first use before any expansion on this page |
| P451 | 284@17 | i | TEMP | named gap - first use before any expansion on this page |
| P451 | 286@17 | i | TMP | named gap - first use before any expansion on this page |
| P451 | 287@17 | i | GID | named gap - first use before any expansion on this page |
| P451 | 288@17 | i | UID | named gap - first use before any expansion on this page |
| P451 | 294@39 | ii | json | documented exclusion - PROSE: lowercase technical/audience prose |
| P451 | 309@15 | i | DEC | named gap - first use before any expansion on this page |
| P451 | 312@16 | i | SHA | named gap - first use before any expansion on this page |
| P451 | 317@16 | v | ACCEPTED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 318@16 | i | LIMITED | named gap - first use before any expansion on this page |
| P451 | 319@16 | i | OUTCOME | named gap - first use before any expansion on this page |
| P451 | 320@16 | i | OWNER | named gap - first use before any expansion on this page |
| P451 | 321@16 | i | SCOPE | named gap - first use before any expansion on this page |
| P451 | 322@16 | i | UTC | named gap - first use before any expansion on this page |
| P451 | 324@16 | i | EVIDENCE | named gap - first use before any expansion on this page |
| P451 | 325@16 | i | ID | named gap - first use before any expansion on this page |
| P451 | 330@16 | i | STATE | named gap - first use before any expansion on this page |
| P451 | 331@16 | v | UNAVAILABLE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 333@16 | v | UNKNOWN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 335@16 | i | BY | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 337@16 | i | LIVE | named gap - first use before any expansion on this page |
| P451 | 338@16 | i | ON | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 340@16 | i | STILL | named gap - first use before any expansion on this page |
| P451 | 342@16 | i | NEXT | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 344@16 | i | STEP | named gap - first use before any expansion on this page |
| P451 | 351@18 | iii | docs/roadmaps/behavioral-eval-runner-backlog.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 352@17 | iv | 11f45f2b3fe4774f519a4153767587532e027e79 | documented exclusion - SHA: commit/blob hash |
| P451 | 353@17 | iv | 882c0b6c8d5eb906df9e7d9d8576937b4c545db7 | documented exclusion - SHA: commit/blob hash |
| P451 | 354@17 | iv | 3fc5230c24fcaf8cb8b77e016ea9acd41b013086 | documented exclusion - SHA: commit/blob hash |
| P451 | 357@16 | i | SAME | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 358@17 | iv | a6c7159739222495a108120e3375f82f191317f9 | documented exclusion - SHA: commit/blob hash |
| P451 | 359@16 | i | MATCH | named gap - first use before any expansion on this page |
| P451 | 361@17 | v | PASSED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 364@17 | i | NTFS | named gap - first use before any expansion on this page |
| P451 | 368@17 | i | RESERVED | named gap - first use before any expansion on this page |
| P451 | 375@17 | i | ERROR | named gap - first use before any expansion on this page |
| P451 | 379@17 | i | MCP | named gap - first use before any expansion on this page |
| P451 | 381@17 | i | CLAUDE | named gap - first use before any expansion on this page |
| P451 | 395@17 | i | AGENTS | named gap - first use before any expansion on this page |
| P451 | 410@17 | i | MATCHED | named gap - first use before any expansion on this page |
| P451 | 425@16 | v | MERGED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 428@17 | iv | fc98ee6 | documented exclusion - SHA: commit/blob hash |
| P451 | 429@17 | iv | fc98ee6bf59bb516064be62ed8c5dc8861c92697 | documented exclusion - SHA: commit/blob hash |
| P451 | 430@17 | iv | def17d77fa2cd9c854bd4b16687f0b0350ebdefe | documented exclusion - SHA: commit/blob hash |
| P451 | 432@18 | iii | docs/design/behavioral-eval-runner-v1.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 435@18 | iii | tools/behavioral_eval_runner/ | documented exclusion - PATH: non-backticked path identifier |
| P451 | 438@16 | v | ⇒ | documented exclusion - OPERATOR: operator glyph |
| P451 | 439@16 | i | JSON | named gap - first use before any expansion on this page |
| P451 | 465@16 | i | NON | named gap - first use before any expansion on this page |
| P451 | 467@16 | i | CLI | named gap - first use before any expansion on this page |
| P451 | 475@18 | iii | tools/behavioral_eval_runner/** | documented exclusion - PATH: non-backticked path identifier |
| P451 | 488@17 | i | AI | named gap - first use before any expansion on this page |
| P451 | 515@17 | i | DCO | named gap - first use before any expansion on this page |
| P451 | 518@17 | v | OK | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 520@17 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 521@17 | i | WSL | named gap - first use before any expansion on this page |
| P451 | 527@17 | i | BUT | named gap - first use before any expansion on this page |
| P451 | 533@17 | i | AST | named gap - first use before any expansion on this page |
| P451 | 537@18 | iv | 28747cc1 | documented exclusion - SHA: commit/blob hash |
| P451 | 538@18 | iv | 58bd6f7 | documented exclusion - SHA: commit/blob hash |
| P451 | 539@17 | i | PRE | named gap - first use before any expansion on this page |
| P451 | 543@18 | iv | 674017e9 | documented exclusion - SHA: commit/blob hash |
| P451 | 544@26 | iii | scripts/tests/test_validator.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 545@26 | iii | scripts/validate-skills.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 553@17 | i | MANUAL | named gap - first use before any expansion on this page |
| P451 | 555@17 | v | HIGH | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 556@17 | i | PROPOSED | named gap - first use before any expansion on this page |
| P451 | 557@17 | i | STANDARD | named gap - first use before any expansion on this page |
| P451 | 560@17 | i | API | named gap - first use before any expansion on this page |
| P451 | 586@17 | v | ± | documented exclusion - OPERATOR: operator glyph |
| P451 | 592@19 | i | SKILL | named gap - first use before any expansion on this page |
| P451 | 601@17 | i | PATH | named gap - first use before any expansion on this page |
| P451 | 603@18 | iv | bd63d0a6 | documented exclusion - SHA: commit/blob hash |
| P451 | 605@17 | i | HKLM | named gap - first use before any expansion on this page |
| P451 | 609@19 | iii | tests/test_review_blockers.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 621@17 | v | ↔ | documented exclusion - OPERATOR: operator glyph |
| P451 | 622@17 | v | ⇔ | documented exclusion - OPERATOR: operator glyph |
| P451 | 624@17 | v | VERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 628@17 | i | ABSOLUTE | named gap - first use before any expansion on this page |
| P451 | 634@17 | i | TOCTOU | named gap - first use before any expansion on this page |
| P451 | 639@17 | i | PARENT | named gap - first use before any expansion on this page |
| P451 | 642@18 | iv | 4b3673d | documented exclusion - SHA: commit/blob hash |
| P451 | 649@17 | i | EXACTLY | named gap - first use before any expansion on this page |
| P451 | 651@17 | i | TOTAL | named gap - first use before any expansion on this page |
| P451 | 655@17 | i | BINDABLE | named gap - first use before any expansion on this page |
| P451 | 660@17 | i | DETECTS | named gap - first use before any expansion on this page |
| P451 | 661@17 | i | PREVENT | named gap - first use before any expansion on this page |
| P451 | 663@17 | i | BASELINE | named gap - first use before any expansion on this page |
| P451 | 665@17 | i | CREATION | named gap - first use before any expansion on this page |
| P451 | 671@17 | i | TYPES | named gap - first use before any expansion on this page |
| P451 | 675@18 | iv | 2d5c582 | documented exclusion - SHA: commit/blob hash |
| P451 | 679@17 | i | ONCE | named gap - first use before any expansion on this page |
| P451 | 680@17 | i | AREA | named gap - first use before any expansion on this page |
| P451 | 682@17 | i | PREVENTS | named gap - first use before any expansion on this page |
| P451 | 690@17 | i | OUR | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 700@17 | i | REQUIRES | named gap - first use before any expansion on this page |
| P451 | 713@17 | i | BKL | named gap - first use before any expansion on this page |
| P451 | 714@17 | i | FFI | named gap - first use before any expansion on this page |
| P451 | 716@22 | ii | workflow | documented exclusion - PROSE: lowercase technical/audience prose |
| P451 | 728@18 | iv | 72e74af6f0183fef25e353ec2bf3a851d83b5df6 | documented exclusion - SHA: commit/blob hash |
| P451 | 730@19 | iii | docs/design/behavioral-eval-runner-v1-fast-track-successor.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 744@16 | i | ZERO | named gap - first use before any expansion on this page |
| P451 | 755@17 | iv | 1145cb75d79bc6ab13876438527235c93320278b | documented exclusion - SHA: commit/blob hash |
| P451 | 757@17 | iv | 47a013fe4de3820f828887dc857dc441edc50272 | documented exclusion - SHA: commit/blob hash |
| P451 | 765@18 | iii | tools/behavioral_eval_runner/graders/ | documented exclusion - PATH: non-backticked path identifier |
| P451 | 774@16 | i | SS | named gap - first use before any expansion on this page |
| P451 | 791@16 | i | CONTROL | named gap - first use before any expansion on this page |
| P451 | 792@16 | i | SCOPED | named gap - first use before any expansion on this page |
| P451 | 796@16 | i | PS | named gap - first use before any expansion on this page |
| P451 | 800@16 | i | CR | named gap - first use before any expansion on this page |
| P451 | 801@16 | i | CRLF | named gap - first use before any expansion on this page |
| P451 | 812@22 | v | H | documented exclusion - PLACEHOLDER: placeholder letter token |
| P451 | 815@18 | v | P | documented exclusion - PLACEHOLDER: placeholder letter token |
| P451 | 816@16 | v | PENDING | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 817@16 | i | SEMANTIC | named gap - first use before any expansion on this page |
| P451 | 822@16 | i | DATA | named gap - first use before any expansion on this page |
| P451 | 838@16 | v | CLOSED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 839@16 | i | COHERENT | named gap - first use before any expansion on this page |
| P451 | 843@16 | i | PER | named gap - first use before any expansion on this page |
| P451 | 844@16 | i | TOPIC | named gap - first use before any expansion on this page |
| P451 | 845@16 | i | TURN | named gap - first use before any expansion on this page |
| P451 | 856@16 | i | RATIFIED | named gap - first use before any expansion on this page |
| P451 | 857@16 | i | ROLE | named gap - first use before any expansion on this page |
| P451 | 863@18 | iii | tools/behavioral_eval_runner/schemas/ | documented exclusion - PATH: non-backticked path identifier |
| P451 | 872@18 | iii | tools/behavioral_eval_runner/fixtures/scenario_a/ | documented exclusion - PATH: non-backticked path identifier |
| P451 | 882@18 | iii | tools/behavioral_eval_runner/__init__.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 885@18 | iii | tools/behavioral_eval_runner/cli.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 892@18 | iii | tools/behavioral_eval_runner/README.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 910@23 | v | M | documented exclusion - PLACEHOLDER: placeholder letter token |
| P451 | 963@17 | i | UTF | named gap - first use before any expansion on this page |
| P451 | 966@17 | i | HOLDOUT | named gap - first use before any expansion on this page |
| P451 | 967@17 | i | TRAIN | named gap - first use before any expansion on this page |
| P451 | 970@18 | iv | f3f82ece | documented exclusion - SHA: commit/blob hash |
| P451 | 971@19 | iii | tests/test_r2_trust_binding.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 979@17 | i | BOTH | named gap - first use before any expansion on this page |
| P451 | 984@17 | i | TRUSTED | named gap - first use before any expansion on this page |
| P451 | 997@17 | i | ABSTAIN | named gap - first use before any expansion on this page |
| P451 | 1000@17 | i | WITHHELD | named gap - first use before any expansion on this page |
| P451 | 1019@18 | iv | 5d16bace | documented exclusion - SHA: commit/blob hash |
| P451 | 1020@18 | iv | 5d16bace5fec9f7c394ad7f3b4147ac9d4ad74f2 | documented exclusion - SHA: commit/blob hash |
| P451 | 1021@18 | iv | 81404d350a26e8349d3c869209ae04f8628e0a95 | documented exclusion - SHA: commit/blob hash |
| P451 | 1022@18 | iv | b84e43ad9f42a793c6f68c2f5aebf0abfad2b8ed | documented exclusion - SHA: commit/blob hash |
| P451 | 1024@17 | v | APPROVED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 1028@19 | iii | docs/roadmaps/behavioral-eval-runner-wp-2b-3-authorization-decision-package.md | documented exclusion - PATH: non-backticked path identifier |
| P451 | 1044@31 | v | 2026-09-11 | documented exclusion - DATE: date/time literal |
| P451 | 1048@16 | i | OFFLINE | named gap - first use before any expansion on this page |
| P451 | 1073@17 | iv | feb7cf261d8efa624c18363c9928e7f0cbdfed4c | documented exclusion - SHA: commit/blob hash |
| P451 | 1076@16 | i | DRAFT | named gap - first use before any expansion on this page |
| P451 | 1085@16 | i | URL | named gap - first use before any expansion on this page |
| P451 | 1089@16 | i | STOP | named gap - first use before any expansion on this page |
| P451 | 1097@16 | i | BPE | named gap - first use before any expansion on this page |
| P451 | 1099@16 | v | COMPLETE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 1103@16 | i | PROVEN | named gap - first use before any expansion on this page |
| P451 | 1109@25 | v | 2026-04-23 | documented exclusion - DATE: date/time literal |
| P451 | 1109@30 | v | 04-23 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 1125@16 | i | END | named gap - first use before any expansion on this page |
| P451 | 1126@16 | i | EVENT | named gap - first use before any expansion on this page |
| P451 | 1127@16 | i | FILE | named gap - first use before any expansion on this page |
| P451 | 1128@16 | i | GENESIS | named gap - first use before any expansion on this page |
| P451 | 1129@16 | i | OPENED | named gap - first use before any expansion on this page |
| P451 | 1131@16 | i | REOPENS | named gap - first use before any expansion on this page |
| P451 | 1134@16 | i | SINGLE | named gap - first use before any expansion on this page |
| P451 | 1135@16 | i | SOURCED | named gap - first use before any expansion on this page |
| P451 | 1136@16 | i | STARTED | named gap - first use before any expansion on this page |
| P451 | 1137@16 | i | STOPS | named gap - first use before any expansion on this page |
| P451 | 1157@16 | i | EXACT | named gap - first use before any expansion on this page |
| P451 | 1166@16 | i | DURABLE | named gap - first use before any expansion on this page |
| P451 | 1171@16 | i | OUTPUT | named gap - first use before any expansion on this page |
| P451 | 1191@18 | iii | tests/test_static_safety.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 1202@17 | i | EXTERNAL | named gap - first use before any expansion on this page |
| P451 | 1203@17 | i | CHANGES | named gap - first use before any expansion on this page |
| P451 | 1205@17 | i | REQUIRED | named gap - first use before any expansion on this page |
| P451 | 1215@17 | i | PROMPT | named gap - first use before any expansion on this page |
| P451 | 1219@17 | i | MD | named gap - first use before any expansion on this page |
| P451 | 1233@17 | i | ACTUAL | named gap - first use before any expansion on this page |
| P451 | 1252@17 | i | ZIP | named gap - first use before any expansion on this page |
| P451 | 1255@17 | i | ORIGINAL | named gap - first use before any expansion on this page |
| P451 | 1256@18 | iv | 52805dc4 | documented exclusion - SHA: commit/blob hash |
| P451 | 1287@17 | i | TWO | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 1298@17 | i | RECORDED | named gap - first use before any expansion on this page |
| P451 | 1300@17 | i | REPORTED | named gap - first use before any expansion on this page |
| P451 | 1304@17 | i | REPLACED | named gap - first use before any expansion on this page |
| P451 | 1305@17 | i | REQUEST | named gap - first use before any expansion on this page |
| P451 | 1306@18 | iv | 52805dc4ea2cd3ccb11a3af79ef557a6d6d32b8d | documented exclusion - SHA: commit/blob hash |
| P451 | 1309@17 | i | ANY | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P451 | 1310@17 | i | REJECTS | named gap - first use before any expansion on this page |
| P451 | 1317@17 | v | × | documented exclusion - OPERATOR: operator glyph |
| P451 | 1319@17 | i | BLOCKER | named gap - first use before any expansion on this page |
| P451 | 1320@17 | i | BLOCKERS | named gap - first use before any expansion on this page |
| P451 | 1321@17 | i | SOUND | named gap - first use before any expansion on this page |
| P451 | 1323@17 | i | NAMED | named gap - first use before any expansion on this page |
| P451 | 1325@17 | i | STAGE | named gap - first use before any expansion on this page |
| P451 | 1332@19 | i | GET | named gap - first use before any expansion on this page |
| P451 | 1337@17 | i | BRAND | named gap - first use before any expansion on this page |
| P451 | 1340@17 | i | INTERNAL | named gap - first use before any expansion on this page |
| P451 | 1351@18 | iv | 530cdefc | documented exclusion - SHA: commit/blob hash |
| P451 | 1352@18 | iv | 747a3968 | documented exclusion - SHA: commit/blob hash |
| P451 | 1359@19 | iii | tools/behavioral_eval_runner/judge/calibration_development_driver.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 1371@17 | i | DUMMY | named gap - first use before any expansion on this page |
| P451 | 1372@19 | iii | tests/test_static_safety_calibration.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 1373@17 | i | THIRD | named gap - first use before any expansion on this page |
| P451 | 1391@18 | iv | ca19b919 | documented exclusion - SHA: commit/blob hash |
| P451 | 1393@17 | i | PROVIDER | named gap - first use before any expansion on this page |
| P451 | 1394@19 | iii | tests/test_calibration_first_live_corrections.py | documented exclusion - PATH: non-backticked path identifier |
| P451 | 1397@17 | v | <32-hex> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P451 | 1401@17 | i | SPECIFIC | named gap - first use before any expansion on this page |
| P451 | 1413@17 | i | COUNT | named gap - first use before any expansion on this page |
| P451 | 1416@17 | i | INPUT | named gap - first use before any expansion on this page |
| P451 | 1424@17 | i | MISMATCH | named gap - first use before any expansion on this page |
| P451 | 1425@17 | i | MODEL | named gap - first use before any expansion on this page |
| P451 | 1435@15 | i | YAML | named gap - first use before any expansion on this page |
| P451 | 1445@17 | iv | f82a4bce770c173df6d4ddc6b920a7b35a6a63e7 | documented exclusion - SHA: commit/blob hash |
| P451 | 1454@17 | iv | 7a804aa | documented exclusion - SHA: commit/blob hash |
| P451 | 1463@16 | i | AEGIS | named gap - first use before any expansion on this page |
| P451 | 1464@16 | i | APR | named gap - first use before any expansion on this page |
| P451 | 1478@17 | iv | 0318b1ecde3ebf5f34bb32f8793efc37b574af39 | documented exclusion - SHA: commit/blob hash |
| P451 | 1479@17 | iv | d35f4a6af25e4d5dd29641e0fa271bf782b1e7df | documented exclusion - SHA: commit/blob hash |
| P451 | 1481@17 | iv | f0ef7bfae43a3f486288d0678efa5eae6b03e3b1 | documented exclusion - SHA: commit/blob hash |
| P451 | 1482@17 | iv | 081404ef88a6e507c8ce0c4e464797d20131655c | documented exclusion - SHA: commit/blob hash |
| P451 | 1483@17 | iv | 7176009113fa208a1b2e816d90d7f929805e93ae | documented exclusion - SHA: commit/blob hash |
| P451 | 1485@17 | iv | 53351b3fac3d75cbbc23341cc96dbeadc1e116ee | documented exclusion - SHA: commit/blob hash |
| P451 | 1504@73 | v | 36047710329 | documented exclusion - RANGE: numeric range/unit token |
| P451 | 1505@16 | i | SUCCESS | named gap - first use before any expansion on this page |
| P451 | 1536@2 | i | AC | named gap - first use before any expansion on this page |
| P451 | 1538@17 | v | MET | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P451 | 1542@18 | i | PROC | named gap - first use before any expansion on this page |
| P451 | 1551@81 | iv | 7b91073202f19c9132f9e1cec471afd683e2ff5f | documented exclusion - SHA: commit/blob hash |
| P451 | 1555@33 | iv | c6e5d5649bf8 | documented exclusion - SHA: commit/blob hash |
| P451 | 1556@31 | iv | b5fd9feda972 | documented exclusion - SHA: commit/blob hash |
| P451 | 1557@31 | iv | 08d91a834460 | documented exclusion - SHA: commit/blob hash |
| P451 | 1558@23 | iv | 6a27b5c8e690 | documented exclusion - SHA: commit/blob hash |
| P451 | 1560@65 | v | <n> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P451 | 1562@267 | iii | _A/evidence/read-lc344-c1/Crows.txt | documented exclusion - PATH: non-backticked path identifier |
| P451 | 1562@456 | iii | tools/skills-manifest.json | documented exclusion - PATH: non-backticked path identifier |
| P452 | 1@71 | v | 2026-10-18 | documented exclusion - DATE: date/time literal |
| P452 | 1@71 | v | 2026-10 | documented exclusion - DATE: date/time literal |
| P452 | 7@56 | v | 6254199750 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 7@92 | v | ACCEPT | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 7@99 | v | 6254232090 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 7@120 | iv | e2a8d0d38f3a0971f3f4ce0841b34b9810015831 | documented exclusion - SHA: commit/blob hash |
| P452 | 7@203 | v | 2026-10-18T19:28:21Z | documented exclusion - DATE: date/time literal |
| P452 | 7@299 | i | PR | named gap - first use before any expansion on this page |
| P452 | 7@359 | iii | docs/evidence/documentation/readability-lane-c-batch-12-2026-10-18.md**. | documented exclusion - PATH: non-backticked path identifier |
| P452 | 7@364 | ii | evidence | documented exclusion - PROSE: lowercase technical/audience prose |
| P452 | 7@387 | ii | readability | documented exclusion - PROSE: lowercase technical/audience prose |
| P452 | 7@412 | v | 12-2026 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 7@420 | v | 10-18 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 9@57 | v | 144-279 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 9@83 | v | 1-11 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 9@104 | v | 304-351 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 9@145 | v | 352-359 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 9@194 | v | 360-367 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 9@241 | iv | e2a8d0d3 | documented exclusion - SHA: commit/blob hash |
| P452 | 9@261 | v | 55151039 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 9@281 | iv | 9085bf6a | documented exclusion - SHA: commit/blob hash |
| P452 | 9@301 | iv | 9a5cb28d | documented exclusion - SHA: commit/blob hash |
| P452 | 9@321 | iv | e3f535e4 | documented exclusion - SHA: commit/blob hash |
| P452 | 9@341 | iv | 3ef6c735 | documented exclusion - SHA: commit/blob hash |
| P452 | 9@361 | iv | 6afc845a | documented exclusion - SHA: commit/blob hash |
| P452 | 9@381 | iv | 4b99f69f | documented exclusion - SHA: commit/blob hash |
| P452 | 9@401 | iv | 2c3c6ffe | documented exclusion - SHA: commit/blob hash |
| P452 | 9@421 | v | 38212595 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 9@441 | iv | f325daac | documented exclusion - SHA: commit/blob hash |
| P452 | 9@461 | iv | 7cea211e | documented exclusion - SHA: commit/blob hash |
| P452 | 9@481 | iv | 6f584c9d | documented exclusion - SHA: commit/blob hash |
| P452 | 11@251 | v | 0-152 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 11@265 | v | 153-305 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 11@292 | v | 306-458 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 11@308 | v | 459-611 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 11@418 | iv | 2db1ffb7 | documented exclusion - SHA: commit/blob hash |
| P452 | 13@245 | v | 6250828860 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 13@305 | v | L39 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 17@45 | i | LF | named gap - first use before any expansion on this page |
| P452 | 19@13 | iii | docs/evidence/ber-bkl-009-static-source-inventory.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 19@53 | ii | inventory | documented exclusion - PROSE: lowercase technical/audience prose |
| P452 | 19@68 | iv | f730288ce31a5b738ef5c0dd5b5356c4c2cabb8b | documented exclusion - SHA: commit/blob hash |
| P452 | 20@13 | iii | docs/evidence/ber-bkl-009a-offline-review.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 20@60 | iv | b5c3070b89e51e1e9937599777360347d7e45190 | documented exclusion - SHA: commit/blob hash |
| P452 | 21@13 | iii | docs/evidence/ber-pr88-closeout-2026-09-12/README.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 21@45 | v | 2026-09-12 | documented exclusion - DATE: date/time literal |
| P452 | 21@45 | v | 2026-09 | documented exclusion - DATE: date/time literal |
| P452 | 21@56 | i | README | named gap - first use before any expansion on this page |
| P452 | 21@68 | iv | 680949b48ec57e64bdb5c08157d94c7046f63238 | documented exclusion - SHA: commit/blob hash |
| P452 | 22@13 | iii | docs/evidence/ber-pr88-closeout-2026-09-12/preflight/final-plan.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 22@82 | iv | f0d85f8aaef1aa466b59a43b2b347bf8042e8607 | documented exclusion - SHA: commit/blob hash |
| P452 | 23@13 | iii | docs/evidence/ber-pr88-closeout-2026-09-12/preflight/main-contract-audit.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 23@91 | iv | 308c78e35d43c30fb7e9bf7ba47603d8cb035927 | documented exclusion - SHA: commit/blob hash |
| P452 | 24@13 | iii | docs/evidence/ber-pr88-closeout-2026-09-12/reviews.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 24@69 | iv | 534b76d4ffa1f00e930118e00039e3c720004cc3 | documented exclusion - SHA: commit/blob hash |
| P452 | 25@13 | iii | docs/evidence/ber-pr88-closeout-2026-09-12/verification.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 25@74 | iv | 888c8b2db974db214cffa25d6d90421c8752c6ed | documented exclusion - SHA: commit/blob hash |
| P452 | 26@13 | iii | docs/evidence/ber-recovery-2026-09-11/README.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 26@40 | v | 2026-09-11 | documented exclusion - DATE: date/time literal |
| P452 | 26@63 | iv | faff8b693ea4d0f59f90310cb0cabdefa4edf0c3 | documented exclusion - SHA: commit/blob hash |
| P452 | 31@38 | v | L2841-2862 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 31@227 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 31@250 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 34@16 | v | L1-132 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 34@193 | i | BER | named gap - first use before any expansion on this page |
| P452 | 35@66 | i | BKL | named gap - first use before any expansion on this page |
| P452 | 35@70 | v | L1 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@92 | v | L9 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@100 | v | L35 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@105 | i | WP | named gap - first use before any expansion on this page |
| P452 | 35@108 | v | L36 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@120 | v | L77 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@125 | i | ZIP | named gap - first use before any expansion on this page |
| P452 | 35@129 | v | L82 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@134 | i | ETA | named gap - first use before any expansion on this page |
| P452 | 35@138 | v | L100 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@147 | v | L106 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@162 | i | SYSTEM | named gap - first use before any expansion on this page |
| P452 | 35@169 | v | L111 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 35@175 | i | APR | named gap - first use before any expansion on this page |
| P452 | 35@179 | v | L113 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 40@11 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 44@16 | v | L1-172 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 45@71 | v | L7 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 45@93 | v | L10 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 45@107 | i | DEC | named gap - first use before any expansion on this page |
| P452 | 45@111 | v | L16 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 45@123 | v | L89 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 45@135 | v | L118 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 45@141 | i | CI | named gap - first use before any expansion on this page |
| P452 | 45@144 | v | L171 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 54@16 | v | L1-115 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 54@190 | i | SDK | named gap - first use before any expansion on this page |
| P452 | 54@195 | i | POSIX | named gap - first use before any expansion on this page |
| P452 | 54@202 | i | DCO | named gap - first use before any expansion on this page |
| P452 | 54@207 | i | QA | named gap - first use before any expansion on this page |
| P452 | 54@214 | i | OD | named gap - first use before any expansion on this page |
| P452 | 55@71 | v | L13 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 55@76 | i | DELIVERY | named gap - first use before any expansion on this page |
| P452 | 55@85 | v | L19 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 55@116 | v | L20 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 55@121 | i | AEGIS | named gap - first use before any expansion on this page |
| P452 | 55@127 | v | L41 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 55@139 | v | L61 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 55@144 | i | UTF | named gap - first use before any expansion on this page |
| P452 | 55@148 | v | L71 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 55@153 | i | TEMP | named gap - first use before any expansion on this page |
| P452 | 55@158 | v | L78 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 55@163 | i | TMP | named gap - first use before any expansion on this page |
| P452 | 64@16 | v | L1-241 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 64@240 | i | JSON | named gap - first use before any expansion on this page |
| P452 | 64@254 | i | LLM | named gap - first use before any expansion on this page |
| P452 | 65@89 | v | L47 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 65@94 | i | STATE | named gap - first use before any expansion on this page |
| P452 | 65@100 | v | L127 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 65@106 | i | SHA | named gap - first use before any expansion on this page |
| P452 | 65@110 | v | L155 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 74@16 | v | L1-298 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@69 | v | L5 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@91 | i | REVIEW | named gap - first use before any expansion on this page |
| P452 | 75@98 | v | L8 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@102 | i | SEMANTIC | named gap - first use before any expansion on this page |
| P452 | 75@129 | v | L15 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@134 | i | SKILL | named gap - first use before any expansion on this page |
| P452 | 75@140 | v | L26 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@145 | i | APPR | named gap - first use before any expansion on this page |
| P452 | 75@150 | v | L31 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@155 | i | ARTF | named gap - first use before any expansion on this page |
| P452 | 75@165 | i | REF | named gap - first use before any expansion on this page |
| P452 | 75@174 | i | SIDE | named gap - first use before any expansion on this page |
| P452 | 75@195 | i | VOCAB | named gap - first use before any expansion on this page |
| P452 | 75@209 | v | L37 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@214 | i | ROUTE | named gap - first use before any expansion on this page |
| P452 | 75@220 | v | L43 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@225 | i | EXECUTES | named gap - first use before any expansion on this page |
| P452 | 75@234 | v | L109 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@240 | i | CHECK | named gap - first use before any expansion on this page |
| P452 | 75@246 | v | L117 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 75@252 | i | INSERT | named gap - first use before any expansion on this page |
| P452 | 75@265 | i | HORIZON | named gap - first use before any expansion on this page |
| P452 | 75@273 | v | L119 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 84@16 | v | L1-64 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 84@146 | ii | candidate | documented exclusion - PROSE: lowercase technical/audience prose |
| P452 | 84@186 | i | CLI | named gap - first use before any expansion on this page |
| P452 | 85@72 | v | L12 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 85@85 | i | APPROVE | named gap - first use before any expansion on this page |
| P452 | 85@93 | v | L27 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 94@16 | v | L1-95 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 94@204 | i | YAML | named gap - first use before any expansion on this page |
| P452 | 95@73 | v | L17 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 95@90 | v | L64 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 95@95 | ii | json | documented exclusion - PROSE: lowercase technical/audience prose |
| P452 | 95@100 | v | L69 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 95@108 | v | L95 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 104@16 | v | L1-168 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 105@125 | v | L29 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 105@137 | v | L30 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 105@200 | v | L66 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 105@220 | v | L122 | documented exclusion - LINE-RANGE: page-line reference |
| P452 | 112@39 | ii | token | documented exclusion - PROSE: lowercase technical/audience prose |
| P452 | 112@57 | i | ONE | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P452 | 114@20 | i | REAL | named gap - first use before any expansion on this page |
| P452 | 114@219 | i | DOTALL | named gap - first use before any expansion on this page |
| P452 | 120@16 | iv | 69be30a3a71d21c70f13a6b20d7da5e15e023d17 | documented exclusion - SHA: commit/blob hash |
| P452 | 126@16 | i | VM | named gap - first use before any expansion on this page |
| P452 | 128@24 | iii | tools/behavioral_eval_runner/evidence.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 135@24 | iii | tools/behavioral_eval_runner/evidence_policy.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 144@24 | iii | tools/behavioral_eval_runner/evidence_policy_preflight.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 145@16 | i | ACL | named gap - first use before any expansion on this page |
| P452 | 147@16 | i | STOP | named gap - first use before any expansion on this page |
| P452 | 150@24 | iii | tools/behavioral_eval_runner/judge/envelope.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 153@24 | iii | tools/behavioral_eval_runner/cli.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 159@24 | iii | tools/behavioral_eval_runner/judge/calibration_development_driver.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 164@17 | iv | 9b85140d | documented exclusion - SHA: commit/blob hash |
| P452 | 171@24 | iii | tools/behavioral_eval_runner/budget.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 177@24 | iii | tools/behavioral_eval_runner/materialize.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 180@24 | iii | tools/behavioral_eval_runner/judge/calibration_ledger.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 211@16 | iv | b4b1195d6162728ffc37d22d038a08e3722db7c0 | documented exclusion - SHA: commit/blob hash |
| P452 | 222@17 | iv | 7e8f0c1067ee0a2e963520bf735a4b7b907a991f | documented exclusion - SHA: commit/blob hash |
| P452 | 223@16 | i | UTC | named gap - first use before any expansion on this page |
| P452 | 229@17 | iv | bfb35cd1aee6cddd239c32377c8388871a0d6633 | documented exclusion - SHA: commit/blob hash |
| P452 | 240@18 | iv | 754fc7a02f85c1f05dc32b4bbd70c1b616979b50 | documented exclusion - SHA: commit/blob hash |
| P452 | 241@18 | iv | f1bfaece5b68551f75e910470becd17ed61ccb7e | documented exclusion - SHA: commit/blob hash |
| P452 | 242@18 | iv | 9cd78be746f81803824bf642258664ba652c9a27 | documented exclusion - SHA: commit/blob hash |
| P452 | 243@19 | iii | tools/behavioral_eval_runner/ | documented exclusion - PATH: non-backticked path identifier |
| P452 | 245@18 | iv | 8928383f0838e2d99ee3a89c44b98b7aba7f1c9b | documented exclusion - SHA: commit/blob hash |
| P452 | 246@29 | iii | scripts/validate-skills.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 247@29 | iii | scripts/tests/test_validator.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 250@53 | iii | tools/behavioral_eval_runner/tests | documented exclusion - PATH: non-backticked path identifier |
| P452 | 251@18 | iv | 27078574d90805b16dcf39b42a9af226eac3c28f | documented exclusion - SHA: commit/blob hash |
| P452 | 264@17 | iv | f5e04ad07a5fd2b34b7470bffd38a50c15ce691a | documented exclusion - SHA: commit/blob hash |
| P452 | 265@17 | iv | d53752d2b600410da122d4b85429c35f30d7c873 | documented exclusion - SHA: commit/blob hash |
| P452 | 266@73 | v | 34668951280 | documented exclusion - RANGE: numeric range/unit token |
| P452 | 275@16 | v | PENDING | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 280@17 | iv | 000352f55b71f0c3e897a482d279d34bfaa3d66b | documented exclusion - SHA: commit/blob hash |
| P452 | 281@17 | iv | c7a92d208a8aec7295afa3e3188dce03a8331d0b | documented exclusion - SHA: commit/blob hash |
| P452 | 284@16 | v | APPROVED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 293@17 | iv | a231bc5 | documented exclusion - SHA: commit/blob hash |
| P452 | 324@17 | iv | 000352f | documented exclusion - SHA: commit/blob hash |
| P452 | 326@17 | iv | ac9e1cdb020f4efb7a52e5ea606c3b329fb486e2 | documented exclusion - SHA: commit/blob hash |
| P452 | 329@17 | iv | a231bc5db820c89467b32dbec533adf01eb56676 | documented exclusion - SHA: commit/blob hash |
| P452 | 330@16 | v | BLOCKED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 331@16 | v | OPEN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 335@16 | i | AI | named gap - first use before any expansion on this page |
| P452 | 336@18 | iii | scripts/tests/ | documented exclusion - PATH: non-backticked path identifier |
| P452 | 338@16 | v | PASS | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 342@31 | i | HEAD | named gap - first use before any expansion on this page |
| P452 | 360@17 | v | ACTIVE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 375@15 | i | INFO | named gap - first use before any expansion on this page |
| P452 | 382@17 | iv | 7fdf02290b0b15ed | documented exclusion - SHA: commit/blob hash |
| P452 | 388@16 | i | EXPECTED | named gap - first use before any expansion on this page |
| P452 | 393@18 | iii | docs/paths/ | documented exclusion - PATH: non-backticked path identifier |
| P452 | 396@18 | iii | docs/skills-catalog.md | documented exclusion - PATH: non-backticked path identifier |
| P452 | 399@16 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 402@16 | i | EVAL | named gap - first use before any expansion on this page |
| P452 | 419@18 | i | NNNN | named gap - first use before any expansion on this page |
| P452 | 420@18 | iii | docs/adr/ | documented exclusion - PATH: non-backticked path identifier |
| P452 | 500@17 | v | COMPLETE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 574@17 | v | × | documented exclusion - OPERATOR: operator glyph |
| P452 | 587@18 | ii | api | documented exclusion - PROSE: lowercase technical/audience prose |
| P452 | 668@17 | iv | 5863fb1ef2fa95f653e7983b74cea16caa95555b | documented exclusion - SHA: commit/blob hash |
| P452 | 669@17 | iv | 88f04538a9fcfad9e13117c7d8d3afb28dbadfe7 | documented exclusion - SHA: commit/blob hash |
| P452 | 683@15 | i | GID | named gap - first use before any expansion on this page |
| P452 | 684@15 | i | UID | named gap - first use before any expansion on this page |
| P452 | 697@16 | i | DISABLED | named gap - first use before any expansion on this page |
| P452 | 703@16 | v | <isolated-SDK-python> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P452 | 705@35 | i | PETERN | named gap - first use before any expansion on this page |
| P452 | 716@36 | iv | 5863fb1 | documented exclusion - SHA: commit/blob hash |
| P452 | 723@16 | v | DONE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 749@18 | iii | scripts/ci/check-environment.py | documented exclusion - PATH: non-backticked path identifier |
| P452 | 755@17 | iv | 8f92e91 | documented exclusion - SHA: commit/blob hash |
| P452 | 756@17 | iv | 8f92e916f86bc0b9df618fb6a7887bd531df8fea | documented exclusion - SHA: commit/blob hash |
| P452 | 757@17 | iv | 499e7e96bd524fe024aec94ed69d11a17f783e13 | documented exclusion - SHA: commit/blob hash |
| P452 | 758@17 | iv | 40bfabc | documented exclusion - SHA: commit/blob hash |
| P452 | 759@17 | iv | c6822e1 | documented exclusion - SHA: commit/blob hash |
| P452 | 768@18 | iii | docs/evidence/ber-recovery-2026-09-11/requirements-windows-py314.txt | documented exclusion - PATH: non-backticked path identifier |
| P452 | 810@251 | ii | workflow | documented exclusion - PROSE: lowercase technical/audience prose |
| P452 | 814@2 | i | AC | named gap - first use before any expansion on this page |
| P452 | 816@17 | v | MET | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P452 | 820@18 | i | PROC | named gap - first use before any expansion on this page |
| P452 | 835@33 | iv | c6e5d5649bf8 | documented exclusion - SHA: commit/blob hash |
| P452 | 836@31 | iv | b5fd9feda972 | documented exclusion - SHA: commit/blob hash |
| P452 | 837@31 | iv | 08d91a834460 | documented exclusion - SHA: commit/blob hash |
| P452 | 838@23 | iv | 6a27b5c8e690 | documented exclusion - SHA: commit/blob hash |
| P452 | 840@65 | v | <n> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P452 | 842@201 | iii | _A/evidence/read-lc352-c1/Crows.txt | documented exclusion - PATH: non-backticked path identifier |
| P452 | 842@390 | iii | tools/skills-manifest.json | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1@71 | v | 2026-10-18 | documented exclusion - DATE: date/time literal |
| P453 | 1@71 | v | 2026-10 | documented exclusion - DATE: date/time literal |
| P453 | 7@59 | v | 6254771111 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 7@95 | i | DELTA | named gap - first use before any expansion on this page |
| P453 | 7@101 | v | ACCEPT | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 7@108 | v | 6254788195 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 7@129 | iv | a32c2a018cbb6dae6937570eb7ba63d120bf0cb8 | documented exclusion - SHA: commit/blob hash |
| P453 | 7@212 | v | 2026-10-18T20:01:51Z | documented exclusion - DATE: date/time literal |
| P453 | 7@308 | i | PR | named gap - first use before any expansion on this page |
| P453 | 7@368 | iii | docs/evidence/documentation/readability-lane-c-batch-13-2026-10-18.md**. | documented exclusion - PATH: non-backticked path identifier |
| P453 | 7@373 | ii | evidence | documented exclusion - PROSE: lowercase technical/audience prose |
| P453 | 7@396 | ii | readability | documented exclusion - PROSE: lowercase technical/audience prose |
| P453 | 7@421 | v | 13-2026 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 7@429 | v | 10-18 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 9@57 | v | 144-279 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 9@83 | v | 1-12 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 9@104 | v | 304-359 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 9@145 | v | 360-367 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 9@194 | v | 368-375 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 9@241 | iv | a32c2a01 | documented exclusion - SHA: commit/blob hash |
| P453 | 9@261 | iv | e2a8d0d3 | documented exclusion - SHA: commit/blob hash |
| P453 | 9@281 | v | 55151039 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 9@301 | iv | 9085bf6a | documented exclusion - SHA: commit/blob hash |
| P453 | 9@321 | iv | 9a5cb28d | documented exclusion - SHA: commit/blob hash |
| P453 | 9@341 | iv | e3f535e4 | documented exclusion - SHA: commit/blob hash |
| P453 | 9@361 | iv | 3ef6c735 | documented exclusion - SHA: commit/blob hash |
| P453 | 9@381 | iv | 6afc845a | documented exclusion - SHA: commit/blob hash |
| P453 | 9@401 | iv | 4b99f69f | documented exclusion - SHA: commit/blob hash |
| P453 | 9@421 | iv | 2c3c6ffe | documented exclusion - SHA: commit/blob hash |
| P453 | 9@441 | v | 38212595 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 9@461 | iv | f325daac | documented exclusion - SHA: commit/blob hash |
| P453 | 9@481 | iv | 7cea211e | documented exclusion - SHA: commit/blob hash |
| P453 | 9@501 | iv | 6f584c9d | documented exclusion - SHA: commit/blob hash |
| P453 | 11@251 | v | 0-153 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 11@265 | v | 154-307 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 11@292 | v | 308-461 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 11@308 | v | 462-612 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 11@418 | iv | 2db1ffb7 | documented exclusion - SHA: commit/blob hash |
| P453 | 13@385 | v | 6250828860 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 13@678 | ii | candidate | documented exclusion - PROSE: lowercase technical/audience prose |
| P453 | 17@45 | i | LF | named gap - first use before any expansion on this page |
| P453 | 19@13 | iii | docs/evidence/ber-recovery-2026-09-11/phase01-independent-final-review.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 19@40 | v | 2026-09-11 | documented exclusion - DATE: date/time literal |
| P453 | 19@40 | v | 2026-09 | documented exclusion - DATE: date/time literal |
| P453 | 19@89 | iv | 80c6104eea629efe50d1e36ed296b4bb3d0125d7 | documented exclusion - SHA: commit/blob hash |
| P453 | 20@13 | iii | docs/evidence/ber-recovery-2026-09-11/preservation-independent-review.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 20@88 | iv | a8a97d4fa055809b401ecc945bb48c77421a6749 | documented exclusion - SHA: commit/blob hash |
| P453 | 21@13 | iii | docs/evidence/ber-recovery-2026-09-11/replacement-plan.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 21@73 | iv | 715cae756120677e998194daec4176990ad2b19d | documented exclusion - SHA: commit/blob hash |
| P453 | 22@13 | iii | docs/evidence/ber-replacement-candidate-1-summary.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 22@68 | iv | 2cf5c71775db96a86f5f2f93ae653a0b7a120cf7 | documented exclusion - SHA: commit/blob hash |
| P453 | 23@13 | iii | docs/evidence/ber-wp2b3-holdout-offline-review.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 23@65 | iv | 57c368ec588dcb7f4c9e2bcaf55f14e1c0975124 | documented exclusion - SHA: commit/blob hash |
| P453 | 24@13 | iii | docs/evidence/control-plane/cp-wp-001-review.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 24@63 | iv | 3b260113be2572b744735031aa8cdf1a47c32fff | documented exclusion - SHA: commit/blob hash |
| P453 | 25@13 | iii | docs/evidence/control-plane/cp-wp-002-codex-handoff.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 25@70 | iv | 27d1a28466474773f7f289b03b435b4c832d39bb | documented exclusion - SHA: commit/blob hash |
| P453 | 26@13 | iii | docs/evidence/control-plane/cp-wp-003a-review.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 26@64 | iv | 04ba1280683cb0f106d73ee71ceba796f1965cc1 | documented exclusion - SHA: commit/blob hash |
| P453 | 31@38 | v | L2841-2862 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 31@227 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 31@250 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 34@16 | v | L1-40 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 34@136 | i | APPROVE | named gap - first use before any expansion on this page |
| P453 | 35@73 | v | L1 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 35@80 | v | L6 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 35@84 | i | POSIX | named gap - first use before any expansion on this page |
| P453 | 35@90 | v | L8 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 35@94 | i | HEAD | named gap - first use before any expansion on this page |
| P453 | 35@99 | v | L13 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 35@104 | i | MAJOR | named gap - first use before any expansion on this page |
| P453 | 35@110 | v | L24 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 35@115 | ii | json | documented exclusion - PROSE: lowercase technical/audience prose |
| P453 | 35@120 | v | L33 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 40@11 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 44@16 | v | L1-36 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 45@77 | v | L17 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 54@16 | v | L1-95 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 55@65 | i | BER | named gap - first use before any expansion on this page |
| P453 | 55@69 | v | L5 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 55@73 | i | DEC | named gap - first use before any expansion on this page |
| P453 | 55@84 | v | L7 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 55@88 | i | README | named gap - first use before any expansion on this page |
| P453 | 55@95 | v | L11 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 55@100 | i | ZIP | named gap - first use before any expansion on this page |
| P453 | 55@104 | v | L67 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 55@120 | v | L73 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 55@125 | i | SDK | named gap - first use before any expansion on this page |
| P453 | 55@129 | v | L90 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 64@16 | v | L1-83 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 64@220 | v | PENDING | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 65@80 | i | PRIVATE | named gap - first use before any expansion on this page |
| P453 | 65@88 | v | L35 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 65@99 | v | L74 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 74@16 | v | L1-81 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 75@71 | v | L4 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 75@75 | i | WP | named gap - first use before any expansion on this page |
| P453 | 75@87 | v | L15 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 84@16 | v | L1-319 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@75 | i | USD | named gap - first use before any expansion on this page |
| P453 | 85@79 | v | L31 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@84 | i | CI | named gap - first use before any expansion on this page |
| P453 | 85@87 | v | L32 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@92 | i | DCO | named gap - first use before any expansion on this page |
| P453 | 85@101 | i | AGENTS | named gap - first use before any expansion on this page |
| P453 | 85@108 | v | L42 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@119 | v | L51 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@142 | v | L64 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@151 | v | L66 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@172 | i | SHOULD | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P453 | 85@179 | v | L70 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@190 | v | L76 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@214 | i | PAUSING | named gap - first use before any expansion on this page |
| P453 | 85@284 | v | L91 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@292 | v | L92 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@297 | i | RELEASED | named gap - first use before any expansion on this page |
| P453 | 85@306 | v | L93 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@311 | i | RESERVED | named gap - first use before any expansion on this page |
| P453 | 85@343 | i | ID | named gap - first use before any expansion on this page |
| P453 | 85@346 | v | L94 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@351 | i | INCLUDED | named gap - first use before any expansion on this page |
| P453 | 85@371 | v | L95 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@383 | v | L108 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@389 | i | UTF | named gap - first use before any expansion on this page |
| P453 | 85@393 | v | L111 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@403 | v | L113 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@479 | i | SHA | named gap - first use before any expansion on this page |
| P453 | 85@483 | v | L120 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@489 | i | URL | named gap - first use before any expansion on this page |
| P453 | 85@493 | v | L124 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@503 | v | L133 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@523 | v | L141 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@539 | i | UTC | named gap - first use before any expansion on this page |
| P453 | 85@553 | v | L147 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@578 | i | UID | named gap - first use before any expansion on this page |
| P453 | 85@592 | v | L148 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@632 | v | L149 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@668 | i | ADJUSTED | named gap - first use before any expansion on this page |
| P453 | 85@677 | v | L150 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@759 | v | L151 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@789 | v | L152 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@815 | i | BOTH | named gap - first use before any expansion on this page |
| P453 | 85@820 | v | L160 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@829 | v | L164 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@840 | v | L185 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@861 | v | L193 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@901 | v | L194 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@921 | v | L195 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@960 | v | L202 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@969 | v | L203 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@975 | i | PLANNED | named gap - first use before any expansion on this page |
| P453 | 85@992 | v | L204 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1002 | v | L227 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1023 | v | L228 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1044 | v | L229 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1065 | v | L230 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1086 | v | L231 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1120 | v | L232 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1171 | v | L233 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1181 | v | L243 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1198 | v | L246 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1208 | v | L262 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1218 | v | L263 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1239 | v | L264 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1260 | v | L265 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1271 | v | L285 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1282 | v | L286 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1293 | v | L287 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1304 | v | L288 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1315 | v | L289 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1336 | v | L290 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1347 | v | L291 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 85@1358 | v | L292 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 94@16 | v | L1-2021 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@68 | i | CP | named gap - first use before any expansion on this page |
| P453 | 95@82 | i | MAC | named gap - first use before any expansion on this page |
| P453 | 95@94 | v | L19 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@106 | v | L23 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@141 | v | L37 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@163 | i | KERNEL | named gap - first use before any expansion on this page |
| P453 | 95@175 | v | MERGED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 95@187 | i | NT | named gap - first use before any expansion on this page |
| P453 | 95@195 | i | REAL | named gap - first use before any expansion on this page |
| P453 | 95@234 | v | L50 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@244 | v | L54 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@252 | v | L57 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@280 | v | L131 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@295 | i | OS | named gap - first use before any expansion on this page |
| P453 | 95@307 | v | L158 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@327 | v | L161 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@337 | v | L162 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@347 | v | L163 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@367 | v | L165 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@377 | v | L166 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@387 | v | L167 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@397 | v | L168 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@407 | v | L169 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@417 | v | L170 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@427 | v | L171 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@437 | v | L172 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@447 | v | L212 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@457 | v | L215 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@477 | v | L248 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@483 | i | STOP | named gap - first use before any expansion on this page |
| P453 | 95@488 | v | L284 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@508 | v | L294 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@518 | v | L314 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@558 | v | L334 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@568 | v | L357 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@574 | i | QA | named gap - first use before any expansion on this page |
| P453 | 95@577 | v | L386 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@587 | v | L389 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@597 | v | L416 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@617 | v | L421 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@623 | i | ITEM | named gap - first use before any expansion on this page |
| P453 | 95@628 | v | L427 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@634 | i | PLAN | named gap - first use before any expansion on this page |
| P453 | 95@645 | i | POLICY | named gap - first use before any expansion on this page |
| P453 | 95@658 | i | SOURCE | named gap - first use before any expansion on this page |
| P453 | 95@682 | v | L444 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@692 | v | L458 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@702 | v | L463 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@712 | v | L471 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@718 | i | RESUME | named gap - first use before any expansion on this page |
| P453 | 95@725 | v | L475 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@731 | i | CLI | named gap - first use before any expansion on this page |
| P453 | 95@735 | v | L482 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@747 | v | L485 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@757 | v | L500 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@767 | v | L501 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@787 | v | L508 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@797 | v | L518 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@803 | i | TDD | named gap - first use before any expansion on this page |
| P453 | 95@807 | v | L521 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@813 | i | PAUSE | named gap - first use before any expansion on this page |
| P453 | 95@819 | v | L522 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@829 | v | L525 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@839 | v | L559 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@849 | v | L564 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@859 | v | L579 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@889 | v | L586 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@909 | v | L631 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@915 | i | RESULT | named gap - first use before any expansion on this page |
| P453 | 95@922 | v | L653 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@932 | v | L909 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@942 | v | L925 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@952 | v | L929 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@978 | i | BLOCKER | named gap - first use before any expansion on this page |
| P453 | 95@986 | v | L938 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@995 | v | L940 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1005 | v | L966 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1015 | v | L967 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1021 | i | URI | named gap - first use before any expansion on this page |
| P453 | 95@1025 | v | L974 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1031 | i | JSON | named gap - first use before any expansion on this page |
| P453 | 95@1036 | v | L999 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1042 | i | DDL | named gap - first use before any expansion on this page |
| P453 | 95@1046 | v | L1050 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1057 | v | L1083 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1075 | i | HOST | named gap - first use before any expansion on this page |
| P453 | 95@1080 | v | L1091 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1087 | i | MANUAL | named gap - first use before any expansion on this page |
| P453 | 95@1109 | v | L1098 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1116 | i | ACL | named gap - first use before any expansion on this page |
| P453 | 95@1120 | v | L1154 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1127 | i | SHM | named gap - first use before any expansion on this page |
| P453 | 95@1144 | v | L1158 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1155 | v | L1194 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1162 | v | L49 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1166 | v | L1392 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1173 | v | L493 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1185 | v | L4962 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1191 | v | L1394 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1198 | v | L9079 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1204 | v | L1395 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1211 | v | L9770 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1217 | v | L1396 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1224 | v | L10260 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1231 | v | L1397 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1238 | v | L12891 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1245 | v | L1398 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1256 | v | L1423 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1263 | v | L715 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1268 | v | L1424 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1275 | v | L5317 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1281 | v | L1425 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1288 | v | L447 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1293 | v | L1426 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1300 | v | L455 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1305 | v | L1445 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1312 | v | L1818 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1318 | v | L1446 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1325 | v | L1832 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1338 | v | L6668 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1344 | v | L1448 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1351 | v | L446 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1356 | v | L1449 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1367 | v | L1460 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1386 | v | L1496 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1406 | v | L1544 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1425 | v | L1618 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1432 | i | ADOPTION | named gap - first use before any expansion on this page |
| P453 | 95@1441 | v | L1657 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1448 | i | DURING | named gap - first use before any expansion on this page |
| P453 | 95@1455 | v | L1702 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1473 | v | L1706 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1480 | v | L420 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1485 | v | L1774 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1496 | v | L1798 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1503 | v | L599 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1508 | v | L1810 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1515 | v | L607 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1531 | v | L1815 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1538 | v | L939 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1543 | v | L1827 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1550 | v | L960 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1566 | v | L1841 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1577 | v | L1846 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1584 | i | FUT | named gap - first use before any expansion on this page |
| P453 | 95@1588 | v | L1914 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1600 | v | L1948 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 95@1611 | v | L1949 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 105@86 | v | L10 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 105@94 | v | L12 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 105@111 | i | AEGIS | named gap - first use before any expansion on this page |
| P453 | 105@122 | i | APR | named gap - first use before any expansion on this page |
| P453 | 105@155 | v | L43 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 105@185 | v | L72 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 105@190 | i | UNPROVEN | named gap - first use before any expansion on this page |
| P453 | 105@199 | v | L77 | documented exclusion - LINE-RANGE: page-line reference |
| P453 | 112@39 | ii | token | documented exclusion - PROSE: lowercase technical/audience prose |
| P453 | 112@45 | ii | inventory | documented exclusion - PROSE: lowercase technical/audience prose |
| P453 | 112@57 | i | ONE | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P453 | 114@219 | i | DOTALL | named gap - first use before any expansion on this page |
| P453 | 141@16 | v | PASS | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 154@27 | iii | tools/behavioral_eval_runner/judge/calibration_dataset.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 155@27 | iii | tools/behavioral_eval_runner/judge/rubric.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 157@16 | i | AI | named gap - first use before any expansion on this page |
| P453 | 158@16 | v | FAIL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 160@16 | v | CRITICAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 164@27 | iii | tools/behavioral_eval_runner/judge/calibration_development_driver.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 177@16 | i | OD | named gap - first use before any expansion on this page |
| P453 | 185@17 | iv | 874750ea5d503b2f2711f520bd6de09bb1381b0b | documented exclusion - SHA: commit/blob hash |
| P453 | 186@17 | iv | 1339c9c6d2c95196899d72994d91136c73d2da55 | documented exclusion - SHA: commit/blob hash |
| P453 | 187@17 | iv | 14e3f17c380dd26ddba1f27c7e041b6064509ba4 | documented exclusion - SHA: commit/blob hash |
| P453 | 190@17 | iv | 6beba11e83e5e8a1655f33302e40959ecc6067e5 | documented exclusion - SHA: commit/blob hash |
| P453 | 210@16 | iv | fa37c0e545dfd096e8327ca5357b0dfc6e2f8bb5 | documented exclusion - SHA: commit/blob hash |
| P453 | 211@16 | iv | bf72d391831c9c6c30eedd295d07a2ff32b47fe4 | documented exclusion - SHA: commit/blob hash |
| P453 | 212@16 | iv | cd4f944406ac79884de204f4d1e135e444316383 | documented exclusion - SHA: commit/blob hash |
| P453 | 221@17 | iv | 0196fe5b4eb30ca72c4bd61d51bedc9489a62115 | documented exclusion - SHA: commit/blob hash |
| P453 | 230@16 | v | OK | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 231@52 | iii | tools/behavioral_eval_runner/tests | documented exclusion - PATH: non-backticked path identifier |
| P453 | 238@17 | iv | 57e6928d2849aa5377daf52c723b85736292585d | documented exclusion - SHA: commit/blob hash |
| P453 | 240@18 | iii | docs/cp-wp-001-durable-state-authority-recovery | documented exclusion - PATH: non-backticked path identifier |
| P453 | 252@17 | iv | 9e3db61 | documented exclusion - SHA: commit/blob hash |
| P453 | 253@17 | iv | 9e3db6193b47ec002f1087b21fe9a55708972544 | documented exclusion - SHA: commit/blob hash |
| P453 | 289@27 | iii | tools/behavioral_eval_runner/README.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 306@16 | v | CLOSED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 310@16 | i | STOPPED | named gap - first use before any expansion on this page |
| P453 | 326@16 | i | CONSUMED | named gap - first use before any expansion on this page |
| P453 | 327@16 | v | MEDIUM | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 339@16 | i | RESOLVED | named gap - first use before any expansion on this page |
| P453 | 348@29 | iii | scripts/validate-skills.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 350@29 | iii | scripts/tests/test_validator.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 384@18 | iv | a0177d5 | documented exclusion - SHA: commit/blob hash |
| P453 | 385@18 | iv | 7cb53e770511f7d3c22e9a57948ffa22095e9bd3 | documented exclusion - SHA: commit/blob hash |
| P453 | 386@18 | iv | a0177d556f61b9849c596604bc71d068e9bc07c0 | documented exclusion - SHA: commit/blob hash |
| P453 | 393@18 | iv | 658932112682c9af53ff963cd404e50600f28f24 | documented exclusion - SHA: commit/blob hash |
| P453 | 438@17 | v | UNKNOWN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 489@18 | iv | 5acf7b64781b50fca1865d4a4ba4bd20c1004452 | documented exclusion - SHA: commit/blob hash |
| P453 | 490@18 | iv | caca8a1aaa3f1bc4c0f3023bbced6a52ba54d57c | documented exclusion - SHA: commit/blob hash |
| P453 | 498@17 | v | PAUSED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 531@18 | iv | 25481c0d7837f05bc636cabe88db71a22b92c19c | documented exclusion - SHA: commit/blob hash |
| P453 | 532@18 | iv | d2bb7aca68942ce921518cdfc71199737eedaac8 | documented exclusion - SHA: commit/blob hash |
| P453 | 539@17 | v | BLOCKED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 606@17 | v | ACTIVE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 610@18 | iv | 5b8cddec05434e905f58957265fc69164151c955 | documented exclusion - SHA: commit/blob hash |
| P453 | 611@18 | iv | 7988b89cbdb26b21d1d960769e04808864cb98d7 | documented exclusion - SHA: commit/blob hash |
| P453 | 645@18 | iv | 2064eee0182a7b9eb3a8fdcb6652b0dc4ad516e3 | documented exclusion - SHA: commit/blob hash |
| P453 | 646@18 | iv | f3568c76761bcfaf7d2412d1aefe66fff8affe19 | documented exclusion - SHA: commit/blob hash |
| P453 | 665@15 | i | API | named gap - first use before any expansion on this page |
| P453 | 666@16 | i | HMAC | named gap - first use before any expansion on this page |
| P453 | 668@16 | i | WAL | named gap - first use before any expansion on this page |
| P453 | 675@17 | iv | 5cd844bb65813efd798e41ab52ff9003ff23366f | documented exclusion - SHA: commit/blob hash |
| P453 | 678@27 | iii | tools/aegis_delivery_control/README.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 682@18 | iii | tools/aegis_delivery_control/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 687@17 | iv | 497a4529 | documented exclusion - SHA: commit/blob hash |
| P453 | 688@17 | iv | 497a4529b84ec223245e001213271a9266514f62 | documented exclusion - SHA: commit/blob hash |
| P453 | 689@17 | iv | ba13394 | documented exclusion - SHA: commit/blob hash |
| P453 | 690@17 | iv | ba133941a5ae897b6202fa9788b183da28b3f12a | documented exclusion - SHA: commit/blob hash |
| P453 | 691@17 | iv | 8456a36 | documented exclusion - SHA: commit/blob hash |
| P453 | 692@17 | iv | 8456a369b64dc3f6ef87e4423a8e877ed0525316 | documented exclusion - SHA: commit/blob hash |
| P453 | 693@17 | iv | 8dfe237 | documented exclusion - SHA: commit/blob hash |
| P453 | 694@17 | iv | 8dfe237280f8837c6254e456767e405d44fbd148 | documented exclusion - SHA: commit/blob hash |
| P453 | 698@17 | iv | be552fb | documented exclusion - SHA: commit/blob hash |
| P453 | 699@17 | iv | be552fb778ec50fd0cbe82eff9f1022235ec11d8 | documented exclusion - SHA: commit/blob hash |
| P453 | 700@16 | v | COMPLETE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 705@16 | i | NO | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P453 | 707@16 | i | OFFLINE | named gap - first use before any expansion on this page |
| P453 | 722@18 | iii | tools/aegis_delivery_control/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 723@18 | iii | tools/aegis_delivery_control/tests/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 724@18 | iii | tools/behavioral_eval_runner/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 725@18 | iii | tools/behavioral_eval_runner/adapters/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 726@18 | iii | tools/behavioral_eval_runner/graders/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 727@18 | iii | tools/behavioral_eval_runner/judge/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 728@18 | iii | tools/behavioral_eval_runner/tests/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 729@18 | iii | scripts/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 730@18 | iii | scripts/ci/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 731@18 | iii | scripts/tests/__pycache__/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 745@18 | iv | fccf4968 | documented exclusion - SHA: commit/blob hash |
| P453 | 745@42 | iv | 8ef2ce8fe1ba | documented exclusion - SHA: commit/blob hash |
| P453 | 751@17 | v | REVISE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 772@19 | iii | tools/aegis_delivery_control/adapters.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 774@19 | iii | tools/aegis_delivery_control/authority.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 776@19 | iii | tools/aegis_delivery_control/cli.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 778@19 | iii | tools/aegis_delivery_control/contracts.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 780@19 | iii | tools/aegis_delivery_control/dispatch.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 782@19 | iii | tools/aegis_delivery_control/storage.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 784@19 | iii | tools/aegis_delivery_control/tests/test_dispatch.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 786@19 | iii | tools/aegis_delivery_control/tests/test_engine.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 788@19 | iii | tools/aegis_delivery_control/tests/test_platform.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 790@19 | iii | tools/aegis_delivery_control/tests/test_recovery.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 792@19 | iii | tools/aegis_delivery_control/tests/test_storage.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 793@19 | iii | docs/README.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 794@19 | iii | docs/roadmaps/resumable-control-plane-backlog.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 805@19 | iii | docs/design/resumable-control-plane-v1.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 806@19 | iii | docs/approvals/APPROVAL_REGISTER.md | documented exclusion - PATH: non-backticked path identifier |
| P453 | 843@18 | iv | a60cdd7b0340123a37473bdd8b57887a2b317072 | documented exclusion - SHA: commit/blob hash |
| P453 | 846@17 | i | KNOWN | named gap - first use before any expansion on this page |
| P453 | 882@17 | i | YES | named gap - first use before any expansion on this page |
| P453 | 884@18 | iv | 7114bc79b0f960d94c8a78b093781268532ebd41 | documented exclusion - SHA: commit/blob hash |
| P453 | 904@18 | iv | 2de362612f43c125829ff8c73e22bcdcfa6147c0 | documented exclusion - SHA: commit/blob hash |
| P453 | 925@18 | iv | c3c94bf3d367380d1ff60835fb72cb300e69c3e4 | documented exclusion - SHA: commit/blob hash |
| P453 | 927@18 | iv | 52e73db | documented exclusion - SHA: commit/blob hash |
| P453 | 928@17 | v | RUNNING | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 940@18 | iv | 13bda54b9bc63e962a3900ac16640fd2bb18d304 | documented exclusion - SHA: commit/blob hash |
| P453 | 943@17 | i | EFFECT | named gap - first use before any expansion on this page |
| P453 | 956@18 | iv | 39b3268adc984e3d0b10e55a42fe37a172229e60 | documented exclusion - SHA: commit/blob hash |
| P453 | 972@17 | i | ACTIVITY | named gap - first use before any expansion on this page |
| P453 | 979@17 | v | UNAVAILABLE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 987@17 | i | IDLE | named gap - first use before any expansion on this page |
| P453 | 992@18 | iv | a0d27bbdd64d7d86bf080355ca933d28760244ab | documented exclusion - SHA: commit/blob hash |
| P453 | 999@18 | iv | 9599bcb748f2290f328561704c860f5cb3b9c4c3 | documented exclusion - SHA: commit/blob hash |
| P453 | 1013@18 | iv | 2bd6112215d78937bb23d694aa933eebf8d417e2 | documented exclusion - SHA: commit/blob hash |
| P453 | 1015@17 | i | OUTCOME | named gap - first use before any expansion on this page |
| P453 | 1017@17 | i | BILLING | named gap - first use before any expansion on this page |
| P453 | 1020@18 | i | PRAGMA | named gap - first use before any expansion on this page |
| P453 | 1022@18 | i | BEGIN | named gap - first use before any expansion on this page |
| P453 | 1045@17 | i | LAUNCHED | named gap - first use before any expansion on this page |
| P453 | 1058@18 | iv | a6b2d8624400d7af3be2cb309db01864d6e8e472 | documented exclusion - SHA: commit/blob hash |
| P453 | 1066@17 | v | COMPLETED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 1082@19 | iv | 39ad374a172122c14d06070f65c1e033da3b5c83 | documented exclusion - SHA: commit/blob hash |
| P453 | 1094@19 | iv | bbc96cffc31b8d1c82ba8877309d14674f133ff5 | documented exclusion - SHA: commit/blob hash |
| P453 | 1109@19 | iv | cf09be260bbffcb78dc44847b317d6c4a0de8237 | documented exclusion - SHA: commit/blob hash |
| P453 | 1110@19 | iv | 676c4e2bc366290f28802721cd1dd99467a71707 | documented exclusion - SHA: commit/blob hash |
| P453 | 1129@20 | iii | tests/_trusted_readiness_store.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1135@51 | iii | tools/aegis_delivery_control/tests | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1144@23 | ii | api | documented exclusion - PROSE: lowercase technical/audience prose |
| P453 | 1148@30 | iii | tools/aegis_delivery_control/dashboard | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1166@19 | iv | 7114bc7 | documented exclusion - SHA: commit/blob hash |
| P453 | 1166@28 | iv | 2de3626 | documented exclusion - SHA: commit/blob hash |
| P453 | 1168@18 | i | DRAFT | named gap - first use before any expansion on this page |
| P453 | 1169@18 | v | OPEN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 1175@19 | iv | 384b3eb | documented exclusion - SHA: commit/blob hash |
| P453 | 1175@28 | iv | c3c94bf | documented exclusion - SHA: commit/blob hash |
| P453 | 1176@19 | iv | 384b3eb5b7e9880dd920477cb1bd98e90e6a29c6 | documented exclusion - SHA: commit/blob hash |
| P453 | 1182@28 | iv | 13bda54 | documented exclusion - SHA: commit/blob hash |
| P453 | 1189@19 | iv | 0cdb6d1 | documented exclusion - SHA: commit/blob hash |
| P453 | 1189@28 | iv | 39b3268 | documented exclusion - SHA: commit/blob hash |
| P453 | 1199@19 | iv | 511f590 | documented exclusion - SHA: commit/blob hash |
| P453 | 1199@28 | iv | a0d27bb | documented exclusion - SHA: commit/blob hash |
| P453 | 1205@19 | iv | 9b4cc6f | documented exclusion - SHA: commit/blob hash |
| P453 | 1205@28 | iv | 9599bcb | documented exclusion - SHA: commit/blob hash |
| P453 | 1211@19 | iv | 637b2caf026ae638ae5ba34af93a788a2c3d6512 | documented exclusion - SHA: commit/blob hash |
| P453 | 1229@19 | iv | 3406e3e22f80f461e35f529900c289c7b93c46ac | documented exclusion - SHA: commit/blob hash |
| P453 | 1239@19 | iv | 8ac0c342b7648b4eb5b8697e260271480af64244 | documented exclusion - SHA: commit/blob hash |
| P453 | 1256@108 | iii | tools/aegis_delivery_control/engine.py | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1283@19 | iv | 04f0bee85202d3493b6be7bf67db32bf914b59fc | documented exclusion - SHA: commit/blob hash |
| P453 | 1311@19 | iv | 15cfdc50c5ae24ad1f5ac88ce623aa489ac6575a | documented exclusion - SHA: commit/blob hash |
| P453 | 1380@19 | iv | b9f31c3f40eab222f0fd5bd47dba60784ef1eae1 | documented exclusion - SHA: commit/blob hash |
| P453 | 1404@19 | iv | a9dbeab2b2e28f2914df32dd55558a2d051517e6 | documented exclusion - SHA: commit/blob hash |
| P453 | 1417@18 | i | READY | named gap - first use before any expansion on this page |
| P453 | 1492@18 | i | APPLY | named gap - first use before any expansion on this page |
| P453 | 1519@20 | iii | tools/aegis_delivery_control/dashboard/ | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1520@20 | iii | tools/aegis_delivery_control/dashboard/index.html | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1522@20 | iii | tools/aegis_delivery_control/dashboard/styles.css | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1523@20 | iii | tools/aegis_delivery_control/dashboard/app.js | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1529@37 | iii | scripts/tests | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1531@19 | v | 35846882128 | documented exclusion - RANGE: numeric range/unit token |
| P453 | 1532@18 | v | DONE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 1540@15 | i | ETA | named gap - first use before any expansion on this page |
| P453 | 1551@17 | iv | 1af342712d27d5e6ea482b3f451106b4dccaf125 | documented exclusion - SHA: commit/blob hash |
| P453 | 1604@146 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 1606@251 | ii | workflow | documented exclusion - PROSE: lowercase technical/audience prose |
| P453 | 1610@2 | i | AC | named gap - first use before any expansion on this page |
| P453 | 1612@17 | v | MET | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P453 | 1616@18 | i | PROC | named gap - first use before any expansion on this page |
| P453 | 1631@33 | iv | c6e5d5649bf8 | documented exclusion - SHA: commit/blob hash |
| P453 | 1632@31 | iv | b5fd9feda972 | documented exclusion - SHA: commit/blob hash |
| P453 | 1633@31 | iv | 08d91a834460 | documented exclusion - SHA: commit/blob hash |
| P453 | 1634@23 | iv | 6a27b5c8e690 | documented exclusion - SHA: commit/blob hash |
| P453 | 1636@65 | v | <n> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P453 | 1638@201 | iii | _A/evidence/read-lc360-c1/Crows.txt | documented exclusion - PATH: non-backticked path identifier |
| P453 | 1638@390 | iii | tools/skills-manifest.json | documented exclusion - PATH: non-backticked path identifier |
| P454 | 1@71 | v | 2026-10-18 | documented exclusion - DATE: date/time literal |
| P454 | 1@71 | v | 2026-10 | documented exclusion - DATE: date/time literal |
| P454 | 7@56 | v | 6255178017 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 7@92 | v | ACCEPT | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 7@99 | v | 6255194863 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 7@120 | iv | 60347ee9baf45d59154e2a484d0167c43c363211 | documented exclusion - SHA: commit/blob hash |
| P454 | 7@203 | v | 2026-10-18T21:04:39Z | documented exclusion - DATE: date/time literal |
| P454 | 7@299 | i | PR | named gap - first use before any expansion on this page |
| P454 | 7@359 | iii | docs/evidence/documentation/readability-lane-c-batch-14-2026-10-18.md**. | documented exclusion - PATH: non-backticked path identifier |
| P454 | 7@364 | ii | evidence | documented exclusion - PROSE: lowercase technical/audience prose |
| P454 | 7@387 | ii | readability | documented exclusion - PROSE: lowercase technical/audience prose |
| P454 | 7@412 | v | 14-2026 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 7@420 | v | 10-18 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 9@57 | v | 144-279 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 9@83 | v | 1-13 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 9@104 | v | 304-367 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 9@145 | v | 368-375 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 9@194 | v | 376-383 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 9@241 | iv | 60347ee9 | documented exclusion - SHA: commit/blob hash |
| P454 | 9@261 | iv | a32c2a01 | documented exclusion - SHA: commit/blob hash |
| P454 | 9@281 | iv | e2a8d0d3 | documented exclusion - SHA: commit/blob hash |
| P454 | 9@301 | v | 55151039 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 9@321 | iv | 9085bf6a | documented exclusion - SHA: commit/blob hash |
| P454 | 9@341 | iv | 9a5cb28d | documented exclusion - SHA: commit/blob hash |
| P454 | 9@361 | iv | e3f535e4 | documented exclusion - SHA: commit/blob hash |
| P454 | 9@381 | iv | 3ef6c735 | documented exclusion - SHA: commit/blob hash |
| P454 | 9@401 | iv | 6afc845a | documented exclusion - SHA: commit/blob hash |
| P454 | 9@421 | iv | 4b99f69f | documented exclusion - SHA: commit/blob hash |
| P454 | 9@441 | iv | 2c3c6ffe | documented exclusion - SHA: commit/blob hash |
| P454 | 9@461 | v | 38212595 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 9@481 | iv | f325daac | documented exclusion - SHA: commit/blob hash |
| P454 | 9@501 | iv | 7cea211e | documented exclusion - SHA: commit/blob hash |
| P454 | 9@521 | iv | 6f584c9d | documented exclusion - SHA: commit/blob hash |
| P454 | 11@251 | v | 0-153 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 11@265 | v | 154-307 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 11@292 | v | 308-461 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 11@308 | v | 462-613 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 11@418 | iv | 2db1ffb7 | documented exclusion - SHA: commit/blob hash |
| P454 | 13@245 | v | 6250828860 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 13@324 | v | L39-L44 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 17@45 | i | LF | named gap - first use before any expansion on this page |
| P454 | 19@13 | iii | docs/evidence/documentation/2026-09-23-skills-catalog-readability-batch.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 19@41 | v | 2026-09-23 | documented exclusion - DATE: date/time literal |
| P454 | 19@41 | v | 2026-09 | documented exclusion - DATE: date/time literal |
| P454 | 19@90 | iv | daf5099cc7add990fcd734c365f2f68fa4dcb5e1 | documented exclusion - SHA: commit/blob hash |
| P454 | 20@13 | iii | docs/evidence/documentation/aegis-setup-routing-readability-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 20@89 | iv | 77ebfc5c60fe0a66379b912469348e118f5dd172 | documented exclusion - SHA: commit/blob hash |
| P454 | 21@13 | iii | docs/evidence/documentation/agent-contributor-docs-readability-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 21@92 | iv | b5605535103dd989d40472b0565ca4917d35aed1 | documented exclusion - SHA: commit/blob hash |
| P454 | 22@13 | iii | docs/evidence/documentation/agentic-loop-retry-correction-2026-09-24.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 22@71 | v | 2026-09-24 | documented exclusion - DATE: date/time literal |
| P454 | 22@87 | iv | fda5a4e39d034f8d1601e631ef78d371c3a89975 | documented exclusion - SHA: commit/blob hash |
| P454 | 23@13 | iii | docs/evidence/documentation/ber-backlog-readability-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 23@81 | iv | b152d293a65202cd967a6154bee8da3a4badcfdd | documented exclusion - SHA: commit/blob hash |
| P454 | 24@13 | iii | docs/evidence/documentation/ber-runner-command-effects-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 24@84 | iv | 7cf6f256447f5935512d9d30d0e6470bb29298b4 | documented exclusion - SHA: commit/blob hash |
| P454 | 25@13 | iii | docs/evidence/documentation/bound-field-digest-corrections-2026-10-15.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 25@72 | v | 2026-10-15 | documented exclusion - DATE: date/time literal |
| P454 | 25@88 | iv | 0fa25dc226bea96928c6c609bb669fb046e892e7 | documented exclusion - SHA: commit/blob hash |
| P454 | 26@13 | iii | docs/evidence/documentation/cloud-skill-readability-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 26@81 | iv | 29dccef847a51882b2e78f11778a533ac4f3b4f6 | documented exclusion - SHA: commit/blob hash |
| P454 | 31@38 | v | L2841-2862 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 31@227 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 31@250 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 34@16 | v | L1-57 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 35@71 | v | L4 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 35@78 | v | L8 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 35@82 | i | README | named gap - first use before any expansion on this page |
| P454 | 35@89 | v | L36 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 40@11 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 44@16 | v | L1-48 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 45@72 | v | L5 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 45@83 | i | UTC | named gap - first use before any expansion on this page |
| P454 | 45@87 | v | L44 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 54@16 | v | L1-56 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 55@65 | i | AGENTS | named gap - first use before any expansion on this page |
| P454 | 55@72 | v | L6 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 55@100 | i | HISTORY | named gap - first use before any expansion on this page |
| P454 | 55@108 | v | L26 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 65@65 | i | SKILL | named gap - first use before any expansion on this page |
| P454 | 74@16 | v | L1-62 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 75@72 | i | APR | named gap - first use before any expansion on this page |
| P454 | 75@76 | v | L7 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 75@102 | i | DEC | named gap - first use before any expansion on this page |
| P454 | 75@106 | v | L37 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 75@111 | i | WP | named gap - first use before any expansion on this page |
| P454 | 75@114 | v | L38 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 75@119 | i | BKL | named gap - first use before any expansion on this page |
| P454 | 75@123 | v | L39 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 75@132 | v | L60 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 84@16 | v | L1-30 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 85@93 | v | L9 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 85@112 | v | L17 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 94@16 | v | L1-1559 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 94@193 | i | AI | named gap - first use before any expansion on this page |
| P454 | 95@71 | v | L3 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@82 | i | SD | named gap - first use before any expansion on this page |
| P454 | 95@85 | v | L16 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@90 | i | HTML | named gap - first use before any expansion on this page |
| P454 | 95@95 | v | L42 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@100 | i | SHA | named gap - first use before any expansion on this page |
| P454 | 95@116 | v | L58 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@121 | i | AEGIS | named gap - first use before any expansion on this page |
| P454 | 95@127 | v | L67 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@141 | i | DCO | named gap - first use before any expansion on this page |
| P454 | 95@145 | v | L69 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@150 | i | CR | named gap - first use before any expansion on this page |
| P454 | 95@153 | v | L108 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@159 | i | CRLF | named gap - first use before any expansion on this page |
| P454 | 95@179 | i | UTF | named gap - first use before any expansion on this page |
| P454 | 95@183 | v | L113 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@189 | i | ASCII | named gap - first use before any expansion on this page |
| P454 | 95@195 | v | L121 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@201 | i | CI | named gap - first use before any expansion on this page |
| P454 | 95@210 | i | API | named gap - first use before any expansion on this page |
| P454 | 95@214 | v | L202 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@220 | i | WRONG | named gap - first use before any expansion on this page |
| P454 | 95@226 | v | L392 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@232 | i | DO | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P454 | 95@235 | v | L660 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@244 | v | L832 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@250 | v | L63 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@254 | v | L833 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@260 | v | L71 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@270 | v | L11 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@274 | v | L834 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@280 | v | L111 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@291 | v | L97 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@301 | v | L137 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@306 | v | L835 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@312 | v | L141 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@323 | v | L149 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@334 | v | L258 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@339 | v | L836 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@355 | v | L263 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@366 | v | L269 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@377 | v | L297 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@382 | v | L837 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@388 | v | L303 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@399 | v | L308 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@414 | v | L838 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@420 | v | L369 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@431 | v | L371 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@442 | v | L381 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@447 | v | L839 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@453 | v | L389 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@464 | v | L398 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@475 | v | L405 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@480 | v | L840 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@486 | v | L416 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@491 | v | L841 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@497 | v | L443 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@502 | v | L842 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@508 | v | L461 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@513 | v | L843 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@519 | v | L504 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@540 | v | L882 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@546 | i | TEXT | named gap - first use before any expansion on this page |
| P454 | 95@557 | v | UNAVAILABILITY | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 95@581 | v | L897 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@587 | v | L35 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@591 | v | L950 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@597 | v | L358 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@608 | v | L384 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@613 | v | L951 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@619 | v | L48 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@623 | v | L952 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@629 | v | L481 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@640 | v | L734 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@645 | v | L953 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@651 | v | L334 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@656 | v | L954 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@662 | v | L280 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@667 | v | L955 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@673 | v | L492 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@678 | v | L956 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@684 | v | L215 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@689 | v | L957 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@695 | v | L100 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@700 | v | L958 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@706 | v | L101 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@728 | v | L109 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@739 | v | L125 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@750 | v | L126 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@761 | v | L291 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@772 | v | L185 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@777 | v | L1068 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@784 | v | L74 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@795 | v | L34 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@799 | v | L1074 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@806 | v | L19 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@810 | v | L1075 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@817 | v | L197 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@829 | v | L195 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@834 | v | L1078 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@845 | v | L1080 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@852 | v | L286 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@857 | v | L1135 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@864 | v | L895 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@876 | v | L898 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@881 | v | L1138 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@888 | v | L879 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@893 | v | L1139 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@900 | v | L528 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@905 | v | L1140 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@917 | v | L1141 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@924 | v | L530 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@929 | v | L1170 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@936 | v | L1001 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@942 | v | L1175 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@952 | v | L1252 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@959 | v | L1126 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@965 | v | L1268 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@972 | v | L1056 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@978 | v | L1269 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@985 | v | L1122 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@991 | v | L1270 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@998 | v | L537 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1010 | v | L541 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1022 | v | L551 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1034 | v | L24 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1038 | v | L1282 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1045 | v | L555 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1050 | v | L1284 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1057 | v | L1058 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1063 | v | L1285 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1070 | v | L1125 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1076 | v | L1287 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1083 | v | L1265 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1089 | v | L1357 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1096 | v | L114 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1101 | v | L1358 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1108 | v | L116 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1120 | v | L118 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1132 | v | L1200 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1151 | v | L1363 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1158 | v | L1315 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1164 | v | L1395 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1171 | v | L129 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1176 | v | L1396 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1183 | v | L242 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1188 | v | L1397 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1195 | v | L245 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1207 | v | L503 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1212 | v | L1399 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1219 | v | L507 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1224 | v | L1428 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1231 | v | L1211 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1237 | v | L1430 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1244 | v | L1320 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1250 | v | L1431 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1260 | v | L1477 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1267 | v | L23 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1271 | v | L1483 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1278 | v | L236 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1283 | v | L1485 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1290 | v | L237 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1302 | v | L239 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1314 | v | L249 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1326 | v | L262 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1331 | v | L1486 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1338 | v | L356 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1343 | v | L1488 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1350 | v | L359 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1362 | v | L370 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1367 | v | L1489 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1374 | v | L375 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1386 | v | L378 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1398 | v | L379 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1410 | v | L385 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1415 | v | L1490 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1422 | v | L387 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1434 | v | L463 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1439 | v | L1491 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1446 | v | L473 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1458 | v | L509 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1463 | v | L1492 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1470 | v | L512 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1482 | v | L817 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1487 | v | L1494 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1494 | v | L820 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1518 | v | L906 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1523 | v | L1495 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1530 | v | L910 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1553 | v | L1498 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1560 | v | L884 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1565 | v | L1544 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 95@1572 | v | L890 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 104@16 | v | L1-59 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 105@65 | i | AWS | named gap - first use before any expansion on this page |
| P454 | 112@39 | ii | token | documented exclusion - PROSE: lowercase technical/audience prose |
| P454 | 112@45 | ii | inventory | documented exclusion - PROSE: lowercase technical/audience prose |
| P454 | 112@57 | i | ONE | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P454 | 114@20 | i | REAL | named gap - first use before any expansion on this page |
| P454 | 114@219 | i | DOTALL | named gap - first use before any expansion on this page |
| P454 | 120@16 | iv | ecfa411 | documented exclusion - SHA: commit/blob hash |
| P454 | 125@18 | iii | docs/skills-catalog.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 127@17 | iv | b2c6db2fdf90eee20aa4de52d184076b7e447f4e | documented exclusion - SHA: commit/blob hash |
| P454 | 128@17 | iv | ad8c1cef62527464aff2e698b58b094a790b058f | documented exclusion - SHA: commit/blob hash |
| P454 | 135@28 | iii | scripts/validate-skills.py | documented exclusion - PATH: non-backticked path identifier |
| P454 | 137@26 | iii | tools/aegis_setup/README.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 145@43 | ii | api | documented exclusion - PROSE: lowercase technical/audience prose |
| P454 | 146@27 | iii | tools/aegis_setup/tests/test_routing_contract.py | documented exclusion - PATH: non-backticked path identifier |
| P454 | 152@16 | i | JSON | named gap - first use before any expansion on this page |
| P454 | 163@17 | iv | d5b007b0a3cc2bd43806a16970f19c84be9a86b0 | documented exclusion - SHA: commit/blob hash |
| P454 | 164@16 | i | YAML | named gap - first use before any expansion on this page |
| P454 | 172@39 | ii | workflow | documented exclusion - PROSE: lowercase technical/audience prose |
| P454 | 186@16 | i | ETA | named gap - first use before any expansion on this page |
| P454 | 197@16 | i | BER | named gap - first use before any expansion on this page |
| P454 | 198@17 | iv | cf63696 | documented exclusion - SHA: commit/blob hash |
| P454 | 210@16 | iv | ebaba9362e3eedba2f419a9072c6477f3ce23024 | documented exclusion - SHA: commit/blob hash |
| P454 | 215@27 | iii | tools/behavioral_eval_runner/README.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 217@38 | ii | json | documented exclusion - PROSE: lowercase technical/audience prose |
| P454 | 230@23 | v | REVISE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 231@17 | v | 6207351316 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 235@17 | v | 6237455039 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 238@17 | iv | 078ec42572ff330a | documented exclusion - SHA: commit/blob hash |
| P454 | 240@17 | iv | 14f1cc5d96ee42c6 | documented exclusion - SHA: commit/blob hash |
| P454 | 242@17 | iv | 7da4fe63b26219de | documented exclusion - SHA: commit/blob hash |
| P454 | 245@16 | i | PROC | named gap - first use before any expansion on this page |
| P454 | 252@17 | i | AEGIS-APR-101 | named gap - first use before any expansion on this page |
| P454 | 258@40 | v | → | documented exclusion - OPERATOR: operator glyph |
| P454 | 273@18 | iv | 3913683c686e6e71 | documented exclusion - SHA: commit/blob hash |
| P454 | 274@18 | v | 2026-10-16T04:50:31Z | documented exclusion - DATE: date/time literal |
| P454 | 275@18 | iv | 8d441a1bfdff46d9 | documented exclusion - SHA: commit/blob hash |
| P454 | 276@18 | v | 2026-10-15T20:58:34Z | documented exclusion - DATE: date/time literal |
| P454 | 277@18 | iv | b1acc2b2f5817fab | documented exclusion - SHA: commit/blob hash |
| P454 | 278@18 | iv | ccfe63ff90cfdb04 | documented exclusion - SHA: commit/blob hash |
| P454 | 279@18 | iv | 7cf3094b11ba4339 | documented exclusion - SHA: commit/blob hash |
| P454 | 280@18 | v | 2026-10-16T01:41:20Z | documented exclusion - DATE: date/time literal |
| P454 | 281@18 | iv | 755e1656024f75f9 | documented exclusion - SHA: commit/blob hash |
| P454 | 282@18 | iv | d10fb1e4977b8ccb | documented exclusion - SHA: commit/blob hash |
| P454 | 283@18 | v | 2026-10-16T01:43:57Z | documented exclusion - DATE: date/time literal |
| P454 | 284@18 | iv | 83e5d149314467e3 | documented exclusion - SHA: commit/blob hash |
| P454 | 285@18 | iv | bd9ccf55efbead2d | documented exclusion - SHA: commit/blob hash |
| P454 | 286@18 | iv | 1fcd0143e13198a3 | documented exclusion - SHA: commit/blob hash |
| P454 | 287@18 | v | 2026-10-16T01:48:55Z | documented exclusion - DATE: date/time literal |
| P454 | 288@18 | iv | 8f2196d6684174ef | documented exclusion - SHA: commit/blob hash |
| P454 | 289@18 | iv | 00092958ec2cc906 | documented exclusion - SHA: commit/blob hash |
| P454 | 290@18 | iv | 121a60bce86cff98 | documented exclusion - SHA: commit/blob hash |
| P454 | 291@18 | v | 2026-10-15T18:32:37Z | documented exclusion - DATE: date/time literal |
| P454 | 292@18 | v | 2026-10-15T19:03:36Z | documented exclusion - DATE: date/time literal |
| P454 | 293@18 | v | 2026-10-15T19:05:22Z | documented exclusion - DATE: date/time literal |
| P454 | 294@18 | v | 2026-10-15T20:57:26Z | documented exclusion - DATE: date/time literal |
| P454 | 295@18 | v | 2026-10-15T22:06:06Z | documented exclusion - DATE: date/time literal |
| P454 | 296@18 | v | 2026-10-16T01:45:01Z | documented exclusion - DATE: date/time literal |
| P454 | 298@18 | iv | 340a14ee6921277a | documented exclusion - SHA: commit/blob hash |
| P454 | 300@18 | iv | 4e50d937ea45ee8e | documented exclusion - SHA: commit/blob hash |
| P454 | 301@18 | iv | 70ef1815189fe918 | documented exclusion - SHA: commit/blob hash |
| P454 | 302@18 | iv | 71a73c01f92b23eb | documented exclusion - SHA: commit/blob hash |
| P454 | 303@18 | iv | 82ed906d2f228f0e | documented exclusion - SHA: commit/blob hash |
| P454 | 304@18 | iv | e71eeab75d0c0b76 | documented exclusion - SHA: commit/blob hash |
| P454 | 305@17 | v | <n> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 308@18 | iv | 1b72bdbbee456702 | documented exclusion - SHA: commit/blob hash |
| P454 | 309@18 | iv | 55acdd8ab96235ea | documented exclusion - SHA: commit/blob hash |
| P454 | 310@18 | iv | 30b62d11a991abcf | documented exclusion - SHA: commit/blob hash |
| P454 | 311@18 | iv | c34e4d0057b09a3f | documented exclusion - SHA: commit/blob hash |
| P454 | 312@18 | iv | 2667aec80380f2ec | documented exclusion - SHA: commit/blob hash |
| P454 | 313@18 | iv | 5feb2e444d998034 | documented exclusion - SHA: commit/blob hash |
| P454 | 314@18 | iv | 64bf6a407e23e47f | documented exclusion - SHA: commit/blob hash |
| P454 | 315@18 | iv | c455488397c4402a | documented exclusion - SHA: commit/blob hash |
| P454 | 316@18 | iv | 45db39e238a3a4e6 | documented exclusion - SHA: commit/blob hash |
| P454 | 317@18 | iv | 6682e8afc5f8ac5e | documented exclusion - SHA: commit/blob hash |
| P454 | 318@18 | iv | 086faa099024ee57 | documented exclusion - SHA: commit/blob hash |
| P454 | 319@18 | iv | 7c5d5bc30a8e4301 | documented exclusion - SHA: commit/blob hash |
| P454 | 320@17 | v | <STAGE-F-DIGEST-PENDING> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 321@17 | v | PENDING | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 345@18 | iv | 14a96bd772f6083e | documented exclusion - SHA: commit/blob hash |
| P454 | 346@18 | v | 2026-10-16T03:00:16Z | documented exclusion - DATE: date/time literal |
| P454 | 347@18 | v | 2026-10-16T06:26:45Z | documented exclusion - DATE: date/time literal |
| P454 | 357@18 | v | 2026-10-16T07:34:58Z | documented exclusion - DATE: date/time literal |
| P454 | 358@18 | iv | 8aed60d23098b041 | documented exclusion - SHA: commit/blob hash |
| P454 | 362@17 | v | <field> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 363@75 | v | <!-- bound-field: end --> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 368@18 | v | 2026-10-15T19:07:51Z | documented exclusion - DATE: date/time literal |
| P454 | 369@18 | v | 2026-10-16T06:56:17Z | documented exclusion - DATE: date/time literal |
| P454 | 370@18 | v | 2026-10-16T16:17:55Z | documented exclusion - DATE: date/time literal |
| P454 | 375@19 | iii | docs/delivery-workflow.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 377@18 | v | 2026-10-15T21:01:18Z | documented exclusion - DATE: date/time literal |
| P454 | 383@18 | v | 2026-10-16T14:00:20Z | documented exclusion - DATE: date/time literal |
| P454 | 385@18 | iv | 1e2150fefd6c2ea9 | documented exclusion - SHA: commit/blob hash |
| P454 | 388@18 | iv | b8e293e668e5b525 | documented exclusion - SHA: commit/blob hash |
| P454 | 395@17 | v | <published> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 396@17 | v | <reading> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 397@17 | v | <current> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 398@17 | v | <anchor> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 399@17 | v | <reason> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 401@18 | v | 2026-10-16T02:01:52Z | documented exclusion - DATE: date/time literal |
| P454 | 402@18 | v | 2026-10-17T17:17:30Z | documented exclusion - DATE: date/time literal |
| P454 | 403@18 | iv | 8356d7b4c2488102 | documented exclusion - SHA: commit/blob hash |
| P454 | 404@40 | iii | _A/evidence/793-c2/retained/uc-771-2026-10-15T18-24-59Z.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 404@71 | v | 771-2026 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 404@75 | v | 2026-10-15T18-24-59Z | documented exclusion - DATE: date/time literal |
| P454 | 405@18 | iv | f2f1ee17cca7458f | documented exclusion - SHA: commit/blob hash |
| P454 | 408@18 | v | 2026-10-15T18:24:59Z | documented exclusion - DATE: date/time literal |
| P454 | 410@18 | v | 2026-10-16T01:05:24Z | documented exclusion - DATE: date/time literal |
| P454 | 411@18 | iv | 3200b7c5f2d153e5 | documented exclusion - SHA: commit/blob hash |
| P454 | 412@18 | iv | f490c16f | documented exclusion - SHA: commit/blob hash |
| P454 | 413@18 | iv | f490c16f9ed23f3d489e42f7696323bffcce6fd3 | documented exclusion - SHA: commit/blob hash |
| P454 | 416@18 | iv | 87d6b460 | documented exclusion - SHA: commit/blob hash |
| P454 | 417@18 | iv | 988b5067 | documented exclusion - SHA: commit/blob hash |
| P454 | 418@18 | iv | 988b50673cdd0e9ab0c15df891744cd02d1d2d2b | documented exclusion - SHA: commit/blob hash |
| P454 | 419@18 | iv | 9e418c8c | documented exclusion - SHA: commit/blob hash |
| P454 | 420@18 | iv | 9e418c8c63e45caa4bca7fb608d45d0df4d44409 | documented exclusion - SHA: commit/blob hash |
| P454 | 421@18 | iv | f459e93f762993071f99716780ece9c5a9448dc8 | documented exclusion - SHA: commit/blob hash |
| P454 | 422@17 | i | HEAD | named gap - first use before any expansion on this page |
| P454 | 430@18 | iv | 6d4295a9 | documented exclusion - SHA: commit/blob hash |
| P454 | 436@18 | iv | ff975270 | documented exclusion - SHA: commit/blob hash |
| P454 | 437@19 | iii | docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 439@19 | iii | docs/evidence/documentation/readability-lane-c-batch-3-2026-10-15.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 439@72 | v | 3-2026 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 439@79 | v | 10-15 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 441@19 | iii | docs/roadmaps/aegis-documentation-readability-backlog.md | documented exclusion - PATH: non-backticked path identifier |
| P454 | 445@17 | v | <added> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 446@26 | v | <deleted> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 446@37 | v | <path> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 450@17 | v | <f> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 451@27 | v | P | documented exclusion - PLACEHOLDER: placeholder letter token |
| P454 | 451@29 | iii | scripts/ci/check_pr_body_skills.py | documented exclusion - PATH: non-backticked path identifier |
| P454 | 452@29 | iii | scripts/check_dco.py | documented exclusion - PATH: non-backticked path identifier |
| P454 | 455@18 | iv | de2bfe7237d6e853fa81925faa9f68a82881bba7 | documented exclusion - SHA: commit/blob hash |
| P454 | 456@18 | iv | 2fdc91ae | documented exclusion - SHA: commit/blob hash |
| P454 | 457@18 | iv | 88300e711714200a | documented exclusion - SHA: commit/blob hash |
| P454 | 460@18 | iv | d86798fb331fe7d7 | documented exclusion - SHA: commit/blob hash |
| P454 | 465@17 | v | × | documented exclusion - OPERATOR: operator glyph |
| P454 | 466@18 | iv | 2afc2d18 | documented exclusion - SHA: commit/blob hash |
| P454 | 467@18 | iv | 2d1363e0 | documented exclusion - SHA: commit/blob hash |
| P454 | 470@18 | iv | 33ba8ddf7431365e | documented exclusion - SHA: commit/blob hash |
| P454 | 471@18 | iv | d07319919fff1732 | documented exclusion - SHA: commit/blob hash |
| P454 | 473@40 | iii | _A/evidence/793-c2/retained/ | documented exclusion - PATH: non-backticked path identifier |
| P454 | 474@18 | iv | d0731991 | documented exclusion - SHA: commit/blob hash |
| P454 | 475@18 | iv | ab8a8c06 | documented exclusion - SHA: commit/blob hash |
| P454 | 476@18 | iv | ab8a8c0667fd1bcf1ce6644af84d3bcf95aa040e | documented exclusion - SHA: commit/blob hash |
| P454 | 511@18 | v | 2026-10-16T02:09:14Z | documented exclusion - DATE: date/time literal |
| P454 | 512@18 | v | 2026-10-16T04:51:25Z | documented exclusion - DATE: date/time literal |
| P454 | 518@18 | iv | 8e9392f8 | documented exclusion - SHA: commit/blob hash |
| P454 | 520@17 | v | FAILED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 525@60 | iv | 47b64a3afc9117d969e1687b1f3f9084591c5d0b | documented exclusion - SHA: commit/blob hash |
| P454 | 527@60 | iv | d436bb613fcf44dc13384bb689b15cbe6cde5a5d | documented exclusion - SHA: commit/blob hash |
| P454 | 528@18 | v | 6206966415 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 529@18 | iv | c50ce2d9 | documented exclusion - SHA: commit/blob hash |
| P454 | 530@18 | iv | c50ce2d9256d27ad9323e74348f48cb7b38d3c08 | documented exclusion - SHA: commit/blob hash |
| P454 | 531@18 | v | 6206838331 | documented exclusion - RANGE: numeric range/unit token |
| P454 | 539@17 | v | L28 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 550@17 | v | L629 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 559@18 | i | NINE | named gap - first use before any expansion on this page |
| P454 | 560@52 | v | L103 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 560@58 | v | L164 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 560@64 | v | L189 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 561@36 | v | L43 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 561@41 | v | L73 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 561@46 | v | L179 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 577@19 | iv | 6d4295a938705546160f7a44af12c6391570f8c9 | documented exclusion - SHA: commit/blob hash |
| P454 | 595@19 | iv | 3b49811d4c22add9 | documented exclusion - SHA: commit/blob hash |
| P454 | 610@19 | iv | ec2f70f1 | documented exclusion - SHA: commit/blob hash |
| P454 | 611@39 | iv | ec2f70f116efe3c82e16831684221bcd102bd5e4 | documented exclusion - SHA: commit/blob hash |
| P454 | 619@19 | iv | 9c5e5539e551738f | documented exclusion - SHA: commit/blob hash |
| P454 | 620@19 | iv | 4d99ca3bc873c8a6 | documented exclusion - SHA: commit/blob hash |
| P454 | 621@19 | iv | 9cc73216e1ba17a1 | documented exclusion - SHA: commit/blob hash |
| P454 | 628@18 | v | L173 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 629@18 | v | L213 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 633@19 | iv | 4ff17269 | documented exclusion - SHA: commit/blob hash |
| P454 | 634@19 | iv | 4ff17269d681571947dfc9d2e055a8fcdc1152a6 | documented exclusion - SHA: commit/blob hash |
| P454 | 635@19 | iv | 50cf08763e280dbc | documented exclusion - SHA: commit/blob hash |
| P454 | 637@18 | v | MET | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 638@19 | i | NOT | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P454 | 640@18 | v | L136 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 643@19 | v | 2026-10-17T07:08:37Z | documented exclusion - DATE: date/time literal |
| P454 | 644@18 | v | L486 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 645@18 | v | L489 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 647@18 | v | L1210 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 648@18 | v | L545 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 650@18 | v | <this path> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 652@19 | iv | 1e9b1ccf | documented exclusion - SHA: commit/blob hash |
| P454 | 653@75 | iv | 1e9b1ccfc4827835747cc8e847494a838b9af257 | documented exclusion - SHA: commit/blob hash |
| P454 | 658@19 | iv | 349ca6bf | documented exclusion - SHA: commit/blob hash |
| P454 | 659@19 | iv | 349ca6bff98b6f539d9b59f4ed47f16633cdc343 | documented exclusion - SHA: commit/blob hash |
| P454 | 662@18 | v | L20 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 667@18 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P454 | 675@18 | v | L319 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 676@18 | v | L348 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 677@18 | v | L352 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 690@18 | v | L534 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 691@18 | v | L539 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 697@18 | v | L1445 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 698@18 | v | L1449 | documented exclusion - LINE-RANGE: page-line reference |
| P454 | 701@19 | iv | a5386f24 | documented exclusion - SHA: commit/blob hash |
| P454 | 707@19 | iv | a4715d9a | documented exclusion - SHA: commit/blob hash |
| P454 | 708@19 | iv | a4715d9a29e83425cfd29a5e3e92bb4a72d7a1c5 | documented exclusion - SHA: commit/blob hash |
| P454 | 709@19 | iv | db16151c68b62bf7 | documented exclusion - SHA: commit/blob hash |
| P454 | 712@19 | v | 2026-10-17T18:18:51.819850Z | documented exclusion - DATE: date/time literal |
| P454 | 716@42 | iv | 8e9392f8c4df0359f2cccd297af4535a0a2cff7c | documented exclusion - SHA: commit/blob hash |
| P454 | 718@19 | iv | cc1f7a8f | documented exclusion - SHA: commit/blob hash |
| P454 | 721@19 | iv | fa11de2c | documented exclusion - SHA: commit/blob hash |
| P454 | 724@18 | v | <this round's commit> | documented exclusion - PLACEHOLDER: angle/brace placeholder |
| P454 | 737@17 | iv | 70ca4eef13521d27c11754979b2bfb90ce3981c5 | documented exclusion - SHA: commit/blob hash |
| P454 | 769@2 | i | AC | named gap - first use before any expansion on this page |
| P454 | 790@33 | iv | c6e5d5649bf8 | documented exclusion - SHA: commit/blob hash |
| P454 | 791@31 | iv | b5fd9feda972 | documented exclusion - SHA: commit/blob hash |
| P454 | 792@31 | iv | 08d91a834460 | documented exclusion - SHA: commit/blob hash |
| P454 | 793@23 | iv | 6a27b5c8e690 | documented exclusion - SHA: commit/blob hash |
| P454 | 797@201 | iii | _A/evidence/read-lc368-c1/Crows.txt | documented exclusion - PATH: non-backticked path identifier |
| P454 | 797@390 | iii | tools/skills-manifest.json | documented exclusion - PATH: non-backticked path identifier |
| P455 | 1@18 | ii | evidence | documented exclusion - PROSE: lowercase technical/audience prose |
| P455 | 1@42 | v | 376-383 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 1@51 | v | 2026-10-18 | documented exclusion - DATE: date/time literal |
| P455 | 1@51 | v | 2026-10 | documented exclusion - DATE: date/time literal |
| P455 | 3@18 | iv | b5a968a0 | documented exclusion - SHA: commit/blob hash |
| P455 | 3@86 | i | LF | named gap - first use before any expansion on this page |
| P455 | 3@101 | ii | inventory | documented exclusion - PROSE: lowercase technical/audience prose |
| P455 | 3@138 | v | FULL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P455 | 3@147 | v | PARTIAL | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P455 | 3@159 | v | UNRUN | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P455 | 3@169 | v | UNVERIFIED | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P455 | 3@203 | v | 384-391 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 5@105 | iii | _A/evidence/read-lc-376-c1/ | documented exclusion - PATH: non-backticked path identifier |
| P455 | 5@360 | i | PR | named gap - first use before any expansion on this page |
| P455 | 5@368 | iv | 70bb8b45 | documented exclusion - SHA: commit/blob hash |
| P455 | 5@380 | iv | 212146ce | documented exclusion - SHA: commit/blob hash |
| P455 | 5@392 | iv | 96ac2b5b | documented exclusion - SHA: commit/blob hash |
| P455 | 5@404 | iv | 39b2d41b | documented exclusion - SHA: commit/blob hash |
| P455 | 5@416 | iv | 49588dfd | documented exclusion - SHA: commit/blob hash |
| P455 | 5@496 | i | DCO | named gap - first use before any expansion on this page |
| P455 | 9@19 | iv | b5a968a003001a0dd9da4a95c894b23753bf8aef | documented exclusion - SHA: commit/blob hash |
| P455 | 9@105 | v | 2026-10-18T21:24:31Z | documented exclusion - DATE: date/time literal |
| P455 | 9@145 | v | 6255361362 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 9@168 | v | ACCEPT | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P455 | 9@177 | v | 6255394745 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 9@251 | iii | docs/evidence/documentation/readability-lane-c-batch-15-2026-10-18.md; | documented exclusion - PATH: non-backticked path identifier |
| P455 | 9@279 | ii | readability | documented exclusion - PROSE: lowercase technical/audience prose |
| P455 | 9@304 | v | 15-2026 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 9@312 | v | 10-18 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 9@448 | ii | workflow | documented exclusion - PROSE: lowercase technical/audience prose |
| P455 | 11@39 | iv | 2db1ffb7 | documented exclusion - SHA: commit/blob hash |
| P455 | 15@13 | iii | docs/evidence/documentation/contributor-merge-reading-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 15@67 | v | 2026-09-23 | documented exclusion - DATE: date/time literal |
| P455 | 15@67 | v | 2026-09 | documented exclusion - DATE: date/time literal |
| P455 | 15@83 | iv | 4c3e38679d7cf2f99a486d7d005c879e0a5b6c4a | documented exclusion - SHA: commit/blob hash |
| P455 | 16@13 | iii | docs/evidence/documentation/control-plane-backlog-readability-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 16@91 | iv | 2e689b5100ce434f9c02ba9f355f3f73c22d3de5 | documented exclusion - SHA: commit/blob hash |
| P455 | 17@13 | iii | docs/evidence/documentation/control-plane-design-readability-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 17@90 | iv | 0839cf20ed98484f0a91614176ca48504c81d666 | documented exclusion - SHA: commit/blob hash |
| P455 | 18@13 | iii | docs/evidence/documentation/control-plane-guide-fields-readability-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 18@96 | iv | f14ef54e8704f2e87df35bfa365ac92f9cd3abe9 | documented exclusion - SHA: commit/blob hash |
| P455 | 19@13 | iii | docs/evidence/documentation/cp-handoff-pinned-citations-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 19@85 | iv | 71107dab0e09b1f7432a21b2cf97dfbd11ef25df | documented exclusion - SHA: commit/blob hash |
| P455 | 20@13 | iii | docs/evidence/documentation/documentation-backlog-current-reading-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 20@95 | iv | 5fd0ee8d1923c1544b596d47c212dcaf3a126598 | documented exclusion - SHA: commit/blob hash |
| P455 | 21@13 | iii | docs/evidence/documentation/evidence-followup-current-reading-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 21@91 | iv | 323bf9fd55fc24502e4af1557514a261f8d2cb00 | documented exclusion - SHA: commit/blob hash |
| P455 | 22@13 | iii | docs/evidence/documentation/execution-handoff-readability-2026-09-23.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 22@87 | iv | e572796a94cabb0cc09d7c1968382ec1a708ca71 | documented exclusion - SHA: commit/blob hash |
| P455 | 25@74 | v | L1 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 29@29 | v | L2841-2862 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 31@264 | v | MET | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P455 | 36@16 | v | L1-28 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 41@16 | v | L1-53 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 51@16 | v | L1-44 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 56@16 | v | L1-32 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 61@16 | v | L1-23 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 66@16 | v | L1-41 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 67@25 | ii | candidate | documented exclusion - PROSE: lowercase technical/audience prose |
| P455 | 71@16 | v | L1-64 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 75@39 | ii | token | documented exclusion - PROSE: lowercase technical/audience prose |
| P455 | 75@57 | i | ONE | documented exclusion - EMPHASIS: all-caps common emphasis word |
| P455 | 77@20 | i | REAL | named gap - first use before any expansion on this page |
| P455 | 77@219 | i | DOTALL | named gap - first use before any expansion on this page |
| P455 | 77@618 | v | DONE | documented exclusion - STATUS: uppercase lifecycle/status keyword |
| P455 | 77@633 | i | APR | named gap - first use before any expansion on this page |
| P455 | 86@15 | i | APPROVAL | named gap - first use before any expansion on this page |
| P455 | 90@15 | i | CP | named gap - first use before any expansion on this page |
| P455 | 91@15 | i | WP | named gap - first use before any expansion on this page |
| P455 | 97@16 | i | UTC | named gap - first use before any expansion on this page |
| P455 | 107@27 | iii | scripts/validate-skills.py | documented exclusion - PATH: non-backticked path identifier |
| P455 | 120@27 | iii | tools/aegis_delivery_control/README.md | documented exclusion - PATH: non-backticked path identifier |
| P455 | 120@56 | i | README | named gap - first use before any expansion on this page |
| P455 | 133@66 | v | 10-11 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 134@17 | iv | 761915207f7974b3d4cab7fb099216188ef3e968 | documented exclusion - SHA: commit/blob hash |
| P455 | 136@27 | iii | tools/aegis_delivery_control/tests/test_dispatch.py | documented exclusion - PATH: non-backticked path identifier |
| P455 | 137@27 | iii | tools/aegis_delivery_control/cli.py | documented exclusion - PATH: non-backticked path identifier |
| P455 | 138@16 | i | JSON | named gap - first use before any expansion on this page |
| P455 | 147@17 | iv | cedd732df2ae9a843d2c02f213299a31b245a9c5 | documented exclusion - SHA: commit/blob hash |
| P455 | 150@17 | iv | 5cd844bb65813efd798e41ab52ff9003ff23366f | documented exclusion - SHA: commit/blob hash |
| P455 | 155@17 | iv | 24d613ebddd6ff4cd6ce35be772f6a80ad1a85f4 | documented exclusion - SHA: commit/blob hash |
| P455 | 158@16 | iv | e2145b14cf5629c336b4bbcb624ef7f5fcc92f01 | documented exclusion - SHA: commit/blob hash |
| P455 | 159@39 | v | 2026-09-12 | documented exclusion - DATE: date/time literal |
| P455 | 166@43 | i | DELIVERY | named gap - first use before any expansion on this page |
| P455 | 167@16 | i | CI | named gap - first use before any expansion on this page |
| P455 | 170@16 | i | BER | named gap - first use before any expansion on this page |
| P455 | 179@17 | iv | 831dd75 | documented exclusion - SHA: commit/blob hash |
| P455 | 213@234 | iii | _A/evidence/read-lc-376-c1/table-check.txt | documented exclusion - PATH: non-backticked path identifier |
| P455 | 217@25 | i | BATCH | named gap - first use before any expansion on this page |
| P455 | 217@329 | v | 6250828860 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 217@487 | v | L45-L47 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 217@720 | v | L36-L40 | documented exclusion - LINE-RANGE: page-line reference |
| P455 | 219@283 | v | 1-14 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 221@54 | iii | _A/evidence/read-lc-376-c1/Crows.txt | documented exclusion - PATH: non-backticked path identifier |
| P455 | 221@267 | iii | _A/... | documented exclusion - PATH: non-backticked path identifier |
| P455 | 225@2 | i | AC | named gap - first use before any expansion on this page |
| P455 | 231@18 | i | PROC | named gap - first use before any expansion on this page |
| P455 | 233@83 | v | 144-279 | documented exclusion - RANGE: numeric range/unit token |
| P455 | 240@86 | i | SKILL | named gap - first use before any expansion on this page |
| P455 | 240@98 | iv | c6e5d5649bf8 | documented exclusion - SHA: commit/blob hash |
| P455 | 241@94 | iv | b5fd9feda972 | documented exclusion - SHA: commit/blob hash |
| P455 | 242@94 | iv | 08d91a834460 | documented exclusion - SHA: commit/blob hash |
| P455 | 243@78 | iv | 6a27b5c8e690 | documented exclusion - SHA: commit/blob hash |
| P455 | 247@440 | iii | tools/skills-manifest.json | documented exclusion - PATH: non-backticked path identifier |
| P455 | 247@462 | ii | json | documented exclusion - PROSE: lowercase technical/audience prose |

## 4. Counts, codes and reconciliation (all tallies sum to 4166)
| Page | Rows | i | ii | iii | iv | v | defined | named | excluded |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P448 | 257 | 47 | 4 | 0 | 48 | 158 | 5 | 38 | 214 |
| P449 | 333 | 34 | 5 | 1 | 203 | 90 | 3 | 30 | 300 |
| P450 | 1427 | 177 | 8 | 7 | 721 | 514 | 0 | 171 | 1256 |
| P451 | 790 | 165 | 8 | 37 | 312 | 268 | 0 | 156 | 634 |
| P452 | 247 | 61 | 8 | 30 | 52 | 96 | 0 | 60 | 187 |
| P453 | 504 | 91 | 8 | 55 | 97 | 253 | 0 | 88 | 416 |
| P454 | 503 | 40 | 7 | 24 | 122 | 310 | 0 | 37 | 466 |
| P455 | 105 | 20 | 7 | 18 | 26 | 34 | 0 | 19 | 86 |
| **Total** | **4166** | **635** | **55** | **172** | **1581** | **1723** | **3** | **280** | **2459** |

**Class sum:** 301+45+17+1235+1144=4166. **Disposition sum:** 3+280+2459=4166. **Exclusion codes sum:** PROSE 55, RANGE 125, DATE 76, STATUS 147, SHA 389, COMMAND 29, PATH 346, LITERAL 619, EMPHASIS 398, PLACEHOLDER 68, LINE-RANGE 1292, OPERATOR 15 = 2459. **Exclusion-code legend:** DATE date/time literal; LINE-RANGE page-line reference; STATUS uppercase lifecycle/status keyword; RANGE numeric range/unit token; PLACEHOLDER angle/brace/letter placeholder; OPERATOR operator glyph; PROSE lowercase technical/audience prose; EMPHASIS all-caps common emphasis word; PATH file/path identifier; COMMAND command/CLI token; SHA commit/blob hash; LITERAL backticked literal/prose identifier. One reconciliation; every tally above sums; zero duplicate mentions (unique keys).

## 5. Whole-page B1-B6 evidence per page; mixed-pin/drift facts
### P448 - union 448 - docs/evidence/documentation/readability-lane-b-batch-9-2026-10-18.md - re-pin - read whole L1-175
- **B1:** title/purpose anchor L1 Readability re-read record — lane B, batch 9 (eight whole-page re-reads); lane record with purpose/scope; audience inferred from record context.
- **B2:** 257 candidate rows; defined 5; named gaps 38; documented exclusions 214; all rows in section 3.
- **B3:** headings/anchors: # Readability re-read record — lane B, batch 9 (eight whole-page re-reads); ## 1. Plan binding and implementation base; ## 2. Lane derivation at this implementation base — re-run, not handed down; ## 3. Change scope and diff accounting; command/example references: git metadata differs from the reader identity but ca; git metadata differs from the reader identity but ca.
- **B4:** page is a batch/evidence record; shipped-vs-proposed claims are record evidence, not a deployed system; no synthetic test described as deployed.
- **B5:** 0 markdown links scanned; navigation/contract preserved; no page edit.
- **B6:** read-only reader independence is **UNVERIFIED**; no non-author purpose-and-use interview claimed; never FULL-supporting.

### P449 - union 449 - docs/evidence/documentation/readability-lane-c-batch-1-2026-10-15.md - pinned-equal - read whole L1-852
- **B1:** title/purpose anchor L1 Readability Phase 4 re-read lane C — Stage C batch record, batch 1, 2026-10-15; lane record with purpose/scope; audience inferred from record context.
- **B2:** 333 candidate rows; defined 3; named gaps 30; documented exclusions 300; all rows in section 3.
- **B3:** headings/anchors: # Readability Phase 4 re-read lane C — Stage C batch record, batch 1, 2026-10-15; ## 1. The instrument's figures at the base, quoted; ## 2. Lane derivation and batch selection, by command; ## 3. Per-page dispositions — 8 of 8 read whole; 6 accepted unchanged with **no row append; command/example references: git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39; git ls-tree -r --name-only e2a3e20b7c20ef8385b219b3.
- **B4:** page is a batch/evidence record; shipped-vs-proposed claims are record evidence, not a deployed system; no synthetic test described as deployed.
- **B5:** 1 markdown links scanned; navigation/contract preserved; no page edit.
- **B6:** read-only reader independence is **UNVERIFIED**; no non-author purpose-and-use interview claimed; never FULL-supporting.

### P450 - union 450 - docs/evidence/documentation/readability-lane-c-batch-10-2026-10-18.md - re-pin - read whole L1-2521
- **B1:** title/purpose anchor L1 Readability Phase 4 re-read lane C - Stage C batch record, batch 10, 2026-10-18; lane record with purpose/scope; audience inferred from record context.
- **B2:** 1427 candidate rows; defined 0; named gaps 171; documented exclusions 1256; all rows in section 3.
- **B3:** headings/anchors: # Readability Phase 4 re-read lane C - Stage C batch record, batch 10, 2026-10-18; ## 1. Plan binding and derivation; ## 2. The eight pages; ## 3. Whole-page re-read evidence and canonical B1-B6 per page; command/example references: git rev-parse <head>^{tree}` | documented exclusion -; git archive` | documented exclusion - inline code/p.
- **B4:** page is a batch/evidence record; shipped-vs-proposed claims are record evidence, not a deployed system; no synthetic test described as deployed.
- **B5:** 4 markdown links scanned; navigation/contract preserved; no page edit.
- **B6:** read-only reader independence is **UNVERIFIED**; no non-author purpose-and-use interview claimed; never FULL-supporting.

### P451 - union 451 - docs/evidence/documentation/readability-lane-c-batch-11-2026-10-18.md - re-pin - read whole L1-1574
- **B1:** title/purpose anchor L1 Readability Phase 4 re-read lane C - Stage C batch record, batch 11, 2026-10-18; lane record with purpose/scope; audience inferred from record context.
- **B2:** 790 candidate rows; defined 0; named gaps 156; documented exclusions 634; all rows in section 3.
- **B3:** headings/anchors: # Readability Phase 4 re-read lane C - Stage C batch record, batch 11, 2026-10-18; ## 1. Plan binding and derivation; ## 2. The eight pages; ## 3. Whole-page re-read evidence and canonical B1-B6 per page; command/example references: git diff --check | documented exclusion - inline; git hash-object | documented exclusion - inline code/id.
- **B4:** page is a batch/evidence record; shipped-vs-proposed claims are record evidence, not a deployed system; no synthetic test described as deployed.
- **B5:** 0 markdown links scanned; navigation/contract preserved; no page edit.
- **B6:** read-only reader independence is **UNVERIFIED**; no non-author purpose-and-use interview claimed; never FULL-supporting.

### P452 - union 452 - docs/evidence/documentation/readability-lane-c-batch-12-2026-10-18.md - re-pin - read whole L1-854
- **B1:** title/purpose anchor L1 Readability Phase 4 re-read lane C - Stage C batch record, batch 12, 2026-10-18; lane record with purpose/scope; audience inferred from record context.
- **B2:** 247 candidate rows; defined 0; named gaps 60; documented exclusions 187; all rows in section 3.
- **B3:** headings/anchors: # Readability Phase 4 re-read lane C - Stage C batch record, batch 12, 2026-10-18; ## 1. Plan binding and derivation; ## 2. The eight pages; ## 3. Whole-page re-read evidence and canonical B1-B6 per page; command/example references: git diff --check | documented exclusion - inline; git diff --check origin/main...HEAD | documented.
- **B4:** page is a batch/evidence record; shipped-vs-proposed claims are record evidence, not a deployed system; no synthetic test described as deployed.
- **B5:** 0 markdown links scanned; navigation/contract preserved; no page edit.
- **B6:** read-only reader independence is **UNVERIFIED**; no non-author purpose-and-use interview claimed; never FULL-supporting.

### P453 - union 453 - docs/evidence/documentation/readability-lane-c-batch-13-2026-10-18.md - re-pin - read whole L1-1650
- **B1:** title/purpose anchor L1 Readability Phase 4 re-read lane C - Stage C batch record, batch 13, 2026-10-18; lane record with purpose/scope; audience inferred from record context.
- **B2:** 504 candidate rows; defined 0; named gaps 88; documented exclusions 416; all rows in section 3.
- **B3:** headings/anchors: # Readability Phase 4 re-read lane C - Stage C batch record, batch 13, 2026-10-18; ## 1. Plan binding and derivation; ## 2. The eight pages; ## 3. Whole-page re-read evidence and canonical B1-B6 per page; command/example references: git status --short --untracked-files=normal | docu; git branch --show-current | documented exclusion -.
- **B4:** page is a batch/evidence record; shipped-vs-proposed claims are record evidence, not a deployed system; no synthetic test described as deployed.
- **B5:** 0 markdown links scanned; navigation/contract preserved; no page edit.
- **B6:** read-only reader independence is **UNVERIFIED**; no non-author purpose-and-use interview claimed; never FULL-supporting.

### P454 - union 454 - docs/evidence/documentation/readability-lane-c-batch-14-2026-10-18.md - re-pin - read whole L1-809
- **B1:** title/purpose anchor L1 Readability Phase 4 re-read lane C - Stage C batch record, batch 14, 2026-10-18; lane record with purpose/scope; audience inferred from record context.
- **B2:** 503 candidate rows; defined 0; named gaps 37; documented exclusions 466; all rows in section 3.
- **B3:** headings/anchors: # Readability Phase 4 re-read lane C - Stage C batch record, batch 14, 2026-10-18; ## 1. Plan binding and derivation; ## 2. The eight pages; ## 3. Whole-page re-read evidence and canonical B1-B6 per page; command/example references: git diff --cached --check | documented exclusion; git diff --check | documented exclusion - inline.
- **B4:** page is a batch/evidence record; shipped-vs-proposed claims are record evidence, not a deployed system; no synthetic test described as deployed.
- **B5:** 0 markdown links scanned; navigation/contract preserved; no page edit.
- **B6:** read-only reader independence is **UNVERIFIED**; no non-author purpose-and-use interview claimed; never FULL-supporting.

### P455 - union 455 - docs/evidence/documentation/readability-lane-c-batch-15-2026-10-18.md - re-pin - read whole L1-262
- **B1:** title/purpose anchor L1 Lane C batch 15 evidence record — block 376-383 (2026-10-18); lane record with purpose/scope; audience inferred from record context.
- **B2:** 105 candidate rows; defined 0; named gaps 19; documented exclusions 86; all rows in section 3.
- **B3:** headings/anchors: # Lane C batch 15 evidence record — block 376-383 (2026-10-18); ## 1. Exact base, plan and scope; ## 2. Eight frozen pages at pinned ref 2db1ffb7; ## 3. Canonical acceptance and dispositions; command/example references: git diff --check | documented exclusion - inline; git diff --check | documented exclusion - inline.
- **B4:** page is a batch/evidence record; shipped-vs-proposed claims are record evidence, not a deployed system; no synthetic test described as deployed.
- **B5:** 4 markdown links scanned; navigation/contract preserved; no page edit.
- **B6:** read-only reader independence is **UNVERIFIED**; no non-author purpose-and-use interview claimed; never FULL-supporting.

## 6. Artifacts - immutable captures and canonical blocks
Canonical policy: the inline blocks below are canonical and independently hash-verifiable; _A/evidence/read-lc448-c1 files are retained, hash-cross-checked working copies, not independently authoritative. New filenames only; no in-place overwrite; superseded captures (old Crows/preview) retained and cited. ONE canonical block per artifact; no duplicate canonical blocks.

### Crows-448.txt canonical block
**Measured:** 1472 B / 4 LF / sha c798cba9d12c5ecfc9b7bc795d32f8a303cffd48afb14c6e042546a17d5dbbef
<!-- artifact:Crows-448.txt:start -->
~~~text
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) @ c6e5d5649bf8 | C batch-24 / sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read all eight pages whole; bound canonical B1-B6/AC1-AC8 and candidate-token rules | 0 FULL / 8 PARTIAL / 0 UNRUN; candidate-token table; no keeper |
| [source-of-truth-reconciler](.claude/skills/source-of-truth-reconciler/SKILL.md) @ b5fd9feda972 | C batch-24 / sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at basis 907a6026; verified mixed pin, frontier/quarters, duplicate-read and A-rows reference | block448-455/batch24; union624/156; 1,031,654/8,697; mixed1+7; 0 page-read rows |
| [change-classification-gate](.claude/skills/change-classification-gate/SKILL.md) @ 08d91a834460 | C batch-24 / sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Classified docs-only exactly one added record path; verified path absent | one added record path; no other path |
| [skill-usage-ledger](.claude/skills/skill-usage-ledger/SKILL.md) @ 6a27b5c8e690 | C batch-24 / sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Resolved manifest hashes; authored rows/Row sources/six fields; retained Crows capture | 4 rows/4 per-row sources/4 six-field lines; capture hash |
~~~
<!-- artifact:Crows-448.txt:end -->

### Crows-448.json canonical block
**Measured:** 1839 B / 121 LF / sha b081b03700a4e7ab7dfb8c4d0a7c0199817b4629f2ecf7e74b52cc5a3bb5fce6
<!-- artifact:Crows-448.json:start -->
~~~text
{
 "table_name": "stage_c_skills",
 "key": "row",
 "where": "stage=C AND agent=sd-c-read-lc-448-c1 AND batch=23",
 "rows": [
  {
   "skill": "acceptance-criteria-reviewer",
   "hash": "c6e5d5649bf8",
   "applied": "read eight pages whole; canonical/candidate audit",
   "apply": "query acceptance row"
  },
  {
   "skill": "source-of-truth-reconciler",
   "hash": "b5fd9feda972",
   "applied": "frontier/quarters/pins/duplicates",
   "apply": "query acceptance row"
  },
  {
   "skill": "change-classification-gate",
   "hash": "08d91a834460",
   "applied": "docs-only one path",
   "apply": "query acceptance row"
  },
  {
   "skill": "skill-usage-ledger",
   "hash": "6a27b5c8e690",
   "applied": "rows/sources/six/capture",
   "apply": "query acceptance row"
  }
 ],
 "inventory": {
  "descriptor": "candidate-token",
  "rows": 4166,
  "classes": {
   "ii": 55,
   "i": 635,
   "v": 1723,
   "iv": 1581,
   "iii": 172
  },
  "dispositions": {
   "excluded": 3559,
   "named": 599,
   "defined": 8
  },
  "codes": {
   "PROSE": 55,
   "RANGE": 125,
   "DATE": 76,
   "STATUS": 147,
   "SHA": 389,
   "COMMAND": 29,
   "PATH": 346,
   "LITERAL": 619,
   "EMPHASIS": 398,
   "PLACEHOLDER": 68,
   "LINE-RANGE": 1292,
   "OPERATOR": 15
  },
  "per_page": {
   "P448": [
    47,
    4,
    0,
    48,
    158
   ],
   "P449": [
    34,
    5,
    1,
    203,
    90
   ],
   "P450": [
    177,
    8,
    7,
    721,
    514
   ],
   "P451": [
    165,
    8,
    37,
    312,
    268
   ],
   "P452": [
    61,
    8,
    30,
    52,
    96
   ],
   "P453": [
    91,
    8,
    55,
    97,
    253
   ],
   "P454": [
    40,
    7,
    24,
    122,
    310
   ],
   "P455": [
    20,
    7,
    18,
    26,
    34
   ]
  }
 },
 "source": "inline record canonical blocks",
 "model": "DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)"
}
~~~
<!-- artifact:Crows-448.json:end -->

### README-448.md canonical block
**Measured:** 880 B / 12 LF / sha d1010456304deb063704e44d674950d2cbc90c089d33f2a515971d66281d1b11
<!-- artifact:README-448.md:start -->
~~~text
# Batch-24 Stage C evidence (read-lc448-c1)

Working evidence for the eight-page candidate-token audit at basis 907a6026.

- Crows-448.txt: four-row Stage C skills capture (canonical inline in record).
- Crows-448.json: support CLI data (table_name stage_c_skills, key row, WHERE stage=C AND agent=sd-c-read-lc-448-c1 AND batch=23).
- preview-448.py: support CLI (path|rows|query <term>); query reads rows and matches skill/applied/result.
- A-rows-ref.txt: four Stage A plan-row reference capture (accepted plan r1; historical plan-role r3).
- MANIFEST-440.txt: measured bytes/LF/SHA for the retained working files.
- Pages P440-P447 are pinned/re-pinned page captures used for the token audit; record-only path remains the only committed path.

The inline record blocks are canonical/verifiable; this directory is retained as hash-cross-checked working evidence, not committed.
~~~
<!-- artifact:README-448.md:end -->

### MANIFEST-448.txt canonical block
**Measured:** 530 B / 5 LF / sha 4dc0b7e154710707b3cb894fd54f355355916955ba8b7211b8a25f5331edc88d
<!-- artifact:MANIFEST-448.txt:start -->
~~~text
Crows-448.txt  sha256=c798cba9d12c5ecfc9b7bc795d32f8a303cffd48afb14c6e042546a17d5dbbef  bytes=1472  lf=4
Crows-448.json  sha256=b081b03700a4e7ab7dfb8c4d0a7c0199817b4629f2ecf7e74b52cc5a3bb5fce6  bytes=1839  lf=121
README-448.md  sha256=d1010456304deb063704e44d674950d2cbc90c089d33f2a515971d66281d1b11  bytes=880  lf=12
preview-448.py  sha256=a791b8ee6d463bf14dcb305c022e88b223d02a5014b88878964318435604be33  bytes=643  lf=15
A-rows-ref.txt  sha256=06f358da9d1525a4f2bf8a532cb202f6a5520a28153b767fbdc08f1160542966  bytes=1194  lf=4
~~~
<!-- artifact:MANIFEST-448.txt:end -->

### preview-448.py canonical block
**Measured:** 643 B / 15 LF / sha a791b8ee6d463bf14dcb305c022e88b223d02a5014b88878964318435604be33
<!-- artifact:preview-448.py:start -->
~~~text
#!/usr/bin/env python3
import json,sys,os
P=os.path.join(os.path.dirname(__file__),"Crows-448.json")
def main(a):
    d=json.load(open(P,encoding="utf-8"))
    if not a or a[0]=="path": print(P); return 0
    if a[0]=="rows": print(json.dumps(d["rows"],indent=1,ensure_ascii=False)); return 0
    if a[0]=="query" and len(a)>1:
        q=a[1]
        m=[r for r in d["rows"] if q in r.get("skill","") or q in r.get("applied","")]
        print(json.dumps(m,indent=1,ensure_ascii=False))
        return 0 if m else 1
    print("usage: preview-448.py [path|rows|query <term>]")
    return 2
if __name__=="__main__": sys.exit(main(sys.argv[1:]))
~~~
<!-- artifact:preview-448.py:end -->

### A-rows-ref.txt canonical block
**Measured:** 1194 B / 4 LF / sha 06f358da9d1525a4f2bf8a532cb202f6a5520a28153b767fbdc08f1160542966
<!-- artifact:A-rows-ref.txt:start -->
~~~text
| acceptance-criteria-reviewer @ c6e5d5649bf8 | A plan / sd-a-read-lc-448-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Bound canonical B1-B6, AC1-AC8 and dispatch/normalization rules to block 448-455; B4 per page; B6 UNVERIFIED | canonical exact; B4 per page; B6 unverified |
| source-of-truth-reconciler @ b5fd9feda972 | A plan / sd-a-read-lc-448-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Re-ran check_index at 907a6026; derived union624/156 quarters/block448-455; 66 lane records; measured eight pages | 740/107/6/617/6/4/633; union623; block448-455; 1,031,654/8,697; 0 page-read rows |
| change-classification-gate @ 08d91a834460 | A plan / sd-a-read-lc-448-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Classified docs-only exactly one added record path; verified path absent at main | one record path; absent |
| skill-usage-ledger @ 6a27b5c8e690 | A plan / sd-a-read-lc-448-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Authored this in-plan Stage A account and retained capture | four rows/sources; non-zero binding |
~~~
<!-- artifact:A-rows-ref.txt:end -->

## 7. Stage A reference (accepted plan r1)
The four Stage A account rows are retained in A-rows-ref.txt (historical plan-role r3 capture; referenced here, not duplicated as a second canonical block).
| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| acceptance-criteria-reviewer @ c6e5d5649bf8 | A plan / sd-a-read-lc-448-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Bound canonical B1-B6, AC1-AC8 and dispatch/normalization rules to block 448-455; B4 per page; B6 UNVERIFIED | canonical exact; B4 per page; B6 unverified |
| source-of-truth-reconciler @ b5fd9feda972 | A plan / sd-a-read-lc-448-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Re-ran check_index at 907a6026; derived union624/156 quarters/block448-455; 66 lane records; measured eight pages | 740/107/6/617/6/4/633; union623; block448-455; 1,031,654/8,697; 0 page-read rows |
| change-classification-gate @ 08d91a834460 | A plan / sd-a-read-lc-448-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Classified docs-only exactly one added record path; verified path absent at main | one record path; absent |
| skill-usage-ledger @ 6a27b5c8e690 | A plan / sd-a-read-lc-448-r1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Authored this in-plan Stage A account and retained capture | four rows/sources; non-zero binding |

## 8. Stage C self account (four skills rows, Row sources, six-field lines)
| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [acceptance-criteria-reviewer](../../../.claude/skills/acceptance-criteria-reviewer/SKILL.md) @ c6e5d5649bf8 | C batch-24 / sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read all eight pages whole; bound canonical B1-B6/AC1-AC8 and candidate-token rules | 0 FULL / 8 PARTIAL / 0 UNRUN; candidate-token table; no keeper |
| [source-of-truth-reconciler](../../../.claude/skills/source-of-truth-reconciler/SKILL.md) @ b5fd9feda972 | C batch-24 / sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read at basis 907a6026; verified mixed pin, frontier/quarters, duplicate-read and A-rows reference | block448-455/batch24; union624/156; 1,031,654/8,697; mixed1+7; 0 page-read rows |
| [change-classification-gate](../../../.claude/skills/change-classification-gate/SKILL.md) @ 08d91a834460 | C batch-24 / sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Classified docs-only exactly one added record path; verified path absent | one added record path; no other path |
| [skill-usage-ledger](../../../.claude/skills/skill-usage-ledger/SKILL.md) @ 6a27b5c8e690 | C batch-24 / sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Resolved manifest hashes; authored rows/Row sources/six fields; retained Crows capture | 4 rows/4 per-row sources/4 six-field lines; capture hash |

<!-- Row source: agent=sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=1; target=this batch-24 record commit from basis 907a6026; source=_A/evidence/read-lc448-c1/Crows-448.txt line 1 of 4; binding=sha256 c798cba9d12c5ecfc9b7bc795d32f8a303cffd48afb14c6e042546a17d5dbbef over 1472 B / 4 LF; table_name=stage_c_skills; key=row; WHERE=stage=C AND agent=sd-c-read-lc-448-c1 AND batch=23; README=README-448.md sha256 d1010456304deb063704e44d674950d2cbc90c089d33f2a515971d66281d1b11 bytes=880 lf=12; contract=d41b0dff; source-vs-disk=verified by embedded verifier; status=current -->
<!-- Row source: agent=sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=2; target=this batch-24 record commit from basis 907a6026; source=_A/evidence/read-lc448-c1/Crows-448.txt line 2 of 4; binding=sha256 c798cba9d12c5ecfc9b7bc795d32f8a303cffd48afb14c6e042546a17d5dbbef over 1472 B / 4 LF; table_name=stage_c_skills; key=row; WHERE=stage=C AND agent=sd-c-read-lc-448-c1 AND batch=23; README=README-448.md sha256 d1010456304deb063704e44d674950d2cbc90c089d33f2a515971d66281d1b11 bytes=880 lf=12; contract=d41b0dff; source-vs-disk=verified by embedded verifier; status=current -->
<!-- Row source: agent=sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=3; target=this batch-24 record commit from basis 907a6026; source=_A/evidence/read-lc448-c1/Crows-448.txt line 3 of 4; binding=sha256 c798cba9d12c5ecfc9b7bc795d32f8a303cffd48afb14c6e042546a17d5dbbef over 1472 B / 4 LF; table_name=stage_c_skills; key=row; WHERE=stage=C AND agent=sd-c-read-lc-448-c1 AND batch=23; README=README-448.md sha256 d1010456304deb063704e44d674950d2cbc90c089d33f2a515971d66281d1b11 bytes=880 lf=12; contract=d41b0dff; source-vs-disk=verified by embedded verifier; status=current -->
<!-- Row source: agent=sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=4; target=this batch-24 record commit from basis 907a6026; source=_A/evidence/read-lc448-c1/Crows-448.txt line 4 of 4; binding=sha256 c798cba9d12c5ecfc9b7bc795d32f8a303cffd48afb14c6e042546a17d5dbbef over 1472 B / 4 LF; table_name=stage_c_skills; key=row; WHERE=stage=C AND agent=sd-c-read-lc-448-c1 AND batch=23; README=README-448.md sha256 d1010456304deb063704e44d674950d2cbc90c089d33f2a515971d66281d1b11 bytes=880 lf=12; contract=d41b0dff; source-vs-disk=verified by embedded verifier; status=current -->

**Binding:** _A/evidence/read-lc448-c1/Crows-448.txt is the four-row Stage C capture (1472 B/4 LF/sha c798cba9d12c5ecfc9b7bc795d32f8a303cffd48afb14c6e042546a17d5dbbef); binding contract d41b0dff; non-zero; source-vs-disk confirmed.

**Six-field lines (fenced, outside bound fields):**
~~~text
acceptance-criteria-reviewer@c6e5d5649bf8 / reason: C batch-24 candidate-token audit / applied: read eight pages, class/dispatch, artifacts/captures / result: 4166 rows; i635/ii55/iii172/iv1581/v1723; disps8/599/3559 / incomplete: D/E/F/G / by: C batch-24, sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
source-of-truth-reconciler@b5fd9feda972 / reason: C batch-24 candidate-token audit / applied: read eight pages, class/dispatch, artifacts/captures / result: 4166 rows; i635/ii55/iii172/iv1581/v1723; disps8/599/3559 / incomplete: D/E/F/G / by: C batch-24, sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
change-classification-gate@08d91a834460 / reason: C batch-24 candidate-token audit / applied: read eight pages, class/dispatch, artifacts/captures / result: 4166 rows; i635/ii55/iii172/iv1581/v1723; disps8/599/3559 / incomplete: D/E/F/G / by: C batch-24, sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
skill-usage-ledger@6a27b5c8e690 / reason: C batch-24 candidate-token audit / applied: read eight pages, class/dispatch, artifacts/captures / result: 4166 rows; i635/ii55/iii172/iv1581/v1723; disps8/599/3559 / incomplete: D/E/F/G / by: C batch-24, sd-c-read-lc-448-c1 (true identity sd-a-789-repl-r2), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
~~~

## 9. PROC-04 method
The body publisher will derive PROC-04 from the FINAL live PR body by: take whole-line witness/skills/security sentinel fields, whitespace-collapse each, join with LF, SHA-256 UTF-8; publish short+full digest and normalized lens; after ALL body edits recompute from live body and ensure published==recomputed literally. Body checker must exit0. The record is canonical for counts/captures; the body binds plan/head/record facts.

## 10. Embedded self-contained fail-safe verifier (extract and run)
Extraction/execution: copy the single fenced python block below to verifier-448.py and run python verifier-448.py <this-record.md>. No third-party dependency. Exit0 prints the expected line; failures print VERIFIER FAIL and exit1; no argument exits2.

<!-- verifier:start -->
~~~python
import io,re,json,hashlib,subprocess,sys,tempfile,os
if len(sys.argv)!=2:
    print('usage: python verifier-448.py <record.md>'); sys.exit(2)
record=sys.argv[1]
try: text=io.open(record,encoding='utf-8').read()
except Exception as e: print('VERIFIER FAIL: cannot read record:',e); sys.exit(2)
errors=[]
pre=text.split('<!-- verifier:start -->')[0]
def err(m): errors.append(m)
# inventory section
try:
 s=text.index('## 3. Candidate-token inventory'); e=text.index('## 4. Counts',s)
except ValueError:
 print('VERIFIER FAIL: inventory section missing'); sys.exit(1)
lines=text[s:e].split('\n')
rows=[];malformed=0
for l in lines:
    if not l.startswith('| P'): continue
    # split respecting backslash escapes
    cells=[];cur='';i=0
    while i<len(l):
        ch=l[i]
        if ch=='\\' and i+1<len(l): cur+=l[i+1];i+=2;continue
        if ch=='|': cells.append(cur.strip());cur='';i+=1;continue
        cur+=ch;i+=1
    cells=[c for c in cells if c!='']
    if len(cells)!=5:
        malformed+=1;continue
    pg,loc,cls,tok,disp=cells
    m=re.fullmatch(r'(\d+)@(\d+)',loc)
    if not pg.startswith('P') or not m or cls not in ('i','ii','iii','iv','v'):
        malformed+=1;continue
    rows.append((pg,int(m.group(1)),int(m.group(2)),cls,tok,disp))
keys=set((r[0],r[1],r[4]) for r in rows)
from collections import Counter,defaultdict
classes=Counter(r[3] for r in rows)
disp=Counter('defined' if r[5].startswith('defined') else 'named' if r[5].startswith('named') else 'excluded' for r in rows)
per=defaultdict(lambda:[0,0,0,0,0]);pdisp=defaultdict(Counter)
for r in rows:
    per[r[0]][['i','ii','iii','iv','v'].index(r[3])]+=1
    pdisp[r[0]][('defined' if r[5].startswith('defined') else 'named' if r[5].startswith('named') else 'excluded')]+=1
if len(rows)!=4166: err('rows %d != 4166'%len(rows))
if len(keys)!=4166: err('unique keys %d != 4166'%len(keys))
if malformed: err('malformed rows %d'%malformed)
if dict(classes)!=dict(i=635,ii=55,iii=172,iv=1581,v=1723): err('classes mismatch '+repr(dict(classes)))
if dict(disp)!=dict(defined=8,named=599,excluded=3559): err('dispositions mismatch '+repr(dict(disp)))
# duplicate defined/named per page/token
seen=defaultdict(int)
for r in rows:
    if r[5].startswith(('defined','named')): seen[(r[0],r[4])]+=1
for k,v in seen.items():
    if v>1: err('duplicate defined/named token %r'% (k,))
# backtick class rule
BT=chr(96)
for r in rows:
    tok=r[4]
    if tok.startswith(BT) and tok.endswith(BT) and r[3] not in ('iv','v'): err('backticked non-iv/v '+repr(r))
    if ('<' in tok or '>' in tok) and not (tok.startswith(BT) and tok.endswith(BT)) and r[5].startswith('named'): err('raw angle named gap '+repr(r))
# codes sum
codes=Counter()
for r in rows:
    if r[5].startswith('documented exclusion - '):
        m=re.match(r'documented exclusion - ([A-Z-]+):',r[5])
        if not m: err('bad exclusion code '+repr(r))
        else: codes[m.group(1)]+=1
if sum(codes.values())!=disp['excluded']: err('code sum mismatch %d'%sum(codes.values()))
# per-page table
try:
 s2=text.index('## 4. Counts'); e2=text.index('## 5. Whole-page',s2)
except ValueError: err('counts section missing'); s2=e2=0
plines=[l for l in text[s2:e2].split('\n') if l.startswith('| P4')]
if len(plines)!=8: err('per-page count table rows %d'%len(plines))
for l in plines:
    c=[x.strip() for x in l.strip('|').split('|')];pg=c[0]
    try: vals=[int(x) for x in c[1:]]
    except: err('bad per-page row');continue
    expect=[sum(per[pg])]+per[pg]+[pdisp[pg].get('defined',0),pdisp[pg].get('named',0),pdisp[pg].get('excluded',0)]
    if vals!=expect: err('per-page mismatch '+pg+' '+repr(vals)+' != '+repr(expect))
# artifacts
def extract(name):
    marker='### '+name+' canonical block'
    i=text.index(marker)
    mstart=text.index('<!-- artifact:'+name+':start -->',i)
    astart=text.index('~~~text',mstart)+len('~~~text')
    # content begins after newline
    if text[astart:astart+1]=='\n': astart+=1
    aend=text.index('~~~',astart)
    content=text[astart:aend]
    if content.endswith('\n'): content=content[:-1]
    measured=re.search(r'\*\*Measured:\*\* (\d+) B / (\d+) LF / sha ([0-9a-f]{64})',text[i:aend])
    return content+'\n', measured
artfacts={}
for name in ['Crows-448.txt','Crows-448.json','README-448.md','MANIFEST-448.txt','preview-448.py','A-rows-ref.txt']:
    try: content,measured=extract(name)
    except Exception as e: err('artifact missing '+name+': '+str(e));continue
    b=content.encode();lf=b.count(b'\n');sha=hashlib.sha256(b).hexdigest()
    if not measured: err('measured missing '+name);continue
    by,ml,ms=int(measured.group(1)),int(measured.group(2)),measured.group(3)
    if (b.__len__(),lf,sha)!=(by,ml,ms): err('artifact mismatch %s (%d,%d,%s) != (%d,%d,%s)'%(name,b.__len__(),lf,sha,by,ml,ms))
    artfacts[name]=(b,lf,sha)
# crows txt four rows
ct=artfacts.get('Crows-448.txt',(b'',0,''))[0].decode('utf-8')
if sum(1 for l in ct.split('\n') if l.startswith('| '))<4: err('Crows txt rows <4')
# crows json totals
try:
 cj=json.loads(artfacts['Crows-448.json'][0].decode('utf-8'))
 inv=cj.get('inventory',{})
 if inv.get('rows')!=len(rows): err('Crows.json rows mismatch')
 if inv.get('classes')!=dict(classes): err('Crows.json classes mismatch')
 if inv.get('dispositions')!=dict(disp): err('Crows.json disps mismatch')
 if inv.get('codes')!=dict(codes): err('Crows.json codes mismatch')
 if len(cj.get('rows',[]))!=4: err('Crows.json support rows !=4')
except Exception as e: err('Crows.json parse: '+str(e))
# support CLI actual run
try:
 tf=os.path.join(os.path.dirname(os.path.abspath(record)),'tmp-verify-448');os.makedirs(tf,exist_ok=True)
 open(os.path.join(tf,'preview-448.py'),'w',encoding='utf-8').write(artfacts['preview-448.py'][0].decode('utf-8'))
 open(os.path.join(tf,'Crows-448.json'),'w',encoding='utf-8').write(artfacts['Crows-448.json'][0].decode('utf-8'))
 out=subprocess.run([sys.executable,os.path.join(tf,'preview-448.py'),'query','acceptance'],capture_output=True,text=True,timeout=10)
 if out.returncode!=0: err('support-cli exit %d'%out.returncode)
 data=json.loads(out.stdout)
 if not data or 'apply' not in data[0]: err('support-cli apply key missing')
except Exception as e: err('support-cli: '+str(e))
# manifest references
try:
 man=artfacts['MANIFEST-448.txt'][0].decode('utf-8')
 for name in ['Crows-448.txt','Crows-448.json','README-448.md','preview-448.py','A-rows-ref.txt']:
  b,lf,sha=artfacts[name]
  if name not in man or sha not in man or str(len(b)) not in man: err('MANIFEST missing '+name)
except Exception as e: err('MANIFEST: '+str(e))
# row sources/stage-a
if len(re.findall(r'<!-- Row source:',pre))!=4: err('row-source count !=4')
readme_sha=artfacts['README-448.md'][2]
if readme_sha not in pre: err('README hash not referenced')
if 'accepted plan r1' not in pre: err('stage-a plan r1 missing')
if 'A plan r3' in pre: err('unexpected A plan r3 under r1')
# stale markers
for bad in ['5568615474','370d0278','two DCO','source-exhaustive proof']:
 if bad in pre: err('stale marker '+bad)
# disk support
base=r'C:\src\Project Aegis\_A\evidence\read-lc448-c1'
for name in ['Crows-448.txt','Crows-448.json','README-448.md','preview-448.py','A-rows-ref.txt','MANIFEST-448.txt']:
 p=os.path.join(base,name)
 if not os.path.exists(p): err('disk evidence missing '+name);continue
 d=open(p,'rb').read()
 if name in artfacts and hashlib.sha256(d).hexdigest()!=artfacts[name][2]: err('disk sha mismatch '+name)
# output
if errors:
 print('VERIFIER FAIL:');[print(' -',e) for e in errors];sys.exit(1)
print('VERIFIER OK rows=%d unique=%d malformed=%d classes=%s disps=%s exclusions=%d codes=%s per-page=8 Crows.json=full-totals+rows-agree raw-placeholders=%d inline-artifacts=6/6 stale=0 span=ok duplicate-token=ok support-cli=ok stage-a=ok row-source=ok crows-full=ok disk-support=ok stale-marker=ok'%(len(rows),len(keys),malformed,dict(classes),dict(disp),disp['excluded'],dict(codes),codes['PLACEHOLDER']))
~~~
<!-- verifier:end -->

**Expected output line:** VERIFIER OK rows=4166 unique=4166 malformed=0 classes={'ii': 55, 'i': 635, 'v': 1723, 'iv': 1581, 'iii': 172} disps={'excluded': 3559, 'named': 599, 'defined': 8} exclusions=3559 codes={'PROSE': 55, 'RANGE': 125, 'DATE': 76, 'STATUS': 147, 'SHA': 389, 'COMMAND': 29, 'PATH': 346, 'LITERAL': 619, 'EMPHASIS': 398, 'PLACEHOLDER': 68, 'LINE-RANGE': 1292, 'OPERATOR': 15} per-page=8 Crows.json=full-totals+rows-agree raw-placeholders=68 inline-artifacts=6/6 stale=0 span=ok duplicate-token=ok support-cli=ok stage-a=ok row-source=ok crows-full=ok disk-support=ok stale-marker=ok

## 11. Boundary
Stage C only: one record path; no page edit; no plan/keeper/index/manifest/tool/test/workflow change; no merge; owner #848 untouched. Candidate-token inventory is table-level self-consistency, never exact-once/source-exhaustive. **Signed with both names - true identity: sd-a-789-repl-r2; stage role: sd-c-read-lc-448-c1.** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
