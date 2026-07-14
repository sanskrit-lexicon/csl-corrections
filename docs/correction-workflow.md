# CDSL Correction Workflow — End-to-End

**Audience:** Maintainers and contributors who apply, validate, and record corrections to dictionaries in the Cologne Digital Sanskrit Lexicon (CDSL).

**Status:** Authoritative. Supersedes ad-hoc readmes scattered across batch directories.

**How to read this:**
- First time? Read § 1 → § 2 → § 3 (the worked tutorial). Total ~15 min.
- Looking up a step? Jump to § 4 (reference) or § 5 (tooling).
- Hit a confusing failure? § 8 (pitfalls).

---

## Table of contents

1. [Why this document exists](#1-why-this-document-exists)
2. [The pipeline at a glance](#2-the-pipeline-at-a-glance)
3. [Tutorial — one correction, end-to-end](#3-tutorial--one-correction-end-to-end)
4. [Reference — the eight stages](#4-reference--the-eight-stages)
5. [Tooling reference](#5-tooling-reference)
6. [Repository topology](#6-repository-topology)
7. [Correction types — which workflow when](#7-correction-types--which-workflow-when)
8. [Pitfalls and gotchas](#8-pitfalls-and-gotchas)
9. [Where this document is linked from](#9-where-this-document-is-linked-from)

---

## 1. Why this document exists

The CDSL pipeline transforms each dictionary's source text in [`csl-orig`](https://github.com/sanskrit-lexicon/csl-orig) into a complete public installation: an XML file, an SQLite database, a PHP web display, and downloadable zip archives. Many scripts coordinate to make this happen, spread across four sibling repositories.

**The most common confusion for new contributors** is the assumption that `csl-orig` is frozen and that corrections live elsewhere — in change files that are applied during generation. That is not how the pipeline works. **Corrections are committed directly to `csl-orig`.** The change files in [`csl-corrections`](https://github.com/sanskrit-lexicon/csl-corrections) are *audit trails generated after the edit*, not inputs consumed by the pipeline.

This document settles that confusion and lays out the exact sequence of steps every correction must follow, with citations to the scripts and existing readmes that prove each step is real, not invented.

> **Authority:** Two committers — [drdhaval2785](https://github.com/drdhaval2785) (Dhaval Patel) and [funderburkjim](https://github.com/funderburkjim) (Jim Funderburk) — have shaped this workflow over many years. Concrete examples of their commits and readmes are linked throughout.

---

## 2. The pipeline at a glance

```
┌─────────────────┐                                                       ┌──────────────┐
│  Maintainer     │   1. edit                                             │  Public      │
│  (you)          │ ───────────────┐                                      │  consumers   │
└─────────────────┘                │                                      │              │
                                   ▼                                      │ • sanskrit-  │
                          ┌────────────────┐    2. regenerate             │   lexicon.   │
                          │   csl-orig     │ ──────────────┐              │   uni-koeln  │
                          │  (source txt)  │               │              │ • zip down-  │
                          └────────────────┘               ▼              │   loads      │
                                   │              ┌────────────────┐      │ • Stardict   │
                                   │              │   csl-pywork   │      │ • JSON       │
                                   │ 3. audit     │  (build tools) │      │ • SQLite     │
                                   ▼              └────────────────┘      └──────▲───────┘
                          ┌────────────────┐               │                     │
                          │ csl-corrections│               ▼                     │
                          │ (change files, │      ┌────────────────┐      4. serve│
                          │  readmes)      │      │csl-websanlexi- │ ────────────┘
                          └────────────────┘      │con (web/php)   │
                                                  └────────────────┘
```

| Step | What flows | From → To |
|---|---|---|
| 1 | A correction (text edit) | maintainer's local copy → `csl-orig/v02/<dict>/<dict>.txt` |
| 2 | The full generation pipeline | `csl-orig` → `<dict>/` installation directory (orig/, pywork/, web/, downloads/) |
| 3 | An audit-trail change file | `csl-corrections/batch_YYYYMMDD/dictionaries/<dict>/change_<dict>_N.txt` |
| 4 | Public artefacts | the Cologne server, GitHub Releases, Stardict, JSON, SQLite mirrors |

**Key invariant:** the canonical text is whatever currently sits at `csl-orig/v02/<dict>/<dict>.txt`. Everything else is derived.

---

## 3. Tutorial — one correction, end-to-end

This walkthrough uses a real example: trimming a stray trailing space inside a literary-source tag in the Apte 1890 dictionary. We'll do the whole workflow once, end-to-end, with explanations.

> **Prerequisites for the tutorial:**
> - All four sibling repos cloned into one parent directory (see § 6).
> - Python 3 with `mako` installed (`pip install mako`).
> - `xmllint`, `sqlite3`, `zip`, `bash` available on `PATH`.
> - Optional: XAMPP for serving the generated display locally — see the [csl-pywork readme](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md) for installation notes.

### The change

In `ap90.txt` at line 42758 we have:

```
<ls n="R.">6. </ls>; <ls n="R.">9. 22</ls>; ...
```

The literary-source tag for *Raghuvaṃśa* has a stray trailing space after `6.`. The correct form is `<ls n="R.">6.</ls>`. Single character delete, one line affected.

### Step 1 — Take a snapshot

```bash
cd $BASE/cologne/csl-corrections
mkdir -p batch_20260601/dictionaries/ap90
cd batch_20260601/dictionaries/ap90
cp $BASE/cologne/csl-orig/v02/ap90/ap90.txt temp_ap90_0.txt
```

> **Why:** The "before" file is the input to the diff tool that produces the audit trail in step 6. Without it you cannot reconstruct what changed.
> **Evidence:** every existing batch readme starts with this snapshot — see [`batch_20250418/dictionaries/mw/readme.txt`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20250418/dictionaries/mw/readme.txt).

### Step 2 — Make the edit

For a single-line edit, the simplest approach is a hand-built change file:

```bash
cat > change_ap90_lstrim.txt <<'EOF'
42758 old <ls n="R.">6. </ls>; <ls n="R.">9. 22</ls>; <ls n="R.">11. 31</ls>; <ls n="R.">13. 61</ls>; <ls>Y. 3. 244</ls>;
;
42758 new <ls n="R.">6.</ls>; <ls n="R.">9. 22</ls>; <ls n="R.">11. 31</ls>; <ls n="R.">13. 61</ls>; <ls>Y. 3. 244</ls>;
EOF

python updateByLine.py temp_ap90_0.txt change_ap90_lstrim.txt temp_ap90_1.txt
```

> **Why:** [`updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/updateByLine.py) applies *line-addressed* edits, which makes the change auditable. Hand-editing the source file directly works but leaves no record of what was modified.
> **Change file format:** paired lines `NNN old <text>` / `NNN new <text>`, with `;` lines as comments. Supports `new` (replace), `ins` (insert after), `del` (delete).

### Step 3 — Promote the corrected file into `csl-orig`

```bash
cp temp_ap90_1.txt $BASE/cologne/csl-orig/v02/ap90/ap90.txt
```

> **Why:** `csl-orig` is the source of truth that the generation pipeline reads from. Until this copy happens, nothing downstream sees the correction.
> **Evidence:** see this exact `cp` in [Jim's MW batch readme](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20250418/dictionaries/mw/readme.txt) (around `# remake xml from temp_mw_1.txt and check`), and in [Dhaval's recurring "DC NN May 2026" commits](https://github.com/sanskrit-lexicon/csl-orig/commits/master?author=drdhaval2785) which land directly on `csl-orig`'s `master`.

### Step 4 — Regenerate the dictionary installation

```bash
cd $BASE/cologne/csl-pywork/v02
sh generate_dict.sh ap90 ../../ap90
```

This runs four sub-stages — see § 4.4 for details. The interesting output to watch for:

```
BEGIN make_xml.py
All records parsed by ET
make_xml.py ENDS !!!!!
```

> **Why:** generating the XML is what catches structural problems in your edit. If you broke a tag, `make_xml.py`'s ElementTree parse will fail loudly.
> **Evidence:** [`generate_dict.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_dict.sh) is the documented entry point, called from every batch readme.

### Step 5 — Validate the XML against the DTD

```bash
cd $BASE/cologne/csl-pywork/v02
sh xmlchk_xampp.sh ap90
```

This runs `xmllint --noout --valid <dict>.xml <dict>.dtd` against the freshly generated XML.

> **Why:** the DTD validation catches anything the ET parse missed — typically attribute-level or referential issues. Jim runs this on every batch; skipping it has historically let bad markup land on the live site.
> **Evidence:** [`xmlchk_xampp.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/xmlchk_xampp.sh); referenced explicitly in [Jim's MW batch readme](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20250418/dictionaries/mw/readme.txt) (`sh xmlchk_xampp.sh mw`).
> **Local Windows caveat:** if `xmllint` is not installed, the ET-parse success from step 4 (`All records parsed by ET`) is a strong-but-incomplete substitute. Install `xmllint` for production work.

### Step 6 — Generate the audit-trail change file

```bash
cd $BASE/cologne/csl-corrections/batch_20260601/dictionaries/ap90
python diff_to_changes_dict.py temp_ap90_0.txt temp_ap90_1.txt change_ap90_1.txt
```

Output: `1 change written to change_ap90_1.txt`.

> **Why:** the audit trail is the durable record of what changed and why. Future investigators (you, a year from now) need to know which lines were touched and by which run.
> **Evidence:** [`diff_to_changes_dict.py`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20250418/dictionaries/mw/diff_to_changes_dict.py) is reused across every batch directory. It assumes equal line counts on both sides; use `diff_to_changes.py` when lines are added or removed.

### Step 7 — Commit and push

```bash
# csl-orig: just the corrected source file
cd $BASE/cologne/csl-orig
git add v02/ap90/ap90.txt
git commit -m "AP90 ls-tag whitespace fix. Close sanskrit-lexicon/AP90#NN"
git push

# csl-corrections: the audit trail + readme
cd $BASE/cologne/csl-corrections
git add batch_20260601/
git commit -m "AP90 ls-trim batch, see https://github.com/sanskrit-lexicon/AP90/issues/NN"
git push
```

> **Why two commits in two repos:** the source of truth (`csl-orig`) and the audit trail (`csl-corrections`) live in different repos for clean separation of concerns. The commit message in `csl-orig` references the issue; the audit-trail commit references the originating batch.
> **Evidence:** the cross-reference pattern is uniform across [Dhaval's recent commits](https://github.com/sanskrit-lexicon/csl-orig/commits/master?author=drdhaval2785) — each one references a `csl-corrections/issues/NNN` ticket.

### Step 8 — Refresh public artefacts (optional, batched in practice)

For routine corrections, the public refresh runs on a schedule from the live server via [`redo_xampp_selective.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/redo_xampp_selective.sh) (`@reboot sleep 120` cron entry). You do not normally need to push to the public site yourself.

For a hand-driven full rebuild on a server you control:

```bash
cd $BASE/cologne/csl-pywork/v02
sh redo_xampp_selective.sh    # picks up new csl-orig commits since the last run
```

This regenerates only the dictionaries whose `.txt` changed in `csl-orig` since the marker file `csl-orig/v02/.xampp_last_run`, then rebuilds Stardict and JSON sibling repos and pushes them.

---

## 4. Reference — the eight stages

A condensed checklist of the workflow, for repeat use.

### 4.1 Snapshot

```bash
cp $BASE/cologne/csl-orig/v02/<dict>/<dict>.txt temp_<dict>_0.txt
```

The "before" file. Keep it until step 6 completes.

### 4.2 Apply changes

```bash
python updateByLine.py temp_<dict>_0.txt change_<dict>_in.txt temp_<dict>_1.txt
```

The change-file directives — `old`/`new` for replace, `ins` for insert-after, `del` for delete. See [`updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/updateByLine.py) source for the exact grammar.

### 4.3 Promote into `csl-orig`

```bash
cp temp_<dict>_1.txt $BASE/cologne/csl-orig/v02/<dict>/<dict>.txt
```

### 4.4 Regenerate

```bash
cd $BASE/cologne/csl-pywork/v02
sh generate_dict.sh <dict> ../../<DictOutDir>
```

`generate_dict.sh` runs four sub-stages — see [`csl-pywork/v02/readme.md § What generate_dict.sh does`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md):

1. **`generate_orig.sh`** → copies `<dict>.txt`, `<dict>_hwextra.txt`, headers, metadata from `csl-orig/v02/<dict>/` into `<outdir>/orig/` and `<outdir>/pywork/`.
2. **`generate_pywork.sh`** → runs `generate.py` against `inventory.txt`, populates `<outdir>/pywork/` by copying shared files, rendering Mako templates with parameters from [`dictparms.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/dictparms.py), copying per-dict `distinctfiles/<dict>/pywork/`, deleting obsolete files.
3. **`generate_web.sh`** (runs from `csl-websanlexicon/v02`) → same C/T/CD/D model into `<outdir>/web/`.
4. **Execute** → inside `<outdir>/pywork/`: `redo_hw.sh` (headwords) → `redo_xml.sh` (XML + xmllint + SQLite) → `redo_postxml.sh` (abbreviation/tooltip/bib SQLite, web/sqlite copy). Then `<outdir>/downloads/redo_all.sh` (zip archives).

### 4.5 Validate XML

```bash
cd $BASE/cologne/csl-pywork/v02
sh xmlchk_xampp.sh <dict>
```

Calls `python3 ../../xmlvalidate.py <outdir>/pywork/<dict>.xml <outdir>/pywork/<dict>.dtd`. Non-zero exit = validation failed.

### 4.6 Audit trail

```bash
cd $BASE/cologne/csl-corrections/batch_YYYYMMDD/dictionaries/<dict>
python diff_to_changes_dict.py temp_<dict>_0.txt temp_<dict>_1.txt change_<dict>_N.txt
```

Equal line counts required. Use [`diff_to_changes.py`](https://github.com/sanskrit-lexicon/csl-corrections/blob/master/batch_20250418/diff_to_changes_dict.py) (without `_dict`) when lines are added or removed.

### 4.7 Commit + push, two repos

| Repo | What to commit | Commit-message convention |
|---|---|---|
| `csl-orig` | corrected `<dict>.txt` only | `<DICT> short description. Close sanskrit-lexicon/<REPO>#NN` or `... See <repo>/issues/NN` |
| `csl-corrections` | `batch_YYYYMMDD/dictionaries/<dict>/` (change file + `readme.txt`) | `<DICT> ... Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/NN` |

### 4.8 Refresh public artefacts

Hands-off (cron-driven `redo_xampp_selective.sh`) for routine corrections. Manual `redo_xampp_all.sh` or `redo_cologne_all.sh` for full rebuilds — only on the production server.

---

## 5. Tooling reference

| Script | Repo / Path | Purpose |
|---|---|---|
| [`updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/updateByLine.py) | `csl-pywork/v02/makotemplates/pywork/` | Apply line-addressed `old`/`new`/`ins`/`del` directives to a text file. |
| [`diff_to_changes_dict.py`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20250418/dictionaries/mw/diff_to_changes_dict.py) | `csl-corrections/batch_*/.../` | Produce an audit-trail change file from two same-line-count files; tracks `<L>` metaline per change. |
| `diff_to_changes.py` | `csl-corrections/batch_*/` | Same as above, no metaline tracking; allows differing line counts. |
| [`generate_dict.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_dict.sh) | `csl-pywork/v02/` | Build a complete `<dict>` installation: orig/, pywork/, web/, downloads/. |
| [`generate_orig.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_orig.sh) | `csl-pywork/v02/` | Sub-stage 1: copy `<dict>.txt` and ancillary files from `csl-orig` into `<outdir>/orig/`. |
| [`generate_pywork.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/generate_pywork.sh) | `csl-pywork/v02/` | Sub-stage 2: assemble `<outdir>/pywork/` from `makotemplates/` + `distinctfiles/<dict>/pywork/`. |
| [`generate_web.sh`](https://github.com/sanskrit-lexicon/csl-websanlexicon/blob/main/v02/generate_web.sh) | `csl-websanlexicon/v02/` | Sub-stage 3: assemble `<outdir>/web/` (PHP display) from the websanlexicon templates. |
| `generate_ab_bib_ls.sh` | `csl-pywork/v02/` | Build `redo.sh` and SQL scripts for abbreviation, tooltip, and bibliography SQLite tables. |
| `redo_hw.sh` → `hw.py` | `<outdir>/pywork/` | Build `<dict>hw.txt` (the headword list extracted from `<dict>.txt`). |
| `redo_xml.sh` → [`make_xml.py`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/makotemplates/pywork/make_xml.py) | `<outdir>/pywork/` | Convert the text source to XML, validate via xmllint, build `<dict>.sqlite`. |
| `redo_postxml.sh` | `<outdir>/pywork/` | Build abbreviation/tooltip/bib SQLite databases; copy `<dict>header.xml` to `web/`. |
| `downloads/redo_all.sh` | `<outdir>/downloads/` | Bundle `<dict>txt.zip`, `<dict>xml.zip`, `<dict>web*.zip` archives for public download. |
| [`xmlchk_xampp.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/xmlchk_xampp.sh) | `csl-pywork/v02/` | Stand-alone xmllint validation pass against the DTD. |
| [`redo_xampp_selective.sh`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/redo_xampp_selective.sh) | `csl-pywork/v02/` | Cron-driven incremental rebuild — picks up `csl-orig` commits since last run; refreshes Stardict, JSON, homepage too. |
| `redo_xampp_all.sh` | `csl-pywork/v02/` | Full rebuild of every dictionary on a local XAMPP server. |
| `redo_cologne_all.sh` | `csl-pywork/v02/` | Full rebuild on the live Cologne production server. |
| [`lsfix2.py`](https://github.com/sanskrit-lexicon/literarysource) (separate workflow) | `literarysource` repo / per-dict `pwgissues/`, `pwkissues/` | Install link targets from a built `index.js` into source `.txt` files — not part of this workflow. |

---

## 6. Repository topology

All four sibling repositories must be cloned into a single parent directory. The recommended layout (matches Jim's `$BASE/cologne/` and Ubuntu `/var/www/html/cologne/`):

```
$BASE/cologne/
  csl-orig/             ← canonical source: v02/<dict>/<dict>.txt files
  csl-pywork/           ← build tooling: generate_dict.sh and friends
  csl-websanlexicon/    ← PHP web display templates
  csl-corrections/      ← audit trails: batch_YYYYMMDD/dictionaries/<dict>/
  <dict>/               ← per-dict installation directory (orig/, pywork/, web/, downloads/)
  <Dict>Scan/2020/      ← scan images for the public viewer (optional)
  cologne-stardict/     ← Stardict format mirror (selective-update only)
  csl-json/             ← JSON format mirror (selective-update only)
  csl-homepage/         ← public landing page (selective-update only)
  hwnorm1/              ← headword normalisation database (selective-update only)
```

| Repository | Role | Who edits it |
|---|---|---|
| [`csl-orig`](https://github.com/sanskrit-lexicon/csl-orig) | The single source of truth. `v02/<dict>/<dict>.txt` is what the pipeline reads. | Maintainers, directly — every correction lands here. |
| [`csl-pywork`](https://github.com/sanskrit-lexicon/csl-pywork) | Pipeline scripts and templates. | Tooling maintainers only. |
| [`csl-websanlexicon`](https://github.com/sanskrit-lexicon/csl-websanlexicon) | PHP display layer templates. | Display-layer maintainers only. |
| [`csl-corrections`](https://github.com/sanskrit-lexicon/csl-corrections) | Audit trails of changes that landed in `csl-orig`. | Whoever made the `csl-orig` commit; usually paired commits. |
| Per-dictionary repos (`MWS`, `PWG`, `AP90`, `PWK`, etc.) | Issue tracker, scholarly discussion, dictionary-specific corrections that haven't yet been promoted to `csl-orig`. Used for **link-target** workflows (`pwkissues/`, `pwgissues/`). | Domain experts. |
| `<dict>/` (generated, not a git repo by default) | The fully built installation: `orig/`, `pywork/`, `web/`, `downloads/`. Recreated on demand from the four sibling repos. | Nobody — it's a build artefact. |

**Why so many siblings?** Each repo has a single concern. `csl-orig` is text-only and reviewable; `csl-pywork` is code-only and testable; `csl-websanlexicon` can change PHP without touching dictionary data; `csl-corrections` accumulates history without polluting source diffs. The downside is the strict sibling-directory requirement.

---

## 7. Correction types — which workflow when

| Correction type | Workflow | Where to file the issue |
|---|---|---|
| **Markup whitespace / element-content fix** (`<ls>`, `<lex>`, `<chg>`, `</div>`, etc.) | This document. `updateByLine.py` → `csl-orig` → `generate_dict.sh` → audit. | The dictionary's repo (PWG, MWS, …) with `markup` label. |
| **Text correction from print scan** (typo in headword, wrong page reference) | Same as above, plus add the correction line to `<dict>_printchange.txt` so the change is anchored to the printed book. | The dictionary's repo with `text-correction` label. |
| **Scholarly editorial correction batch** (Scott, Andhrabharati batches) | Jim's batch workflow: `correctionform.txt` → `tempwork_*_correctionform.txt` → split into `done.txt` / `todo.txt` → `printchange.txt` → `updateByLine.py` → `csl-orig` → audit. See [`batch_20250418/dictionaries/mw/readme.txt`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20250418/dictionaries/mw/readme.txt). | [`csl-corrections`](https://github.com/sanskrit-lexicon/csl-corrections/issues) (cross-cuts dictionaries). |
| **Link target / link splitting** (`<ls>SOURCE N</ls>` → click-through to PDF page) | Separate workflow: PDF → index file → `make_js_index.py` → `index.js` → `lsfix2.py` → installs into `pw`, `pwg`, `pwkvn`, `sch`, `mw`, etc. See [`PWG/CLAUDE.md`](https://github.com/sanskrit-lexicon/PWG/blob/main/CLAUDE.md) § "Link-target pipeline" and [`PWK/pwkissues/`](https://github.com/sanskrit-lexicon/PWK/tree/main/pwkissues). | The dictionary's repo with `link-target` or `link-splitting` label. |
| **Bibliography / `<ls>` ↔ source matching** | [`pw_ls/pwbib/`](https://github.com/sanskrit-lexicon/PWG/tree/main/pwg_ls/pwg_dhaval) pipeline: `crefmatch.py` → `pwbib1.py` → fuzzy match. | The dictionary's repo with `markup` or `text-correction` label. |
| **Headword normalisation** | `hwnorm1` / `hwnorm2` cross-dictionary alignment. Out of scope for this document. | [`hwnorm1`](https://github.com/sanskrit-lexicon/hwnorm1) or [`hwnorm2`](https://github.com/sanskrit-lexicon/hwnorm2). |
| **Display-layer bug** (PHP rendering, CSS, JS) | Edit `csl-websanlexicon` directly; regenerate affected dictionaries to pick up template changes. | [`csl-websanlexicon`](https://github.com/sanskrit-lexicon/csl-websanlexicon/issues). |
| **Pipeline bug** (build script breaks, generation regression) | Edit `csl-pywork`; test with `generate_dict.sh` on a representative dictionary. | [`csl-pywork`](https://github.com/sanskrit-lexicon/csl-pywork/issues). |

When in doubt, the [Cologne tooling runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md) describes which repository owns which class of issue.

---

## 8. Pitfalls and gotchas

Brief catalogue of failure modes. Each one is a thing that has bitten someone — read once, internalise, move on.

- **UTF-8 BOM.** Some text editors and some Python invocations add a 3-byte BOM (`EF BB BF`) at the start of a file. `csl-orig` files never have one. When writing files programmatically, use `open(f, 'w', encoding='utf-8')` — never `utf-8-sig`. After any bulk edit, verify with `python -c "open('<dict>.txt','rb').read(3).hex()"` and expect anything other than `efbbbf`.

- **`<LEND>` in dictionary intros.** AP90, MW, and BUR have `<LEND>` markers in their preface/introduction sections (lines 3–17). `hw.py` errors out on these with `init_entries Error 2. Not expecting <LEND>`. This is pre-existing and not your bug. On a production XAMPP install, `<dict>hw.txt` is pre-built and the error is silently absorbed. In a from-scratch local rebuild it will surface; ignore it for whitespace-only changes.

- **`diff_to_changes_dict.py` requires equal line counts.** It pairs lines positionally. If your edit added or removed any line, this script raises `ERROR: files have different number of lines`. Switch to `diff_to_changes.py` (no `_dict` suffix).

- **CRLF on Windows.** Git Bash and PowerShell can normalise line endings on write. The `csl-orig` repo's `.gitattributes` already handles `*.txt` as `text=auto`, so commits stay LF. The `warning: CRLF will be replaced by LF` message on `git add` is informational — let it through, don't `-c core.autocrlf=false` your way around it.

- **`python3` vs `python` on Windows.** The pipeline scripts call `python3` literally. Git Bash on Windows usually only exposes `python`. Workaround: create a wrapper shim once: `mkdir -p /tmp/pybin && printf '#!/bin/bash\npython "$@"\n' > /tmp/pybin/python3 && chmod +x /tmp/pybin/python3 && export PATH=/tmp/pybin:$PATH`. Add the export to your shell rc to make it persistent.

- **`xmllint` missing.** `xmlchk_xampp.sh` and `redo_xml.sh` both shell out to `xmllint`. If it is not installed locally, you'll see `xmllint: command not found`. ET-parse success from `make_xml.py` (`All records parsed by ET`) is necessary but not sufficient; install `libxml2-utils` (Linux) or GnuWin32 (Windows) for full DTD validation.

- **Line numbers shift between revisions.** If somebody else committed a correction to the same `<dict>.txt` between your snapshot and your apply, your change-file line numbers may no longer match. Always `git pull` and re-snapshot before applying.

- **`distinctfiles/` is for per-dict overrides, not for change files.** Files in `csl-pywork/v02/distinctfiles/<dict>/pywork/` are abbreviation tables, transcoders, and dictionary-specific Python overrides. Putting a change file there will not apply it to anything.

- **`printchange.txt` is for print errors only.** It documents intentional divergences from the scanned book — typically a clear scholarly correction to what the printed book got wrong. Don't use it for digital-format issues like markup whitespace. Those go straight into `<dict>.txt` with an audit trail in `csl-corrections`.

- **Two-repo commit pairing.** A `csl-orig` commit without a matching `csl-corrections` batch loses the audit trail; a `csl-corrections` commit without the matching `csl-orig` edit is misleading. Always commit both, ideally within minutes of each other, with cross-referenced commit messages.

- **`generate_dict.sh` regenerates from scratch.** It does not preserve manual edits inside `<outdir>/pywork/` or `<outdir>/web/`. If you ever find yourself hand-editing a generated file, you are working against the pipeline — move the edit upstream into `csl-pywork` or `csl-websanlexicon`.

---

## 9. Where this document is linked from

- [`csl-corrections/CLAUDE.md`](../CLAUDE.md) — primary index entry.
- [`csl-corrections/README.md`](../README.md) — overview link.
- [`csl-pywork/v02/readme.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/v02/readme.md) — referenced from the "What `generate_dict.sh` does" section.
- [`csl-pywork/CLAUDE.md`](https://github.com/sanskrit-lexicon/csl-pywork/blob/main/CLAUDE.md) — referenced as the cross-repo correction workflow.
- [`csl-observatory/runbook/cologne-tooling-runbook.md`](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md) — referenced as the correction-workflow authority.
- [`COLOGNE/CONTRIBUTING.md`](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/CONTRIBUTING.md) — referenced in the source-file-edits clause.

If you move this file, update all the back-references.

---

## Document history

| Date | Change | Author |
|---|---|---|
| 2026-05-29 | Initial version. Documents the workflow as practised by Jim Funderburk (`batch_20250114/`, `batch_20250418/`) and Dhaval Patel (recurring `DC NN <month>` commits + `batches/20251126/`). Synthesises lessons from the 2026-05 markup-fix sweep (BOR, AP90, GRA, MW, AP, BUR, INM, KRM, BOP, MW72) including the BOM-encoding postmortem. | — |
