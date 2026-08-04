=== 2026-08 BATCH — SHIPPED 04-08-2026 ===
Batch PR: https://github.com/sanskrit-lexicon/csl-orig/pull/2884 (@WAITING maintainer merge; auto-merge OFF)
Dicts: ap90 (2) + mw72 (54 ins) + pwg (1) = 57 changes · issues CORRECTIONS#434 residual,
  COLOGNE#178, csl-devanagari#42
Workflow: queued via /cologne-correction-queue (Grok 4.5 H1523, Sonnet 5), shipped via
  /cologne-batch-pr.
Shipped by: Opus 5 (claude-opus-5), 04-08-2026.

--- validation ---
Re-validated against csl-orig origin/main at batch time (base cc2d1992):
  ap90  273716 -> 273716 lines, 2 replacements, "All records parsed by ET"
  mw72  443101 -> 443155 lines, 54 insertions,  "All records parsed by ET"
  pwg   593597 -> 593597 lines, 1 replacement,  "All records parsed by ET"
BOM clean (ap90 3c4c3e, mw72 0a5b50, pwg 3c483e). Diff scope confirmed to be exactly the
intended edits and nothing else.

NO SWAP WINDOW was used. Earlier batches validated by temporarily copying the corrected
text INTO csl-orig and restoring it afterwards ("restored+md5-verified after each swap
window"); a failed restore there corrupts canonical data. This batch instead built the
isolated tree first and then staged the corrected text into it:
  sh generate_orig.sh <dict> tempparent/<dict>      # pristine text from csl-orig
  cp <corrected>.txt tempparent/<dict>/orig/<dict>.txt
  sh generate_pywork.sh <dict> tempparent/<dict>
  (cd tempparent/<dict>/pywork && sh redo_hw.sh && sh redo_xml.sh)
csl-orig was never written to. The build was confirmed to have CONSUMED the corrected text
(staged orig/ file and generated XML both checked) rather than trusting a green result.

--- how the change files were applied ---
NOT by running updateByLine.py once per file in sequence. Two reasons, both measured:

1. The queued change files are each addressed to the PRISTINE dictionary, so applying them
   in sequence breaks as soon as one of them shifts or rewrites a line another one targets.
   mw72's own queue readme already said so ("apply change_1 and change_2 both against
   *original* mw72 line numbers"); change_mw72_1's 9 insertions shift every later anchor.
   Resolution: apply everything in ONE pass keyed to original line numbers — replacements
   by line, insertions collected per anchor, emitted in file order.

2. updateByLine.py is byte-unsafe on the Windows setup used here: it doubles the carriage
   return (+1 byte/line, measured as +273,723 bytes over 273,715 ap90 lines), which rewrites
   every line in the diff. Files must be read and written with newline='' to preserve CRLF.

--- entries NOT shipped in this batch ---
change_ap90_1.txt  DROPPED as a duplicate. Byte-identical to an edit already shipping in
  csl-orig PR #2879 (line 257097, sarpis L=29859, "of the seven seas. --Comp. {#--AsutiH#}"
  -> "of the seven seas. {#--AsutiH#}"). Shipping the same correction in two open PRs would
  collide at merge. Kept here for the audit trail; it ships via #2879, not #2884.

mw (change_mw_1.txt, change_mw_2.txt)  HELD — still in batch_pending/, deliberately.
  Those files are addressed to a base that is NOT csl-orig origin/main: 20,618 of 21,817
  records fail against it. Five upstream July correction commits (de8c1862, d649aee8,
  921c916f, 54e06384, 4b0fdecd) net-deleted one line at 59923, shifting every later line
  number by one (and changing content at the divergence, alAtaSanti -> alAtaSAnti). They
  need content-relocation onto origin/main and a fresh XML gate before they can ship —
  the previously recorded "All records parsed by ET" was measured on the wrong base and
  does not transfer. Tracked as Uprava H2270.

_Dr. Mārcis Gasūns_
