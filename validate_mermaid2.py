import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

diagrams = {
    'closed_by_ms': '''pie title Issues closed by milestone
  "Digitization Quality" : 2702
  "Structured Data" : 37
  "Major Enhancements" : 13''',
    'open_by_type': '''pie title Open issues by type
  "text-correction" : 17
  "question" : 15
  "bug" : 13
  "content-enhancement" : 12
  "markup" : 9
  "scan-quality" : 2
  "encoding" : 2''',
    'all_by_type': '''pie title All 2822 issues by type
  "text-correction" : 2676
  "markup" : 33
  "bug" : 32
  "question" : 28
  "content-enhancement" : 25
  "scan-quality" : 24
  "encoding" : 4''',
    'pipeline_dag': '''flowchart LR
  U["User submission"] --> C["csl-corrections\ncfr.tsv"]
  C -->|review| E["Edit v02/dict/dict.txt"]
  E -->|git push| O["csl-orig master"]
  O -->|Actions: update-stardict| SD["stardict-sanskrit"]
  O -->|Actions: generate-dict| DB["SQLite + web formats"]
  O -->|Actions: regenerate-hwnorm1| HW["hwnorm1c.sqlite"]''',
}

for name, diag in diagrams.items():
    text = f'```mermaid\n{diag}\n```'
    r = subprocess.run(
        ['gh', 'api', 'markdown', '-X', 'POST',
         '-f', f'text={text}', '-f', 'mode=markdown'],
        capture_output=True, encoding='utf-8')
    if 'pl-k' in r.stdout:
        print(f'{name}: VALID')
    else:
        print(f'{name}: INVALID -- {r.stdout[:150]}')
