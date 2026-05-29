readme.txt for csl-corrections/batch_20260529/dictionaries/ap90

AP90 markup fix — 2026-05-29

Description: Remove trailing space inside <ls n="R.">6. </ls> at line 42758
Changes applied: 1
csl-orig commit: 863d559
Issue: https://github.com/sanskrit-lexicon/AP90/issues/30

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/ap90
  cp C:/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt temp_ap90_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_ap90_0.txt ../../../ap90/markup-fix-audit/markup_fix_changes.txt temp_ap90_1.txt
  cp temp_ap90_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh ap90  ../../ap90
  sh xmlchk_xampp.sh ap90
  # XML result: Pre-existing hw.py <LEND> error in intro section (unrelated to this fix)

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/ap90
  python diff_to_changes_dict.py temp_ap90_0.txt temp_ap90_1.txt change_ap90_markup_1.txt
  # 1 changes written to change_ap90_markup_1.txt

Note: A spurious UTF-8 BOM was added by the fix and removed in commit 922602c.

Files:
  change_ap90_markup_1.txt  — updateByLine audit trail (1 changes)
