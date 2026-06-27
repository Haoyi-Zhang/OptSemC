#!/usr/bin/env python3
"""Check that probe-coverage diagnostics are nontrivial and current."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'probe_coverage_depth_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
path=ART/'evaluation'/'probe_coverage_matrix.csv'
if path.exists():
    data=list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    by={int(r['strength']):r for r in data}
    add('strengths_1_2_3_present', all(k in by for k in (1,2,3)), str(sorted(by)))
    add('onewise_complete', float(by.get(1,{}).get('coverage_rate',0)) >= 0.999, by.get(1,{}).get('coverage_rate',''))
    add('twowise_nontrivial', int(by.get(2,{}).get('covered',0)) >= 1000, by.get(2,{}).get('covered',''))
    add('threewise_nontrivial', int(by.get(3,{}).get('covered',0)) >= 5000, by.get(3,{}).get('covered',''))
else:
    for name in ['strengths_1_2_3_present','onewise_complete','twowise_nontrivial','threewise_nontrivial']:
        add(name, False, 'missing')
counts=ART/'evaluation'/'probe_feature_value_counts.csv'
add('feature_value_counts_present', counts.exists() and sum(1 for _ in counts.open(encoding='utf-8')) > 20 if counts.exists() else False, '')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Probe coverage depth check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

