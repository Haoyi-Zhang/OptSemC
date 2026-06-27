#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'workload_suite_depth_check.csv'
rows=[]
def add(c,o,d=''):
    rows.append({'check':c,'passed':str(bool(o)).lower(),'details':str(d)})
mat=ART/'evaluation'/'workload_suite_matrix.csv'
dep=ART/'evaluation'/'workload_suite_depth.csv'
if mat.exists() and dep.exists():
    m=list(csv.DictReader(mat.open(newline='', encoding='utf-8'))); d=list(csv.DictReader(dep.open(newline='', encoding='utf-8')))
    add('motif_matrix_substantial', len(m)>=50, len(m))
    add('all_motifs_covered', all(r['covered']=='true' for r in m), '')
    add('suite_depth_nonzero', all(int(r['min_hits'])>0 for r in d), '')
else:
    for c in ['motif_matrix_substantial','all_motifs_covered','suite_depth_nonzero']: add(c,False,'missing')
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Workload suite depth check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed!=len(rows): sys.exit(1)
