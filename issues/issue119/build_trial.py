# -*- coding: utf-8 -*-
"""csl-corrections#119 — trial: pwk7 'Nachträge und Verbesserungen' headwords absent from MW.

Question (Andhrabharati, issue comment 4359094604, 01-05-2026): MW's 1899 annexure
(the `<info n="sup"/>` supplemental entries) appears to draw on the *letzte Nachträge*
of the Böhtlingk PW kürzere Fassung, yet some entries there — e.g. `kāritra`, sitting
right next to `kārāpaka` (which MW DID take) — never became MW entries. Can the
comparison "MW vs PWG/pwk" be automated to find such skipped entries?

Method: deterministic SLP1 `<k1>`/`<k2>` headword-set join over `csl-orig/v02`,
reusing the H1310/H1326 cross-dictionary census machinery
(SanskritGrammar/data/pwg_lexicon_only_audit/build_census.py) — but in the
*complement* direction: not "PWG words attested elsewhere" (ghost-word hunting),
but "pwk words MW never absorbed" (coverage-gap hunting).

Inputs (read-only):
  csl-orig/v02/pwkvn  = digitization of the 'Nachträge und Verbesserungen' sections
                        of Böhtlingk's Sanskrit-Wörterbuch in kürzerer Fassung
                        (the "pwk7 Nachträge" of the issue comment)
  csl-orig/v02/mw     = Monier-Williams
  csl-orig/v02/{pw,pwg,gra,bhs,sch,ap90,ap,vcp,skd} = comparison corpus

Outputs (next to this script):
  pwk7_nachtraege_absent_from_mw.tsv  — sharp shortlist (explicit '*' Nachträge only)
  pwkvn_absent_from_mw_all.tsv        — broad pool (every pwkvn headword absent from MW)

Usage:
  CSL_ORIG_V02=/path/to/csl-orig/v02 python build_trial.py
"""
import os
import re
import sys
import csv
import json

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
CSL = os.environ.get('CSL_ORIG_V02') or 'C:/Users/user/Documents/GitHub/csl-orig/v02'
if not os.path.isdir(CSL):
    sys.exit(f'ERROR: csl-orig/v02 not found at {CSL} (set CSL_ORIG_V02)')

# dictionaries that corroborate independently of the Böhtlingk tradition
INDEP = ['bhs', 'gra', 'sch', 'ap90', 'ap', 'vcp', 'skd', 'pwg']


def load_dict(code):
    """Return (k1 set, k2 set) of SLP1 headwords for a csl-orig dictionary."""
    k1, k2 = set(), set()
    for fn in (f'{code}.txt', f'{code}_hwextra.txt'):
        p = os.path.join(CSL, code, fn)
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as f:
            for line in f:
                for m in re.findall(r'<k1>([^<]+)', line):
                    w = m.strip()
                    if w:
                        k1.add(w)
                for m in re.findall(r'<k2>([^<]+)', line):
                    for w in m.split(','):
                        w = w.strip()
                        if w:
                            k2.add(w)
    return k1, k2


def parse_pwkvn_entries():
    """Yield (k1, k2, pc, gloss) per entry of the pwkvn digitization."""
    path = os.path.join(CSL, 'pwkvn', 'pwkvn.txt')
    k1 = k2 = pc = None
    body = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('<L>'):
                m = re.match(r'<L>\d+<pc>([^<]*)<k1>([^<]*)<k2>([^<]*)', line)
                if m:
                    pc, k1, k2 = m.group(1), m.group(2), m.group(3)
                    body = []
            elif line.startswith('<LEND>'):
                if k1 is not None:
                    yield k1, k2, pc, ' '.join(body)
                k1 = None
            elif k1 is not None:
                body.append(line.strip())


def main():
    # --- MW side ---------------------------------------------------------
    mw_k1, mw_k2 = load_dict('mw')
    mw_all = mw_k1 | mw_k2
    mwtxt = open(os.path.join(CSL, 'mw', 'mw.txt'), encoding='utf-8').read()
    # the 1899 annexure layer = entries carrying <info n="sup"/>
    mw_sup = set()
    for chunk in re.split(r'(?=<L>)', mwtxt):
        m = re.search(r'<k1>([^<]+)', chunk)
        if m and '<info n="sup"/>' in chunk:
            mw_sup.add(m.group(1))
    # body mentions: MW's older digitization marks display spans <s>X</s>
    mw_tok = set(re.findall(r'<s>([^<]+)</s>', mwtxt)) | set(re.findall(r'\{#([^#{}]+)#\}', mwtxt))
    print(f'MW: {len(mw_k1):,} k1 headwords ({len(mw_all):,} with alternates), '
          f'{len(mw_sup):,} supplemental (<info n="sup"/>)', file=sys.stderr)

    # --- comparison sets -------------------------------------------------
    dsets = {}
    for code in INDEP:
        a, b = load_dict(code)
        dsets[code] = a | b
        print(f'  {code}: {len(dsets[code]):,} headwords', file=sys.stderr)

    # --- pwkvn side ------------------------------------------------------
    star, broad = [], []
    seen = set()
    n_star = 0
    for k1, k2, pc, gloss in parse_pwkvn_entries():
        if k1 in seen:
            continue
        seen.add(k1)
        is_star = k2.startswith('*')
        if is_star:
            n_star += 1
        absent = k1 not in mw_all
        hits = [d for d in INDEP if k1 in dsets[d]]
        rec = (k1, pc, gloss[:220].replace('\t', ' '), ','.join(hits),
               'Y' if k1 in mw_tok else '')
        if absent:
            broad.append(rec)
        if absent and is_star:
            star.append(rec)

    pwkvn_words = seen
    inter_sup = len({w for w in pwkvn_words if w in mw_sup})
    print(f'pwkvn: {len(pwkvn_words):,} entries ({n_star:,} explicit Nachträge, k2 "*")',
          file=sys.stderr)
    print(f'  in MW supplemental layer: {inter_sup:,}', file=sys.stderr)
    print(f'  in MW anywhere:           {len([w for w in pwkvn_words if w in mw_all]):,}',
          file=sys.stderr)
    print(f'  absent from MW:           {len(broad):,}', file=sys.stderr)
    print(f'  absent AND explicit Nachtrag: {len(star):,}', file=sys.stderr)

    # --- write -----------------------------------------------------------
    hdr = 'k1\tpc\tpwkvn_gloss\tindep_hits\tmw_body_mention\n'
    key = lambda r: (-len([x for x in r[3].split(',') if x]), r[0])
    for fn, rows in (('pwk7_nachtraege_absent_from_mw.tsv', star),
                     ('pwkvn_absent_from_mw_all.tsv', broad)):
        with open(os.path.join(HERE, fn), 'w', encoding='utf-8', newline='') as f:
            f.write(hdr)
            for r in sorted(rows, key=key):
                f.write('\t'.join(r) + '\n')
        print(f'wrote {fn} ({len(rows):,} rows)', file=sys.stderr)

    # --- classify the sharp shortlist ------------------------------------
    def cls(gloss):
        if 'MAHĀVY' in gloss:
            return 'mahavyutpatti-new'
        if re.search(r'zu streichen|fehlerhaft|lies |\bst\.\b|zu lesen', gloss):
            return 'verbesserung-correction'
        return 'other'

    from collections import Counter
    print('\n=== sharp shortlist breakdown ===')
    for k, v in Counter(cls(r[2]) for r in star).most_common():
        print(f'  {k}: {v}')
    mv = [r for r in star if cls(r[2]) == 'mahavyutpatti-new']
    print(f'  Mahāvyutpatti class: {len(mv)}; corroborated by >=2 indep dicts: '
          f'{sum(1 for r in mv if len([x for x in r[3].split(",") if x]) >= 2)}; '
          f'by bhs: {sum(1 for r in mv if "bhs" in r[3])}; '
          f'in MW body at all: {sum(1 for r in mv if r[4])}')


if __name__ == '__main__':
    main()
