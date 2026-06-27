#!/usr/bin/env python3
"""Check that zero-issue summaries do not coexist with stale detail rows."""
from __future__ import annotations
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evaluation'
OUT = E / 'stale_diagnostic_outputs.csv'

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def metric(path: Path, key: str):
    for row in read_csv(path):
        if row.get('metric') == key or row.get('check') == key:
            return row.get('value') or row.get('details') or row.get('passed')
    return None

checks=[]
def add(name, ok, details=''):
    checks.append({'check':name,'passed':str(bool(ok)).lower(),'details':details})
try:
    issues=int(metric(E/'probe_validity.csv','issues') or -1)
    detail=read_csv(E/'probe_validity_issues.csv') if (E/'probe_validity_issues.csv').exists() else []
    add('probe_validity_detail_matches_summary', (issues==0 and len(detail)==0) or (issues==len(detail)), f'summary={issues};detail_rows={len(detail)}')
except Exception as exc:
    add('probe_validity_detail_matches_summary', False, type(exc).__name__)
try:
    pp={r.get('metric'):r.get('value') for r in read_csv(E/'public_provenance_summary.csv')}
    bad=[r for r in read_csv(E/'public_provenance_check.csv') if r.get('passed')=='false' or r.get('status')=='FAIL']
    add('public_provenance_detail_matches_summary', pp.get('public_provenance_issues')=='0' and len(bad)==0, f"summary={pp.get('public_provenance_issues')};bad_rows={len(bad)}")
except Exception as exc:
    add('public_provenance_detail_matches_summary', False, type(exc).__name__)
try:
    audit_issue=metric(E/'grounded_rule_audit_summary.csv','audit_issues') or metric(E/'grounded_rule_audit_summary.csv','rules_with_issues')
    audit_path=E/'grounded_rule_audit.csv'
    bad=[]
    if audit_path.exists():
        bad=[r for r in read_csv(audit_path) if r.get('passed')=='false' or r.get('status')=='FAIL']
    add('grounded_rule_audit_detail_matches_summary', str(audit_issue)=='0' and len(bad)==0, f'summary={audit_issue};bad_rows={len(bad)}')
except Exception as exc:
    add('grounded_rule_audit_detail_matches_summary', False, type(exc).__name__)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(checks)
passed=sum(r['passed']=='true' for r in checks)
print(f'Stale diagnostic-output check: {passed}/{len(checks)} passed')
for r in checks:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(checks): raise SystemExit(1)
