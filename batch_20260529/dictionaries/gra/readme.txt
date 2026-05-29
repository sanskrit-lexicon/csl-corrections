readme.txt for csl-corrections/batch_20260529/dictionaries/gra

GRA markup fix — 2026-05-29

Description: Remove leading spaces inside <chg type="del"> tags (60 lines)
Changes applied: 60
csl-orig commit: a74c199
Issue: https://github.com/sanskrit-lexicon/GRA/issues/37

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/gra
  cp C:/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt temp_gra_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_gra_0.txt ../../../gra/markup-fix-audit/markup_fix_changes.txt temp_gra_1.txt
  cp temp_gra_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/gra/gra.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh gra  ../../gra
  sh xmlchk_xampp.sh gra
  # XML result: All records parsed by ET

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/gra
  python diff_to_changes_dict.py temp_gra_0.txt temp_gra_1.txt change_gra_markup_1.txt
  # 60 changes written to change_gra_markup_1.txt

Files:
  change_gra_markup_1.txt  — updateByLine audit trail (60 changes)
