#!/usr/bin/env python3
"""Ensure the paper mainline uses grounded corpus counts and not quarantined legacy counts."""
from __future__ import annotations
from pathlib import Path
import csv, re, sys
ROOT = Path(__file__).resolve().parents[2]
latex = ROOT/'Paper'/'latex'
# Prefer the stable main draft; fall back to the newest draft if reused.
draft = latex/'paper.tex'
if not draft.exists():
    drafts = sorted(latex.glob('optsem_c_*_draft.tex'), key=lambda p: p.stat().st_mtime, reverse=True)
    draft = drafts[0] if drafts else None
files = list((latex/'sections').glob('*.tex'))
if draft is not None:
    files.append(draft)
forbidden_patterns = [
    r'current corpus contains 746', r'746 accepted contract rules', r'112 public source records',
    r'747 frozen evidence segments', r'legacy 746-rule corpus is retained', r'stress-test layer',
    r'optsem_c_v2[0-6]_', r'paper/latex/', r'artifact/', r'\.jsonl', r'\.csv', r'\.py'
]
rows=[]; fail=False
for f in sorted(set(files)):
    text=f.read_text(errors='ignore') if f.exists() else ''
    for pat in forbidden_patterns:
        matches=list(re.finditer(pat,text,re.I))
        rows.append({'file':str(f.relative_to(ROOT)),'pattern':pat,'matches':len(matches),'pass':'yes' if not matches else 'no'})
        if matches: fail=True
out=ROOT/'artifact/evaluation/mainline_grounded_only_check.csv'
out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=['file','pattern','matches','pass']); w.writeheader(); w.writerows(rows)
summary=ROOT/'artifact/evaluation/mainline_grounded_only_summary.csv'
with summary.open('w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=['metric','value']); w.writeheader(); w.writerow({'metric':'status','value':'FAIL' if fail else 'PASS'}); w.writerow({'metric':'checked_files','value':len(files)})
print('Mainline grounded-only check', 'FAIL' if fail else 'PASS')
sys.exit(1 if fail else 0)
