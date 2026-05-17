import subprocess, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ORG = 'sanskrit-lexicon'
REPO = 'csl-orig'

issues = []
page = 1
while True:
    r = subprocess.run(
        ['gh', 'api', f'repos/{ORG}/{REPO}/issues?state=all&per_page=100&page={page}',
         '--jq', '[.[] | {n:.number, state:.state, title:.title, labels:[.labels[].name], comments:.comments}]'],
        capture_output=True, encoding='utf-8')
    if r.returncode != 0 or not r.stdout.strip():
        break
    batch = json.loads(r.stdout)
    if not batch:
        break
    issues.extend(batch)
    page += 1
    if page % 5 == 0:
        print(f'Fetched {len(issues)} issues (page {page-1})...', flush=True)

print(f'Total: {len(issues)} issues')

# Pattern: dict:linenum  e.g. "ap:23496", "mw:161697.1", "shs:32313"
dict_linenum = re.compile(r'^[a-z0-9]+:\d+[\d.]*\s*$', re.IGNORECASE)

# Categorise
by_label = {}
unlabeled_correction = []  # dict:linenum with no labels
unlabeled_other = []       # no labels, not dict:linenum pattern

for i in issues:
    n = i['n']
    lbls = i['labels']
    title = i['title'].strip()
    state = i['state']

    if not lbls:
        if dict_linenum.match(title):
            unlabeled_correction.append(n)
        else:
            unlabeled_other.append((n, state, title))
    else:
        key = ','.join(sorted(lbls))
        by_label.setdefault(key, []).append((n, state, title))

print(f'\nunlabeled dict:linenum corrections: {len(unlabeled_correction)}')
print(f'unlabeled other: {len(unlabeled_other)}')

print('\n--- Labeled groups ---')
for k, v in sorted(by_label.items(), key=lambda x: -len(x[1])):
    print(f'[{k}] ({len(v)}):')
    for n, s, t in v[:5]:
        print(f'  #{n} ({s}) {t[:70]}')
    if len(v) > 5:
        print(f'  ... and {len(v)-5} more')

print('\n--- Unlabeled other (open) ---')
for n, s, t in unlabeled_other:
    if s == 'open':
        print(f'  #{n} ({s}) {t[:80]}')

print('\n--- Unlabeled other (closed, sample) ---')
closed_other = [(n, s, t) for n, s, t in unlabeled_other if s == 'closed']
print(f'Total closed unlabeled non-pattern: {len(closed_other)}')
for n, s, t in closed_other[:20]:
    print(f'  #{n} ({s}) {t[:80]}')
