#!/usr/bin/env python3
"""Validate full SQL execution outputs for the generated probe suite."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation' / 'sql_probe_execution_check.csv'
summary_path = ROOT / 'evaluation' / 'sql_probe_execution_summary.csv'
records_path = ROOT / 'evaluation' / 'sql_probe_execution.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
summary={}
if summary_path.exists():
    summary={r['metric']:r['value'] for r in csv.DictReader(summary_path.open(newline='', encoding='utf-8'))}
records=list(csv.DictReader(records_path.open(newline='', encoding='utf-8'))) if records_path.exists() else []
add('all_4216_probe_records_present', len(records)==4216, f'rows={len(records)}')
add('all_probes_plan_successfully', summary.get('plan_successes')=='4216', summary)
add('all_probes_execute_successfully', summary.get('execution_successes')=='4216' and summary.get('execution_failures')=='0', summary)
add('plans_have_nontrivial_diversity', int(summary.get('distinct_plan_hashes','0')) >= 80, summary.get('distinct_plan_hashes','0'))
add('result_rows_nonzero', int(summary.get('total_result_rows','0')) > 0, summary.get('total_result_rows','0'))
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"SQL probe execution check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r)
if passed != len(rows): sys.exit(1)
