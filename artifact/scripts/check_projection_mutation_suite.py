#!/usr/bin/env python3
"""Check the projection mutation suite."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'projection_mutation_suite_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
path=ART/'evaluation'/'projection_mutation_suite.csv'
if path.exists():
    data=list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    by={r['projection']:r for r in data}
    add('projection_count_ge_40', len(data)>=40, str(len(data)))
    add('strict_negative_control_zero_false', int(by.get('strict',{}).get('false_equivalences',-1))==0, by.get('strict',{}).get('false_equivalences','missing'))
    add('lossy_controls_have_false', all(int(by[m]['false_equivalences'])>0 for m in ('keyword','yesno','operator_only')), '')
    add('known_singleton_repairs_present', int(by.get('keyword+placement',{}).get('false_equivalences',1))==0 and int(by.get('operator_only+layer',{}).get('false_equivalences',1))==0, '')
else:
    for name in ['projection_count_ge_40','strict_negative_control_zero_false','lossy_controls_have_false','known_singleton_repairs_present']:
        add(name, False, 'missing')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Projection mutation suite check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

