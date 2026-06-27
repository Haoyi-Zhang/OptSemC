#!/usr/bin/env python3
"""Validate multi-catalog SQL execution summary."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT/'evaluation'
OUT = E/'sql_probe_multicatalog_check.csv'
rows=[]

def add(check, passed, details=''):
    rows.append({'check': check, 'passed': str(bool(passed)).lower(), 'details': str(details)})

def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))
try:
    summary = read_csv(E/'sql_probe_multicatalog_summary.csv')
    totals = {r['metric']: r['value'] for r in read_csv(E/'sql_probe_multicatalog_totals.csv')}
    add('three_catalog_sizes_present', [r['rows_per_table'] for r in summary] == ['1','5','17'], [r['rows_per_table'] for r in summary])
    add('all_catalog_runs_execute', totals.get('total_probe_catalog_runs') == '12648' and totals.get('total_execution_successes') == '12648' and totals.get('total_execution_failures') == '0', totals)
    add('per_catalog_full_coverage', all(r['probes'] == '4216' and r['plan_successes'] == '4216' and r['execution_successes'] == '4216' for r in summary), summary)
    add('nontrivial_result_population', int(totals.get('total_result_rows','0')) > 30000, totals.get('total_result_rows'))
    add('stable_plan_diversity', all(int(r['distinct_plan_hashes']) >= 80 for r in summary), ';'.join(r['distinct_plan_hashes'] for r in summary))
except Exception as exc:
    add('multicatalog_exception_free', False, type(exc).__name__)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'SQL multi-catalog execution check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed'] != 'true':
        print('FAIL', r['check'], r['details'])
if passed != len(rows):
    sys.exit(1)
