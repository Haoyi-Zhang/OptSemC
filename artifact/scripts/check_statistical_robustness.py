#!/usr/bin/env python3
"""Check grounded statistical robustness outputs used by the paper."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ci = ROOT / 'evaluation' / 'grounded' / 'conditional_trap_confidence.csv'
neg = ROOT / 'evaluation' / 'grounded' / 'negative_control.csv'
loo = ROOT / 'evaluation' / 'grounded' / 'leave_one_engine_summary.csv'
errors=[]
for p in [ci, neg, loo]:
    if not p.exists():
        errors.append(f'missing {p}')
if not errors:
    rows=list(csv.DictReader(ci.open()))
    if len(rows) < 3:
        errors.append('expected at least three projection rows in conditional_trap_confidence')
    for r in rows:
        if float(r['bootstrap_low']) > float(r['conditional_rate']) or float(r['bootstrap_high']) < float(r['conditional_rate']):
            errors.append(f"bootstrap interval does not cover rate for {r['method']}")
        if int(r['projected_equivalences']) <= 0:
            errors.append(f"no projected equivalences for {r['method']}")
    neg_rows=list(csv.DictReader(neg.open()))
    if not neg_rows or neg_rows[0].get('passed') != 'true':
        errors.append('strict negative control did not pass')
if errors:
    print('Statistical robustness check FAILED')
    for e in errors:
        print(e)
    sys.exit(1)
print('Statistical robustness check passed')
