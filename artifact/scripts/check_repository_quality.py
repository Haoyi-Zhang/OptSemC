#!/usr/bin/env python3
"""Check that the repository-quality score was generated and is package-grade."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifact" / "evaluation" / "repository_quality_check.csv"
score_file = ROOT / "artifact" / "evaluation" / "repository_quality.csv"
audit_file = ROOT / "artifact" / "evaluation" / "repository_audit.csv"
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
if score_file.exists():
    score_rows=list(csv.DictReader(score_file.open(newline='', encoding='utf-8')))
    row=score_rows[0] if score_rows else {}
    pct=float(row.get('percent',0) or 0)
    add('score_file_present', True, f"percent={pct}")
    add('score_package_grade', pct >= 95.0 and row.get('passed')=='true', f"percent={pct}")
else:
    add('score_file_present', False, 'missing')
    add('score_package_grade', False, 'missing')
if audit_file.exists():
    audit=list(csv.DictReader(audit_file.open(newline='', encoding='utf-8')))
    add('audit_all_hard_gates_pass', bool(audit) and all(r.get('passed')=='true' for r in audit), f"{sum(r.get('passed')=='true' for r in audit)}/{len(audit)}")
    add('audit_has_at_least_ten_dimensions', len(audit) >= 10, str(len(audit)))
else:
    add('audit_all_hard_gates_pass', False, 'missing')
    add('audit_has_at_least_ten_dimensions', False, 'missing')
with OUT.open('w', newline='', encoding='utf-8') as f:
    import csv as _csv
    w=_csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Repository quality check: {passed}/{len(rows)} passed")
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)

