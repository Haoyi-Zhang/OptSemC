#!/usr/bin/env python3
"""Validate executable external benchmark motif coverage."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation' / 'external_motif_execution_check.csv'
summary_path = ROOT / 'evaluation' / 'external_motif_execution_summary.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
summary={}
if summary_path.exists():
    summary={r['metric']: r['value'] for r in csv.DictReader(summary_path.open(newline='', encoding='utf-8'))}
records=list(csv.DictReader((ROOT/'evaluation'/'external_motif_execution.csv').open(newline='', encoding='utf-8'))) if (ROOT/'evaluation'/'external_motif_execution.csv').exists() else []
add('external_motif_rows_present', len(records) >= 90, f'rows={len(records)}')
add('twelve_external_suites_present', summary.get('suites') == '12', summary)
add('all_external_motifs_matched', summary.get('external_motifs') == summary.get('matched_motifs') and summary.get('matched_motifs') == '90', summary)
add('all_external_motif_probes_executable', summary.get('execution_failures') == '0' and summary.get('executed_motifs') == '90', summary)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"External motif execution check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r)
if passed != len(rows): sys.exit(1)
