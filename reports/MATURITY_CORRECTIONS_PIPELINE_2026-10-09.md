# Maturity audit — Cologne corrections pipeline as estate reference (H6289)

_Created: 12-10-2026 · Last updated: 12-10-2026_

**Executor:** OxAlpha (opencode/z-ai/glm-5.3-flash). **Handoff:** [H6289](https://github.com/gasyoun/Uprava/blob/main/handoffs/H6289-OxAlpha_csl-corrections_maturity-corrections-pipeline_09.10.26.md).
**Worktree:** `h6289-drain` off `origin/main` @ `bc2d8b9`. **Analysis window:** 2014-01-01 → 2026-10-12 (registry lane), 2019 → 2026-10-12 (issue lane), last 90 days highlighted.
**Prior art consumed, not duplicated:** [PIPELINE_AUDIT_CSL_ORIG_CORRECTION_QUEUE_06-08-2026.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/PIPELINE_AUDIT_CSL_ORIG_CORRECTION_QUEUE_06-08-2026.md) (H2022 hygiene lane), [H6106](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H6106-OxAlpha_COLOGNE_zenodo-dicts-batch-coverage_05.10.26.md) (DOI baseline), [BATCH_RUNBOOK.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_RUNBOOK.md).

---

## 1. Verdict: **4 / 5**

The pipeline is the estate's strongest correction contour: enforced intake registry, gated derived census, durable queue, enforced issue taxonomy, fenced upstream. It loses a point not for engineering but for **land velocity at the far tail** — three consecutive correction batches (July + August 2026) sit unmerged upstream after 60+ days, and the intake registry's verdict column has been unmaintained since 2023. A reference should be honest about both.

| Axis | Score | Basis |
|---|---|---|
| Intake automation (cron + registry) | 5/5 | daily cron commits alive as of 2026-10-11; 26,942-row append-only registry |
| Machine verification depth | 5/5 | 100% of queued records pass updateByLine→XML gates; census selftest + durability gate both green live |
| Issue pipeline discipline | 4/5 | taxonomy verifier-enforced; P50 close = 6 days (n=127); 64 open backlog, oldest 1,898 days |
| Land velocity (report→upstream merge) | 2/5 | P50 report→parked fast; upstream merge tail **stalled**: #2879, #2884, #2885 all OPEN 60+ days |
| Citable-liveness (DOI) | 5/5 | live DataCite count 422 ≥ baseline 417; delta explained; canary record resolves with payload |

## 2. Queue metrics (evidence: `gh api` + local registry, receipts §7)

### 2.1 Report→land, issue lane (`gh api`, all 127 closed `text-correction` issues)

- **P50 = 6 days, P90 = 74 days** (min 0, max 465, n=127).
- Recent 90-day window (2026-07-14…2026-10-12): **8 closed, P50 = 19 d, P90 = 22 d** — slower but steady; the last cluster (#306–#310) closed exactly on batch day 2026-08-04, i.e. issues are closed at batch-drain, not at report.
- Open backlog: **64 issues**; age P50 = 39 days, oldest **1,898 days** (pre-taxonomy era residue).

### 2.2 Report→verdict, CFR form registry lane (`cfr_ab/cfr_ab.tsv`, 26,942 rows)

- 8,599 rows carry a dated "Corrected <date>" verdict: **P50 = 88 days, P90 = 205 days** — the historical form era (2014–2017: 8,848 of 8,599 verdicts; 2016 alone 7,070).
- **Finding (weak spot):** verdict-year distribution hits **zero in 2018–2026 except 60 (2019), 23 (2020), 11 (2021), 110 (2022), 2 (2023)**. The modern agent pipeline lands corrections via `batches/` + issues and stopped writing dated verdicts back into the registry. The registry is append-only for arrivals but its closure field is dead — the single best "copy the lesson, not the artifact" item for other contours.

### 2.3 Volume and cadence (`data/derived/correction_loci.tsv`, 61,430 records)

- Last-30-days landed volume: **0** (latest batch `batch_20260804`, 21,875 records). Window extended per the handoff fail-rule; explanation below, not a stall: the pipeline parks into `batch_pending` and ships **one consolidated monthly PR** — and the last three monthly PRs are still awaiting upstream merge (§2.4), so nothing new has been promoted since 04-08.
- Batch-month volume is deliberately lumpy: 22,131 (2026-05, BOR markup bulk), 21,875 (2026-08, mw markup bulk), 2,477 (2025-11), tens-to-hundreds for human steady-state months.
- Current queue depth: **1 validated change file** (`batch_pending/dictionaries/pw/change_pw_h3152_link_splitting.txt`) + 2 repo-housekeeping items — queue is near-clear.

### 2.4 Land tail — the load-bearing weak spot

`gh api repos/sanskrit-lexicon/csl-orig/pulls` (12-10-2026): the three most recent correction-batch PRs are **all OPEN**:

| PR | Title | Created | Merged |
|---|---|---|---|
| csl-orig [#2885](https://github.com/sanskrit-lexicon/csl-orig/pull/2885) | corrections: mw 2026-08 batch (21,811 lines) | 2026-08-04 | **OPEN (69 d)** |
| csl-orig [#2884](https://github.com/sanskrit-lexicon/csl-orig/pull/2884) | corrections: 2026-08 batch (57 changes) | 2026-08-04 | **OPEN (69 d)** |
| csl-orig [#2879](https://github.com/sanskrit-lexicon/csl-orig/pull/2879) | corrections: 2026-07 batch (ap90, 15 changes) | 2026-07-12 | **OPEN (92 d)** |

Local half (report→parked→validated→PR opened) is fast and disciplined; the merge is human-gated by the foreign maintainer. **This is correct governance (csl-orig tolerates no noise, merge is `@WAITING` not stalled on our side) — but a maturity reference must name it:** the metric that actually reaches the printed dictionary is report→*upstream merge*, and it currently dominates every other latency in the pipeline.

## 3. Machine-verifier share

- **100% of queued/landed correction records** pass the machine gates: `updateByLine.py` parse + XML validation at queue time, delivery-base re-validation (`git show origin/main:…`) at drain time ([correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md), [BATCH_RUNBOOK.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_RUNBOOK.md)).
- By origin (`process` column): **bulk (machine-generated markup batches) 30,053 = 48.9%**, human 31,377 = 51.1% of all 61,430 records.
- **Live receipts, 12-10-2026, this worktree:**
  - `python scripts/build_correction_loci.py --selftest` → `SELFTEST OK — census invariants hold (100% <pc> header coverage included)`, exit 0.
  - `python scripts/check_batch_pending_tracked.py` → `OK — all batch_pending files tracked and working tree clean`, exit 0 (checker now runs `git fetch` + tracking-branch ahead-count — the H2022 fix-wave landed).

## 4. Zenodo/DOI liveness (live probes, 12-10-2026)

- **DataCite counter (live):** `api.datacite.org/dois?query=relatedIdentifiers.relatedIdentifier:*sanskrit-lexicon*` → **total = 422** vs H6106 baseline **417** → **canary gate PASS (≥417)**.
- **Delta +5 explained, not hand-waved:** 4× `csl-standards — CDSL data standards & export profiles` (concept+version pairs minted 2026-10-06 and 2026-10-10/11, i.e. after H6106) + 1× OBS-T Correction-Event Corpus version record (2026-10-06).
- **32/32 concept coverage:** the 05-10-2026 mint wave is visible live (recids 23151226–23151395 resolving, e.g. VEI `zenodo.23151395/96`, Vācaspatyam `…31394/93`, Stchoupak `…31391/92`, SKD `…31389/90`, Śabda-Sāgara `…31381/82`, Nachträge `…31378/77`, Purana Index `…31376/75`); registry [data/zenodo_dict_concept_dois.json](https://github.com/gasyoun/Uprava/blob/main/data/zenodo_dict_concept_dois.json).
- **Own-data canary:** `curl -L zenodo.org/api/records/23151390` (SKD) → title `Śabdakalpadruma — Rājā Rādhākānta Deva · Calcutta, 1822–1858`, `isSupplementTo` → `github.com/sanskrit-lexicon/SKD/tree/main`, 1 file, 11,315,836 bytes — **PASS**.

## 5. Regression policy

1. **Delivery-base re-validation at drain:** `/cologne-batch-pr` re-validates every queued record against `git show origin/main:…`, never the working tree (the D3 lesson, measured at 20,618/21,817 failures on 04-08-2026).
2. **Census invariants:** `build_correction_loci.py --selftest` gates the derived layer; the summary figures in this report re-derive from it.
3. **Durability gate (H2086):** queue files must be tracked+pushed same session; checker now fetches and compares the tracking branch (post-H2022 hardening verified live above).
4. **Base-staleness guard:** `scripts/pre_push_stale_base_check.py` on pre-push.
5. **Byte-shape discipline:** BOM check + CR-doubling lesson (H2022 D4) documented at both skills.
6. **Issue taxonomy verifier:** `csl-corrections_verify.py` enforces 9 types × 3 severity × 4 milestones on every issue.

## 6. Переносимые практики (portable practices for other estate contours)

1. **Append-only intake registry + daily cron** (`cfr_ab.tsv` + 00:00 UTC fetch): every inbound correction lands in one greppable TSV before any human touches it. Copy to: Systema support inbox, samskrtam feedback, Gramota-form contours.
2. **Derived census with a `--selftest` invariant gate**: never hand-maintain counts; parse the raw change records into one TSV and gate rebuilds with invariants. Copy to: every `census`/`доля`-style reporting doc in the estate.
3. **Durability gate on staging areas** ("tracked + pushed same session, checker fails on unpushed, fetch-first"): the H2086 pattern generalizes to any agent-parked WIP (queue folders, review packets).
4. **One consolidated upstream PR per month, fenced upstream**: batch noise discipline keeps a foreign maintainer willing to review. Copy to: any contour shipping to repos we don't own.
5. **Validate against the delivery base, not the working tree**: re-validate at ship time against `git show origin/main:` — the single highest-value anti-stale measure in the pipeline.
6. **Verifier-enforced taxonomy** (types/severities/milestones via script, not convention): keeps the tracker machine-queryable, which is exactly what made §2.1 computable in one `gh api` pass.
7. **Anti-pattern to copy as a warning:** knowledge stored in the LAST stage (H2022 D1–D4 — the drain skill knew three lessons the queue skill never received). Any estate skill pair feeding each other must carry the same constraints at BOTH ends.
8. **Anti-pattern to fix here (target of practice 2):** the registry's verdict column is dead since 2023 — closure must be written back by the landing stage, not by human memory.

## 7. Receipts (verbatim probes, 12-10-2026)

```
# DataCite live count
$ curl -s "https://api.datacite.org/dois?query=relatedIdentifiers.relatedIdentifier:*sanskrit-lexicon*&page[size]=1"
→ meta.total = 422   (baseline 417, H6106)   → PASS ≥417

# Newest org-linked DOIs (sort=-created, page 1)
2026-10-11 10.5281/zenodo.23294361 csl-standards — CDSL data standards & export profiles
2026-10-10 10.5281/zenodo.23287891 csl-standards — CDSL data standards & export profiles
2026-10-06 10.5281/zenodo.23181181 csl-standards — …
2026-10-06 10.5281/zenodo.23181157 csl-standards — …
2026-10-06 10.5281/zenodo.23177770 OBS-T: CDSL Correction-Event Corpus …
2026-10-05 10.5281/zenodo.23151395 The Vedic Index of Names and Subjects …
   (+ 26 further 2026-10-05 H6106-wave concept/version pairs)

# Zenodo own-data canary
$ curl -sL https://zenodo.org/api/records/23151390
→ title: Śabdakalpadruma — Rājā Rādhākānta Deva · Calcutta, 1822–1858
  related: isSupplementTo https://github.com/sanskrit-lexicon/SKD/tree/main
  files: 1 (11,315,836 bytes)

# gh api queue lane (12-10-2026)
$ gh api repos/sanskrit-lexicon/csl-corrections --jq '{open_issues_count, updated_at}'
→ {"open_issues":68,"updated":"2026-10-12T03:35:24Z"}
text-correction closed issues: n=127, close P50=6d P90=74d; last-90d n=8 P50=19d P90=22d
open issues: n=64, oldest=1898d, P50 age=39d
$ gh api repos/sanskrit-lexicon/csl-orig/pulls (correction batches)
2885 2026-08-04 OPEN · 2884 2026-08-04 OPEN · 2879 2026-07-12 OPEN

# Live verifier receipts (worktree h6289-drain @ bc2d8b9)
$ python3 scripts/build_correction_loci.py --selftest
SELFTEST OK — census invariants hold (100% <pc> header coverage included)
$ python3 scripts/check_batch_pending_tracked.py
OK — all batch_pending files tracked and working tree clean

# Local lanes (this worktree)
cfr_ab/cfr_ab.tsv: 26,942 rows; 8,599 dated verdicts → P50=88d P90=205d; verdict years 2014–2023, none 2024–2026
data/derived/correction_loci.tsv: 61,430 records; bulk 30,053 (48.9%) / human 31,377
batch months (last 6): 2025-11:2477 · 2026-02:53 · 2026-05:22131 · 2026-06:25 · 2026-07:15 · 2026-08:21875
last-30d landed: 0 (latest batch_20260804; monthly consolidated cadence + upstream merge tail §2.4)
queue depth: 1 change file + 2 housekeeping items
```

## 8. Risks & honest caveats

- **«Эталон» ≠ «идеален»:** upstream merge tail (§2.4) and the dead registry verdict column (§2.2) are recorded as first-class weak spots, per the handoff risk clause.
- **"LG-фиксы" term UNVERIFIED as written:** "LG" appears only in the H6289 mission text — no `csl-lg` repo exists in `sanskrit-lexicon` (404) and no prior art defines it. Interpreted as "liveness of the fix pipeline" and measured via the issue-fix lane (§2.1) + live verifier receipts (§3); if LG names something specific, this row needs MG's one-line ruling.
- Registry lane historical skew: P50/P90 in §2.2 describe the pre-agent era; the current equivalent is §2.1.
- Foreign-org repo touched: **read-only** (`gh api` + `curl`); the only change on our side is this report.

---

_Dr. Mārcis Gasūns_
