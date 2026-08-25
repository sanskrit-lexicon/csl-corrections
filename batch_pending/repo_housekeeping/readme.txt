repo_housekeeping queue — non-dictionary housekeeping for sanskrit-lexicon repos
Filed per /cologne-correction-queue durability contract (H2086): validated, queued, pushed.
Delivered at the monthly batch window alongside dictionary corrections.

## Batch 2026-08-24 — changelog filename casing normalization

> DELIVERED 25-08-2026: 22/22 rename PRs open (one branch `chore-changelog-casing` + one PR per repo); DCS verified no-op with written verdict on its row. Monthly-window merge set.

MG ruling 24-08-2026 («go» on ox-alpha close): normalize every lowercase
`changelog.md` to `CHANGELOG.md` across gasyoun-owned repos was executed same-day
(9 repos, direct); these fenced sanskrit-lexicon/* upstreams ship via this queue
instead — no direct pushes, no solo PRs (Cologne fence).

Per-repo action at drain time, for each repo below:
  git fetch origin
  git worktree add -b chore-changelog-casing <tmp> origin/<branch>
  git -C <tmp> mv changelog.md __t && git -C <tmp> mv __t CHANGELOG.md
  sweep remaining lowercase `changelog.md` references in tracked files -> CHANGELOG.md
  commit "chore: rename changelog.md to CHANGELOG.md, update references"
  push as ONE consolidated multi-repo PR set at the monthly window (or fold into
  the batch PR if maintainers prefer a single housekeeping PR per repo)

Status dots: 🔵 clean validation · 🟡 caveat worth human glance · 🔴 do not file.

🔵 24-08-2026 AMAR [main@9656170] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/AMAR/pull/15
🔵 24-08-2026 AP [main@3aed8dc] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/AP/pull/52
🔵 24-08-2026 AP90 [master@8c1b50f] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/AP90/pull/53
🔵 24-08-2026 BHS [main@9112631] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/BHS/pull/21
🔵 24-08-2026 CAE [main@f266123] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/CAE/pull/14
🔵 24-08-2026 CCS [main@d17ea98] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/CCS/pull/11
🔵 24-08-2026 FRI [main@579eb37] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/FRI/pull/23
🔵 24-08-2026 GRA [main@6bf8d65] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/GRA/pull/61
🔵 24-08-2026 KNA [main@4df5052] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/KNA/pull/12
🔵 24-08-2026 KOW [main@47b9d13] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/KOW/pull/10
🔵 24-08-2026 LRV [main@3a83454] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/LRV/pull/45
🔵 24-08-2026 MCI [master@c58bcbc] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/MCI/pull/10
🔵 24-08-2026 MD [main@03dfa91] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/MD/pull/30
🟡 24-08-2026 MWS [master@0018775] rename changelog.md -> CHANGELOG.md; MWS is high-traffic - re-validate base moved before branch | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/MWS/pull/293 (re-validated 25-08-2026: tip unchanged at 0018775)
🔵 24-08-2026 PUI [main@46dc6e8] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/PUI/pull/11
🔵 24-08-2026 PWG [main@038bae5] rename changelog.md -> CHANGELOG.md; PWG is active drain lane - re-validate base | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/PWG/pull/234 (re-validated 25-08-2026: tip unchanged at 038bae5)
🔵 24-08-2026 PWK [main@f92d49f] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/PWK/pull/146
🔵 24-08-2026 STC [main@86ad4a0] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/STC/pull/11
🔵 24-08-2026 VEI [master@dc79d76] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/VEI/pull/11
🔵 24-08-2026 Wil-YAT [main@b445233] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/Wil-YAT/pull/12
🔵 24-08-2026 csl-corrections [main@2caea26] rename changelog.md -> CHANGELOG.md (this repo itself) | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/csl-corrections/pull/371 (base moved +1 CRON commit; branched off 0391930)
🔵 24-08-2026 csl-standards [main@5f9549c] rename changelog.md -> CHANGELOG.md | OxAlpha (opencode/x-preview-f-free) | PR https://github.com/sanskrit-lexicon/csl-standards/pull/133
🟡 24-08-2026 DCS [main@916520e] NO root changelog tracked on origin/main; local clone holds untracked changelog.md - verify provenance/ownership before any change; likely leave-upstream-alone | OxAlpha (opencode/x-preview-f-free) | VERDICT 25-08-2026 (OxAlpha): leave-upstream-alone — origin/main@916520e tracks no root changelog file (git ls-tree empty); the untracked local changelog.md is session-local residue, not upstream content — do not push it, do not delete without MG's word

Already-uppercase on origin (no action): sanskrit-lexicon.github.io, csl-santam,
sanskrit-util, COLOGNE, csl-observatory, MW72, WIL, csl-devanagari, csl-guides.

Releases/tags for fenced repos are OUT OF SCOPE: upstream-owned release surface.
