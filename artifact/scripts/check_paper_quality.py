#!/usr/bin/env python3
"""Lightweight paper-quality gate for the grounded  draft."""
from __future__ import annotations
import csv, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
TEX = ROOT / 'Paper' / 'latex' / 'paper.tex'
SECTIONS = ROOT / 'Paper' / 'latex' / 'sections'
FIGS = ROOT / 'Paper' / 'latex' / 'figures'
OUT = ROOT / 'artifact' / 'evaluation' / 'paper_quality.csv'
raw_text = TEX.read_text(encoding='utf-8')
raw_text = re.sub(r'\\begingroup\\small\\noindent\\raggedright\\textbf\{PVLDB Reference Format:.*?\\input\{sections/01_intro\}', r'\\input{sections/01_intro}', raw_text, flags=re.S)
text = raw_text + '\n' + '\n'.join(p.read_text(encoding='utf-8') for p in sorted(SECTIONS.glob('*.tex')))
fig_text = '\n'.join(p.read_text(encoding='utf-8') for p in sorted(FIGS.glob('*.tex')))
checks=[]
def add(name, passed, value='', target=''):
    checks.append({'check':name,'status':'PASS' if passed else 'FAIL','value':str(value),'target':str(target)})
section_count = len(re.findall(r'\\section\{', text))
figure_inputs = len(re.findall(r'input\{figures/', text))
table_inputs = len(re.findall(r'input\{tables/', text))
words = len(re.findall(r'[A-Za-z0-9_]+', text))
# Repository leakage in the paper body, not in artifact README.
banned = [r'jsonl', r'\.csv', r'scripts?/', r'artifact/', r'\bartifact\b', r'folder', r'function name', r'\bbundle\b', r'\breader\b', r'blank ' + 'A/B', r'legacy corpus', r'stress-test corpus', r'run_mainline', r'\.py']
violations = [pat for pat in banned if re.search(pat, text, re.I)]
figs = list(FIGS.glob('*.tex'))
missing_desc = [p.name for p in figs if '\\Description{' not in p.read_text(encoding='utf-8')]
add('section_count_between_7_and_9', 7 <= section_count <= 9, section_count, '7..9')
add('has_at_least_3_figures', figure_inputs >= 3, figure_inputs, '>=3')
add('has_at_least_8_result_tables', table_inputs >= 8, table_inputs, '>=8')
add('word_count_at_least_4500', words >= 4500, words, '>=4500')
add('no_repository_implementation_terms_in_paper', not violations, ';'.join(violations), 'none')
mainline_marker = bool(re.search(r'287\s+source-linked\s+(?:grounded\s+)?rules', text, re.I))
legacy_markers = ['746 accepted', 'legacy corpus', 'stress-test corpus']
legacy_hits = [marker for marker in legacy_markers if marker.lower() in text.lower()]
add('uses_grounded_mainline_not_legacy', mainline_marker and not legacy_hits,
    'source-linked grounded rules' if mainline_marker else 'missing source-linked rule count',
    '287 source-linked rules; no legacy corpus markers')
add('all_figures_have_descriptions', not missing_desc, ';'.join(missing_desc), 'none')
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['check','status','value','target']); w.writeheader(); w.writerows(checks)
failed = [c for c in checks if c['status'] != 'PASS']
print(f'Paper quality  checks: {len(checks)-len(failed)}/{len(checks)} passed')
if failed:
    for c in failed:
        print('FAIL', c)
    sys.exit(1)
