#!/usr/bin/env python3
"""Check feature-family held-out repair stability."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
E = ROOT / 'evaluation'
OUT = E / 'feature_holdout_repair_check.csv'
rows=[]
def add(check, passed, details=''):
    rows.append({'check': check, 'passed': str(bool(passed)).lower(), 'details': str(details)})
def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))
try:
    detail = read_csv(E/'feature_holdout_repair.csv')
    summary = read_csv(E/'feature_holdout_repair_summary.csv')
    add('feature_holdout_folds_present', len(detail) >= 15, len(detail))
    add('headline_methods_present', {r['method'] for r in summary} == {'keyword','operator_only','yesno'}, ','.join(sorted(r['method'] for r in summary)))
    add('heldout_false_equivalences_nonzero', sum(int(r['heldout_false_equivalences_total']) for r in summary) > 0, '')
    add('robust_basis_resolves_all_heldout', all(int(r['robust_basis_unresolved_total']) == 0 for r in summary), '')
    add('robust_basis_is_layer_placement', all(r['robust_basis'] == 'layer+placement' for r in summary), '')
    add('point_minimum_stress_is_nontrivial', any(int(r['learned_minimum_unresolved_total']) > 0 for r in summary), '')
except Exception as exc:
    add('feature_holdout_repair_readable', False, type(exc).__name__)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Feature-holdout repair check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)
