readme.txt for csl-corrections/batch_20260529/dictionaries/bor

BOR markup fix — 2026-05-29

Description: Remove spaces before </div> throughout bor.txt
Changes applied: 21990
csl-orig commit: 442e0d7
Issue: https://github.com/sanskrit-lexicon/BOR/issues/4

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/bor
  cp C:/xampp/htdocs/cologne/csl-orig/v02/bor/bor.txt temp_bor_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_bor_0.txt ../../../bor/markup-fix-audit/markup_fix_changes.txt temp_bor_1.txt
  cp temp_bor_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/bor/bor.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh bor  ../../bor
  sh xmlchk_xampp.sh bor
  # XML result: All records parsed by ET

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/bor
  python diff_to_changes_dict.py temp_bor_0.txt temp_bor_1.txt change_bor_markup_1.txt
  # 21990 changes written to change_bor_markup_1.txt

Files:
  change_bor_markup_1.txt  — updateByLine audit trail (21990 changes)
