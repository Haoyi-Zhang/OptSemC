#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'sql_shape_diagnostics_check.csv'
rows=[]
def add(c,o,d=''):
    rows.append({'check':c,'passed':str(bool(o)).lower(),'details':str(d)})
shape=ART/'evaluation'/'sql_shape_diagnostics.csv'; issues=ART/'evaluation'/'sql_shape_feature_issues.csv'
if shape.exists() and issues.exists():
    s=list(csv.DictReader(shape.open(newline='', encoding='utf-8'))); i=list(csv.DictReader(issues.open(newline='', encoding='utf-8')))
    add('all_probes_shaped', len(s)==4216, len(s))
    add('join_and_group_shapes_present', any(r['has_join']=='true' for r in s) and any(r['has_group']=='true' for r in s), '')
    add('feature_shape_issues_bounded', len(i)==1 and i[0]['probe_id']=='none', str(i[:3]))
else:
    for c in ['all_probes_shaped','join_and_group_shapes_present','feature_shape_issues_bounded']: add(c,False,'missing')
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'SQL shape diagnostics check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL',r['check'],r['details'])
if passed!=len(rows): sys.exit(1)
