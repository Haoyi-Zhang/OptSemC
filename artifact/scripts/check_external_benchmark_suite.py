#!/usr/bin/env python3
"""Check external benchmark-family coverage outputs."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
OUT=ART/'evaluation'/'external_benchmark_suite_check.csv'
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
path=ART/'evaluation'/'external_benchmark_suite.csv'
if path.exists():
    data=list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    add('suite_rows_present', len(data)>=8, f'suites={len(data)}')
    add('all_suites_fully_covered', data and all(r['motifs']==r['covered_motifs'] for r in data), '')
    add('all_suites_have_probe_hits', data and all(int(r['matching_probes'])>0 for r in data), '')
    add('motif_count_substantial', sum(int(r['motifs']) for r in data) >= 40, str(sum(int(r['motifs']) for r in data)))
else:
    for name in ['suite_rows_present','all_suites_fully_covered','all_suites_have_probe_hits','motif_count_substantial']:
        add(name, False, 'missing')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"External benchmark suite check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

