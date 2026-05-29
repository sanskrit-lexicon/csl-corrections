readme.txt for csl-corrections/batch_20260529/dictionaries/bop

BOP markup fix — 2026-05-29

Description: Remove leading spaces inside <lang n="Avestan"> and <lang n="greek"> tags (39 lines)
Changes applied: 39
csl-orig commit: 3f53192
Issue: https://github.com/sanskrit-lexicon/BOP/issues/8

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/bop
  cp C:/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt temp_bop_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_bop_0.txt ../../../bop/markup-fix-audit/markup_fix_changes.txt temp_bop_1.txt
  cp temp_bop_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh bop  ../../bop
  sh xmlchk_xampp.sh bop
  # XML result: All records parsed by ET

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/bop
  python diff_to_changes_dict.py temp_bop_0.txt temp_bop_1.txt change_bop_markup_1.txt
  # 39 changes written to change_bop_markup_1.txt

Files:
  change_bop_markup_1.txt  — updateByLine audit trail (39 changes)
