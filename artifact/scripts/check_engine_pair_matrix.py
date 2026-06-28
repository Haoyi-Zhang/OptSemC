#!/usr/bin/env python3
"""Check engine-pair false-equivalence matrix consistency."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'engine_pair_matrix_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
path=ART/'evaluation'/'engine_pair_false_portability_matrix.csv'
if path.exists():
    data=list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    add('matrix_rows_present', len(data) >= 60, str(len(data)))
    methods={r['projection'] for r in data}
    add('headline_methods_present', methods=={'keyword','yesno','operator_only'}, str(methods))
    sums={m:sum(int(r['false_equivalences']) for r in data if r['projection']==m) for m in methods}
    add('headline_false_counts_match', sums.get('keyword')==254 and sums.get('yesno')==6 and sums.get('operator_only')==238, str(sums))
else:
    for name in ['matrix_rows_present','headline_methods_present','headline_false_counts_match']:
        add(name, False, 'missing')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Engine-pair matrix check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)
