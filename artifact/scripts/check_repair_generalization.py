#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'evaluation/grounded/repair_generalization_summary.csv'
out=ROOT/'evaluation/repair_generalization_check.csv'
check_rows=[]
def add(check, passed, details=''):
    check_rows.append({'check':check,'passed':str(bool(passed)).lower(),'details':str(details)})
if not path.exists():
    print('missing repair_generalization_summary.csv')
    add('probe_fold_repair_stability_summary_present', False, 'missing')
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(check_rows)
    sys.exit(1)
summary_rows=list(csv.DictReader(path.open()))
errors=[]
add('probe_fold_repair_stability_summary_present', bool(summary_rows), f'rows={len(summary_rows)}')
for r in summary_rows:
    if float(r['heldout_resolution_rate']) < 1.0:
        errors.append(f"{r['method']} heldout resolution below 1.0")
    if int(r['heldout_false_equivalences']) <= 0 and r['method'] in {'keyword','operator_only'}:
        errors.append(f"{r['method']} has no heldout false equivalences")
methods={r.get('method') for r in summary_rows}
add('probe_fold_repair_stability_methods_present', methods == {'keyword','operator_only','yesno'}, ';'.join(sorted(methods)))
add('probe_fold_repair_stability_resolves_heldout', not errors, ';'.join(errors[:10]))
out.parent.mkdir(parents=True, exist_ok=True)
with out.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(check_rows)
if errors:
    print('Probe-fold repair stability check FAILED')
    for e in errors: print(e)
    sys.exit(1)
print(f'Probe-fold repair stability check: {sum(r["passed"]=="true" for r in check_rows)}/{len(check_rows)} passed')
