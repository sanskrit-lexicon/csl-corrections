# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**csl-corrections** is a Sanskrit Lexicon **data-store** repository — part of the Cologne Digital Sanskrit Lexicon (CDSL) infrastructure.

## Correction Workflow (authoritative)

The end-to-end workflow for applying corrections to dictionary text in `csl-orig` lives in **[docs/correction-workflow.md](docs/correction-workflow.md)**. That document is the authoritative reference for:

- Repository topology (which sibling repos must be cloned together and why)
- The 8-stage workflow (snapshot → apply → promote → regenerate → validate → audit → commit → refresh)
- The full tooling reference (every script that runs and what it does)
- Which workflow to use for which correction type (markup, link target, scholarly, etc.)
- Pitfalls and gotchas (BOM, `<LEND>`, CRLF, line-count mismatches, `xmllint` setup)

Read it once end-to-end on first contact; refer back to § 4 (reference) and § 8 (gotchas) thereafter.

### Critical preflight for old correction issues

Before applying any old `csl-orig` / dictionary text-correction issue, search the
`csl-corrections` CFR and batch history for the same dictionary, L number,
headword, old text, and new text. If the registry records the proposal as
`No change`, rejected, deferred, or otherwise not to be applied, **stop** unless a
maintainer explicitly reopens the decision.

Also decide before editing whether an accepted correction should be a plain
replacement or should preserve the original text with an inline correction layer,
for example `{{old->new||YYYYMMDD|author|issue|}}`. Document this registry check
and layer/plain-replacement decision in the batch readme or handoff notes.

## Repo Category

`data-store` — see the [tooling runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md) for category-specific conventions.

## GitHub Issue Conventions

This repository uses the **Cologne tooling-repo taxonomy**. All issues must have:
- **Exactly one type label** (9 options)
- **Exactly one severity label** (4 levels)
- **One milestone** (5 options)

### Type Labels
- `bug` — Code defect (wrong output, broken contract)
- `feature` — Net-new capability
- `enhancement` — Improvement to existing capability
- `performance` — Speed, memory, throughput optimization
- `tech-debt` — Refactoring, cleanup, dependency updates
- `security` — CVE, auth issue, credential exposure
- `documentation` — Prose docs, API docs, comments
- `infrastructure` — CI/CD, deploy, data pipelines, build tooling
- `question` — Research, proposals, open discussions

### Severity Labels
- `trivial` — Cosmetic, < 1 hour
- `minor` — Single function/component
- `major` — Multiple files, design decision
- `critical` — Blocks users, data loss/security CVE

### Milestones
- **API Stability** — performance, security, regressions
- **User Experience** — bugs, features, enhancements
- **Data Quality** — data-pipeline issues, integrity
- **Developer Experience** — tech-debt, infrastructure, docs
- **Community** — questions, proposals, discussions

## Cross-Repo Coordination

The org-level project [Tooling Roadmap](https://github.com/orgs/sanskrit-lexicon/projects/9) tracks tool work across all repositories.

## Operational hazard notes

Destructive-risk facts for this repo (do-not-rerun scripts, decoys, traps) are
registered centrally in an org-private hub
([Uprava DANGER_FACTS.md](https://github.com/gasyoun/Uprava/blob/main/DANGER_FACTS.md),
org members only); the public-safe subset is mirrored in the generated block of
[AGENTS.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/AGENTS.md). Check them
before running anything that writes.
