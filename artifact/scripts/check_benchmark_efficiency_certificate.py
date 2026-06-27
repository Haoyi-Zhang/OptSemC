#!/usr/bin/env python3
"""Validate frozen benchmark-efficiency outputs without recomputing random trials."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'evaluation' / 'grounded'

def read_csv(p):
    with p.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))
rows=[]
def add(name, ok, details=''):
    rows.append((name, bool(ok), details))
try:
    eff=read_csv(G/'benchmark_efficiency.csv')
    summary={r['metric']:r['value'] for r in read_csv(G/'benchmark_efficiency_summary.csv')}
    order=read_csv(G/'diagnostic_probe_order.csv')
    add('efficiency_rows_present', len(eff) >= 2, f'rows={len(eff)}')
    add('diagnostic_order_present', len(order) > 0, f'rows={len(order)}')
    b50=next((r for r in eff if r['budget']=='50'), None)
    b100=next((r for r in eff if r['budget']=='100'), None)
    add('budget50_diagnostic_coverage_matches_summary', b50 is not None and b50['diagnostic_rule_coverage']==summary.get('diagnostic_budget50_rule_coverage'), str(b50))
    add('budget100_full_coverage', b100 is not None and b100['generated_rule_coverage']=='1.000000' and b100['diagnostic_rule_coverage']=='1.000000', str(b100))
    add('summary_full_budgets', summary.get('generated_full_rule_coverage_budget')=='100' and summary.get('diagnostic_full_rule_coverage_budget')=='100', str(summary))
except Exception as exc:
    add('benchmark_efficiency_certificate_exception', False, type(exc).__name__)
passed=sum(ok for _n,ok,_d in rows)
print(f'Benchmark efficiency certificate: {passed}/{len(rows)} passed')
for name,ok,details in rows:
    if not ok: print('FAIL', name, details)
if passed != len(rows): sys.exit(1)
