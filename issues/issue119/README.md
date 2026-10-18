# csl-corrections#119 — trial: pwk7 "Nachträge" headwords absent from MW

_Created: 14-09-2026 · Last updated: 14-09-2026_

Trial run for the question in [issue #119, comment 4359094604](https://github.com/sanskrit-lexicon/csl-corrections/issues/119#issuecomment-4359094604)
(Andhrabharati, 01-05-2026):

> I presume that MW (and his team of associates) **skipped adding (by error?!)** this
> "kāritra" as an entry; … [And I recall even suggesting (once) to add such entries by
> comparing MW with PWG/pwk.]

**Answer: yes, the comparison can be automated.** It is a deterministic SLP1 headword-set
join, it runs in ~4 s over the local `csl-orig/v02` digitizations, and it isolates exactly
the class the comment describes — with `kāritra` reproduced as the first test case.

## 1. The `kāritra` case, verified end-to-end

| witness | evidence |
|---|---|
| **`pwkvn`** (the Nachträge of the Böhtlingk *kürzere Fassung*) | `<L>16013<pc>7-331-d<k1>kAritra<k2>*kAritra` — `n. = ceṣṭita, MAHĀVY. 245, 844, Vgl. cāritra` |
| **MW** | **zero occurrences** — not a `<k1>`, not a `<k2>`, not a `<s>…</s>` body span |
| `bhs` (Edgerton, Buddhist Hybrid Sanskrit) | L=4759 — the "BHS indicates such interpretation" of the comment |
| `sch` (Schmidt, Nachträge) | L=10440 |
| `pw` (kürzere Fassung) | L=216013, `*`-marked |

The decisive detail: on the **same page** (`7-331-d`) the preceding entry is
`kārāpaka` (L=16011, `*`-marked), which MW **did** absorb as a supplemental entry
(`ID=48659.2`, `<info n="sup"/>`) — the very entry whose `(cf. next)` lost its target.
MW also has `cāritra` (8 entries) and `kārayitṛ` (2). It has everything around
`kāritra` and not `kāritra`. The commenter's premise holds.

`<info n="sup"/>` is MW's own marker for the annexure: *"The entry is from the supplement;
… a new supplementary word. Although the printed edition has these entries in a separate
section after the body of the dictionary, the Cologne digitization has merged these
entries into the body"* (`mw-meta2.txt`, 18-06-2018). That is precisely the merge that
breaks the sequential reference.

## 2. Data and method

- **`pwkvn`** = *"Digitization of the 'Nachträge und Verbesserungen' sections of the
  Böhtlingk Sanskrit-Wörterbuch in kürzerer Fassung"* (`pwkvn-meta2.txt`, 15-04-2022) —
  the "letzte Nachträge of pwk7" of the comment.
- Join key: SLP1 `<k1>` (plus comma-delimited `<k2>` alternates), all from
  `csl-orig/v02` (read-only, fenced).
- Machinery reused, not rebuilt: the H1310/H1326 cross-dictionary census
  ([`SanskritGrammar/data/pwg_lexicon_only_audit/build_census.py`](https://github.com/gasyoun/SanskritGrammar/blob/master/data/pwg_lexicon_only_audit/build_census.py)),
  run in the **complement** direction — that audit hunted PWG words attested *elsewhere*
  (ghost-words); this trial hunts pwk words MW *never absorbed* (coverage gaps).
- Reproduce: `python build_trial.py` (`CSL_ORIG_V02` overrides the data path).

## 3. Results

| quantity | count |
|---|---:|
| `pwkvn` entries parsed | 14,399 |
| …of which explicit Nachträge (`<k2>*…`) | 933 |
| MW `<k1>` headwords | 194,083 |
| MW supplemental entries (`<info n="sup"/>`) | 6,067 |
| `pwkvn` entries found in MW's **supplemental** layer | 1,956 |
| `pwkvn` entries found in MW anywhere | 9,617 |
| **`pwkvn` entries absent from MW** | **4,782** |
| **absent *and* an explicit Nachtrag** | **410** |

The 1,956 pwkvn words sitting in MW's supplemental layer are the quantitative support for
the postulate that the annexure drew on pwk7 — strong, though not proof of the exact edition used.

**The 410-row sharp shortlist** (`pwk7_nachtraege_absent_from_mw.tsv`) splits into:

| class | count | meaning |
|---|---:|---|
| **Mahāvyutpatti-sourced new entries** | **272** | the `kāritra` class — new Buddhist vocabulary entered in pwk7 from Mahāvyutpatti, never taken into MW |
| other new words | 131 | sourced from Kāśikā, Pāṇini, GAṆAP. etc. |
| *Verbesserungen* (corrections) | 7 | `lies …`, `zu streichen`, `fehlerhaft für …` — re-spellings/strikes, **not** coverage gaps |

Of the 272 Mahāvyutpatti entries: **142 are independently confirmed by Edgerton's BHS
dictionary**, 256 by Schmidt's Nachträge, **139 by ≥2 independent digitized dictionaries**,
and only 2 appear anywhere in MW's body text.

Top of the shortlist by independent corroboration:

| word | independent witnesses | pwkvn gloss |
|---|---|---|
| `amUlaka` | bhs, sch, ap90, ap | `n.` eine unbegründete Anklage, MAHĀVY. 258 |
| `gArDa` | bhs, sch, pwg | MAHĀVY. 110,36 fehlerhaft für `gArdDya` |
| `AdarSamuKa` | bhs, sch | `m.` N.pr. eines Schlangendämons, MAHĀVY. |
| `AjYeya` | bhs, sch | `Adj.` zu erkennen, MAHĀVY. 20 |
| `Akampya` | bhs, sch | `m.` ein best. Samādhi, MAHĀVY. |
| `alipta` | bhs, sch | `Adj.` unbefleckt, MAHĀVY. 19 |
| **`kAritra`** | **bhs, sch** | `n.` = ceṣṭita, MAHĀVY. 245, 844, Vgl. cāritra |

## 4. Honest limitations

1. **Spelling-level join, homonyms collapsed** — the same caveat the H1310 audit records.
2. **"Absent from MW"** = no `<k1>`/`<k2>` headword and no `<s>…</s>` body span. A compound
   or a variant spelling could still hide a word from the join.
3. **Deliberate exclusion is a live alternative to "error".** MW is a general dictionary;
   Mahāvyutpatti is Buddhist technical vocabulary. Edgerton's BHS is the arbiter of whether
   a word is real (142/272 so confirmed) — not of whether MW *ought* to have carried it.
   Each row needs editorial adjudication; the join supplies the candidate pool, not the verdict.
4. **The annexure-source inference** (1,956 matching supplemental entries) is consistent
   with, but does not prove, MW's use of this exact edition.
5. `pwkvn` mixes Nachträge (new words) and Verbesserungen (corrections); only the former are
   coverage gaps — hence the 410-row filter on the `*` marker.

## 5. Next steps

1. Adjudicate the 272 (or the 139-word ≥2-corroborated core) word by word.
2. Decide whether `csl-corrections` stages **MW additions** at all — adding entries is not
   `updateByLine.py`'s job, so this would need a supplement-file convention, not a change file.
3. Extend the same join to the big `pwg` and `gra` complements — 11,303 / 1,356 candidates
   respectively (larger, lower precision: MW's Vedic selectivity, not oversight).
4. Post the trial outcome on the issue.

## Files

| file | content |
|---|---|
| `build_trial.py` | the whole trial, reproducible, ~4 s |
| `pwk7_nachtraege_absent_from_mw.tsv` | 410 explicit Nachträge absent from MW, with gloss + corroboration |
| `pwkvn_absent_from_mw_all.tsv` | broad pool: all 4,782 pwkvn entries absent from MW |

_Гасунс_
