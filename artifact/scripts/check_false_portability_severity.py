#!/usr/bin/env python3
"""Validate false-equivalence severity outputs used by the paper."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evaluation'
OUT = E / 'false_portability_severity_check.csv'
rows: list[dict[str,str]] = []

def add(check: str, passed: bool, details: str = '') -> None:
    rows.append({'check': check, 'passed': str(bool(passed)).lower(), 'details': details})

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))
try:
    severity = {r['projection']: r for r in read_csv(E/'false_portability_severity.csv')}
    add('severity_file_present', bool(severity), f'rows={len(severity)}')
    add('headline_false_counts_match', int(severity['keyword']['false_equivalences']) == 254 and int(severity['operator_only']['false_equivalences']) == 238 and int(severity['yesno']['false_equivalences']) == 6, '')
    add('strict_repair_control_zero', int(severity['operator_kind_surface']['false_equivalences']) == 0, severity['operator_kind_surface'])
    add('severity_nontrivial_for_headlines', float(severity['keyword']['mean_exact_distance']) > 0.7 and float(severity['operator_only']['mean_exact_distance']) > 0.7, f"keyword={severity['keyword']['mean_exact_distance']};operator={severity['operator_only']['mean_exact_distance']}")
    add('extreme_single_field_baselines_severe', int(severity['placement_only']['false_equivalences']) > 10000 and int(severity['state_only']['false_equivalences']) > 20000, '')
    add('dominant_fields_interpretable', severity['keyword']['dominant_field_delta'] in {'operator','placement','variant','layer'} and severity['operator_only']['dominant_field_delta'] in {'kind','layer','variant','placement'}, f"keyword={severity['keyword']['dominant_field_delta']};operator={severity['operator_only']['dominant_field_delta']}")
except Exception as exc:
    add('severity_exception_free', False, type(exc).__name__)

with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details'])
    w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'False-portability severity check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed'] != 'true':
        print('FAIL', r['check'], r['details'])
if passed != len(rows):
    sys.exit(1)
