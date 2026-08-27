# Roadmap — csl-corrections interconnection, 2026-08

_Created: 26-08-2026 · Last updated: 27-08-2026_

Index: [PLAN_CSL_CORRECTIONS_INTERCONNECTION_2026-08.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/PLAN_CSL_CORRECTIONS_INTERCONNECTION_2026-08.md).
Programme roadmap: [ROADMAP_SPINE_INTERCONNECTION_2026H2.md](https://github.com/gasyoun/Uprava/blob/main/docs/ROADMAP_SPINE_INTERCONNECTION_2026H2.md).

**Wave 1 shipped 27-08-2026.** A box may only be ticked after a human has launched the
handoff and its PR has merged — a tick ahead of that is a defect.

## Wave 1 — csl-corrections's wiring change

- [x] [H3571 (Opus 5)](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3571-Opus_csl-corrections_interconnect-cslcorrections-batchpr-bridge-family_26.08.26.md) · medium — shipped 27-08-2026, [PR #376](https://github.com/sanskrit-lexicon/csl-corrections/pull/376)

## Order and prerequisites

Independent of the other thirteen repos — a failure here blocks nothing else. Cross-repo ordering lives in the programme roadmap.

## Done

- **27-08-2026 — Wave 1 ([PR #376](https://github.com/sanskrit-lexicon/csl-corrections/pull/376), Opus 5 `claude-opus-5`).** The ruling-F1 pointer line
  now stands in [CLAUDE.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/CLAUDE.md):
  infra gotchas go to [Uprava/FINDINGS.md](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md),
  Sanskrit-data gotchas to [SanskritLexicography/FINDINGS.md](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md),
  and this repo keeps no registries of its own. Nothing here touched `csl-orig`.

  ⚠️ **The ruling-F8 SHARED_CODE row was already standing** and was **not** re-added. It landed
  out of programme order on 27-08-2026 as row 27 of
  [SHARED_CODE.md](https://github.com/gasyoun/github-spine/blob/main/SHARED_CODE.md) under
  [H3561](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3561-Opus_github-spine_interconnect-spine-aistate-sharedcode-families_26.08.26.md)
  ([github-spine PR #127](https://github.com/gasyoun/github-spine/pull/127)), written from the shipped
  code rather than from this handoff's spec. It was read line by line against this handoff's
  acceptance and states all three fence clauses verbatim in its rule column — agents never commit or
  push to `csl-orig` and never open a small per-correction PR; change files here are an audit trail,
  not applied at generation time; delivery is one consolidated PR at most roughly monthly — so no
  enrichment was owed either. A second row for the same family would be a duplicate, not an adjacent
  row to keep. Same resolution as
  [H3570](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3570-Opus_SanskritKaraoke_interconnect-karaoke-timing-caption-family_26.08.26.md)
  reached for row 28.

Verification gates: [VERIFICATION_SPINE_INTERCONNECTION.md](https://github.com/gasyoun/Uprava/blob/main/docs/VERIFICATION_SPINE_INTERCONNECTION.md).
For csl-corrections specifically: wiring score at or above **40** (or a written reason it
deliberately did not move), no new `interlinks_edges_check.py` errors or warnings beyond the
26-08-2026 baseline of four errors and thirteen warnings, and the README passing Gate 4's three
questions when read cold.

_Dr. Mārcis Gasūns_
