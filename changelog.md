# Changelog

All notable changes to csl-corrections are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

## [Unreleased]

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
