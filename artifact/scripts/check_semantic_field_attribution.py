#!/usr/bin/env python3
"""Validate semantic-field Shapley attribution output.

The Shapley efficiency property requires field attributions to sum to the
number of false-equivalence witnesses for each projection. This check makes
sure the attribution table is not a disconnected descriptive statistic.
"""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'evaluation' / 'grounded'
path = G / 'semantic_field_shapley.csv'
out = ROOT / 'evaluation' / 'semantic_field_attribution_check.csv'
rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')))
by = {}
for r in rows:
    m = r['method']
    by.setdefault(m, {'total': int(r['false_equivalences']), 'sum': 0.0, 'fields': 0})
    by[m]['sum'] += float(r['shapley_total'])
    by[m]['fields'] += 1
out_rows=[]; ok_all=True
for m, d in sorted(by.items()):
    diff = abs(d['sum'] - d['total'])
    ok = diff < 1e-4 and d['fields'] >= 8
    ok_all &= ok
    out_rows.append({'method':m,'false_equivalences':d['total'],'shapley_total_sum':f"{d['sum']:.6f}",'abs_error':f"{diff:.8f}",'fields':d['fields'],'passed':str(ok).lower()})
with out.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['method','false_equivalences','shapley_total_sum','abs_error','fields','passed'])
    w.writeheader(); w.writerows(out_rows)
print(f"Semantic-field attribution check: {sum(r['passed']=='true' for r in out_rows)}/{len(out_rows)} passed")
if not ok_all:
    sys.exit(1)
