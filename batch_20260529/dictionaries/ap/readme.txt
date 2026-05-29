readme.txt for csl-corrections/batch_20260529/dictionaries/ap

AP markup fix — 2026-05-29

Description: Remove trailing space inside <ls>MS. 12. 1. 10. </ls> at line 151977
Changes applied: 1
csl-orig commit: 51a764b
Issue: https://github.com/sanskrit-lexicon/AP/issues/29

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/ap
  cp C:/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt temp_ap_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_ap_0.txt ../../../ap/markup-fix-audit/markup_fix_changes.txt temp_ap_1.txt
  cp temp_ap_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh ap  ../../ap
  sh xmlchk_xampp.sh ap
  # XML result: All records parsed by ET

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/ap
  python diff_to_changes_dict.py temp_ap_0.txt temp_ap_1.txt change_ap_markup_1.txt
  # 1 changes written to change_ap_markup_1.txt

Note: A spurious UTF-8 BOM was added by the fix and removed in commit 922602c.

Files:
  change_ap_markup_1.txt  — updateByLine audit trail (1 changes)
