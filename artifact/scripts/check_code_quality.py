#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'python_code_quality_check.csv'
rows=[]
def add(c,o,d=''):
    rows.append({'check':c,'passed':str(bool(o)).lower(),'details':str(d)})
sumf=ART/'evaluation'/'python_code_quality_summary.csv'
if sumf.exists():
    s={r['metric']:r['value'] for r in csv.DictReader(sumf.open(newline='', encoding='utf-8'))}
    add('all_syntax_ok', s.get('python_files')==s.get('syntax_ok_files'), str(s))
    add('function_surface_large', int(s.get('functions',0))>=200, s.get('functions',''))
    add('class_surface_large', int(s.get('classes',0))>=25, s.get('classes',''))
else:
    for c in ['all_syntax_ok','function_surface_large','class_surface_large']: add(c,False,'missing')
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Code quality check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL',r['check'],r['details'])
if passed!=len(rows): sys.exit(1)
