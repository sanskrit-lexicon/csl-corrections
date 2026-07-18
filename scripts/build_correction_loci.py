#!/usr/bin/env python3
"""Build data/derived/correction_loci.tsv — one row per correction record
across all change files in this repo (both dialects: standard paired
old/new records and the GRA inline <chg type=...><old>...</old></chg>
wrapper, which parses identically because the wrapper lives inside the
line content).

Spec: docs/HYPOTHESES_AND_VIZ_MEMO.md §5.1 (H271 backlog #1, built per H294).

Columns:
    dict, L, pc_page, pc_col, k1, k2, line, batch, batch_date, process,
    directive, tag_context, old, new

Scope: every change_*.txt under batch_*/ and batches/*/ (35 files as of
2026-07-07). The daily/ CFR stream is layer 5.2 and deliberately NOT
processed here. csl-orig is never touched.

Census notes (measured 2026-07-07, frozen in --selftest):
  - 39,606 meta-headers `; <L>...<pc>...`, 100% carrying <pc>.
  - 39,540 records = 39,536 old->new pairs + 4 old->del pairs (all four
    del in batch_20260626/dictionaries/stc/). The memo §1 figure 39,544
    counted the 4 del lines in addition to their own old lines; the
    honest record count is 39,540.
  - Header/record delta of 66 = 75 commented-out records in
    batch_20240623/change_1.txt (headers present, directives `;`-disabled)
    minus 1 headerless `; None` record in batch_20250418 ap minus 8
    headerless records in batch_20260626 stc.
  - batch_20240623/change_1.txt sits at the batch root without a
    dictionaries/ folder; its readme_install.txt shows it is MW.

Usage:
    python scripts/build_correction_loci.py            # build the TSV
    python scripts/build_correction_loci.py --selftest # build + assert census
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'data' / 'derived' / 'correction_loci.tsv'

COLUMNS = ['dict', 'L', 'pc_page', 'pc_col', 'k1', 'k2', 'line', 'batch',
           'batch_date', 'process', 'directive', 'tag_context', 'old', 'new']

# The two machine-generated bulk markup batches (memo §0.3); everything
# else is steady human correction.
BULK_FILES = {
    'batch_20260529/dictionaries/bor/change_bor_markup_1.txt',
    'batch_20250418/dictionaries/lrv/markhom/change_lrv_1.txt',
}

# Change files not under a dictionaries/<dict>/ folder.
DICT_OVERRIDES = {
    'batch_20240623/change_1.txt': 'mw',  # per its readme_install.txt
}

HEADER_RE = re.compile(
    r'^; <L>(?P<L>[^<]*)<pc>(?P<pc>[^<]*)<k1>(?P<k1>[^<]*)'
    r'(?:<k2>(?P<k2>[^<]*))?')
DIRECTIVE_RE = re.compile(r'^(?P<ln>\d+) (?P<dir>old|new|del|ins)(?: ?(?P<text>.*))?$')
SEPARATOR_RE = re.compile(r'^;-{10,}')
TAG_RE = re.compile(r'<(/?)([A-Za-z][A-Za-z0-9]*)([^>]*)>')


def find_change_files():
    files = []
    for top in sorted(REPO.glob('batch_*')):
        if top.is_dir():
            files.extend(sorted(top.rglob('change_*.txt')))
    batches = REPO / 'batches'
    if batches.is_dir():
        for sub in sorted(batches.iterdir()):
            if sub.is_dir():
                files.extend(sorted(sub.rglob('change_*.txt')))
    return files


def batch_of(rel):
    """('batch_20240623' | 'batches/20251126', 'YYYY-MM-DD') from a rel path."""
    parts = rel.split('/')
    if parts[0] == 'batches':
        bid, stamp = 'batches/' + parts[1], parts[1]
    else:
        bid, stamp = parts[0], parts[0].split('_')[1]
    return bid, f'{stamp[:4]}-{stamp[4:6]}-{stamp[6:8]}'


def dict_of(rel):
    if rel in DICT_OVERRIDES:
        return DICT_OVERRIDES[rel]
    parts = rel.split('/')
    if 'dictionaries' in parts:
        return parts[parts.index('dictionaries') + 1]
    raise ValueError(f'cannot resolve dict for {rel}')


def split_pc(pc):
    """'001-12' -> ('001','12'); '2,3' -> ('2','3'); '0003' -> ('0003','')."""
    m = re.match(r'^([^,-]*)[,-](.*)$', pc)
    return (m.group(1), m.group(2)) if m else (pc, '')


def tag_context(old, new):
    """Innermost open tag at the first old/new divergence point ('text' if none)."""
    if not old:
        return 'text'
    p, m = 0, min(len(old), len(new))
    while p < m and old[p] == new[p]:
        p += 1
    stack = []
    for t in TAG_RE.finditer(old[:p]):
        closing, name, attrs = t.group(1), t.group(2), t.group(3)
        if attrs.rstrip().endswith('/'):
            continue
        if closing:
            if name in stack:
                while stack and stack[-1] != name:
                    stack.pop()
                if stack:
                    stack.pop()
        else:
            stack.append(name)
    return stack[-1] if stack else 'text'


def esc(s):
    return s.replace('\\', '\\\\').replace('\t', '\\t')


def parse_file(path):
    """Yield rows; also return header stats via the returned tuple."""
    rel = path.relative_to(REPO).as_posix()
    dct = dict_of(rel)
    batch, batch_date = batch_of(rel)
    process = 'bulk' if rel in BULK_FILES else 'human'
    rows, headers_seen, headers_with_pc = [], 0, 0
    header = None   # (L, pc_page, pc_col, k1, k2)
    pending = None  # (line_number, old_text)
    with open(path, encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip('\r\n')
            if line.startswith('﻿'):
                line = line.lstrip('﻿')
            if line.startswith('; <L>'):
                m = HEADER_RE.match(line)
                if m:
                    headers_seen += 1
                    pc = m.group('pc')
                    if pc:
                        headers_with_pc += 1
                    page, col = split_pc(pc)
                    header = (m.group('L'), page, col,
                              m.group('k1'), m.group('k2') or '')
                    pending = None
                continue
            if line == '; None':
                header = ('', '', '', '', '')
                pending = None
                continue
            if SEPARATOR_RE.match(line):
                header = None
                pending = None
                continue
            if line.startswith(';') or not line.strip():
                continue
            m = DIRECTIVE_RE.match(line)
            if not m:
                continue
            ln, d, text = m.group('ln'), m.group('dir'), m.group('text') or ''
            if d == 'old':
                pending = (ln, text)
            elif d in ('new', 'del', 'ins'):
                old_text = ''
                if pending and pending[0] == ln:
                    old_text = pending[1]
                L, page, col, k1, k2 = header or ('', '', '', '', '')
                new_text = text if d != 'del' else ''
                ctx = 'line' if d == 'del' else tag_context(old_text, new_text)
                rows.append([dct, L, page, col, k1, k2, ln, batch, batch_date,
                             process, d, ctx, esc(old_text), esc(new_text)])
                pending = None
    return rows, headers_seen, headers_with_pc


EXPECTED = {  # census snapshot 2026-07-18 (G14 bump) — update when new batches land
    'files': 37,
    'rows': 39555,
    'headers': 39606,
    'new': 39551,
    'del': 4,
    'ins': 0,
    'bor_bulk': 21990,
    'lrv_markhom_bulk': 8063,
    'rows_without_pc': 24,  # 15 headerless ap90 + 8 stc + 1 `; None` ap record
}


def main():
    selftest = '--selftest' in sys.argv
    files = find_change_files()
    all_rows, headers, headers_pc = [], 0, 0
    per_file = {}
    for path in files:
        rows, h, hpc = parse_file(path)
        rel = path.relative_to(REPO).as_posix()
        per_file[rel] = len(rows)
        all_rows.extend(rows)
        headers += h
        headers_pc += hpc

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(COLUMNS) + '\n')
        for r in all_rows:
            f.write('\t'.join(r) + '\n')

    n_new = sum(1 for r in all_rows if r[10] == 'new')
    n_del = sum(1 for r in all_rows if r[10] == 'del')
    n_ins = sum(1 for r in all_rows if r[10] == 'ins')
    no_pc = sum(1 for r in all_rows if not r[2])
    print(f'files parsed        : {len(files)}')
    print(f'rows written        : {len(all_rows)} -> {OUT.relative_to(REPO)}')
    print(f'meta-headers        : {headers} ({headers_pc} with <pc>)')
    print(f'directives          : new={n_new} del={n_del} ins={n_ins}')
    print(f'rows without <pc>   : {no_pc}')
    counts = {}
    for r in all_rows:
        key = (r[0], r[9])
        counts[key] = counts.get(key, 0) + 1
    for (d, p), n in sorted(counts.items()):
        print(f'  {d:<6} {p:<5} {n}')

    if selftest:
        got = {
            'files': len(files),
            'rows': len(all_rows),
            'headers': headers,
            'new': n_new,
            'del': n_del,
            'ins': n_ins,
            'bor_bulk': per_file.get(
                'batch_20260529/dictionaries/bor/change_bor_markup_1.txt', 0),
            'lrv_markhom_bulk': per_file.get(
                'batch_20250418/dictionaries/lrv/markhom/change_lrv_1.txt', 0),
            'rows_without_pc': no_pc,
        }
        failed = [k for k in EXPECTED if got[k] != EXPECTED[k]]
        assert headers_pc == headers, \
            f'<pc> coverage not 100%: {headers_pc}/{headers}'
        assert not failed, \
            'census mismatch: ' + ', '.join(
                f'{k} expected {EXPECTED[k]} got {got[k]}' for k in failed)
        print('SELFTEST OK — census invariants hold '
              '(100% <pc> header coverage included)')


if __name__ == '__main__':
    main()
