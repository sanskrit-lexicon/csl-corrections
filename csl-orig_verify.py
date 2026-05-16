import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ORG = 'sanskrit-lexicon'
REPO = 'csl-orig'

TYPE_LABELS = {'link-target','link-splitting','markup','text-correction',
               'content-enhancement','encoding','scan-quality','bug','question'}
SEV_LABELS  = {'minor','medium','hard'}

# Milestone numbers for this repo (DTB=4, DQ=5, SD=6, ME=7)
TYPE_TO_MS = {
    'link-target': 4, 'link-splitting': 4,
    'text-correction': 5, 'encoding': 5, 'bug': 5, 'scan-quality': 5,
    'markup': 6, 'question': 6,
    'content-enhancement': 7,
}

def fetch_all():
    issues = []
    page = 1
    while True:
        r = subprocess.run(
            ['gh', 'api',
             f'repos/{ORG}/{REPO}/issues?state=all&per_page=100&page={page}',
             '--jq', '[.[] | {number:.number, labels:[.labels[].name], milestone:.milestone.number}]'],
            capture_output=True, encoding='utf-8')
        if r.returncode != 0 or not r.stdout.strip():
            break
        batch = json.loads(r.stdout)
        if not batch:
            break
        issues.extend(batch)
        page += 1
    return issues

issues = fetch_all()
print(f'Fetched {len(issues)} issues')

missing_type = []; missing_sev = []; missing_ms = []; multi_type = []; wrong_ms = []

for i in issues:
    n = i['number']; lbls = set(i['labels']); ms = i['milestone']
    types = lbls & TYPE_LABELS
    sevs  = lbls & SEV_LABELS
    if len(types) == 0:   missing_type.append(n)
    elif len(types) > 1:  multi_type.append((n, types))
    if len(sevs) == 0:    missing_sev.append(n)
    if ms is None:        missing_ms.append(n)
    elif len(types) == 1:
        t = list(types)[0]
        if TYPE_TO_MS.get(t) != ms:
            wrong_ms.append((n, t, f'expected ms{TYPE_TO_MS.get(t)} got ms{ms}'))

print(f'missing_type  ({len(missing_type)}): {sorted(missing_type)[:20]}')
print(f'multi_type    ({len(multi_type)}): {multi_type[:10]}')
print(f'missing_sev   ({len(missing_sev)}): {sorted(missing_sev)[:20]}')
print(f'missing_ms    ({len(missing_ms)}): {sorted(missing_ms)[:20]}')
print(f'wrong_ms      ({len(wrong_ms)}): {wrong_ms[:10]}')

if not any([missing_type, multi_type, missing_sev, missing_ms, wrong_ms]):
    print('ALL CHECKS PASSED')
else:
    print('ISSUES FOUND - fix before proceeding')
    print(f'  Total unlabeled: {len(missing_type)} type, {len(missing_sev)} sev, {len(missing_ms)} milestone')
