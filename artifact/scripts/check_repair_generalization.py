#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'evaluation/grounded/repair_generalization_summary.csv'
if not path.exists():
    print('missing repair_generalization_summary.csv')
    sys.exit(1)
rows=list(csv.DictReader(path.open()))
errors=[]
for r in rows:
    if float(r['heldout_resolution_rate']) < 1.0:
        errors.append(f"{r['method']} heldout resolution below 1.0")
    if int(r['heldout_false_equivalences']) <= 0 and r['method'] in {'keyword','operator_only'}:
        errors.append(f"{r['method']} has no heldout false equivalences")
if errors:
    print('Repair generalization check FAILED')
    for e in errors: print(e)
    sys.exit(1)
print('Repair generalization check passed')
