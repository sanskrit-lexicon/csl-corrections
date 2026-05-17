import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ORG = 'sanskrit-lexicon'
REPO = 'csl-corrections'

type_labels = {
    'link-target','link-splitting','markup','text-correction',
    'content-enhancement','encoding','scan-quality','bug','question'
}
sev_labels = {'minor','medium','hard'}

# Actual milestone numbers from API
ms_title_to_num = {
    'Dictionary to Book': 1,
    'Digitization Quality': 2,
    'Structured Data': 3,
    'Major Enhancements': 4,
}
type_to_ms = {
    'link-target': 1, 'link-splitting': 1,
    'text-correction': 2, 'encoding': 2, 'bug': 2, 'scan-quality': 2,
    'markup': 3, 'question': 3,
    'content-enhancement': 4,
}

def fetch_all_issues():
    issues = []
    page = 1
    while True:
        r = subprocess.run(
            ['gh', 'api',
             f'repos/{ORG}/{REPO}/issues?state=all&per_page=100&page={page}',
             '--jq', '[.[] | {number:.number, labels:[.labels[].name], milestone:.milestone.number}]'],
            capture_output=True, encoding='utf-8')
        if r.returncode != 0:
            print(f'API error page {page}: {r.stderr[:200]}', flush=True)
            break
        if not r.stdout.strip():
            break
        batch = json.loads(r.stdout)
        if not batch:
            break
        issues.extend(batch)
        page += 1
    return issues

issues = fetch_all_issues()
print(f'Fetched {len(issues)} issues')

missing_type = []
missing_sev = []
missing_ms = []
multi_type = []
wrong_ms = []

for i in issues:
    n = i['number']
    lbls = set(i['labels'])
    ms = i['milestone']
    types = lbls & type_labels
    sevs = lbls & sev_labels

    if len(types) == 0:
        missing_type.append(n)
    elif len(types) > 1:
        multi_type.append((n, types))

    if len(sevs) == 0:
        missing_sev.append(n)

    if ms is None:
        missing_ms.append(n)
    elif len(types) == 1:
        t = list(types)[0]
        expected_ms = type_to_ms.get(t)
        if expected_ms != ms:
            wrong_ms.append((n, t, f'expected ms{expected_ms} got ms{ms}'))

print(f'missing_type  ({len(missing_type)}): {sorted(missing_type)}')
print(f'multi_type    ({len(multi_type)}): {multi_type}')
print(f'missing_sev   ({len(missing_sev)}): {sorted(missing_sev)}')
print(f'missing_ms    ({len(missing_ms)}): {sorted(missing_ms)}')
print(f'wrong_ms      ({len(wrong_ms)}): {wrong_ms}')

if not any([missing_type, multi_type, missing_sev, missing_ms, wrong_ms]):
    print('ALL CHECKS PASSED')
else:
    print('ISSUES FOUND - fix before proceeding')
