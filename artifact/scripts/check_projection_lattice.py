#!/usr/bin/env python3
"""Check projection-lattice certificates used by the OptSem-C package."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'evaluation' / 'grounded'
OUT = ROOT / 'evaluation' / 'projection_lattice_check.csv'
SUMMARY = G / 'projection_lattice_summary.csv'
POINTS = G / 'projection_lattice_points.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))
try:
    summary=read_csv(SUMMARY); points=read_csv(POINTS)
    add('projection_lattice_files_present', bool(summary) and bool(points), f'summaries={len(summary)};points={len(points)}')
except Exception as exc:
    summary=[]; points=[]; add('projection_lattice_files_present', False, type(exc).__name__)
index={(r.get('scope'), r.get('field_universe')):r for r in summary}
def mins(scope, universe): return index.get((scope, universe), {}).get('example_minimum_safe_sets','').split(';')
def min_size(scope, universe):
    try: return int(index.get((scope, universe), {}).get('minimum_safe_size',-99))
    except ValueError: return -99
def base(scope, universe):
    try: return int(index.get((scope, universe), {}).get('baseline_false_equivalences',-1))
    except ValueError: return -1
add('keyword_placement_single_field_frontier', min_size('keyword','semantic_no_variant')==1 and 'placement' in mins('keyword','semantic_no_variant'), index.get(('keyword','semantic_no_variant'),{}))
add('operator_only_layer_single_field_frontier', min_size('operator_only','semantic_no_variant')==1 and 'layer' in mins('operator_only','semantic_no_variant'), index.get(('operator_only','semantic_no_variant'),{}))
add('yesno_semantic_single_field_frontier', min_size('yesno','semantic_no_variant')==1 and any(f in mins('yesno','semantic_no_variant') for f in ['layer','placement','state']), index.get(('yesno','semantic_no_variant'),{}))
add('all_projection_core_two_field_frontier', min_size('all_projections','core_semantic_state_free')==2 and 'layer+placement' in mins('all_projections','core_semantic_state_free'), index.get(('all_projections','core_semantic_state_free'),{}))
add('baseline_false_counts_match_mainline', base('keyword','semantic_no_variant')==254 and base('operator_only','semantic_no_variant')==238 and base('all_projections','semantic_no_variant')==498, '')
try:
    empty=[r for r in points if r.get('fields')=='EMPTY' and int(r.get('false_remaining','0'))>0]
    add('empty_augmentations_remain_unsafe', len(empty)==8, f'nonzero_empty={len(empty)}')
except Exception as exc:
    add('empty_augmentations_remain_unsafe', False, type(exc).__name__)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Projection lattice check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)
