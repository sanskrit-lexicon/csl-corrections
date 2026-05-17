import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

diagrams = {
    'pipeline_dag': '''flowchart LR
  F["Web form"] -->|submit| T["cfr.tsv"]
  T -->|cfr_adj.py| C["xxx_correctionform.txt"]
  T -->|mark resolved| T
  C -->|review| E["csl-orig source edit"]
  E -->|update_user_corrections.sh| B["build + push csl-orig"]
  T -->|post_github_issues.sh| G["GitHub issues on csl-orig"]''',
    'all_by_type': '''pie title All issues by type
  "text-correction" : 123
  "question" : 40
  "bug" : 22
  "encoding" : 13
  "markup" : 12
  "content-enhancement" : 7
  "link-target" : 2
  "scan-quality" : 1''',
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
        print(f'{name}: INVALID -- {r.stdout[:200]}')
