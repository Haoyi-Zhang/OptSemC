#!/usr/bin/env python3
"""Check grounded statistical robustness outputs used by the paper."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation' / 'statistical_robustness_check.csv'
ci = ROOT / 'evaluation' / 'grounded' / 'conditional_trap_confidence.csv'
neg = ROOT / 'evaluation' / 'grounded' / 'negative_control.csv'
loo = ROOT / 'evaluation' / 'grounded' / 'leave_one_engine_summary.csv'
check_rows=[]
def add(check, passed, details=''):
    check_rows.append({'check': check, 'passed': str(bool(passed)).lower(), 'details': str(details)})
for p in [ci, neg, loo]:
    if not p.exists():
        add(f'exists:{p.name}', False, p.relative_to(ROOT))
    else:
        add(f'exists:{p.name}', True, p.relative_to(ROOT))
if all(r['passed'] == 'true' for r in check_rows):
    ci_rows=list(csv.DictReader(ci.open()))
    if len(ci_rows) < 3:
        add('projection_rows_ge_3', False, len(ci_rows))
    else:
        add('projection_rows_ge_3', True, len(ci_rows))
    for r in ci_rows:
        covers = float(r['bootstrap_low']) <= float(r['conditional_rate']) <= float(r['bootstrap_high'])
        add(
            f"bootstrap_covers_rate:{r['method']}",
            covers,
            f"rate={r['conditional_rate']}; bootstrap=[{r['bootstrap_low']},{r['bootstrap_high']}]",
        )
        add(f"projected_equivalences_positive:{r['method']}", int(r['projected_equivalences']) > 0, r['projected_equivalences'])
    neg_rows=list(csv.DictReader(neg.open()))
    add(
        'strict_negative_control_passed',
        bool(neg_rows) and neg_rows[0].get('passed') == 'true',
        f"false={neg_rows[0].get('false_equivalences', 'missing')}" if neg_rows else 'missing',
    )
failed = [r for r in check_rows if r['passed'] != 'true']
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['check', 'passed', 'details'])
    w.writeheader()
    w.writerows(check_rows)
if failed:
    print('Statistical robustness check FAILED')
    for r in failed:
        print(r)
    sys.exit(1)
print('Statistical robustness check passed')
