#!/usr/bin/env python3
"""Subprocess-level regression tests for the PR-body bound-field checker.

Six fixture cases - one per enforced rule - run scripts/ci/check_pr_body_skills.py
as a subprocess and assert its real exit status and message, mirroring the
link-checker self-test pattern (workflow L177-178):

  (a) valid body (full table + row sources + security + witness)   -> exit 0
  (b) missing skills field                                        -> nonzero naming skills
  (c) empty skills field without a no-skill statement             -> nonzero
  (d) rows without Row source records                             -> nonzero naming the rows
  (e) missing security field                                      -> nonzero naming security
  (f) skills/security/row-source present but NO witness pair      -> nonzero naming witness

    python -B -m unittest scripts.tests.test_pr_body_skills_check -v
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "ci" / "check_pr_body_skills.py"

VALID_BODY = """## Aegis skills used (required)

<!-- bound-field: skills -->

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |
| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |

<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->

<!-- bound-field: end -->

## Security-relevant surface? (required)

<!-- bound-field: security -->

- [x] Yes

<!-- bound-field: end -->

## Reconciliation witness (required)

<!-- bound-field: witness -->

| 1 | The `MG` block | unchanged | |

<!-- bound-field: end -->
"""

NO_SKILL_BODY = """## Aegis skills used (required)

<!-- bound-field: skills -->

No matching skill exists for this change - that is a valid answer.

<!-- bound-field: end -->

## Security-relevant surface? (required)

<!-- bound-field: security -->

- [x] No

<!-- bound-field: end -->

## Reconciliation witness (required)

<!-- bound-field: witness -->

| 1 | The `MG` block | unchanged | |

<!-- bound-field: end -->
"""


def _run(body: str, author: str | None = None) -> tuple[int, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                     encoding="utf-8") as handle:
        handle.write(body)
        path = handle.name
    try:
        cmd = [sys.executable, "-B", str(CHECKER), "--body-file", path]
        if author:
            cmd += ["--author", author]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr
    finally:
        Path(path).unlink()


class TestPrBodySkillsCheck(unittest.TestCase):

    def test_a_valid_body_passes(self) -> None:
        code, output = _run(VALID_BODY)
        self.assertEqual(code, 0, output)
        self.assertIn("OK", output)

    def test_b_missing_skills_field_fails_naming_skills(self) -> None:
        body = VALID_BODY.replace("<!-- bound-field: skills -->", "")
        body = body.replace("<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->", "")
        body = body.replace("| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |", "")
        body = body.replace("| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |", "")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("skills", output)

    def test_c_empty_field_without_no_skill_statement_fails(self) -> None:
        body = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "")
        body = body.replace(
            "| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |",
            "")
        body = body.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("empty", output)

    def test_c2_no_skill_statement_satisfies_the_field(self) -> None:
        code, output = _run(NO_SKILL_BODY)
        self.assertEqual(code, 0, output)

    def test_d_uncovered_rows_fail_naming_the_rows(self) -> None:
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("2", output)
        self.assertIn("Row source", output)

    def test_e_missing_security_field_fails_naming_security(self) -> None:
        body = VALID_BODY.replace(
            "<!-- bound-field: security -->\n\n- [x] Yes\n\n<!-- bound-field: end -->",
            "<!-- bound-field: security -->\n\n- [x] Yes")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("security", output)

    def test_f_missing_witness_field_fails_naming_witness(self) -> None:
        body = VALID_BODY.replace(
            "<!-- bound-field: witness -->\n\n| 1 | The `MG` block | unchanged | |\n\n<!-- bound-field: end -->",
            "<!-- bound-field: witness -->\n\n| 1 | The `MG` block | unchanged | |")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("witness", output)

    def test_g_bot_authors_are_exempt(self) -> None:
        code, output = _run("", author="dependabot[bot]")
        self.assertEqual(code, 0, output)

    def test_h_two_stage_blocks_each_covered_pass(self) -> None:
        # The repository convention is PER-BLOCK: each stage's table block is
        # followed by its own Row source record naming ITS rows (row=1..3).
        second_block = """
| `change-classification-gate` | Stage D / auditor | Re-checked the class. | agreed. |
| `phased-work-handoff-designer` | Stage D / auditor | Re-checked the handoff. | agreed. |
| `scoped-approval-register` | Stage D / auditor | Re-checked the authority. | agreed. |

<!-- Row source: agent=b; stage=D; round=1; row=1..3; target=head H; source=SD-D comment; binding=def456. -->
"""
        body = VALID_BODY.replace(
            "<!-- bound-field: end -->\n\n## Security-relevant surface? (required)",
            second_block + "\n<!-- bound-field: end -->\n\n## Security-relevant surface? (required)")
        code, output = _run(body)
        self.assertEqual(code, 0, output)

    def test_i_unnamed_row_in_block_fails_naming_it(self) -> None:
        # A block of three rows whose record names only rows 1..2: row 3 is
        # unnamed and must be reported - per-block ordinals, not a global
        # counter.
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("block 1", output)
        self.assertIn("2", output)

    def test_j_limits_field_in_row_source_is_accepted(self) -> None:
        # The repository's real records carry `; limits=` fields; the parser
        # must accept them without mangling the ordinals or the binding.
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; limits=UNRUN; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertEqual(code, 0, output)

    def test_k_row_source_outside_skills_field_does_not_cover(self) -> None:
        # The Row source scan is scoped to the skills bound field: a record
        # sitting in the WITNESS field must not cover the skills table.
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "")
        body = body.replace(
            "## Reconciliation witness (required)",
            "<!-- Row source: agent=outsider; stage=X; round=1; row=1..2; target=head H; source=outsider note; binding=zzz999. -->\n\n## Reconciliation witness (required)")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("block 1", output)

    def test_l_alignment_colon_separator_rows_are_not_data(self) -> None:
        # A separator row with alignment colons (| :--- | ---: |) is not a
        # data row and must not be counted.
        body = VALID_BODY.replace(
            "| --- | --- | --- | --- |",
            "| :--- | :---: | ---: | :--- |")
        code, output = _run(body)
        self.assertEqual(code, 0, output)

    def test_m_unbounded_row_range_is_rejected(self) -> None:
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1..1000000000; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("10000", output)

    def test_n_duplicate_skills_opener_rejected(self) -> None:
        # A second whole-line opening marker for the same field is a
        # duplicate and must be rejected by name (Codex P2 4241067026).
        body = VALID_BODY.replace(
            "## Security-relevant surface? (required)",
            "<!-- bound-field: skills -->\n\n## Security-relevant surface? (required)")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("duplicate skills", output)

    def test_o_five_cell_row_is_not_a_data_row(self) -> None:
        # A row with an unescaped pipe (five cells) is not a valid
        # skills-table data row; when it is the only candidate row the
        # empty-field rule fires (Codex P2 4241067027).
        body = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "| `change-classification-gate` | Stage C / agent | Classified | the diff. | backend-api. |")
        body = body.replace(
            "| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |",
            "")
        body = body.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("empty", output)

    def test_p_record_missing_structural_field_fails(self) -> None:
        # Every Row source record must carry agent=, stage=, round=,
        # target=, source= and binding= (Codex P2 4241113131).
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: row=1..2; binding=x -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("missing required field", output)
        self.assertIn("agent", output)

    def test_r_parenthetical_row_ordinals_accepted(self) -> None:
        # The repository's real records append a parenthetical to the
        # ordinals (row=1..2 (skills table rows above)); the ordinal spec is
        # the leading token and must be parsed.
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2 (skills table rows above); target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertEqual(code, 0, output)

    def test_s_consecutive_per_row_records_combine(self) -> None:
        # One record per row is permitted: consecutive records after one
        # table block name the SAME block's rows, combined (P1 4241144025).
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1; target=head H; source=SD-C comment; binding=aaa111. -->\n<!-- Row source: agent=a; stage=C; round=1; row=2; target=head H; source=SD-C comment; binding=bbb222. -->")
        code, output = _run(body)
        self.assertEqual(code, 0, output)
        # And an uncovered row still fails.
        body2 = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1; target=head H; source=SD-C comment; binding=aaa111. -->")
        code2, output2 = _run(body2)
        self.assertNotEqual(code2, 0)
        self.assertIn("2", output2)

    def test_t_escaped_pipe_stays_content(self) -> None:
        # GFM supports \| inside a cell: a four-cell row with an escaped
        # content pipe stays four cells; a genuinely five-cell row is still
        # rejected (P2 4241144029).
        body = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "| `change-classification-gate` | Stage C / agent | Classified the \\| diff. | backend-api. |")
        code, output = _run(body)
        self.assertEqual(code, 0, output)

    def test_u_multiline_comment_only_no_skill_fails(self) -> None:
        # A multiline HTML comment hiding the phrase is not a visible
        # statement (P2 4241144033).
        body = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "<!--\nno matching skill\n-->")
        body = body.replace(
            "| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |",
            "")
        body = body.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("empty", output)

    def test_v_source_locators_honored_by_count_sum(self) -> None:
        # The row= token names SOURCE positions, not local table positions:
        # a one-row table sourced from row 42 passes, a span larger than the
        # block passes, and a count-sum below the block size fails.
        body = VALID_BODY.replace(
            "| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |",
            "")
        body = body.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=42; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertEqual(code, 0, output)
        body2 = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1..3; target=head H; source=SD-C comment; binding=abc123. -->")
        code2, output2 = _run(body2)
        self.assertEqual(code2, 0, output2)
        body3 = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=7; target=head H; source=SD-C comment; binding=abc123. -->")
        code3, output3 = _run(body3)
        self.assertNotEqual(code3, 0)

    def test_w_standalone_line_and_commented_table_are_not_rows(self) -> None:
        # Only rows inside a real header+delimiter table count; a standalone
        # four-cell line or a table hidden inside a multiline comment is not
        # a data row (P2 4241170246).
        standalone = VALID_BODY.replace(
            "| Skill | Stage / agent | How applied | Result / evidence |",
            "")
        standalone = standalone.replace(
            "| --- | --- | --- | --- |",
            "")
        code, output = _run(standalone)
        self.assertNotEqual(code, 0)
        self.assertIn("empty", output)
        commented = VALID_BODY.replace(
            "| Skill | Stage / agent | How applied | Result / evidence |\n| --- | --- | --- | --- |",
            "<!--\n| Skill | Stage / agent | How applied | Result / evidence |\n| --- | --- | --- | --- |\n-->")
        code2, output2 = _run(commented)
        self.assertNotEqual(code2, 0)
        self.assertIn("empty", output2)
        code3, output3 = _run(VALID_BODY)
        self.assertEqual(code3, 0, output3)

    def test_x_untouched_template_body_fails(self) -> None:
        # The untouched template's placeholder row and placeholder record
        # values are not answers: the body must fail as an unanswered table
        # (P1 4241208614).
        body = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "| <skill name, linked to its repository `SKILL.md`> | <the stage, round and agent identity> | <how applied> | <result> |")
        body = body.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=<author>; stage=<stage>; round=<round>; row=<source ordinal/locator>; target=<target>; source=<source>; binding=<binding> -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)

    def test_y_fenced_code_only_structure_fails(self) -> None:
        # Sentinels, tables and Row source records written as a fenced code
        # sample are not real body content (P2 4241208615).
        fenced = "```\n<!-- bound-field: skills -->\n| Skill | Stage / agent | How applied | Result / evidence |\n| --- | --- | --- | --- |\n| `x` | y | z | w |\n<!-- Row source: agent=a; stage=C; round=1; row=1; target=head H; source=s; binding=b. -->\n<!-- bound-field: end -->\n```"
        body = VALID_BODY.replace("<!-- bound-field: skills -->", fenced)
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("skills", output)

    def test_z_malformed_delimiter_cells_fail(self) -> None:
        # A delimiter row without >=3 hyphens per cell is not a GFM
        # delimiter (P2 4241208617).
        body = VALID_BODY.replace(
            "| --- | --- | --- | --- |",
            "| : | : | : | : |")
        code, output = _run(body)
        self.assertNotEqual(code, 0)

    def test_aa_lookalike_marker_line_cannot_inflate_coverage(self) -> None:
        # A user-authored line that LOOKS like the internal marker must not
        # be accepted as a record (P2 4241208620).
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "@@ROWSOURCE@@deadbeef@@0@@")
        code, output = _run(body)
        self.assertNotEqual(code, 0)

    def test_bb_intervening_prose_stops_record_attachment(self) -> None:
        # A record separated from its table by unrelated prose does not
        # attach; the table's rows stay unnamed (P2 4241208622).
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "Some unrelated prose between the table and its record.\n\n<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("Row source", output)

    def test_cc_nonpositive_ordinals_rejected(self) -> None:
        # row=0..1 must not count as two source rows (P2 4241208624).
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=0..1; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("nonpositive", output)

    def test_dd_fence_matches_opener_character_and_length(self) -> None:
        # A 3-backtick line inside a 4-backtick fence does NOT close it
        # (P2 4241244623): the structure stays inside the fence and is not
        # recognized.
        fenced = "````\n<!-- bound-field: skills -->\n```\n| Skill | Stage / agent | How applied | Result / evidence |\n| --- | --- | --- | --- |\n| `x` | y | z | w |\n````"
        body = VALID_BODY.replace("<!-- bound-field: skills -->", fenced)
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("skills", output)

    def test_ee_complete_header_required(self) -> None:
        # All four header cells must match the documented header
        # (P2 4241244625).
        wrong = VALID_BODY.replace(
            "| Skill | Stage / agent | How applied | Result / evidence |",
            "| Skill | Owner | Deadline | Notes |")
        code, output = _run(wrong)
        self.assertNotEqual(code, 0)
        code2, output2 = _run(VALID_BODY)
        self.assertEqual(code2, 0, output2)

    def test_ff_negation_is_not_a_no_skill_answer(self) -> None:
        # A line that QUOTES the phrase in a negation is not the standalone
        # affirmative answer (P2 4241244629).
        negated = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "")
        negated = negated.replace(
            "| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |",
            "A matching skill exists; do not use the phrase \"no matching skill\" here.")
        negated = negated.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "")
        code, output = _run(negated)
        self.assertNotEqual(code, 0)
        self.assertIn("empty", output)
        affirmative = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "No matching skill exists for this change.")
        affirmative = affirmative.replace(
            "| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |",
            "")
        affirmative = affirmative.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "")
        code2, output2 = _run(affirmative)
        self.assertEqual(code2, 0, output2)

    def test_gg_duplicate_numeric_ordinals_do_not_inflate(self) -> None:
        # row=1,1 for a two-row block must not pass by blind cardinality
        # (P2 4241244631).
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1,1; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)

    def test_hh_indented_code_is_not_marker_content(self) -> None:
        # A four-space-indented chunk renders as a code block: markers
        # written there are not body content (P2 4241285829).
        indented = "    <!-- bound-field: skills -->"
        body = VALID_BODY.replace("<!-- bound-field: skills -->", indented)
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("skills", output)

    def test_ii_duplicate_named_locators_do_not_inflate(self) -> None:
        # row=alpha,alpha for a two-row block must not pass (P2 4241285833).
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=alpha,alpha; target=head H; source=SD-C comment; binding=abc123. -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)

    def test_jj_early_comment_terminator_rejects_the_record(self) -> None:
        # A Row source line whose FIRST --> is not the end (binding outside
        # the comment) is not a valid record (P2 4241285835).
        body = VALID_BODY.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment -->; binding=abc123. -->")
        code, output = _run(body)
        self.assertNotEqual(code, 0)

    def test_kk_markdown_line_endings_only(self) -> None:
        # GFM line endings are LF/CRLF/CR only: a body joined with U+2028
        # must not be treated as lines (P2 4241285837), while an LF body
        # passes.
        joined = VALID_BODY.replace("\n", "\u2028")
        code, output = _run(joined)
        self.assertNotEqual(code, 0)
        code2, output2 = _run(VALID_BODY)
        self.assertEqual(code2, 0, output2)

    def test_q_comment_only_no_skill_line_is_not_a_statement(self) -> None:
        # An HTML-comment-only occurrence is not a visible no-matching-skill
        # statement (Codex P2 4241113135).
        body = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "")
        body = body.replace(
            "| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |",
            "<!-- no matching skill -->")
        body = body.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "")
        code, output = _run(body)
        self.assertNotEqual(code, 0)
        self.assertIn("empty", output)
        # And the VISIBLE statement still satisfies the field.
        visible = VALID_BODY.replace(
            "| `change-classification-gate` | Stage C / agent | Classified the diff. | backend-api. |",
            "No matching skill exists for this change.")
        visible = visible.replace(
            "| `phased-work-handoff-designer` | Stage C / agent | Handoff structure. | SD-C comment. |",
            "")
        visible = visible.replace(
            "<!-- Row source: agent=a; stage=C; round=1; row=1..2; target=head H; source=SD-C comment; binding=abc123. -->",
            "")
        code2, output2 = _run(visible)
        self.assertEqual(code2, 0, output2)


if __name__ == "__main__":
    unittest.main()
