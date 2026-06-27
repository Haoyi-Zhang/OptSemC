#!/usr/bin/env python3
"""Validate exact Shapley attribution outputs for semantic-field repair analysis."""
from __future__ import annotations
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'evaluation' / 'grounded'
OUT = ROOT / 'evaluation' / 'shapley_attribution_check.csv'

rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':details})

def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

shapley = read_csv(G/'semantic_field_shapley.csv')
cond = {r['method']: int(r['false_equivalences']) for r in read_csv(G/'conditional_trap_rate.csv') if r['method'] in {'keyword','yesno','operator_only'}}
by_method={}
for r in shapley:
    by_method.setdefault(r['method'], []).append(r)

required={'keyword','yesno','operator_only'}
add('required_methods_present', required.issubset(by_method.keys()), f'methods={sorted(by_method.keys())}')
for method in sorted(required):
    rows_m=by_method.get(method, [])
    shares=[float(r['share']) for r in rows_m]
    fes={int(r['false_equivalences']) for r in rows_m}
    add(f'{method}_has_eight_fields', len(rows_m)==8, f'fields={len(rows_m)}')
    add(f'{method}_shares_nonnegative', all(x >= -1e-12 for x in shares), '')
    add(f'{method}_shares_sum_to_one', abs(sum(shares)-1.0) < 5e-6 or cond.get(method,0)==0, f'sum={sum(shares):.12f}')
    add(f'{method}_false_equivalences_match_conditional', fes == {cond.get(method)}, f'shapley={sorted(fes)} cond={cond.get(method)}')

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Shapley attribution check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r)
if passed != len(rows): sys.exit(1)
