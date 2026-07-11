# csl-corrections

_Created: 16-12-2019 · Last updated: 11-07-2026_

CDSL **data-store** repository in the [Sanskrit Lexicon](https://github.com/sanskrit-lexicon) project. It is the staging ground and audit trail for text corrections to the Cologne dictionaries: individual change-files are validated locally and **parked in dated batch folders here**, then shipped upstream into [`csl-orig`](https://github.com/sanskrit-lexicon/csl-orig) as **one consolidated pull request roughly monthly** — never as direct pushes or per-issue noise. The change-files are the durable record of what was corrected and why; they survive re-derivation of the dictionaries from `csl-orig`.

## Repository role

- **Intake** — corrections arrive from the correction form, a daily cron fetch, and issue triage, and are logged in the `cfr_ab` registry (see the batch runbook below).
- **Staging** — each validated correction is filed into a dated batch folder under [`batches/`](https://github.com/sanskrit-lexicon/csl-corrections/tree/main/batches) (e.g. [`batches/20251126/`](https://github.com/sanskrit-lexicon/csl-corrections/tree/main/batches/20251126)), as a paired `old`/`new` change-file per dictionary. `csl-orig` itself is never touched here.
- **Delivery** — accumulated batches are re-validated against current upstream and merged into `csl-orig` as a single monthly consolidated PR.
- **Derived data** — every parked change-file is also parsed into a machine-readable correction census for analysis (see [Derived data](#derived-data--correction-loci)).

## Documentation

📘 **[Correction Workflow — End-to-End](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)** — the authoritative guide for applying corrections to `csl-orig` dictionary text. Covers the full pipeline (snapshot → apply → validate → audit → commit), tooling reference, repository topology, and pitfalls. This is the canonical reference that the wider org's `CLAUDE.md` and sibling-repo READMEs point at.

📗 **[Batch Processing Runbook](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_RUNBOOK.md)** — the operator manual for everything *around* that workflow: intake (form → daily cron → `cfr_ab` registry), the mandatory preflight, batch-folder assembly and lifecycle, derived-data rebuilds, and issue-taxonomy upkeep — with a symptom→cause→cure table and glossary.

## Example change file

A real paired old→new record from
[`batches/20251126/dictionaries/mw/change_mw_1.txt`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batches/20251126/dictionaries/mw/change_mw_1.txt)
— MW line 8104, root `aYj` (SLP1), fixing a sandhi typo in the perfect stem
(`A-naYja` → `AnaYja`):

```
; <L>2267<pc>11,1<k1>aYj<k2>aYj<e>1
8104 old <s>aYj</s> ¦ <ab>cl.</ab> 7. <ab>P.</ab> <ab>Ā.</ab> <s>ana/kti</s>, <s>aNkte/</s>, <s>A-naYja</s>, <s>aYjizyati</s> or <s>aNkzyati</s>, <s>AYjIt</s>, <s>aYjitum</s> or <s>aNktum</s>, to apply an ointment or pigment, smear with, anoint;
;
8104 new <s>aYj</s> ¦ <ab>cl.</ab> 7. <ab>P.</ab> <ab>Ā.</ab> <s>ana/kti</s>, <s>aNkte/</s>, <s>AnaYja</s>, <s>aYjizyati</s> or <s>aNkzyati</s>, <s>AYjIt</s>, <s>aYjitum</s> or <s>aNktum</s>, to apply an ointment or pigment, smear with, anoint;
;---------------------------------------------------
```

Applied per the org-wide pattern documented in [`docs/correction-workflow.md`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md):

```sh
python updateByLine.py mw.txt change_mw_1.txt mw_corrected.txt
```

The `;`-prefixed lines are comments/separators; the `<L>` header line records
the source record's original locus (`<pc>` page/column, `<k1>`/`<k2>` head
keys) so the change survives re-derivation from `csl-orig`.

## Derived data — correction loci

[`data/derived/correction_loci.tsv`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/data/derived/correction_loci.tsv)
holds **one row per correction record** (39,540 as of 07-07-2026) parsed from every
change file in the batch folders — both dialects (standard paired `old`/`new` records
and the GRA inline `<chg>` wrapper). Columns: `dict, L, pc_page, pc_col, k1, k2, line,
batch, batch_date, process, directive, tag_context, old, new`, with
`process ∈ {bulk, human}` separating the two machine-generated markup batches
(BOR 21,990 + LRV/markhom 8,063 = 76% of records) from steady human correction.
Corrector identity is deliberately excluded. Spec and hypotheses:
[`docs/HYPOTHESES_AND_VIZ_MEMO.md`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/HYPOTHESES_AND_VIZ_MEMO.md) §5.1.

Rebuild (validates the census invariants) and regenerate the figures:

```sh
python scripts/build_correction_loci.py --selftest
python scripts/build_correction_viz.py
```

![Correction velocity by batch month](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/img/correction_velocity_timeline.svg)

![Correction density per dictionary](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/img/correction_density_per_dict.svg)

![Batch composition treemap](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/img/correction_batch_treemap.svg)

Entry counts for the density chart come from
[`data/derived/dict_entry_counts.tsv`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/data/derived/dict_entry_counts.tsv)
(`grep -c '^<L>'` over csl-orig v02, cached here so the viz never needs csl-orig).

## GitHub Issue Conventions

This repository follows the [Cologne tooling-repo taxonomy](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md). Every issue carries exactly one **type** label, one **severity** level, and one **milestone**:

- **9 type labels**: `bug`, `feature`, `enhancement`, `performance`, `tech-debt`, `security`, `documentation`, `infrastructure`, `question`
- **4 severity levels**: `trivial`, `minor`, `major`, `critical`
- **5 milestones**: API Stability, User Experience, Data Quality, Developer Experience, Community
- **Org Project**: [Tooling Roadmap](https://github.com/orgs/sanskrit-lexicon/projects/9)

Full label/severity/milestone definitions are in [CLAUDE.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/CLAUDE.md). For live counts and the current backlog, see the [issue tracker](https://github.com/sanskrit-lexicon/csl-corrections/issues).

---

_Dr. Mārcis Gasūns_
