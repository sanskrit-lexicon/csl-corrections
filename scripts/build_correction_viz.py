#!/usr/bin/env python3
"""Regenerate the three corrections-native visualisations under docs/img/
from data/derived/correction_loci.tsv (memo docs/HYPOTHESES_AND_VIZ_MEMO.md
§3; built per H294).

  1. correction_velocity_timeline.svg — monthly records, human vs bulk
  2. correction_density_per_dict.svg  — records per 1k entries, bulk hatched
  3. correction_batch_treemap.svg     — batch × dict composition (BOR/LRV skew)

Entry counts come from data/derived/dict_entry_counts.tsv (grep -c '^<L>'
over csl-orig v02, cached so this script never needs csl-orig). The memo
suggested union_headwords.tsv, but that list covers only 5 of the 16
touched dicts (ap, gra, inm, mw, skd) — csl-orig <L> counts cover all.

Usage: python scripts/build_correction_viz.py
"""

import csv
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parent.parent
LOCI = REPO / 'data' / 'derived' / 'correction_loci.tsv'
ENTRIES = REPO / 'data' / 'derived' / 'dict_entry_counts.tsv'
IMG = REPO / 'docs' / 'img'

# Reference palette (dataviz skill): categorical slots 1–2, chrome inks.
HUMAN, BULK = '#2a78d6', '#1baf7a'
SURFACE, INK, INK2, MUTED, GRID, BASE = (
    '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7')

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'DejaVu Sans', 'sans-serif'],
    'text.color': INK, 'axes.edgecolor': BASE, 'axes.labelcolor': INK2,
    'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.linewidth': 0.8,
    'svg.fonttype': 'none', 'figure.facecolor': SURFACE,
    'axes.facecolor': SURFACE, 'savefig.facecolor': SURFACE,
})


def load_rows():
    with open(LOCI, encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def load_entries():
    with open(ENTRIES, encoding='utf-8') as f:
        return {r['dict']: int(r['entries'])
                for r in csv.DictReader(f, delimiter='\t')}


def style_axes(ax):
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.grid(axis='y', color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def viz_timeline(rows):
    months = sorted({r['batch_date'][:7] for r in rows})
    per = {m: Counter() for m in months}
    for r in rows:
        per[r['batch_date'][:7]][r['process']] += 1
    fig, ax = plt.subplots(figsize=(8.5, 3.4), dpi=100)
    x = range(len(months))
    h = [per[m]['human'] for m in months]
    b = [per[m]['bulk'] for m in months]
    ax.bar(x, h, 0.62, color=HUMAN, label='human', zorder=3)
    ax.bar(x, b, 0.62, bottom=h, color=BULK, hatch='///',
           edgecolor=SURFACE, linewidth=0.8, label='bulk (machine batch)',
           zorder=3)
    for i, m in enumerate(months):
        total = h[i] + b[i]
        ax.text(i, total + 500, f'{total:,}', ha='center', va='bottom',
                fontsize=8, color=INK2)
    ax.set_xticks(list(x), months, fontsize=8)
    ax.set_ylabel('correction records', fontsize=9)
    ax.set_title('Correction velocity by batch month — human vs bulk process',
                 fontsize=11, color=INK, loc='left', pad=12)
    ax.legend(frameon=False, fontsize=8, loc='upper left')
    ax.set_ylim(0, max(h[i] + b[i] for i in x) * 1.18)
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(IMG / 'correction_velocity_timeline.svg')
    plt.close(fig)


def viz_density(rows, entries):
    per = {}
    for r in rows:
        per.setdefault(r['dict'], Counter())[r['process']] += 1
    dicts = sorted(per, key=lambda d: -(sum(per[d].values()) * 1000
                                        / entries[d]))
    fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=100)
    y = range(len(dicts))
    hd = [per[d]['human'] * 1000 / entries[d] for d in dicts]
    bd = [per[d]['bulk'] * 1000 / entries[d] for d in dicts]
    ax.barh(y, hd, 0.62, color=HUMAN, label='human', zorder=3)
    ax.barh(y, bd, 0.62, left=hd, color=BULK, hatch='///',
            edgecolor=SURFACE, linewidth=0.8, label='bulk (machine batch)',
            zorder=3)
    for i, d in enumerate(dicts):
        total = hd[i] + bd[i]
        n = sum(per[d].values())
        ax.text(total + 12, i, f'{total:,.1f}  ({n:,} rec)', va='center',
                fontsize=7.5, color=INK2)
    ax.set_yticks(list(y), [d.upper() for d in dicts], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel('correction records per 1,000 entries', fontsize=9)
    ax.set_title('Correction density per dictionary (entries from csl-orig)',
                 fontsize=11, color=INK, loc='left', pad=12)
    ax.legend(frameon=False, fontsize=8, loc='lower right')
    ax.set_xlim(0, max(hd[i] + bd[i] for i in y) * 1.30)
    ax.grid(axis='x', color=GRID, linewidth=0.6)
    ax.grid(axis='y', visible=False)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(IMG / 'correction_density_per_dict.svg')
    plt.close(fig)


def slice_dice(items, x, y, w, h, vertical):
    """Simple slice-and-dice treemap: items = [(label, value, payload)]."""
    total = sum(v for _, v, _ in items)
    out = []
    for label, v, payload in items:
        frac = v / total
        if vertical:
            out.append((label, payload, (x, y, w, h * frac)))
            y += h * frac
        else:
            out.append((label, payload, (x, y, w * frac, h)))
            x += w * frac
    return out


def viz_treemap(rows):
    per_batch = {}
    for r in rows:
        per_batch.setdefault(r['batch'], Counter())[
            (r['dict'], r['process'])] += 1
    batches = sorted(per_batch,
                     key=lambda b: -sum(per_batch[b].values()))
    fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=100)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Batch composition — batch × dictionary × process '
                 '(area = records)', fontsize=11, color=INK, loc='left',
                 pad=12)
    items = [(b, sum(per_batch[b].values()), per_batch[b]) for b in batches]
    for b, counts, (x, y, w, h) in slice_dice(items, 0, 0, 1, 1, False):
        cells = sorted(counts.items(), key=lambda kv: -kv[1])
        cell_items = [(f'{d}', n, p) for (d, p), n in cells]
        for d, proc, (cx, cy, cw, ch) in slice_dice(cell_items, x, y, w, h,
                                                    True):
            color = BULK if proc == 'bulk' else HUMAN
            ax.add_patch(Rectangle(
                (cx, cy), cw, ch, facecolor=color,
                hatch='///' if proc == 'bulk' else None,
                edgecolor=SURFACE, linewidth=1.5))
            area = cw * ch
            n = dict(cells)[(d, proc)]
            if area > 0.012:
                ax.text(cx + cw / 2, cy + ch / 2,
                        f'{d.upper()}\n{n:,}', ha='center', va='center',
                        fontsize=min(11, 6 + area * 60), color='#ffffff')
        total = sum(counts.values())
        label = b.replace('batches/', '') .replace('batch_', '')
        if w > 0.04:
            ax.text(x + w / 2, -0.045, f'{label}\n{total:,}', ha='center',
                    va='top', fontsize=7.5, color=INK2)
    handles = [Rectangle((0, 0), 1, 1, facecolor=HUMAN),
               Rectangle((0, 0), 1, 1, facecolor=BULK, hatch='///',
                         edgecolor=SURFACE)]
    ax.legend(handles, ['human', 'bulk (machine batch)'], frameon=False,
              fontsize=8, loc='upper left', bbox_to_anchor=(0, -0.10))
    fig.tight_layout()
    fig.savefig(IMG / 'correction_batch_treemap.svg', bbox_inches='tight')
    plt.close(fig)


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    entries = load_entries()
    viz_timeline(rows)
    viz_density(rows, entries)
    viz_treemap(rows)
    print(f'wrote 3 SVGs to {IMG.relative_to(REPO)} from {len(rows):,} rows')


if __name__ == '__main__':
    main()
