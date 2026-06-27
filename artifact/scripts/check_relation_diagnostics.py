#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'relation_diagnostics_check.csv'
rows=[]
def add(c,o,d=''):
    rows.append({'check':c,'passed':str(bool(o)).lower(),'details':str(d)})
path=ART/'evaluation'/'relation_diagnostics.csv'
if path.exists():
    data=list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    by={r['projection']:r for r in data}
    add('rows_present', len(data)>=5, len(data))
    add('strict_no_false_kernel_classes', int(by.get('strict',{}).get('false_projected_classes',1))==0, by.get('strict',{}).get('false_projected_classes','missing'))
    add('lossy_kernel_classes_exist', int(by.get('keyword',{}).get('false_projected_classes',0))>0 and int(by.get('operator_only',{}).get('false_projected_classes',0))>0, '')
else:
    for c in ['rows_present','strict_no_false_kernel_classes','lossy_kernel_classes_exist']: add(c,False,'missing')
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Relation diagnostics check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL',r['check'],r['details'])
if passed!=len(rows): sys.exit(1)
