readme.txt for csl-corrections/batch_20260529/dictionaries/mw72

MW72 markup fix — 2026-05-29

Description: Whitespace trims in various paired tags (24 lines)
Changes applied: 24
csl-orig commit: 3f53192
Issue: https://github.com/sanskrit-lexicon/MW72/issues/6

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/mw72
  cp C:/xampp/htdocs/cologne/csl-orig/v02/mw72/mw72.txt temp_mw72_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_mw72_0.txt ../../../mw72/markup-fix-audit/markup_fix_changes.txt temp_mw72_1.txt
  cp temp_mw72_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/mw72/mw72.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh mw72  ../../mw72
  sh xmlchk_xampp.sh mw72
  # XML result: All records parsed by ET

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/mw72
  python diff_to_changes_dict.py temp_mw72_0.txt temp_mw72_1.txt change_mw72_markup_1.txt
  # 24 changes written to change_mw72_markup_1.txt

Files:
  change_mw72_markup_1.txt  — updateByLine audit trail (24 changes)
