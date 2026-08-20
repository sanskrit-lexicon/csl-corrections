# pw pending corrections (local queue — promote via /cologne-batch-pr)

- status: clean pass · 2026-08-19 · link-splitting · pw 141 lines / 142 <ls> elements / +181 addresses ·
  one <ls> holding several sibling addresses split into one element per address, using the
  n= continuation form pw.txt already uses elsewhere (<ls n="Chr. 240,">28</ls>) ·
  validated against delivery base origin/main:v02/pw/pw.txt blob 985658de43bc09d4ebf639ba561979a24fc14f9e:
  updateByLine 141/141 transactions applied, 643112 records in and out, <L>/<LEND> 170556/170556 unchanged,
  <ls> 98485 -> 98666 (+181); independent diff of base vs applied: exactly 141 lines changed,
  every changed line equals the proposed `new`, every proposed `old` matched the base, no other line moved ·
  generator: SanskritLexicography/RussianTranslation/src/ls_split_changefile.py · Opus 5 (claude-opus-5) H3152

## Scope note — why pw and not pwg

The same generator over pwg.txt proposes ZERO changes, and that is the correct result.
PWG's genuine multi-address citations already use the n= continuation form; its remaining
multi-address <ls> elements are page references (11087 (p. 572)), note markers (83, N. 6)
and Oxford-catalogue column letters (100,a. 101,b), none of which are two addresses.
An earlier, looser rule proposed 2,838 pwg lines — every one of which would have produced
a link that resolves to a real but WRONG place. The rule now refuses a split unless every
address is purely numeric, all addresses have the same component count, and the element
body carries no nested markup.

## Not in this queue

The unwrapped Rgveda/Atharvaveda addresses of the same handoff are NOT a csl-orig
correction: they live in the Nachtragsworterbuch layer, scraped from nws.uzi.uni-halle.de,
which csl-orig does not carry. They are wrapped at render time only.
