11-07-2026 🟡 change_ap90_1.txt — AP90#14 residual paired-parens-outside-Devanagari (14 instances)
  Issue: https://github.com/sanskrit-lexicon/AP90/issues/14
  Description: {#(X)#} -> ({#X#}) — moves parenthesis pairs outside the SLP1
    Devanagari markup, matching the pattern already applied in the maintainer's
    prior 513-change pass on this issue. These 14 are residual instances that
    pass missed. Superseded PR #2863 (branch fix/ap90-paren-outside-slp1),
    which bundled these lines together with unrelated already-shipped/duplicate
    changes to mw.txt and stc.txt — this queue entry carries ONLY the ap90.txt
    lines, re-located by content against current csl-orig main (line numbers
    shifted since #2863 was opened) and re-verified all 14 unique matches.
  Validated: updateByLine.py applied 14/14 "new" transactions cleanly against
    current v02/ap90/ap90.txt (273715 lines in, 273715 lines out); output BOM
    check clean (first bytes 3c4c3e).
  Caveat (🟡, not 🔵): make_xml.py / generate_dict.sh full XML-parse validation
    was NOT completed this pass — the sanctioned temporary swap-into-csl-orig
    step that validation requires was declined by the permission system as an
    unauthorized direct write to csl-orig, even though it is self-reverting.
    A human should run generate_dict.sh ap90 against this change file (or
    authorize the swap explicitly) before this ships in the next batch PR.
  Prepared by: Sonnet 5 (claude-sonnet-5), 11-07-2026.

11-07-2026 🔵 change_ap90_2.txt — CORRECTIONS#434 "AP90 - Compounds stated twice": sarpis (L29859) residual
  Issue: https://github.com/sanskrit-lexicon/CORRECTIONS/issues/434
  Description: Removes the duplicate, unbracketed "--Comp." marker at physical
    line 257097 of the sarpis entry (29859): "of the seven seas. --Comp.
    {#--AsutiH#}" -> "of the seven seas. {#--AsutiH#}". Maintainer SergeA
    verified against ed.3 (1924): all three reported cases (ayAta, muKaM,
    sarpis) are 1st-edition print errors with no duplication in ed.3. The other
    two (ayAta L3946, muKaM L23227) already carry a single {@--Comp.@} in
    current csl-orig — sarpis is the residual instance.
  Validated: updateByLine.py applied 1/1 "new" transaction cleanly against
    current v02/ap90/ap90.txt (273715 lines in, 273715 lines out — line-count
    parity); output BOM check clean (first bytes 3c4c3e); diff is exactly the
    one intended line; all {#..#}/{@..@}/{%..%}/<..>/[..] markup-delimiter
    counts identical old-vs-new (text-only edit, no markup touched); full
    generate_dict.sh XML rebuild against a temp swap-in returned "All records
    parsed by ET" (make_xml.py, exit 0), csl-orig restored byte-identical to
    HEAD afterward.
  Prepared by: Opus 4.8 (claude-opus-4-8), 11-07-2026 (G13, handoff H756).
