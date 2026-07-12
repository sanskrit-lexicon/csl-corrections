# Correction-data hypotheses, visualisations, and new data layers — design memo

_Created: 07-07-2026 · Last updated: 08-07-2026_

**What this is.** The deep-analysis memo commissioned by
[H271](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H271-Fable_csl-corrections_correction-hypotheses-atlas-DH-ACL_07.07.26.md):
what new, testable hypotheses the ~39.5k-record correction corpus in this repo supports, which
visualisations should exist (here and in [`csl-atlas`](https://github.com/sanskrit-lexicon/csl-atlas)),
which unmined data layers can become new sections, and which ACL-Anthology methods transfer.
**Memo only — nothing was built or changed in the data.** The atlas-facing half lives in the
cross-linked sibling memo
[`csl-atlas/docs/DH_IMPROVEMENT_MEMO.md`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/DH_IMPROVEMENT_MEMO.md).

**Provenance.** Researched and written 07-07-2026 by Fable 5 (`claude-fable-5`); repo census,
atlas inventory, org reuse map, and the live ACL-Anthology fetch were run the same day by four
parallel Explore subagents (also Fable 5 `claude-fable-5`, inherited). All counts below were
measured against the working tree at `origin/main` = the `[CRON] daily corrections for 2026-07-06`
commit. This is one memo in a sequential five-repo series; the only finished sibling at write
time was [H265](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H265-Fable_SanskritLexicography_acl-anthology-dh-standards-reverse-dict_07.07.26.md)
(its deliverable:
[`ReverseDictionary/ACL_DH_COMPATIBILITY_ANALYSIS.md`](https://github.com/gasyoun/SanskritLexicography/blob/master/ReverseDictionary/ACL_DH_COMPATIBILITY_ANALYSIS.md)),
whose venue landscape and Responsible-NLP/data-statement standards are reused here, not re-fetched.

---

## 0. Headline findings

1. **The event-level typology is already built — do not rebuild it.**
   [`csl-observatory`](https://github.com/sanskrit-lexicon/csl-observatory) owns OBS-T
   ([`reports/obs_t_paper_draft.md`](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/reports/obs_t_paper_draft.md),
   paper A12): a 50,953-event correction corpus (release CSV
   [`correction_events_release.csv`](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/observatory/site/src/data/correction_events_release.csv)
   = 52,498 rows read 07-07-2026), 43 dicts, 210 correctors, 2014–2026, with a 9-label
   microstructure component per event, ERRANT-style edit types, OCR classes, corrector identity,
   latency, evidence labels, and a train/test split — plus per-dict fingerprints
   (χ²(112) = 58,934.6, Cramér's V = 0.411) and Mann-Kendall diachronic trends already computed.
   Every hypothesis below is framed as a **gap beyond OBS-T**, consuming it where possible.
2. **What this repo uniquely holds is the *locus + full-line* layer.** OBS-T's schema
   ([`data/schema/correction-event.schema.json`](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/data/schema/correction-event.schema.json))
   carries `lcode` but **no page/column field** — while **every one of the 39,606 change-file
   meta-headers here carries `<pc>`** (verified: 39,606/39,606 match `^; <L>…<pc>`). The paired
   `old`/`new` records also preserve the **full source line with markup** (`<s>`, `<lex>`,
   `<ls>`, `<info>`), where OBS-T normalizes to IAST. Loci + raw markup diffs are the two signals
   nobody has mined.
3. **The corpus is two different processes, not one.** 30,053 of 39,544 records (76%) come from
   two bulk machine-generated markup batches
   ([`batch_20260529/dictionaries/bor/change_bor_markup_1.txt`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20260529/dictionaries/bor/change_bor_markup_1.txt)
   = 21,990; [`batch_20250418/dictionaries/lrv/markhom/change_lrv_1.txt`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20250418/dictionaries/lrv/markhom/change_lrv_1.txt)
   = 8,063). The remaining ~9.5k records — plus the daily CFR stream — are steady human
   correction. Any statistic that pools them without a `process` split is misleading; the split
   is itself a feature (hypothesis C2).
4. **The highest-leverage build is one derived table.** A single locus-resolved
   `correction_loci.tsv` (§5.1) unlocks four atlas visualisations, extends the forensic
   copy-detection stream, and upgrades OBS-T with a spatial dimension — small build, many
   consumers. It heads the ranked backlog (§7).

---

## 1. Ground truth (measured 07-07-2026)

| Fact | Value | Where |
|---|---|---|
| Correction records (all change files) | **39,544** (39,540 old/new pairs + 4 `del`; no `ins` in data) | 10 batches: 6 legacy `batch_*/` + 4 nested `batches/*/` |
| Skew | BOR markup 21,990 + LRV markhom 8,063 = **76%** of records | see §0.3 |
| Dicts actually touched by change files | ~17 (ap, ap90, bop, bor, bur, gra, inm, krm, lrv, mw, mw72, pw, pui, shs, skd, stc, + root batch) | batch folders |
| `<pc>` locus coverage | **100%** — 39,606/39,606 meta-headers | grep over all change files |
| Daily CFR stream | **91 folders**, 2026-04-04 → 2026-07-03; 8-col TSV, per-row timestamp + **submitter identity** (col 8) | [`daily/`](https://github.com/sanskrit-lexicon/csl-corrections/tree/main/daily) |
| Master correction ledger | [`correctionform.txt`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/correctionform.txt): 26,246 records, 0 pending, as of 2026-04-26; per-record date, user, status | repo root |
| Historical CFR archive | 2020: 77 rows · 2021: 303 · 2022: 331 (+ 3 MB master TSVs) | [`app/correction_response/`](https://github.com/sanskrit-lexicon/csl-corrections/tree/main/app/correction_response) |
| Commit rhythm | daily `[CRON]` bot commits + human `DC <date>` commits; Jim Funderburk (392+39) and Dhaval Patel (233+61+56+2) dominate | `git log` |
| GRA dialect | inline `<chg type="del|chg" n="N" src="gra"><old>…</old></chg>` wrappers inside otherwise standard records | [`batch_20260529/dictionaries/gra/`](https://github.com/sanskrit-lexicon/csl-corrections/tree/main/batch_20260529/dictionaries/gra) |

Reproducibility snapshot: all velocity/stream figures in this memo refer to the CFR range
**2026-04-04 → 2026-07-03** and the ledger state **as of 2026-04-26**; the stream is live and
growing, so re-runs will differ.

What already consumes this repo (do not duplicate): the csl-atlas forensic scripts
[`f4_shared_corrections.py`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/scripts/forensic/f4_shared_corrections.py)
and [`f4b_ahlborn_nulltest.py`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/scripts/forensic/f4b_ahlborn_nulltest.py)
read it into
[`data/forensic/shared_corrections.csv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/forensic/shared_corrections.csv)
(290 rows, keyed SLP1 headword + dict) — the APPARATUS-NOT-ERRORS evidence. No atlas *page*
ingests corrections yet; that is the gap the sibling memo targets.

---

## 2. Thread 1 — hypotheses (each: claim · inputs · method · confound · outcomes)

### C1 — Locus-resolved error typology per dictionary

- **Claim.** Per-dict error-density fingerprints differ not only by *component* (OBS-T already
  shows this) but by *where on the printed page* and *at which markup depth* errors sit; the raw
  markup-level diffs separate error classes OBS-T's IAST normalization merges (e.g. `<ls>`
  citation slips vs `<s>` transliteration slips at the same string distance).
- **Inputs.** All change files (full `old`/`new` lines + `<pc>`/`<k1>` headers); OBS-T release
  CSV for the component labels; entry counts per dict from
  [`union_headwords.tsv`](https://github.com/gasyoun/SanskritLexicography/blob/master/HeadwordLists/union/union_headwords.tsv)
  for normalization.
- **Method.** ERRANT-style edit extraction over the raw lines (Bryant et al. 2017,
  [P17-1074](https://aclanthology.org/P17-1074/)), classified by the tag context the edit falls
  inside (`<s>`/`<lex>`/`<ls>`/plain text); join to OBS-T events by (dict, lcode) to inherit its
  labels; report raw AND per-1k-entries densities.
- **Confound.** The 76% bulk-batch skew (§0.3) — report with `process ∈ {bulk, human}` split
  always; BOR/LRV would otherwise dominate every figure.
- **Positive / null.** Positive: tag-context distributions differ significantly per dict after
  the split (χ², effect size), giving each dict a dirt-fingerprint by layer. Null: differences
  vanish once bulk batches are excluded — meaning OBS-T's component labels already capture
  everything and the markup layer adds nothing.

### C2 — Two-process correction dynamics (velocity, half-life, backlog)

- **Claim.** Bulk machine batches and steady human corrections have distinguishable dynamics;
  for the human stream, per-dict correction velocity is declining for "surface-stable" dicts
  (a measurable *correction half-life*), while backlog latency (submission → `Corrected` status)
  is roughly constant.
- **Inputs.** [`daily/`](https://github.com/sanskrit-lexicon/csl-corrections/tree/main/daily)
  CFR TSVs (per-row timestamps), `correctionform.txt` (per-record `status = Corrected <date>` →
  latency), batch folder dates, OBS-T's `latency_days` for the 2014–2026 backdrop.
- **Method.** Fit per-dict arrival-rate curves separately per process; half-life = time for the
  human-stream rate to halve; survival analysis on submission→commit latency. OBS-T's
  Mann-Kendall trends are component-level — this is dict-level and process-split, which it does
  not report.
- **Confound.** The daily stream is only 91 days old — seasonality claims are underpowered;
  say so. Corrector-population changes (one prolific submitter joining/leaving) masquerade as
  velocity change; control by corrector identity (col 8).
- **Positive / null.** Positive: dicts cluster into converging / churning / dormant with
  distinct half-lives — directly actionable for "what to digitize-QA next". Null: rates are
  corrector-driven noise; then the actionable object is the corrector, not the dict (→ C5).

### C3 — Shared-error copy detection via correction loci

- **Claim.** The same error corrected the same way at *corresponding loci* in two dictionaries
  is stronger inheritance evidence than shared headword anomalies — a correction is a
  human-certified error, removing the "maybe both are legitimate variants" escape that weakens
  anomaly-based signals.
- **Inputs.** Change files (dict, `<k1>`, `<pc>`, old→new); atlas forensic layer
  ([`shared_corrections.csv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/forensic/shared_corrections.csv),
  [`pair_shared_typo_counts.csv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/forensic/pair_shared_typo_counts.csv));
  [`ls_citation_edges.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/citations/ls_citation_edges.tsv)
  for the lineage backdrop.
- **Method.** Key corrections by `slp1_form_key` (from
  [`sanskrit-util`](https://github.com/sanskrit-lexicon/sanskrit-util) v0.4.0 — never
  re-implement the folding) + normalized old-string; count cross-dict matches; test against the
  null of independent OCR noise via per-glyph confusion base rates (from C4). Extends F4's 290
  rows; **extension, not duplication** — the cladistics stay in csl-atlas
  (HYPOTHESIS_INDEX APPARATUS-NOT-ERRORS is the owner).
- **Confound.** Convergent errors: two typesetters independently confusing the same glyph pair
  is common (b→v is the org's top confusion). The null model must be confusion-aware, not
  uniform.
- **Positive / null.** Positive: shared-corrected-error pairs concentrate on the already-suspected
  lineage edges (PWG→PW→MW…) beyond confusion-rate expectation. Null: matches are proportional
  to dict size × confusion rates — itself a useful negative control for the genealogy papers.
- **Scope guard (per H271 §7):** if this grows into a full forensic build, it spins out as its
  own handoff; this memo only specifies the correction-loci extension.

### C4 — OCR/print-vs-digital signatures per source edition

- **Claim.** Print-deviation corrections (the `printchange.txt` class — deviations from the
  scanned print) and digital-artifact corrections have different character-confusion signatures,
  and each source edition (typeface/typesetter) has a stable confusion matrix.
- **Inputs.** Change files split by the `printchange` boundary documented in
  [`docs/correction-workflow.md`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
  (a labeled split, not noise); OBS-T's `ocr_class`/`edit_ops` for the normalized view; raw
  SLP1/markup lines here for the unnormalized view.
- **Method.** Character-level alignment over old→new inside `<s>`…`</s>` spans; per-dict (proxy
  for edition) confusion matrices; compare against the DCS grapheme frequencies
  ([`VisualDCS/derived-data/Fonetika/regen-2026/`](https://github.com/gasyoun/VisualDCS/tree/master/derived-data/Fonetika/regen-2026))
  to separate "confusable glyph" from "frequent glyph". Method transfer: the Sanskrit post-OCR
  benchmark's SLP1-byte modelling (Maheshwari et al. 2022,
  [2022.findings-emnlp.466](https://aclanthology.org/2022.findings-emnlp.466/)) and romanised-
  Sanskrit post-OCR (Krishna et al. 2018, [K18-1034](https://aclanthology.org/K18-1034/)).
- **Confound.** Corrections are a *biased sample* of errors — only errors someone noticed. The
  org's own finding that 12 years of corrections cover ~10–14% of the estimated error population
  ([SanskritLexicography FINDINGS §46](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md))
  caps all detection-rate claims; state confusion matrices as *reported-error* matrices.
- **Positive / null.** Positive: per-edition matrices are stable across batches (split-half
  reliability) → a usable prior for auto-flagging not-yet-corrected text. Null: matrices are dominated
  by a few global pairs (b/v, ṇ/n) with no edition effect — then a single global prior suffices.

### C5 — Corrector-signature stylometry (invented)

- **Claim.** The ~210 correctors are not interchangeable: each has a stable profile over
  (component, dict, edit size, latency) — e.g. citation-checkers vs typo-hunters — and profile
  mix explains most apparent diachronic "maturation" in OBS-T's surface→meaning shift.
- **Inputs.** CFR col 8 + `correctionform.txt` `user=` field + OBS-T `corrector`/`corrector_name`.
- **Method.** Per-corrector component distributions; decompose OBS-T's era shift into
  within-corrector change vs corrector-population change (a Blinder–Oaxaca-style decomposition).
  IAA framing per Artstein & Poesio 2008 ([J08-4004](https://aclanthology.org/J08-4004/)) where
  two correctors touch the same locus.
- **Confound.** Identity strings are messy (emails vs bare names, Jim/Dhaval under multiple
  identities in git); needs an alias map first — same problem the org solved for sigla, reuse
  that pattern. Privacy: aggregate or pseudonymize third-party submitter emails in anything
  published (they are personal data; `/publish-safety-check` gate before any release).
- **Positive / null.** Positive: population change explains the era shift → reframes OBS-T's
  "maturation signal" finding. Null: shift holds within correctors → strengthens it. Either
  outcome is publishable as an OBS-T companion analysis.

### C6 — Intra-edition spatial clustering of errors (invented)

- **Claim.** Corrections cluster by page/column position within each printed edition — column
  boundaries, page turns, and dense-abbreviation zones are error hotspots — making `<pc>` the
  honest "spatial" dimension of the atlas (the geographic layer stays deferred, §6).
- **Inputs.** The 100%-coverage `<pc>` field (§1); page counts per edition from the scan
  metadata the Dictionary-to-Book workflow already holds.
- **Method.** Per-dict density over normalized page position and column; spatial autocorrelation
  (are consecutive pages' densities correlated?); hotspot detection vs a uniform-per-entry null.
- **Confound.** Corrector reading behavior: people proofread alphabet stretches (a-, ka-
  clusters), which *induces* spatial clustering with no typesetting cause. Distinguish via the
  bulk batches (machine passes have no reading bias) as a control.
- **Positive / null.** Positive: stable hotspots → a prioritized proofreading map per dict (the
  atlas heatmap, sibling memo §3.2). Null: clustering is pure reader-bias → still yields a map
  of *unproofread* territory, arguably more useful.

### C7 — Fix-regression rate (invented)

- **Claim.** A measurable fraction of corrections are themselves later re-corrected (same dict +
  L-number/line touched in a later batch or CFR row), and this re-correction rate is higher for
  meaning-layer fixes than surface fixes — an error half-life *of the fixes*.
- **Inputs.** Cross-batch joins on (dict, L) across the 10 batches + ledger + daily stream;
  SanskritSpellCheck's measured caveats as priors (~9% of typo "corrections" are collisions,
  queue decays ~0.8%/week —
  [SanskritLexicography FINDINGS](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md)
  §24–25).
- **Method.** Longitudinal locus tracking; survival curve of a fix; classify re-corrections as
  refinement vs revert. Method transfer: annotation-error-detection framing (Klie et al. 2023,
  [2023.cl-1.4](https://aclanthology.org/2023.cl-1.4/)) treats prior fixes as annotations to
  audit.
- **Confound.** Line numbers shift as csl-orig evolves — join on `<L>` + `<k1>` (stable), never
  raw line number; that is exactly what the meta-header was designed for.
- **Positive / null.** Positive: nonzero regression rate concentrated in sense-layer fixes →
  argues for the review-sheet gating the org already practices. Null: fixes are final →
  validates the current single-reviewer pipeline.

---

## 3. Thread 2 — visualisations

**Corrections-native (this repo — keep tiny; it's a data-store).** The README already carries
two mermaid pies (issue type/severity). Add at most three static, regenerable artifacts, all
derivable from `correction_loci.tsv` (§5.1) by one script:

| Viz | Content | Effort |
|---|---|---|
| Correction-velocity timeline | monthly records, human vs bulk process split, 2014–2026 (ledger + batches + stream) | S |
| Per-dict density bars | records per 1k entries, component-colored, bulk hatched | S |
| Batch-composition treemap | batch × dict × component — makes the BOR/LRV skew visible at a glance | S |

**Atlas-hosted (derived viz belongs in csl-atlas — full specs in the sibling memo
[`DH_IMPROVEMENT_MEMO.md`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/DH_IMPROVEMENT_MEMO.md) §3):**
error-density radar axes for the roadmap's per-dict radar (M3), the `<pc>` correction-locus
heatmap, the shared-corrected-error network overlay on the lineage graph, and the diachronic
correction-front strip. All Observable Plot + d3, Chart-Trust-Block'd, CSV-download per table —
no new stack, no Leaflet (geographic layer deferred, §6).

**HOLD-bank items unblocked by a correction feed** (from
[`csl-atlas/docs/METALEXICOGRAPHY_ROADMAP.md`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/METALEXICOGRAPHY_ROADMAP.md),
ranked): **(1)** §2.6 editorial-overlay KPIs — correction counts *are* the KPI, buildable
immediately from the loci table; **(2)** §3 per-dict radar — gains its editorial axes the same
way; **(3)** §7.1 attention timeline — remains observatory-owned (MW-ATTENTION boundary),
consume, don't build. The L0–L10 typology and 35×20 heatmap are *not* correction-gated; they
stay HOLD on their own merits.

---

## 4. Thread 5 — ACL-Anthology method transfer (live-fetched 07-07-2026)

Venues and submission standards are already covered by H265's
[`ACL_DH_COMPATIBILITY_ANALYSIS.md`](https://github.com/gasyoun/SanskritLexicography/blob/master/ReverseDictionary/ACL_DH_COMPATIBILITY_ANALYSIS.md)
(§1–2: LaTeCH-CLfL 2027 nearest, WSC 2027 flagship, Responsible-NLP checklist, data statements)
— reused, not re-fetched. The method papers below were fetched/verified today; each is mapped to
the hypothesis or viz it improves.

| Paper | What it does | Transfers to |
|---|---|---|
| Rijhwani et al. 2020, [2020.emnlp-main.478](https://aclanthology.org/2020.emnlp-main.478/) | copy-mechanism seq2seq post-OCR for endangered languages | C4 baseline architecture for auto-proposing fixes from sparse gold corrections |
| Rijhwani et al. 2021, [2021.tacl-1.76](https://aclanthology.org/2021.tacl-1.76/) | lexically-aware post-OCR (wordlist-constrained decoding) | C4 — the union headword list is the constraint lexicon, natively available |
| RESOURCEFUL 2025, [2025.resourceful-1.8](https://aclanthology.org/2025.resourceful-1.8/) | LLM post-OCR "no free lunches" evaluation | expectation-setting protocol before any LLM correction pass (pairs with C7 auditing) |
| LaTeCH-CLfL 2020, [2020.latechclfl-1.6](https://aclanthology.org/2020.latechclfl-1.6/) | two-step detect-then-correct pipeline | the queue architecture `/cologne-correction-queue` already implements — cite as precedent |
| Klie et al. 2023, [2023.cl-1.4](https://aclanthology.org/2023.cl-1.4/) | annotation-error-detection survey + protocol (nessie) | C7 fix-regression auditing; justifies how correction candidates are surfaced/scored |
| Weber et al. 2024, [2024.law-1.19](https://aclanthology.org/2024.law-1.19/) | error-taxonomy construction for generative data | formalizing the C1 typology into a defensible published taxonomy |
| Bryant et al. 2017, [P17-1074](https://aclanthology.org/P17-1074/) | ERRANT: extract-edit-then-classify | C1 edit extraction over old→new pairs (OBS-T already carries `errant_type` — extend to markup context) |
| Ahmadi et al. 2020, [2020.lrec-1.395](https://aclanthology.org/2020.lrec-1.395/) | ELEXIS MWSA sense-alignment task + relation inventory | cross-dict sense linking for the atlas dossier (sibling memo §4) |
| GlobaLex 2020, [2020.globalex-1.14](https://aclanthology.org/2020.globalex-1.14/) | supervised MWSA baseline (BERT over definition pairs) | concrete baseline if sense alignment is attempted |
| TIAD 2022, [2022.gwll-1.4](https://aclanthology.org/2022.gwll-1.4/) | translation inference across dictionary graphs | validating cross-references missing in one dict but attested in others |
| Artstein & Poesio 2008, [J08-4004](https://aclanthology.org/J08-4004/) | inter-coder agreement survey | C5; any dual-corrector adjudication (`/gold-adjudicate` already encodes this) |
| ACL 2021, [2021.acl-long.548](https://aclanthology.org/2021.acl-long.548/) | empirical IRR interpretation | defending agreement levels with few expert annotators |
| Maheshwari et al. 2022, [2022.findings-emnlp.466](https://aclanthology.org/2022.findings-emnlp.466/) | Sanskrit post-OCR benchmark; ByT5 + SLP1 ≈ +23 WER/CER | **most directly reusable** — C4 model recipe on our exact language/script problem |
| Krishna et al. 2018, [K18-1034](https://aclanthology.org/K18-1034/) | romanised-Sanskrit post-OCR, copy-augmented seq2seq | C4 for the IAST-transliterated dicts |
| Mondaca & Rau 2020, [2020.ldl-1.2](https://aclanthology.org/2020.ldl-1.2/) | **CDSL itself** → OntoLex-Lemon | the modelling target for exports — build routed to [`csl-standards`](https://github.com/gasyoun/csl-standards), per the atlas boundary |
| Tsukagoshi et al. 2025, [2025.wsc-csdh.5](https://aclanthology.org/2025.wsc-csdh.5/) | accent-aware Vedic OCR (transformer) | C4 confusion priors for accent-carrying dicts (GRA) |
| Bavaresco et al. 2025, [2025.acl-short.20](https://aclanthology.org/2025.acl-short.20/) | JUDGE-BENCH: LLM-vs-human judge agreement | gate before trusting any LLM adjudication of corrections |
| EMNLP 2024, [2024.emnlp-main.2](https://aclanthology.org/2024.emnlp-main.2/) | CoT + majority-vote LLM dataset cleansing | cheap first-pass triage recipe for correction candidates |
| ACL 2025, [2025.acl-long.782](https://aclanthology.org/2025.acl-long.782/) | statistical test for replacing human annotators with LLMs | the formal gate for where LLM review may replace vs augment humans |
| Belyaev et al. 2021, [2021.iwclul-1.7](https://aclanthology.org/2021.iwclul-1.7/) | Abaev dictionary retro-digitization in TEI | comparable end-to-end case study for the methods section of any paper here |

**Paper angle worth registering:** the correction corpus + loci layer is a natural OBS-T
*companion paper* ("where errors live on the printed page"), not a competitor — C5/C6/C7 each
produce a finding OBS-T explicitly lacks. Route any scaffold through `/paper-scaffold` with a
stable Axx ID; venue facts per H265.

---

## 5. Thread 4 — new data layers worth deriving

| # | Layer | Derived from | Evidence grade (per [`EVIDENCE_LABELS.md`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/EVIDENCE_LABELS.md)) | Status |
|---|---|---|---|---|
| 5.1 | **`correction_loci.tsv`** — one row per record: dict, L, `<pc>` page, column, k1, k2, line, batch/date, process (bulk/human), directive, tag-context, old/new | all change files (+ ledger join for dates) | `derived` (fixed rule over `observed` headers) | **not built — backlog #1** |
| 5.2 | CFR live-stream layer — per-day arrivals, dict, submitter (pseudonymized), status latency | [`daily/`](https://github.com/sanskrit-lexicon/csl-corrections/tree/main/daily) + `correctionform.txt` | `derived` | not built |
| 5.3 | Corrector alias map + profiles | CFR col 8, ledger `user=`, git authors, OBS-T correctors | `derived`, promoted `reviewed` after human confirmation of merges | not built (C5 prerequisite) |
| 5.4 | Cross-dict shared-locus table — form-keyed corrections matched across dicts | 5.1 + sanskrit-util `slp1_form_key` | `inferred` (matches are candidates until reviewed) | not built (C3 prerequisite; extends forensic F4) |
| 5.5 | Per-edition confusion matrices | 5.1 old/new `<s>`-span alignment | `derived`; the printchange/digital split is `observed` | not built (C4 prerequisite) |

Registration duty when any of these is actually built: a manifest row in
[`kosha/data/manifest/datasets.json`](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)
same pass, and a feed line in
[`Uprava/PROJECT_INTERLINKS.md`](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md).
Note 5.3 carries personal data (emails) — restricted tier, `/publish-safety-check` before any
public artifact.

---

## 6. Deferred: the geographic layer

Settled by MG ruling 07-07-2026 (recorded in H271): the "atlas" stays metaphorical for now. The
one open item is a human task — **compile the per-dictionary imprint-city list (~1 day, no ready
source)** — mirrored to
[`Uprava/GTD_NEXT_ACTIONS.md`](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md)
as a `@DO`. Until then, the honest spatial dimension is intra-edition (`<pc>`, hypothesis C6).
Not re-litigated here.

---

## 7. Ranked backlog

Each item: statement · data · method/source · effort (S/M/L) · builder tier.

| Rank | Item | Data | Method / standard | Effort | Tier |
|---|---|---|---|---|---|
| 1 | **Build `correction_loci.tsv` (§5.1) + the 3 corrections-native viz (§3)** — one parser over both change-file dialects (standard + GRA `<chg>`), kosha manifest row | all change files | line-grammar parse; ERRANT-style edit spans ([P17-1074](https://aclanthology.org/P17-1074/)) | **M** | Sonnet |
| 2 | ✅ **DONE 08-07-2026 (H306, Fable 5 `claude-fable-5`)** — Atlas correction feed: loci heatmap + radar axes + Trust Blocks (sibling memo §3) → [csl-atlas PR #226](https://github.com/sanskrit-lexicon/csl-atlas/pull/226): [`/tools/correction-loci`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/src/tools/correction-loci.md) page + committed packet via [`build-correction-feed.mjs`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/scripts/build-correction-feed.mjs); component-mix + fix-latency radar axes still open (need OBS-T event feed, not 5.1) | 5.1 | Observable Plot; [CHART_TRUST_TEMPLATE](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/CHART_TRUST_TEMPLATE.md) | M | Sonnet |
| 3 | C2 two-process velocity study (+ §5.2 stream layer) | 5.1, 5.2, OBS-T | survival/trend analysis | M | Opus |
| 4 | C3 shared-locus copy detection (§5.4) feeding the lineage overlay | 5.1, forensic F4, citations | confusion-aware null model | M | Opus |
| 5 | C4 per-edition confusion matrices (§5.5); optional ByT5+SLP1 pilot | 5.1 | [2022.findings-emnlp.466](https://aclanthology.org/2022.findings-emnlp.466/) | M (L with pilot) | Opus |
| 6 | C5 corrector stylometry + alias map (§5.3); OBS-T era-shift decomposition | 5.2, 5.3, OBS-T | [J08-4004](https://aclanthology.org/J08-4004/); decomposition | M | Opus/Fable |
| 7 | C6 spatial hotspot analysis + C7 fix-regression tracking | 5.1 | autocorrelation; [2023.cl-1.4](https://aclanthology.org/2023.cl-1.4/) | M | Opus |
| 8 | OBS-T companion-paper scaffold (loci + C5/C6/C7 findings) | ranks 3–7 outputs | `/paper-scaffold`; venues per H265 | L | Fable |

Leverage logic: rank 1 is the fan-in — every hypothesis and every atlas viz consumes it; ranks
2–7 are independently parallelizable once it exists; rank 8 waits for at least two positive
results. Rank 1 is minted as its own handoff (see registry) so a Sonnet session can start it
from one line.

---

_Cross-links: atlas-facing sibling memo
[`csl-atlas/docs/DH_IMPROVEMENT_MEMO.md`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/DH_IMPROVEMENT_MEMO.md) ·
series anchor H265
[`ACL_DH_COMPATIBILITY_ANALYSIS.md`](https://github.com/gasyoun/SanskritLexicography/blob/master/ReverseDictionary/ACL_DH_COMPATIBILITY_ANALYSIS.md) ·
event-level corpus: OBS-T in
[`csl-observatory`](https://github.com/sanskrit-lexicon/csl-observatory)._

_Dr. Mārcis Gasūns_
