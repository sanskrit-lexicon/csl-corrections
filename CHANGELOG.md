_Created: 13-06-2026 · Last updated: 06-09-2026_

# Changelog

All notable changes to csl-corrections are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

## [Unreleased]
### Changed

- **H3885 — submitter e-mail privacy + fail-loud intake + honest form feedback**
  (OxAlpha `x-preview-f-free`, executing Opus 5's minted mission, 06-09-2026).
  Nothing in a nightly commit carries a submitter address any more:
  `cfr_email_mask.py` pseudonymises the e-mail column (HMAC-SHA256, optional
  `CFR_EMAIL_SALT` secret, `:<status>` suffix preserved, idempotent) and is
  applied where the leaks actually were — `cfr_adj.py` masks the raw
  `daily/<date>/*.tsv` in place before parsing, `scripts/update_cfr_ab.py`
  masks every `cfr_ab/cfr_ab.tsv` line including the pre-20260404 block, and a
  new `scripts/check_no_emails.py` gate refuses the nightly commit if any
  address survived. `fetch_yesterday_cfr.sh` now uses `curl -fsS --retry 3`
  (a 404 = "no submissions yesterday" = clean exit 0, not a saved error page)
  under `set -euo pipefail`. `app/correction_form_response.php` checks
  fopen/flock/fwrite/fflush, answers HTTP 500 with a machine-readable error
  token on failure, caps fields at 2000 chars, and restricts CORS to
  `sanskrit-lexicon.uni-koeln.de`; `app/correction_form.php` shows the
  thank-you page only on a confirmed success (postMessage + same-origin
  status-token fallback + 15 s timeout) instead of on any iframe load. The
  nightly issue body drops the `, user=…` fragment. Git history is NOT
  rewritten — purging the 2,848 address-bearing lines already in `cfr_ab`
  history remains a separate maintainer decision. Deployment of `app/` to the
  Cologne server is a maintainer act. Evidence:
  [CODEBASE_IMPROVEMENT_MAP_2026-09.md](https://github.com/gasyoun/csl-observatory/blob/main/docs/CODEBASE_IMPROVEMENT_MAP_2026-09.md)
  §6.3 Rank 1 (findings B2/B3/B13/B14).

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
