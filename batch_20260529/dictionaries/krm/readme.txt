readme.txt for csl-corrections/batch_20260529/dictionaries/krm

KRM markup fix — 2026-05-29

Description: Remove trailing spaces in <s> tags (5 lines)
Changes applied: 5
csl-orig commit: 969e0b8
Issue: https://github.com/sanskrit-lexicon/KRM/issues/4

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/krm
  cp C:/xampp/htdocs/cologne/csl-orig/v02/krm/krm.txt temp_krm_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_krm_0.txt ../../../krm/markup-fix-audit/markup_fix_changes.txt temp_krm_1.txt
  cp temp_krm_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/krm/krm.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh krm  ../../krm
  sh xmlchk_xampp.sh krm
  # XML result: All records parsed by ET

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/krm
  python diff_to_changes_dict.py temp_krm_0.txt temp_krm_1.txt change_krm_markup_1.txt
  # 5 changes written to change_krm_markup_1.txt

Note: A spurious UTF-8 BOM was added by the fix and removed in commit 922602c.

Files:
  change_krm_markup_1.txt  — updateByLine audit trail (5 changes)
