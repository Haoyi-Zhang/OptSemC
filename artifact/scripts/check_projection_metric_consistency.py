#!/usr/bin/env python3
"""Check that all grounded projection-failure outputs use the same semantics.

This is a guard against a subtle artifact error: if two scripts implement a
coarse projection slightly differently, the paper can report one false-
equivalence count while the artifact contains another. The check ties together
trap-rate, conditional false-equivalence, and repair-certificate outputs.
"""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
paths = {
    'trap': ROOT/'evaluation/grounded/trap_rate.csv',
    'conditional': ROOT/'evaluation/grounded/conditional_trap_rate.csv',
    'repair': ROOT/'evaluation/grounded/repair_certificate_summary.csv',
}
errors=[]
for name,p in paths.items():
    if not p.exists(): errors.append(f'missing {name}: {p}')
if errors:
    print('Projection metric consistency check FAILED')
    print('\n'.join(errors)); sys.exit(1)
trap = {r['method']: r for r in csv.DictReader(paths['trap'].open())}
cond = {r['method']: r for r in csv.DictReader(paths['conditional'].open())}
repair = {r['method']: r for r in csv.DictReader(paths['repair'].open())}
main_methods = ['keyword','yesno','operator_only']
for m in main_methods:
    if m not in trap: errors.append(f'{m} missing from trap_rate.csv')
    if m not in cond: errors.append(f'{m} missing from conditional_trap_rate.csv')
    if m not in repair: errors.append(f'{m} missing from repair_certificate_summary.csv')
    if m in trap and m in cond:
        if int(trap[m]['false_equivalence']) != int(cond[m]['false_equivalences']):
            errors.append(f'{m}: trap false_equivalence {trap[m]["false_equivalence"]} != conditional false_equivalences {cond[m]["false_equivalences"]}')
        if int(trap[m]['comparisons']) != int(cond[m]['comparisons']):
            errors.append(f'{m}: comparison denominator mismatch')
    if m in repair and m in cond:
        if int(repair[m]['false_equivalences']) != int(cond[m]['false_equivalences']):
            errors.append(f'{m}: repair certificate false-equivalence count differs from conditional result')
# Field-preserving negative controls must not create false equivalence.
for m in ['no_placement','no_modality','no_decision_time','no_observability']:
    if m in trap and int(trap[m]['false_equivalence']) != 0:
        errors.append(f'{m}: expected zero false equivalence, found {trap[m]["false_equivalence"]}')
if errors:
    print('Projection metric consistency check FAILED')
    for e in errors: print(e)
    sys.exit(1)
print('Projection metric consistency check passed')
