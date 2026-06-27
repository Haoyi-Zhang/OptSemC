#!/usr/bin/env python3
"""Check that the paper snapshot uses the stable current-draft naming and no stale package labels."""
from __future__ import annotations
import csv, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'artifact' / 'evaluation' / 'package_coherence.csv'
checks=[]

def add(name, passed, details=''):
    checks.append({'check':name,'passed':str(bool(passed)).lower(),'details':details})

# Stable draft should exist, old versioned drafts should not be present in the package package.
stable = ROOT / 'Paper' / 'latex' / 'paper.tex'
add('stable_main_tex_exists', stable.exists(), str(stable.relative_to(ROOT)))
old = list((ROOT/'Paper'/'latex').glob('optsem_c_v*_*.tex')) + list((ROOT/'Paper'/'latex').glob('optsem_c_v*_*.pdf'))
add('no_old_versioned_drafts_in_package', len(old)==0, '|'.join(str(p.relative_to(ROOT)) for p in old[:10]))
# Tables in active sections should not use stale vNN filenames.
active_text = ''
for p in [stable] + sorted((ROOT/'Paper'/'latex'/'sections').glob('*.tex')):
    if p.exists(): active_text += '\n' + p.read_text(encoding='utf-8', errors='ignore')
patterns = [r'tab_v\d+', r'optsem_c_v\d+', r'v\d+[-_ ]']
violations=[]
for pat in patterns:
    if re.search(pat, active_text): violations.append(pat)
add('no_stale_version_labels_in_active_paper', not violations, '|'.join(violations))
# README should point to stable draft.
readme_path = ROOT/'README.md' if (ROOT/'README.md').exists() else ROOT/'artifact'/'README.md'
readme = readme_path.read_text(encoding='utf-8', errors='ignore') if readme_path.exists() else ''
add('readme_points_to_stable_draft', ('Paper/latex/paper.tex' in readme or ('Paper/latex/paper.tex' in readme or 'paper/latex/paper.tex' in readme)) and 'optsem_c_v29' not in readme and 'optsem_c_v30' not in readme, '')
# Evidence example table should not contain textual ellipses from truncation.
table_text = ''.join(p.read_text(encoding='utf-8', errors='ignore') for p in (ROOT/'Paper'/'latex'/'tables').glob('*.tex'))
add('no_truncated_table_ellipses', '...' not in table_text and '…' not in table_text, '')
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(checks)
passed=sum(r['passed']=='true' for r in checks)
print(f'Package coherence checks: {passed}/{len(checks)} passed')
if passed != len(checks):
    for r in checks:
        if r['passed']!='true': print('FAIL', r)
    sys.exit(1)
