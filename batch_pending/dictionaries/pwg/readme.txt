# pwg — AllvsPWG faultfinder-pool pass ledger (H3486)

This directory is the pass ledger for the H3486 AllvsPWG correction-queue pass.
NOTE: actual pw.txt change files (when a pass has survivors) belong in `dictionaries/pw/`
— the csl-orig dict code the /cologne-batch-pr drain iterates (see existing pw/ entry).
This pwg/ path is named per the handoff text and carries pass records only.

- status: pass complete, 0 survivors queued · 2026-09-04 · H3486 correction-queue pass over
  AllvsPWG-priority.txt (99 candidates, frozen input) vs delivery base
  origin/main:v02/pw/pw.txt blob 985658de43bc09d4ebf639ba561979a24fc14f9e:
  78/99 verdict fixed (suspect spelling absent at tip — pool was generated over the 2013
  Cologne PWG scan headwords (sanhw1 "PWG":"2013"); the modern pw re-digitization already
  superseded that transcription class); 21/99 rejected-with-reason (11+1 correct-Sandhi
  false positives R1, 6 PWG-documented-apparatus forms R2, 3 scan-first single-source R3);
  0 change files -> no updateByLine run, no XML build, csl-orig untouched ·
  pass report: Uprava docs/REPORT_H3486_allvspwg_correction_queue_pass_04-09-2026.md ·
  issue: sanskrit-lexicon/csl-corrections#386 ·
  OxAlpha (opencode/z-ai/glm-5.3-flash) H3486
