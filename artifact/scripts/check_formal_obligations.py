#!/usr/bin/env python3
"""Check finite formal obligation outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'formal_obligations_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
path=ART/'evaluation'/'formal_obligations.csv'
if path.exists():
    data=list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    add('obligation_rows_present', len(data)>=20, str(len(data)))
    add('all_obligations_pass', data and all(r['passed']=='true' for r in data), f"{sum(r['passed']=='true' for r in data)}/{len(data)}")
    obligations={r['theorem'] for r in data}
    add('state_projection_lattice_covered', {'state_join_semilattice','projection_determinism','strict_projection_identity','field_lattice'}.issubset(obligations), ','.join(sorted(obligations)))
else:
    for name in ['obligation_rows_present','all_obligations_pass','state_projection_lattice_covered']:
        add(name, False, 'missing')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Formal obligations check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)
