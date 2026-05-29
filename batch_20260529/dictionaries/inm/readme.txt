readme.txt for csl-corrections/batch_20260529/dictionaries/inm

INM markup fix — 2026-05-29

Description: Remove trailing space inside <is>Śyenakapotākhyāna </is> at line 7716
Changes applied: 1
csl-orig commit: 969e0b8
Issue: https://github.com/sanskrit-lexicon/INM/issues/10

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/inm
  cp C:/xampp/htdocs/cologne/csl-orig/v02/inm/inm.txt temp_inm_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_inm_0.txt ../../../inm/markup-fix-audit/markup_fix_changes.txt temp_inm_1.txt
  cp temp_inm_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/inm/inm.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh inm  ../../inm
  sh xmlchk_xampp.sh inm
  # XML result: All records parsed by ET

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/inm
  python diff_to_changes_dict.py temp_inm_0.txt temp_inm_1.txt change_inm_markup_1.txt
  # 1 changes written to change_inm_markup_1.txt

Note: A spurious UTF-8 BOM was added by the fix and removed in commit 922602c.

Files:
  change_inm_markup_1.txt  — updateByLine audit trail (1 changes)
