_Created: 13-06-2026 · Last updated: 05-09-2026_

# Changelog

All notable changes to csl-corrections are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

## [Unreleased]

## [1.0.1] - 2026-08-30
### Changed

- **H3571 — ruling-F1 hub-FINDINGS pointer line** (Opus 5 `claude-opus-5`, 27-08-2026).
  [CLAUDE.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/CLAUDE.md) now names
  where this repo's gotchas go — infra/process to
  [Uprava/FINDINGS.md](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md), Sanskrit data to
  [SanskritLexicography/FINDINGS.md](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md)
  — states that this repo keeps no registries of its own, and points at the queue-to-batch-PR
  bridge's SHARED_CODE family row 27 (ruling F8), which was verified standing and deliberately not
  re-added. Roadmap Wave 1 ticked. `csl-orig` untouched.

- **H2820 — CLAUDE.md truth-pass** (Grok 4.6 `grok-4.6`, 16-08-2026). What this
  repo is (correction staging / audit trail), how to run
  (`updateByLine.py`, `build_correction_loci.py --selftest`,
  `/cologne-correction-queue` + `/cologne-batch-pr`), and the
  never-commit/`csl-orig` fence. Taxonomy tables removed. AGENTS.md twin
  regenerated.

### Added
- **Pipeline audit — csl-orig correction queue (H2022, Fable 5 `claude-fable-5`).**
  [docs/PIPELINE_AUDIT_CSL_ORIG_CORRECTION_QUEUE_06-08-2026.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/PIPELINE_AUDIT_CSL_ORIG_CORRECTION_QUEUE_06-08-2026.md)
  — call graph, silent-failure census, capability inventory and six ranked gap specs for the
  `/cologne-correction-queue` → `/cologne-batch-pr` path, plus a dual-run adjudication against the
  Grok 4.5 (`grok-4.5`) lane of 01-08-2026. Audit-only; gap execution is
  [H2306](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2306-Sonnet_csl-corrections_queue-skill-durability-contract-reconcile_06.08.26.md).
  Headline: the H2086 durability fix shipped a doc and a checker but never updated the skill that
  fills the queue, which still says "never push it"; the queue stage also still opens the csl-orig
  swap window its sibling skill bans by name, and validates against the working tree rather than the
  delivery base.

## [1.0.0] - 2026-06-13

### Added
- Added this changelog so repository-level changes have a stable home.
- Recorded the current repository purpose: CDSL data-store repository in the Sanskrit Lexicon project.

### Recent Git History
- 2026-06-03 ai-wip: journal F6-final (stratified, prose own across strata) + forensic migration to csl-atlas
- 2026-06-03 ai-wip: journal F5 — MW copies PWG's citation order (structural copycat)
- 2026-06-03 ai-wip: journal F4b — CORRECTIONS cloned, headword-error question settled (MW didn't copy errors)
- 2026-06-03 ai-wip: journal F4a + SKD/VCP citation-tagging correction
- 2026-06-03 ai-wip: journal L3 forensic suite (F0-F3) — MW copied skeleton, recomposed flesh

_Dr. Mārcis Gasūns_
