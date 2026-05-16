import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ORG = 'sanskrit-lexicon'
REPO = 'csl-corrections'

def fetch_issues_with_label(label, state='all'):
    items = []
    page = 1
    while True:
        r = subprocess.run(
            ['gh', 'api', f'repos/{ORG}/{REPO}/issues',
             '-f', f'state={state}', '-f', f'labels={label}',
             '-f', 'per_page=100', '-f', f'page={page}',
             '--jq', '[.[] | {number:.number, state:.state}]'],
            capture_output=True, encoding='utf-8')
        batch = json.loads(r.stdout)
        if not batch:
            break
        items.extend(batch)
        page += 1
    return items

type_labels = ['link-target','link-splitting','markup','text-correction',
               'content-enhancement','encoding','scan-quality','bug','question']

print(f'{"Label":<25} {"Open":>6} {"Closed":>7} {"Total":>6}')
print('-' * 46)
for lbl in type_labels:
    issues = fetch_issues_with_label(lbl)
    open_c = sum(1 for i in issues if i['state'] == 'open')
    closed_c = sum(1 for i in issues if i['state'] == 'closed')
    print(f'{lbl:<25} {open_c:>6} {closed_c:>7} {len(issues):>6}')

print('DONE')
