readme.txt for csl-corrections/batch_20260529/dictionaries/mw

MW markup fix — 2026-05-29

Description: Remove trailing spaces in <lex>, <bio>, <arab>, <bot>, <chg><old> tags (9 lines)
Changes applied: 9
csl-orig commit: 8b051ab
Issue: https://github.com/sanskrit-lexicon/MWS/issues/194

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/mw
  cp C:/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_mw_0.txt ../../../mw/markup-fix-audit/markup_fix_changes.txt temp_mw_1.txt
  cp temp_mw_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh mw  ../../mw
  sh xmlchk_xampp.sh mw
  # XML result: Pre-existing hw.py <LEND> error in intro section (unrelated to this fix)

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/mw
  python diff_to_changes_dict.py temp_mw_0.txt temp_mw_1.txt change_mw_markup_1.txt
  # 9 changes written to change_mw_markup_1.txt

Note: A spurious UTF-8 BOM was added by the fix and removed in commit 922602c.

Files:
  change_mw_markup_1.txt  — updateByLine audit trail (9 changes)
