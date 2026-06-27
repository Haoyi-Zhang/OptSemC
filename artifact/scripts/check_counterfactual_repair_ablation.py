#!/usr/bin/env python3
"""Check counterfactual repair ablation outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'counterfactual_repair_ablation_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
path=ART/'evaluation'/'counterfactual_repair_ablation.csv'
if path.exists():
    data=list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    lookup={(r['scope'],r['field_set']):r for r in data}
    add('headline_rows_present', all((m,'placement') in lookup for m in ('keyword','yesno','operator_only')), str(len(data)))
    add('all_headline_layer_placement_resolves_all', int(lookup.get(('all_headline','layer+placement'),{}).get('unresolved',1))==0, lookup.get(('all_headline','layer+placement'),{}).get('unresolved','missing'))
    add('singletons_not_all_sufficient', int(lookup.get(('all_headline','layer'),{}).get('unresolved',0))>0 and int(lookup.get(('all_headline','placement'),{}).get('unresolved',0))>0, '')
else:
    for name in ['headline_rows_present','all_headline_layer_placement_resolves_all','singletons_not_all_sufficient']:
        add(name, False, 'missing')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Counterfactual repair ablation check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

