#!/usr/bin/env python3
"""Check guard-support diagnostics used by the corpus-quality audit."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
E = ROOT / 'evaluation'
OUT = E / 'guard_quality_check.csv'
rows=[]
def add(check, passed, details=''):
    rows.append({'check': check, 'passed': str(bool(passed)).lower(), 'details': str(details)})
def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))
def metric(path, key):
    for r in read_csv(path):
        if r.get('metric') == key: return r.get('value')
    return None
try:
    support = read_csv(E/'guard_support.csv')
    add('all_287_rules_audited', len(support) == 287, len(support))
    zero = [r for r in support if int(r['support_count']) == 0]
    add('no_zero_support_rules', not zero, ';'.join(r['rule_id'] for r in zero[:10]))
    add('support_counts_within_probe_domain', all(0 < int(r['support_count']) <= int(r['total_probes']) == 4216 for r in support), '')
    classes = {r['support_class'] for r in support}
    add('support_classes_cover_narrow_to_global', {'narrow','medium','broad','global'} <= classes, ','.join(sorted(classes)))
except Exception as exc:
    add('guard_support_readable', False, type(exc).__name__)
try:
    issues = read_csv(E/'guard_dimension_issues.csv')
    add('no_invalid_guard_dimensions', len(issues) == 0, len(issues))
except Exception as exc:
    add('guard_dimension_issues_readable', False, type(exc).__name__)
try:
    ov = read_csv(E/'guard_overlap_summary.csv')
    same = int(float(metric(E/'guard_overlap_summary.csv','same_action_state_pairs') or -1))
    contain = int(float(metric(E/'guard_overlap_summary.csv','guard_containment_pairs') or -1))
    add('same_action_guard_overlap_audited', same >= 0, same)
    add('guard_containment_is_finite', 0 <= contain <= same, f'{contain}/{same}')
except Exception as exc:
    add('guard_overlap_summary_readable', False, type(exc).__name__)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Guard quality check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)
